"""Capture real browser screenshots of the preserved notebook-output HTML.

Requires Chromium/Chrome and websocket-client (installed by JupyterLab).
Usage: python scripts/capture_evidence.py --browser /path/to/chrome.exe
Browser profile and temporary browser files stay in the ignored lab directory.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

import websocket

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", type=Path, required=True)
    args = parser.parse_args()
    profile = ROOT / "_lakehouse" / "evidence-browser"
    profile.mkdir(parents=True, exist_ok=True)
    port_file = profile / "DevToolsActivePort"
    if port_file.exists():
        port_file.unlink()
    browser = subprocess.Popen([
        str(args.browser.resolve()), "--headless", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", "--remote-debugging-port=0",
        "--remote-allow-origins=http://127.0.0.1", f"--user-data-dir={profile}", "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    socket = None
    try:
        deadline = time.monotonic() + 20
        while not port_file.exists():
            if browser.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError("Headless Chromium did not start")
            time.sleep(0.1)
        port = port_file.read_text().splitlines()[0]
        with urlopen(f"http://127.0.0.1:{port}/json/list", timeout=10) as response:
            pages = json.load(response)
        socket = websocket.create_connection(pages[0]["webSocketDebuggerUrl"],
                                              origin="http://127.0.0.1", timeout=20)
        message_id = 0

        def call(method, params=None):
            nonlocal message_id
            message_id += 1
            socket.send(json.dumps(dict(id=message_id, method=method, params=params or {})))
            while True:
                message = json.loads(socket.recv())
                if message.get("id") == message_id:
                    if "error" in message:
                        raise RuntimeError(message["error"])
                    return message.get("result", {})

        call("Page.enable")
        call("Emulation.setDeviceMetricsOverride", dict(width=1280, height=900,
                                                        deviceScaleFactor=1, mobile=False))
        for source in sorted((ROOT / "submission" / "evidence").glob("[0-9][0-9]_*.html")):
            call("Page.navigate", dict(url=source.resolve().as_uri()))
            # Query the DOM until the intended document and rendered body are ready.
            for _ in range(100):
                state = call("Runtime.evaluate", dict(expression="JSON.stringify({url:location.href,ready:document.readyState})",
                                                       returnByValue=True))
                status = json.loads(state["result"]["value"])
                if status["url"] == source.resolve().as_uri() and status["ready"] == "complete":
                    break
                time.sleep(0.05)
            else:
                raise RuntimeError(f"Page did not load: {source.name}")
            size = call("Page.getLayoutMetrics")["cssContentSize"]
            screenshot = call("Page.captureScreenshot", dict(format="png", captureBeyondViewport=True,
                clip=dict(x=0, y=0, width=1280, height=size["height"], scale=1)))
            destination = ROOT / "submission" / "screenshots" / f"nb{source.stem}.png"
            destination.write_bytes(base64.b64decode(screenshot["data"]))
            print(f"Captured {destination.name}: 1280 x {size['height']:.0f}", flush=True)
    finally:
        if socket is not None:
            socket.close()
        browser.terminate()
        try:
            browser.wait(timeout=10)
        except subprocess.TimeoutExpired:
            browser.kill()
            browser.wait()


if __name__ == "__main__":
    main()

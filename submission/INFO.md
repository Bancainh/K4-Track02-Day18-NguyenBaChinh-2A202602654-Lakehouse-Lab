# Thông tin bài nộp

- **Họ tên:** Nguyễn Bá Chính
- **MSSV:** 2A202602654
- **Mã bài:** K4-Track02-Day18
- **Repository:** [Bancainh/K4-Track02-Day18-NguyenBaChinh-2A202602654-Lakehouse-Lab](https://github.com/Bancainh/K4-Track02-Day18-NguyenBaChinh-2A202602654-Lakehouse-Lab)
- **Đường chạy:** lightweight cho cả NB1–NB8.
- **Môi trường:** Windows 11 Pro 64-bit (10.0.26200), Python 3.11.9, PowerShell, venv `.venv/`.
- **Dependencies đã cài:** xem [requirements-lock.txt](requirements-lock.txt).
- **Kiểm tra và số liệu:** xem [RESULTS.md](RESULTS.md), [metrics.json](evidence/metrics.json) và [logs/](logs/).
- **Khai báo AI:** [AI_USAGE.md](AI_USAGE.md).

## Nội dung

Tám notebook tại [notebooks/](notebooks/) giữ code, output thực thi, assertion và phần giải thích tiếng Việt cuối notebook. Ảnh tại [screenshots/](screenshots/) là ảnh chụp trình duyệt render output được trích từ chính notebook; trang nguồn nằm trong [evidence/](evidence/). Toàn bộ output vẫn có trong notebook và log, kể cả các đoạn không nằm trong ảnh.

Các bổ sung so với đề: NB1 dùng kết quả exception thực tế thay cờ `True` cố định, kiểm tra ghi lỗi không thay version/số dòng và in JSON commit; NB4 đặt timezone DuckDB về UTC để ngày khớp generator, kiểm tra đủ grid ngày/model và chất lượng các metric, in đầy đủ Gold; NB6 loại checkpoint khỏi bộ đếm file dữ liệu và xác minh/in file theo pointer `_last_checkpoint`. Không bỏ assertion hoặc hạ ngưỡng gốc.

## Tái lập trên PowerShell

Chạy từ thư mục gốc repo:

```powershell
$env:PYTHONUTF8 = '1'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r submission/requirements-lock.txt
.\.venv\Scripts\python.exe scripts/verify_lite.py
.\.venv\Scripts\python.exe scripts/generate_data_lite.py
.\.venv\Scripts\python.exe scripts/generate_ai_data.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts/run_all.py
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name lakehouse-lab --display-name 'Lakehouse Lab (.venv)'
.\.venv\Scripts\python.exe scripts/build_submission.py
# Dùng đường dẫn Chrome/Chromium hiện có trên máy để chụp lại ảnh:
.\.venv\Scripts\python.exe scripts/capture_evidence.py --browser 'DUONG_DAN_CHROME_EXE'
```

`build_submission.py` chạy từng notebook bằng kernel của venv rồi lưu output; không chỉ chuyển định dạng. Notebook nộp cũng có cell tìm repo root để import helper khi mở từ `submission/notebooks/`. Chạy lại sẽ reset các bảng scratch theo code đề và thay artifact cục bộ; không dùng để ghi đè bằng chứng đã chốt sau deadline.

Không đưa `.venv/`, `_lakehouse/`, cache hay blob sinh ra vào Git. Không thực hiện đường Spark hoặc bonus tùy chọn trong bài nộp này. Commit SHA và PR được bổ sung khi chốt/push bài lên GitHub.

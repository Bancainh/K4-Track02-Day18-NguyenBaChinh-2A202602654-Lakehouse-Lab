# Kết quả — Nguyễn Bá Chính, 2A202602654

Thực thi notebook ngày `2026-10-04T16:12:29+07:00` trên Windows 11 Pro, Python 3.11.9, đường lightweight. Số liệu là kết quả máy này; timing có thể thay đổi khi chạy lại. Không tự quy đổi bảng này thành điểm chấm.

- Smoke: **9/9 PASS**, xem [log](logs/smoke.txt).
- Pytest: **24/24 PASS**, xem [log](logs/pytest.txt).
- `run_all.py`: **8/8 PASS**, xem [log](logs/run_all.txt).
- Jupyter kernel: **8/8 notebook đã thực thi**, giữ output và giải thích; không có cell lỗi.

| Notebook | Số đo thực tế | Tiêu chí đối chiếu đã đạt |
|---|---|---|
| NB1 | 2 JSON commit; ghi sai schema bị chặn; tier được thêm; 4 dòng, 2 nhóm tier | Log + enforcement + evolution |
| NB2 | 200 → 55 file; 344.51 → 28.68 ms; speedup 12.01×; pruning 55× | ≥100 file; speedup≥3× hoặc pruning≥10× |
| NB3 | MERGE 100,000 dòng; 5 version gồm RESTORE; 0 score âm; 150,000 dòng sau restore | 100K MERGE; ≥5 version; score<0=0 |
| NB4 | 200,000 → 190,052; loại 9,948 retry; 7 ngày UTC × 3 model = 21 nhóm | Dedup; ≥7×3; p50≤p95; cost>0; error_rate∈[0,1] |
| NB5 | SqlCatalog; 10 → 1 file (10×); field_id=4; spec [1, 2]; 5,500 dòng | Catalog/day(ts); pruning≥5×; field-ID; ≥2 specs |
| NB6 | 200 → 11 file (18.18×); skip 90%; VACUUM 16,906,688 byte; xóa 3 orphan; Iceberg 20→3 snapshots và 17 list được sweep; checkpoint có mặt | 5 job; compaction≥10×; skip≥50%; dữ liệu còn nguyên |
| NB7 | Amplification 200.05×; int8 nhỏ 5.80×; recall@10=0.904; fidelity=1.000; bảng/index cũ=0/8 hit; 8 delete event | ≥5×; ≥3×; recall≥0.80; fidelity≥0.95; tái hiện lifecycle bug |
| NB8 | 2 policy; pin v0 với 1,578 bước (hiện tại 1,978); 5 lượt list→1 catalog read; input_required; task completed; 4 bucket + UNCLASSIFIED; loại 334 dòng | Medallion/version pin; cache/confirmation/task; provenance |

## Bằng chứng từng notebook

- 01_delta_basics: [notebook](notebooks/01_delta_basics.ipynb), [ảnh](screenshots/nb01_delta_basics.png), [log](logs/01_delta_basics.txt), [trang output dùng chụp ảnh](evidence/01_delta_basics.html).
- 02_optimize_zorder: [notebook](notebooks/02_optimize_zorder.ipynb), [ảnh](screenshots/nb02_optimize_zorder.png), [log](logs/02_optimize_zorder.txt), [trang output dùng chụp ảnh](evidence/02_optimize_zorder.html).
- 03_time_travel: [notebook](notebooks/03_time_travel.ipynb), [ảnh](screenshots/nb03_time_travel.png), [log](logs/03_time_travel.txt), [trang output dùng chụp ảnh](evidence/03_time_travel.html).
- 04_medallion: [notebook](notebooks/04_medallion.ipynb), [ảnh](screenshots/nb04_medallion.png), [log](logs/04_medallion.txt), [trang output dùng chụp ảnh](evidence/04_medallion.html).
- 05_iceberg_catalog: [notebook](notebooks/05_iceberg_catalog.ipynb), [ảnh](screenshots/nb05_iceberg_catalog.png), [log](logs/05_iceberg_catalog.txt), [trang output dùng chụp ảnh](evidence/05_iceberg_catalog.html).
- 06_maintenance: [notebook](notebooks/06_maintenance.ipynb), [ảnh](screenshots/nb06_maintenance.png), [log](logs/06_maintenance.txt), [trang output dùng chụp ảnh](evidence/06_maintenance.html).
- 07_vectors_multimodal: [notebook](notebooks/07_vectors_multimodal.ipynb), [ảnh](screenshots/nb07_vectors_multimodal.png), [log](logs/07_vectors_multimodal.txt), [trang output dùng chụp ảnh](evidence/07_vectors_multimodal.html).
- 08_agents_provenance: [notebook](notebooks/08_agents_provenance.ipynb), [ảnh](screenshots/nb08_agents_provenance.png), [log](logs/08_agents_provenance.txt), [trang output dùng chụp ảnh](evidence/08_agents_provenance.html).

JSON số liệu: [metrics.json](evidence/metrics.json). Phiên bản gói: [requirements-lock.txt](requirements-lock.txt).

## Giải thích và giới hạn

NB1 dùng flag exception thật, kiểm tra version/số dòng không thay đổi khi ghi lỗi và in commit JSON. NB4 thêm kiểm tra chất lượng Gold và đặt UTC khi phân nhóm theo ngày. NB6 loại checkpoint khỏi bộ đếm file dữ liệu và in checkpoint theo pointer _last_checkpoint; file checkpoint tự sinh ở v99/v199 không phải orphan dữ liệu. Đối chiếu trực tiếp trên dữ liệu Bronze cho thấy timezone mặc định Asia/Bangkok tạo 8 ngày (01–08/04); UTC tạo đúng 7 ngày (01–07/04). Không sửa generator hay hạ ngưỡng rubric.

NB5 tỷ lệ metadata/data là tỷ lệ byte với data, không phải phần trăm tổng dung lượng. NB6 chỉ chứng minh hành vi engine/phiên bản đã cài: VACUUM bỏ qua orphan chưa commit, expiry chưa xóa Avro vật lý. Retention 0 áp dụng scratch lab. NB7 amplification lấy từ footer (uncompressed row-group size); recall trên embedding tổng hợp. NB8 replay chỉ kiểm tra số bước, confirmed do caller đặt, delete_rows là no-op, bucket provenance là fixture minh họa. Phân tích chi tiết nằm cuối mỗi notebook.

## Chốt bài nộp

Đã chuẩn bị đầy đủ phần bắt buộc trong workspace. Chưa commit/push, mở PR hay gửi liên kết qua kênh lớp. Người nộp tự chạy/đối chiếu, đọc và chỉnh reflection theo [khai báo AI](AI_USAGE.md), sau đó chốt commit SHA và nộp theo [SUBMISSION.md](../docs/SUBMISSION.md). Không làm bonus tùy chọn.

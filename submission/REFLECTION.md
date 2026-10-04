# Reflection — Nguyễn Bá Chính, 2A202602654

Với pipeline LLM observability trong bài này, anti-pattern dễ gặp nhất là bỏ maintenance. Mỗi request hoặc micro-batch tạo ít dữ liệu nhưng nhiều file; truy vấn dashboard phải mở nhiều file, đọc nhiều metadata và chịu thêm chi phí request. Compaction giúp giảm file, còn clustering làm khoảng min/max đủ hẹp để skipping hiệu quả.

Chỉ chạy VACUUM chưa đủ: file do writer lỗi trước commit không được delta-rs thu hồi trong phép đo lab. Snapshot expiry của PyIceberg cũng không tự xóa manifest list vật lý ở đường chạy đã kiểm tra. Vì vậy cần đo file/byte trước và sau từng job, ghép expiry với orphan sweep, dùng tuổi file và tập tham chiếu phù hợp để bảo vệ writer và snapshot còn hiệu lực.

Tôi chọn theo dõi số file, kích thước trung bình, metadata/data và độ trễ truy vấn; lên lịch compaction, clustering, expiry và orphan cleanup theo tải ingest. Retention phải đủ cho reader và nhu cầu replay, thay vì dùng retention 0 như scratch lab.

Phần soạn và giải thích có hỗ trợ Codex; phạm vi và việc cần tự kiểm tra được khai trong [AI_USAGE.md](AI_USAGE.md).

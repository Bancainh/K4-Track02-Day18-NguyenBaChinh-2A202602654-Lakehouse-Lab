# Khai báo sử dụng AI

**Công cụ:** OpenAI Codex. **Người nộp:** Nguyễn Bá Chính — 2A202602654.

Codex hỗ trợ đọc README và tài liệu nộp bài, cài môi trường trong repo, bổ sung kiểm tra NB1/NB4, sửa việc đếm file/in checkpoint ở NB6, chạy scripts/tests và notebook trên máy của người dùng, viết script lưu output và chụp trang bằng chứng, soạn phần giải thích tiếng Việt, bảng kết quả và bản nháp reflection. Không sử dụng output của học viên khác.

Các số liệu trong notebook, log, `metrics.json` và ảnh được lấy từ quá trình thực thi tại workspace này. Không tạo output giả, thay số đo để đạt ngưỡng, bỏ assertion hoặc hạ tiêu chí. Dữ liệu và embedding đều tổng hợp bằng generator của đề; không gọi LLM/encoder/API bên ngoài trong notebook.

Phần lời giải/reflection có hỗ trợ soạn bởi AI, không phải lời khẳng định rằng người nộp đã tự thực thi thủ công hoặc đã hiểu toàn bộ nội dung. Theo `docs/RULES.md`, trước khi nộp, người nộp cần tự chạy lại, kiểm tra và giải thích được kết quả; đọc và chỉnh reflection để phản ánh nhận định cá nhân. Ghi rõ hỗ trợ AI trong bài nộp này.

NB6 dùng hành vi engine/phiên bản của lab; NB7 chỉ dùng vector tổng hợp và ước tính amplification từ footer; NB8 là mô phỏng offline, không xác lập tuân thủ MCP hay quyền sử dụng dữ liệu thật. Các giới hạn đó được giữ trong giải thích notebook.

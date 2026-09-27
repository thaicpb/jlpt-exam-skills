@AGENTS.md

## Ghi chú riêng cho Claude

- Bốn skill được Claude Code tự nhận qua `.claude/skills/` (symlink tới `skills/`). Khi yêu cầu khớp mô tả skill, dùng skill đó mà không cần người dùng gọi tên; người dùng cũng có thể gõ `/jlpt-vocabulary-flashcards`, `/jlpt-n2-vocabulary-coach`…
- Claude Code: tạo HTML trong `outputs/`, báo đường dẫn tuyệt đối để mở bằng browser.
- Claude Desktop/Cowork: lưu HTML vào thư mục dự án người dùng đã chọn và trình bày file; chỉ đăng artifact khi người dùng muốn giữ lâu hoặc chia sẻ.
- Với ảnh từ vựng, đọc ảnh trực tiếp (Claude hỗ trợ ảnh), phóng to vùng chữ nhỏ trước khi chép.

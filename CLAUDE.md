@AGENTS.md

## Ghi chú riêng cho Claude

- Bốn skill được Claude Code tự nhận qua `.claude/skills/` (symlink tới `skills/`). Khi yêu cầu khớp mô tả skill, dùng skill đó mà không cần người dùng gọi tên; người dùng cũng có thể gõ `/jlpt-vocabulary-flashcards`, `/jlpt-n2-vocabulary-coach`…
- Claude Desktop/Cowork không tự đăng ký skill trong `.claude/skills/`: chọn skill theo bảng trong `AGENTS.md`, đọc đầy đủ `skills/<tên>/SKILL.md` (và các `references/` nó yêu cầu) rồi làm theo; chạy script bằng shell từ `skills/<tên>`.
- Lệnh gọi skill tương đương giữa hai bên: Codex `$jlpt-n1-vocabulary-coach` ↔ Claude `/jlpt-n1-vocabulary-coach`. Câu mẫu trong `skills/<tên>/agents/openai.yaml` (`default_prompt`) cũng là yêu cầu hợp lệ cho Claude.
- `agents/openai.yaml` là metadata giao diện của Codex; Claude chỉ dựa vào frontmatter `SKILL.md`. Khi sửa `description` trong `SKILL.md`, cập nhật `short_description` tương ứng để hai bên nhất quán.
- Claude Code: tạo HTML trong `outputs/`, báo đường dẫn tuyệt đối để mở bằng browser.
- Claude Desktop/Cowork: lưu HTML vào thư mục dự án người dùng đã chọn và trình bày file; chỉ đăng artifact khi người dùng muốn giữ lâu hoặc chia sẻ.
- Với ảnh từ vựng, đọc ảnh trực tiếp (Claude hỗ trợ ảnh), phóng to vùng chữ nhỏ trước khi chép.
- Bài kiểm tra N1/N2: tuân thủ mục **Chất lượng đáp án** trong `SKILL.md`. Khi cần xác minh phương án nhiễu ngoài CSV, dùng WebSearch/web fetch trên từ điển tiếng Nhật đáng tin cậy (goo辞書, コトバンク, Weblio辞書…) và chỉ ghi căn cứ đã thực sự tra. Không tra web để lấy từ mục tiêu. Nếu không có công cụ web, thay phương án chưa xác minh được thay vì đoán.

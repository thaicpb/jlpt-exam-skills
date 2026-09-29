# JLPT Exam Skills — hướng dẫn cho AI agent

Tài liệu dùng chung cho mọi agent (Claude, Codex…). Người dùng là người học tiếng Nhật, thường không lập trình; trả lời bằng tiếng Việt.

## Cấu trúc

- `resources/<LEVEL>/goi/daiN.csv`: từ vựng theo cấp độ/bài, UTF-8 BOM, bốn cột `từ mới, cách đọc, nghĩa tiếng việt, ví dụ sử dụng minh hoạ`. Danh sách bài hiện có: liệt kê `resources/*/goi/*.csv`.
- `resources/<LEVEL>/goi/daiN.examples.json`: bản dịch Việt + furigana cho câu mẫu (dùng cho flashcard).
- Dữ liệu mỗi bài chỉ gồm `.csv` và `.examples.json`; không tạo hoặc yêu cầu tệp `.provenance.json`.
- `skills/<tên>/`: nguồn chính của bốn skill (`SKILL.md`, `scripts/`, `assets/`, `references/`).
- `.claude/skills/<tên>`: symlink tới `skills/<tên>` để Claude Code tự nhận skill. Luôn sửa trong `skills/`, không tạo bản sao.
- `outputs/`: nơi lưu HTML/JSON tạo ra cho người học (đã gitignore).
- `webapp/` + `tools/build_webapp.py`: web app flashcard (PWA) cho iPhone. Build ra `dist/` (gitignore); GitHub Actions `.github/workflows/webapp.yml` tự build và deploy lên GitHub Pages khi `resources/` thay đổi. Sau khi thêm/sửa bài, chạy `python3 tools/build_webapp.py` để chắc dữ liệu hợp lệ.

## Chọn skill

| Yêu cầu của người dùng | Skill |
| --- | --- |
| Tự học, ôn, lật thẻ, flashcard (N1/N2) | `jlpt-vocabulary-flashcards` |
| Bài tập / quiz / kiểm tra từ vựng **N2** (6 dạng) | `jlpt-n2-vocabulary-coach` |
| Bài tập / quiz / kiểm tra từ vựng **N1** (4 dạng) | `jlpt-n1-vocabulary-coach` |
| Ảnh danh sách từ → bài CSV mới | `jlpt-image-to-vocabulary-csv` |
| "Có những bài nào?" | Liệt kê `resources/*/goi/*.csv`, không cần skill |

Luôn đọc đầy đủ `SKILL.md` của skill được chọn trước khi làm. Không trộn phạm vi: flashcard không chấm điểm; N1 và N2 không dùng chung builder.

## Quy tắc bắt buộc

- Từ mục tiêu chỉ lấy từ CSV của dự án; không lấy từ web hoặc trí nhớ. Thiếu dữ liệu thì báo rõ, không ép đủ số câu.
- Không ghi đè CSV trong `resources/` nếu người dùng chưa yêu cầu rõ.
- Chạy script từ thư mục skill (`cd skills/<tên>`); các đường dẫn `../../resources`, `../../outputs` tính từ đó. Chỉ cần Python 3 chuẩn, không cài thêm gói.
- Không đưa toàn bộ corpus vào hội thoại; nạp đúng phạm vi bằng `--lesson`, `--limit`, `--sample`.

## Kiểm tra

```bash
for d in skills/*/; do (cd "$d/scripts" && python3 -m unittest discover -p 'test_*.py'); done
```

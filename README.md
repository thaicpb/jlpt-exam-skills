# JLPT Exam Skills

Bộ dữ liệu và công cụ hỗ trợ tự học từ vựng tiếng Nhật theo chuẩn JLPT, dành cho người Việt. Bạn có thể học trực tiếp trên [web app](https://thaicpb.github.io/jlpt-exam-skills/) hoặc trò chuyện với AI (Claude, Codex…) để tạo thẻ nhớ và bài luyện theo nhu cầu. Không cần biết lập trình.

## Nội dung

- **Từ vựng N1 và N2**, sắp xếp theo bài. Mỗi từ có cách đọc, nghĩa tiếng Việt và câu ví dụ kèm furigana, bản dịch.
- **Đề kiểm tra từ vựng N1** theo từng bài, có đáp án và giải thích tiếng Việt cho mọi lựa chọn.
- **Bốn skill cho AI**: bộ hướng dẫn giúp AI tạo thẻ nhớ, bài luyện N1/N2 và nhập từ vựng mới từ ảnh.

Bài luyện và đề kiểm tra do dự án biên soạn để ôn tập, **không phải đề JLPT chính thức**.

## Học trên web app

Mở [https://thaicpb.github.io/jlpt-exam-skills/](https://thaicpb.github.io/jlpt-exam-skills/), chọn cấp độ rồi chọn bài.

- **Thẻ nhớ**: lật thẻ, nghe phát âm, vuốt để chuyển thẻ, đánh dấu **★ Cần xem lại** và ôn riêng nhóm này. Tiến độ được lưu trên thiết bị.
- **Kiểm tra N1**: chế độ **Kiểm tra** chỉ hiện điểm và giải thích sau khi nộp. Chế độ **Luyện tập** hiện giải thích ngay. Sau khi nộp có thể làm lại câu sai hoặc cả đề.
- **Dùng trên iPhone**: mở link bằng Safari, chọn **Chia sẻ → Thêm vào MH chính**. Mở app một lần khi có mạng, chờ thông báo đã lưu offline, sau đó có thể học không cần mạng.
- **Sao lưu tiến độ**: Safari có thể xoá dữ liệu nếu lâu không mở app. Vào ⚙︎ → **Sao chép** để lưu mã sao lưu; khi cần, dán vào **Khôi phục**.

## Học cùng AI

Mở thư mục dự án trong một ứng dụng AI đọc được tệp, rồi yêu cầu bằng ngôn ngữ tự nhiên. AI tự chọn skill phù hợp:

| Skill | Mục đích |
| --- | --- |
| `jlpt-vocabulary-flashcards` | Tự học và ôn bằng thẻ nhớ, không chấm điểm |
| `jlpt-n2-vocabulary-coach` | Bài luyện, bài kiểm tra từ vựng N2 (sáu dạng) |
| `jlpt-n1-vocabulary-coach` | Bài luyện, bài kiểm tra từ vựng N1 (bốn dạng) |
| `jlpt-image-to-vocabulary-csv` | Nhập bài từ vựng mới từ ảnh sách |

Cách mở theo từng ứng dụng:

- **Claude Code**: chạy `claude` tại thư mục dự án. Skill được nhận tự động; có thể gọi trực tiếp như `/jlpt-n1-vocabulary-coach`.
- **Claude Desktop (Cowork)**: chọn thư mục dự án làm thư mục làm việc. Nếu AI chưa dùng skill, thêm câu “Hãy đọc CLAUDE.md và làm theo skill phù hợp”.
- **Codex**: mở thư mục dự án; `AGENTS.md` hướng dẫn chọn skill, có thể gọi trực tiếp như `$jlpt-n1-vocabulary-coach`.

Kết quả là tệp HTML tương tác, lưu trong `outputs/`.

### Ví dụ yêu cầu

> Cho tôi học 10 từ N2 bài 1 bằng thẻ nhớ.

> Chia toàn bộ bài 5 N1 thành các bộ thẻ 20 từ.

> Đây là các từ tôi hay nhầm: […]. Tạo thẻ nhớ để ôn lại.

> Tạo bài luyện N2 gồm 6 câu, mỗi dạng một câu, giải thích ngay sau mỗi câu.

> Tạo bài kiểm tra N1 25 câu đủ bốn dạng, chỉ hiện đáp án sau khi nộp.

> Đọc các ảnh này và tạo bài từ vựng N2 mới, không ghi đè bài cũ.

Từ được học hoặc kiểm tra luôn lấy từ dữ liệu của dự án. Nếu không đủ từ phù hợp, AI sẽ báo rõ thay vì tự thêm. Muốn biết hiện có những bài nào, chỉ cần hỏi AI.

### Dạng bài

| Dạng bài | Yêu cầu | N2 | N1 |
| --- | --- | :---: | :---: |
| 漢字読み — Đọc kanji | Chọn cách đọc của từ gạch dưới | ✓ | ✓ |
| 表記 — Cách viết | Chọn kanji đúng cho từ viết bằng kana | ✓ | |
| 語形成 — Cấu tạo từ | Chọn phần còn thiếu để tạo thành từ | ✓ | |
| 文脈規定 — Ngữ cảnh | Chọn từ phù hợp điền vào câu | ✓ | ✓ |
| 言い換え類義 — Gần nghĩa | Chọn cách diễn đạt gần nghĩa nhất | ✓ | ✓ |
| 用法 — Cách dùng | Chọn câu dùng từ đúng | ✓ | ✓ |

### Nhập từ vựng từ ảnh

Đính kèm ảnh rõ chữ, đúng thứ tự trang. AI giữ nguyên từ, cách đọc và thứ tự trong sách, tự soạn nghĩa tiếng Việt và câu ví dụ còn thiếu. Chữ nào không đọc chắc, AI sẽ hỏi lại thay vì đoán. Bài mới được lưu thành bài tiếp theo, không ghi đè bài cũ.

## Cấu trúc dự án

```text
resources/<LEVEL>/goi/     Từ vựng theo bài (daiN.csv) và chú thích câu ví dụ (daiN.examples.json)
resources/N1/exams/        Ngân hàng đề kiểm tra N1 theo bài
skills/                    Bốn skill cho AI (.claude/skills/ là symlink tới đây)
webapp/                    Mã nguồn web app (PWA)
tools/build_webapp.py      Kiểm tra dữ liệu và đóng gói web app vào dist/
AGENTS.md, CLAUDE.md       Hướng dẫn cho AI agent
```

## Cập nhật và triển khai

1. Thêm hoặc sửa bài trong `resources/`. CSV dùng UTF-8 BOM, bốn cột: từ mới, cách đọc, nghĩa tiếng Việt, ví dụ.
2. Kiểm tra và build:

   ```bash
   python3 tools/build_webapp.py
   python3 -m http.server 8000 --directory dist   # xem thử tại http://localhost:8000
   ```

3. Push lên nhánh `main`. Workflow [Deploy flashcard web app](https://github.com/thaicpb/jlpt-exam-skills/actions/workflows/webapp.yml) tự build và triển khai lên GitHub Pages. Không commit `dist/`.
4. Mở lại web app khi có mạng; khi thấy **“Có bài học mới”**, bấm **Cập nhật**.

Chạy kiểm thử cho các skill:

```bash
for d in skills/*/; do (cd "$d/scripts" && python3 -m unittest discover -p 'test_*.py'); done
```

**Triển khai bản sao của riêng bạn:** trên GitHub, vào **Settings → Pages → Source** và chọn **GitHub Actions** (không chọn *Deploy from a branch*, vì như vậy trang sẽ chỉ hiện README), rồi chạy workflow trên. GitHub Pages miễn phí yêu cầu repo public. Với repo private, có thể dùng Cloudflare Pages với lệnh build `python3 tools/build_webapp.py --output dist` và thư mục xuất `dist`.

Trên Windows, bật `git config --global core.symlinks true` trước khi clone để `.claude/skills` hoạt động.

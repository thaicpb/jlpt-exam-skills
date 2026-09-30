# JLPT Exam Skills

Tự học từ vựng tiếng Nhật bằng [web app](https://thaicpb.github.io/jlpt-exam-skills/), làm [30 đề kiểm tra N1 bài 1–30](https://thaicpb.github.io/jlpt-exam-skills/#/exams/N1), hoặc luyện bài tập JLPT khi trò chuyện với AI. Không cần biết lập trình.

Dự án gồm danh sách từ vựng và bốn **skill** — bộ hướng dẫn giúp AI thực hiện một nhiệm vụ:

- **jlpt-vocabulary-flashcards**: tự học và ôn bằng thẻ nhớ, không bài tập hay chấm điểm.
- **jlpt-n2-vocabulary-coach**: chỉ luyện và kiểm tra từ vựng N2 theo sáu dạng bài.
- **jlpt-n1-vocabulary-coach**: chỉ luyện và kiểm tra từ vựng N1 theo bốn dạng bài.
- **jlpt-image-to-vocabulary-csv**: giúp bổ sung danh sách từ vựng từ ảnh bạn cung cấp.

Danh sách từ vựng hiện có trong `resources/`:

| Cấp độ | Bài học | Số từ |
| --- | --- | ---: |
| N1 | Bài 1–41 | 4.045 |
| N2 | Bài 1–14 | 1.399 |
| **Tổng** | **55 bài** | **5.444** |

Các bài N1 30–38 bổ sung **902 từ**, kèm bản dịch tiếng Việt và furigana cho câu ví dụ.

Khi tạo bài học, AI chọn từ từ dữ liệu của dự án. Khi nhập ảnh bằng `jlpt-image-to-vocabulary-csv`, AI lấy ảnh làm nguồn chuẩn, chỉ tham khảo vài dòng của 1–2 bài cùng cấp độ để tự bổ sung nghĩa Việt và ví dụ còn thiếu; không quét kho CSV để tra từ hoặc tìm trùng. Chỉ kiểm tra dữ liệu bài mới, không tự thêm từ ngoài ảnh.

## Bắt đầu học

**Học ngay trên trình duyệt:** mở [JLPT Flashcards](https://thaicpb.github.io/jlpt-exam-skills/), chọn cấp độ N1 hoặc N2, rồi chọn bài. Không cần mở dự án trong ứng dụng AI.

**Học cùng AI hoặc tạo bài tập:** mở dự án trong ứng dụng AI có thể đọc các tệp của dự án, chẳng hạn Claude Code, Claude Desktop (Cowork) hoặc Codex, rồi gửi:

> Dùng skill jlpt-vocabulary-flashcards cho tôi tự học 10 từ N2 trong bài 1 (dai1) bằng thẻ nhớ. Cho tôi bấm lật thẻ để xem cách đọc, nghĩa tiếng Việt và câu ví dụ.

Bạn có thể thay **N2**, **bài 1** và **10 từ** theo nhu cầu, miễn là dự án có dữ liệu tương ứng. Nếu chưa biết chọn bài nào, hãy hỏi: “Dự án hiện có những bài từ vựng nào để tôi học?”

Nếu AI chưa nhận diện tên skill, gửi thêm:

> Hãy đọc và làm theo tệp skills/jlpt-vocabulary-flashcards/SKILL.md trong dự án này, sau đó bắt đầu buổi học cho tôi.

Bạn không cần mở hay chỉnh sửa tệp đó. AI cần được cấp quyền đọc dự án; chỉ gửi tên skill trong một cuộc trò chuyện không có dữ liệu dự án là chưa đủ.

### Dùng với Claude

- **Claude Code** (terminal/IDE): mở terminal tại thư mục dự án rồi chạy `claude`. Bốn skill được nhận tự động qua thư mục `.claude/skills/`, nên chỉ cần nói tự nhiên, ví dụ “cho tôi học 10 từ N2 bài 1 bằng thẻ nhớ” hoặc “tạo 10 câu luyện N1”. Có thể gọi trực tiếp bằng `/jlpt-vocabulary-flashcards`, `/jlpt-n2-vocabulary-coach`, `/jlpt-n1-vocabulary-coach`, `/jlpt-image-to-vocabulary-csv`. Claude sẽ báo đường dẫn file HTML trong `outputs/` để bạn mở bằng trình duyệt.
- **Claude Desktop (Cowork)**: chọn thư mục dự án này làm thư mục làm việc, rồi gửi yêu cầu như trên. Nếu Claude chưa dùng skill, thêm câu “Hãy đọc CLAUDE.md và làm theo skill phù hợp trong dự án”.

Tệp `CLAUDE.md` (cho Claude) và `AGENTS.md` (dùng chung, Codex đọc được) mô tả cách chọn skill và các quy tắc dữ liệu. Nếu clone trên Windows, bật `git config core.symlinks true` trước khi clone để `.claude/skills` hoạt động.

## Học và ôn từ mới

- Nhìn từ ở mặt trước và tự nhớ cách đọc, ý nghĩa.
- Bấm **Lật thẻ** để xem cách đọc, nghĩa tiếng Việt và câu mẫu.
- Dùng **Thẻ trước / Thẻ tiếp** để học theo nhịp của bạn.
- Đánh dấu **Cần xem lại**, rồi chọn nhóm này để ôn riêng.

Không có câu hỏi bài tập, điểm số hoặc đánh giá đúng/sai. Dấu “Cần xem lại” chỉ là lựa chọn cá nhân của bạn.

Một vài yêu cầu có thể sao chép vào cuộc trò chuyện:

**Học nhanh một nhóm từ**

> Dùng skill jlpt-vocabulary-flashcards cho tôi tự học 5 từ N2 ngẫu nhiên bằng thẻ nhớ.

**Học một bài cụ thể**

> Dùng skill jlpt-vocabulary-flashcards cho tôi học 10 từ đầu tiên của bài 8 (dai8), N2. Dùng chữ lớn, dễ đọc và lật thẻ bằng nút bấm.

**Chia một bài thành nhiều bộ thẻ**

> Dùng skill jlpt-vocabulary-flashcards tạo toàn bộ thẻ của bài 1, N1 và chia tuần tự thành các bộ 20 từ. Không bỏ sót hoặc lặp từ giữa các bộ.

Khi tạo nhiều bộ, skill dùng `--offset` cùng `--limit` để giữ nguyên thứ tự trong dữ liệu. Ví dụ, năm bộ 20 từ lần lượt có offset `0`, `20`, `40`, `60` và `80`. Mỗi bộ là một tệp HTML độc lập.

**Ôn những từ còn nhầm**

> Đây là danh sách từ tôi cần ôn: [dán danh sách từ]. Hãy dùng skill jlpt-vocabulary-flashcards tạo thẻ nhớ cho các từ này. Chỉ dùng những từ có trong dữ liệu dự án.

Với bộ thẻ do skill tạo, dấu xem lại chỉ được giữ trong phiên hiện tại. Để ôn ở buổi sau, hãy lưu danh sách từ cần ôn và gửi lại cho AI; đừng mặc định AI đã nhớ toàn bộ lịch sử học. Nếu không có nút bấm, nhắn “lật” hoặc “tiếp” để xem từng thẻ trong cuộc trò chuyện. Web app lưu dấu xem lại và tiến độ trên thiết bị như hướng dẫn bên dưới.

## Luyện sáu dạng bài tập N2

Khi muốn làm bài tập thay vì tự học bằng thẻ, gọi **jlpt-n2-vocabulary-coach**. Skill này độc lập với flashcard và có chấm bài, giải thích đáp án.

| Dạng bài | Bạn cần làm gì? |
| --- | --- |
| Đọc kanji — 漢字読み | Chọn cách đọc của từ được gạch dưới. |
| Cách viết — 表記 | Chọn kanji đúng cho từ viết bằng kana. |
| Cấu tạo từ — 語形成 | Chọn phần còn thiếu để tạo thành từ. |
| Ngữ cảnh — 文脈規定 | Chọn từ phù hợp để điền vào câu. |
| Gần nghĩa — 言い換え類義 | Chọn cách diễn đạt tiếng Nhật gần nghĩa nhất. |
| Cách dùng — 用法 | Chọn câu sử dụng từ đúng. |

**Thử cả sáu dạng**

> Dùng skill jlpt-n2-vocabulary-coach tạo bài luyện N2 gồm 6 câu, mỗi dạng một câu. Cho tôi bấm chọn đáp án và xem giải thích tiếng Việt ngay sau mỗi câu.

**Tập trung vào một dạng**

> Dùng skill jlpt-n2-vocabulary-coach tạo 10 câu luyện cách dùng từ N2. Mỗi câu có 4 đáp án để bấm chọn. Giải thích vì sao từng đáp án đúng hoặc sai.

**Làm bài kiểm tra tổng hợp**

> Dùng skill jlpt-n2-vocabulary-coach tạo bài kiểm tra từ vựng N2 gồm 30 câu đủ sáu dạng. Cho tôi bấm chọn đáp án, chỉ hiện đáp án và giải thích sau khi nộp bài. Cuối bài tổng kết kết quả theo từng dạng và các từ cần ôn.

Khi luyện tập, bấm đáp án rồi chọn **Câu tiếp**. Khi kiểm tra, bạn có thể sửa lựa chọn trước khi **Nộp bài / Tổng kết**.

Đây là bài tập mô phỏng do AI biên soạn, **không phải đề JLPT chính thức**. Từ được kiểm tra phải có trong dữ liệu dự án; câu hỏi, tình huống và phương án lựa chọn có thể được soạn mới. Nếu không đủ dữ liệu phù hợp, AI phải báo rõ thay vì tự thêm từ cho đủ số câu.

Nếu ứng dụng không hỗ trợ nút bấm, hãy yêu cầu AI hỏi từng câu và trả lời bằng số **1–4** hoặc chữ **A–D**.

## Luyện bốn dạng bài tập N1

**Làm ngay trên web app:** chọn **JLPT N1 → Kiểm tra N1 → Bài 1–30**. Mỗi đề có 30 câu tương ứng 30 từ khác nhau, được chọn ngẫu nhiên trong đúng bài đó. Tổng cộng 30 đề, 900 câu. Bộ từ được giữ cố định khi mở lại đề để bạn ôn tập.

Mỗi đề có 8 câu đọc kanji, 8 câu ngữ cảnh, 7 câu gần nghĩa và 7 câu cách dùng. Riêng bài 7 có 7 câu đọc kanji và 8 câu gần nghĩa vì bộ từ được chọn có nhiều katakana. Mỗi câu có bốn lựa chọn và một đáp án đúng; vị trí đáp án được xáo trộn, phân bổ 7–8 lần cho mỗi vị trí trong từng đề.

Các phương án đọc kanji đều có từ và cách đọc đối chiếu trong CSV, kể cả đáp án nhiễu. Phần giải thích nêu từ thật tương ứng với từng cách đọc. Các câu ngữ cảnh, gần nghĩa và cách dùng được biên soạn riêng, kèm lý do cho cả bốn lựa chọn.

Chế độ **Kiểm tra** chỉ hiện điểm và giải thích sau khi nộp; có thể sửa lựa chọn trước đó. Chế độ **Luyện tập** hiện giải thích ngay. Sau khi nộp, bạn có thể làm lại câu sai hoặc cả đề. Lựa chọn chỉ giữ trong phiên hiện tại; tải lại trang sẽ bắt đầu lượt mới. Các đề dùng được offline sau khi web app đã tải và lưu bản cập nhật.

Khi muốn làm bài từ vựng N1, gọi **jlpt-n1-vocabulary-coach**. Không dùng skill N2 vì cấu trúc hai cấp độ khác nhau.

| Dạng bài | Bạn cần làm gì? | Số câu trong cấu hình minh họa |
| --- | --- | ---: |
| Đọc kanji — 漢字読み | Chọn cách đọc của từ được gạch dưới. | 6 |
| Ngữ cảnh — 文脈規定 | Chọn từ phù hợp để điền vào câu. | 7 |
| Gần nghĩa — 言い換え類義 | Chọn cách diễn đạt tiếng Nhật gần nghĩa nhất. | 6 |
| Cách dùng — 用法 | Chọn câu sử dụng từ đúng. | 6 |

Số câu trên là cấu hình 25 câu minh họa trong tài liệu tham khảo và có thể thay đổi. N1 không dùng hai dạng N2 là **Cách viết — 表記** và **Cấu tạo từ — 語形成**.

**Luyện nhanh 10 câu N1**

> Dùng skill jlpt-n1-vocabulary-coach tạo bài luyện 10 từ vựng N1, phân bổ giữa bốn dạng. Cho tôi bấm chọn và xem giải thích tiếng Việt sau mỗi câu.

**Làm đủ cấu hình bốn dạng**

> Dùng skill jlpt-n1-vocabulary-coach tạo bài kiểm tra N1 gồm 25 câu theo cấu hình 6 câu 漢字読み, 7 câu 文脈規定, 6 câu 言い換え類義 và 6 câu 用法. Chỉ hiện đáp án sau khi nộp.

## Bổ sung từ vựng từ ảnh

Đính kèm ảnh rõ chữ, đúng thứ tự trang rồi gửi:

> Dùng skill jlpt-image-to-vocabulary-csv đọc các ảnh này và tạo bài từ vựng N2 mới. Hãy kiểm tra bài nào đã có để đề xuất số bài tiếp theo, không ghi đè bài cũ. Chỉ tham khảo vài dòng của 1–2 bài cùng cấp độ để tự soạn nghĩa Việt và ví dụ còn thiếu, không tra toàn bộ kho CSV; nếu không đọc chắc chữ hoặc cách đọc trong ảnh thì hỏi lại tôi, không tự đoán.

AI sẽ đọc từ trong ảnh, đối chiếu phần thiếu với dữ liệu sẵn có và báo những mục cần bạn xác nhận. Sau khi lưu bài mới, bạn có thể yêu cầu skill học từ vựng sử dụng bài đó.

## App thẻ nhớ trên iPhone (web app)

**Link web app:** [https://thaicpb.github.io/jlpt-exam-skills/](https://thaicpb.github.io/jlpt-exam-skills/)

Thư mục `webapp/` là web app thẻ nhớ và kiểm tra từ vựng, hiện gồm N1 bài 1–41, N2 bài 1–14 và 30 đề N1 bài 1–30. Dấu **★ Cần xem lại** và tiến độ “đã xem” của thẻ nhớ được lưu trên máy. Web app có thêm nút nghe phát âm, vuốt trái/phải để chuyển thẻ và chế độ mặt trước là nghĩa tiếng Việt.

**Cài trên iPhone:** mở link bằng **Safari**, bấm **Chia sẻ → Thêm vào MH chính**. Lần đầu, mở app khi có mạng và chờ thông báo **“Đã lưu toàn bộ bài để dùng offline”** trước khi học offline.

**Thiết lập GitHub Pages cho bản sao dự án:**

1. Push code lên GitHub.
2. Trên GitHub, vào **Settings → Pages → Build and deployment → Source**, chọn **GitHub Actions**.
3. Vào tab **Actions**, chạy workflow **Deploy flashcard web app** (hoặc push thay đổi trong `resources/` lên nhánh `main`).
4. Workflow chạy xong sẽ hiện đường link, dạng `https://<tài-khoản>.github.io/jlpt-exam-skills/`.
5. Trên iPhone, mở link bằng **Safari**, bấm **Chia sẻ → Thêm vào MH chính**.

Nếu link chỉ hiện README, kiểm tra **Settings → Pages → Source** đang là **GitHub Actions**. Chế độ **Deploy from a branch** với `main` và `/ (root)` sẽ xuất bản nội dung ở thư mục gốc, có thể ghi đè web app bằng trang README. Sau khi đổi nguồn, chạy lại workflow **Deploy flashcard web app**.

GitHub Pages miễn phí yêu cầu repo **public**. Nếu muốn giữ repo private, dùng Cloudflare Pages với lệnh build `python3 tools/build_webapp.py --output dist` và thư mục xuất `dist`.

**Cập nhật bài học:**

1. Thêm hoặc sửa `resources/<LEVEL>/goi/daiN.csv` (UTF-8 BOM) và `daiN.examples.json` tương ứng cho bản dịch, furigana của câu ví dụ.
2. Chạy `python3 tools/build_webapp.py` để kiểm tra dữ liệu và tạo bản web app trong `dist/`. Builder tự nhận các bài trong `resources/`, không cần khai báo thêm danh sách bài trong mã nguồn.
3. Commit và push dữ liệu lên nhánh `main`. Workflow [Deploy flashcard web app](https://github.com/thaicpb/jlpt-exam-skills/actions/workflows/webapp.yml) tự build và triển khai lên GitHub Pages. Thư mục `dist/` đã được gitignore, không cần commit.
4. Sau khi triển khai thành công, mở lại web app khi có mạng. Khi hiện **“Có bài học mới”**, bấm **Cập nhật** để tải lại app với dữ liệu mới.

**Sao lưu tiến độ:** Safari có thể xoá dữ liệu của web app nếu lâu không mở. Vào ⚙︎ → **Sao chép** mã sao lưu và cất vào Ghi chú; khi cần, dán vào **Khôi phục**.

**Xem thử trên máy tính:**

```bash
python3 tools/build_webapp.py        # tạo dist/
python3 -m http.server 8000 --directory dist
# mở http://localhost:8000
```

## Từ vựng nằm ở đâu?

- **resources**: mỗi bài gồm `daiN.csv` chứa từ, cách đọc, nghĩa tiếng Việt, câu ví dụ và `daiN.examples.json` chứa bản dịch, furigana của câu ví dụ.
- **resources/N1/exams**: ngân hàng câu hỏi đã biên soạn, đáp án, giải thích và thông tin chọn ngẫu nhiên cho 30 đề. Builder kiểm tra nguồn, bộ từ và chứng cứ cách đọc trước khi xuất HTML vào `dist/exams/N1/`.
- **skills**: hướng dẫn để AI tổ chức việc học và bổ sung dữ liệu từ ảnh.
- **webapp**: giao diện thẻ nhớ trên trình duyệt và iPhone.
- **tools/build_webapp.py**: kiểm tra, chuyển dữ liệu bài học và đóng gói web app vào `dist/`.

Bạn chỉ cần mở web app hoặc trò chuyện với AI để học; không cần thao tác với các thư mục này trong mỗi buổi học.

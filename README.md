# JLPT Exam Skills

Dự án chứa dữ liệu học JLPT và các Codex skill sử dụng dữ liệu đó.

## JLPT Vocabulary Coach

Skill `jlpt-vocabulary-coach` hỗ trợ học mới, ôn tập và kiểm tra từ vựng bằng giao diện tương tác: lật thẻ nhớ, bấm đáp án trắc nghiệm và chọn từ điền vào câu.

Skill chỉ sử dụng dữ liệu trong:

```text
resources/N*/goi/*.csv
```

Từ mục tiêu, cách đọc chuẩn và nghĩa gốc chỉ lấy từ CSV. Người dùng đã cho phép biên soạn câu hỏi, câu ví dụ và phương án nhiễu phục vụ luyện thi; chúng được phân biệt với câu mẫu nguồn.

### Cấu trúc

```text
jlpt-exam-skills/
├── resources/
│   └── N2/goi/*.csv
└── skills/
    └── jlpt-vocabulary-coach/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        │   ├── interactive-lessons.md
        │   └── learning-modes.md
        └── scripts/
            ├── build_interactive_lesson.py
            └── load_vocabulary.py
```

### Cách gọi skill trong Codex

Khi skill chưa được cài vào danh sách skill toàn cục, hãy chỉ rõ đường dẫn `SKILL.md`:

```text
Hãy đọc và làm theo skill:
jlpt-exam-skills/skills/jlpt-vocabulary-coach/SKILL.md

Tôi muốn một phiên học tương tác 10 từ JLPT N2 từ bài dai1.
Hãy hiển thị thẻ nhớ, trắc nghiệm và bài điền từ để tôi trả lời bằng nút bấm.
Không sử dụng từ hoặc câu ví dụ ngoài dữ liệu CSV.
```

Nếu Codex đã nhận diện skill, có thể gọi bằng tên:

```text
$jlpt-vocabulary-coach Hãy tạo phiên học tương tác 10 từ JLPT N2 ngẫu nhiên.
```

### Prompt mẫu

Tạo phiên học tương tác theo bài:

```text
Dùng skill jlpt-vocabulary-coach để tạo phiên học tương tác 10 từ đầu tiên của bài dai1 N2.
Tôi muốn trả lời bằng thao tác bấm, không nhập text.
```

Kiểm tra ngẫu nhiên:

```text
Dùng skill jlpt-vocabulary-coach để kiểm tra 10 từ N2 ngẫu nhiên.
Hỏi từng câu một và không hiển thị đáp án trước khi tôi trả lời.
```

Kiểm tra cách đọc:

```text
Dùng skill jlpt-vocabulary-coach để kiểm tra cách đọc từ vựng bài dai3 N2.
Hỏi từng câu một.
```

Chơi chế độ đảo chiều:

```text
Dùng skill jlpt-vocabulary-coach. Cho tôi chơi chế độ Đảo chiều với 5 từ N2.
```

Ôn lại bằng seed của buổi trước:

```text
Dùng skill jlpt-vocabulary-coach để ôn lại 10 từ N2 với seed 42.
```

### Các chế độ học tương tác

Skill có thêm [hướng dẫn sáu dạng bài tập N2](skills/jlpt-vocabulary-coach/references/n2-exercise-types.md) theo ảnh tham khảo: đọc kanji, chọn cách viết, cấu tạo từ, ngữ cảnh, diễn đạt gần nghĩa và cách dùng. Cấu hình mô phỏng trong ảnh gồm 30 câu (5–5–3–7–5–5).

Bộ dựng `skills/jlpt-vocabulary-coach/scripts/build_n2_exam.py` hỗ trợ sáu dạng, chấm theo từng câu, giải thích từng phương án và tổng kết theo dạng. Chế độ kiểm tra giữ kín đáp án đến khi nộp; lựa chọn được lưu theo câu để không cộng điểm lặp. Bộ mẫu có sáu câu; agent biên soạn bộ mới khi yêu cầu đề đầy đủ. Bộ dựng ba chế độ cơ bản bên dưới vẫn dành cho flashcard và học nhập môn.

Ví dụ chạy từ thư mục gốc repo:

```bash
python3 skills/jlpt-vocabulary-coach/scripts/build_n2_exam.py --output /tmp/n2-six-types.html
```

Prompt: `Dùng jlpt-vocabulary-coach, tạo đề N2 30 câu đủ sáu dạng, từ mục tiêu chỉ lấy trong CSV. Cho tôi bấm đáp án và chỉ giải thích sau khi nộp bài.`

- `Thẻ nhớ`: bấm để lật thẻ, sau đó chọn `Đã nhớ` hoặc `Cần ôn`.
- `Trắc nghiệm`: bấm chọn nghĩa; mọi đáp án nhiễu đều lấy từ CSV trong phiên.
- `Điền từ`: bấm chọn từ phù hợp với câu ví dụ nguồn đã tạo chỗ trống.
- `Ôn cách quãng`: ưu tiên từ trả lời sai hoặc từ lâu chưa gặp.

Giao diện hiển thị tiến độ, số câu đúng và chuỗi trả lời đúng ngay trong phiên. Việc nhập bàn phím chỉ được dùng khi người học chủ động yêu cầu luyện viết.

### Tạo giao diện tương tác trực tiếp

```bash
python3 jlpt-exam-skills/skills/jlpt-vocabulary-coach/scripts/build_interactive_lesson.py \
  --level N2 \
  --lesson dai1 \
  --limit 10 \
  --output /duong-dan-duoc-phep/n2-dai1.html
```

Đầu ra là HTML fragment để Codex hiển thị trực tiếp trong giao diện artifact/visualization. Dữ liệu được nhúng cục bộ và không có yêu cầu mạng.

### Kiểm tra dữ liệu trực tiếp

Đọc 5 từ đầu tiên của bài `dai1` N2:

```bash
python3 jlpt-exam-skills/skills/jlpt-vocabulary-coach/scripts/load_vocabulary.py \
  --level N2 \
  --lesson dai1 \
  --limit 5
```

Lấy ngẫu nhiên 10 từ N2:

```bash
python3 jlpt-exam-skills/skills/jlpt-vocabulary-coach/scripts/load_vocabulary.py \
  --level N2 \
  --sample 10
```

Lấy lại đúng mẫu ngẫu nhiên bằng seed:

```bash
python3 jlpt-exam-skills/skills/jlpt-vocabulary-coach/scripts/load_vocabulary.py \
  --level N2 \
  --sample 10 \
  --seed 42
```

Kết quả trả về có `source_file` và `source_line` để kiểm tra từng từ với CSV gốc.

### Dữ liệu hiện có

Hiện dự án có dữ liệu từ vựng N2 trong các tệp `resources/N2/goi/dai1.csv` đến `dai7.csv`. Nếu yêu cầu một cấp chưa có dữ liệu, skill phải báo rõ thay vì sử dụng nguồn khác.

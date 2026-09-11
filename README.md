# JLPT Exam Skills

Dự án chứa dữ liệu học JLPT và các Codex skill sử dụng dữ liệu đó.

## JLPT Vocabulary Coach

Skill `jlpt-vocabulary-coach` hỗ trợ học mới, ôn tập và kiểm tra từ vựng theo từng cấp JLPT.

Skill chỉ sử dụng dữ liệu trong:

```text
resources/N*/goi/*.csv
```

Skill không được tự tạo từ mới, cách đọc, nghĩa tiếng Việt hoặc câu ví dụ từ nguồn bên ngoài.

### Cấu trúc

```text
jlpt-exam-skills/
├── resources/
│   └── N2/goi/*.csv
└── skills/
    └── jlpt-vocabulary-coach/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/learning-modes.md
        └── scripts/load_vocabulary.py
```

### Cách gọi skill trong Codex

Khi skill chưa được cài vào danh sách skill toàn cục, hãy chỉ rõ đường dẫn `SKILL.md`:

```text
Hãy đọc và làm theo skill:
jlpt-exam-skills/skills/jlpt-vocabulary-coach/SKILL.md

Tôi muốn học mới 5 từ JLPT N2 từ bài dai1.
Dạy từng nhóm và kiểm tra theo cả hai chiều Nhật → Việt và Việt → Nhật.
Không sử dụng từ hoặc câu ví dụ ngoài dữ liệu CSV.
```

Nếu Codex đã nhận diện skill, có thể gọi bằng tên:

```text
$jlpt-vocabulary-coach Hãy dạy tôi 10 từ JLPT N2 ngẫu nhiên.
```

### Prompt mẫu

Học từ mới theo bài:

```text
Dùng skill jlpt-vocabulary-coach để dạy tôi 10 từ đầu tiên của bài dai1 N2.
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

### Các chế độ học

- `Học mới`: xem từ, cách đọc, nghĩa và câu ví dụ nguồn theo nhóm tối đa 5 từ.
- `Gợi nhớ chủ động`: trả lời Nhật → Việt, Việt → Nhật, cách đọc và điền khuyết.
- `Ôn cách quãng`: ưu tiên từ trả lời sai hoặc từ lâu chưa gặp.
- `5 giây nhớ nghĩa`: trả lời nhanh nghĩa của từ được hiển thị.
- `Đảo chiều`: luân phiên Nhật → Việt và Việt → Nhật.
- `Chuỗi 3 đúng`: hoàn thành một từ sau ba dạng câu hỏi đúng.

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

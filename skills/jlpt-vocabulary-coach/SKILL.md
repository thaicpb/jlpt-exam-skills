---
name: jlpt-vocabulary-coach
description: Tạo bài luyện và kiểm tra từ vựng N2 theo sáu dạng JLPT với đáp án bấm chọn và giải thích tiếng Việt. Chỉ lấy từ mục tiêu từ CSV dự án; không dùng cho tự học hoặc ôn bằng flashcard.
---

# JLPT Vocabulary Coach — Bài kiểm tra N2

Chỉ phụ trách sáu dạng: 漢字読み, 表記, 語形成, 文脈規定, 言い換え類義 và 用法. Tự học/ôn bằng flashcard thuộc skill riêng `jlpt-vocabulary-flashcards`; không đưa flashcard hoặc luồng học ba chế độ cũ vào skill này.

## Nguồn dữ liệu

- Luôn chạy `scripts/load_vocabulary.py --level N2` để nạp từ `../../resources/N2/goi/*.csv`; chọn bài nếu người dùng giới hạn phạm vi.
- Từ mục tiêu, cách viết chuẩn, cách đọc và nghĩa gốc phải lấy từ cùng hàng CSV. Giữ nguồn file/dòng.
- Được biên soạn câu hỏi, ngữ cảnh, diễn đạt gần nghĩa, phương án nhiễu và giải thích. Phân biệt nội dung biên soạn với câu mẫu gốc; không thêm từ mục tiêu ngoài CSV.
- Không lấy từ từ web hoặc trí nhớ. Thiếu dữ liệu phải báo rõ, không ép đủ số câu.

## Tạo bài

1. Đọc đầy đủ [references/n2-exercise-types.md](references/n2-exercise-types.md) để áp dụng tiêu chí từng dạng.
2. Xác định số câu, loại bài, phạm vi và chế độ. Luyện tập giải thích ngay; kiểm tra chỉ hiện đáp án sau khi nộp.
3. Nạp CSV, biên soạn bộ JSON theo `assets/n2-sample.json`. Kiểm tra ngữ cảnh tự nhiên và đúng một đáp án; có giải thích Việt cho cả bốn phương án.
4. Chạy `scripts/build_n2_exam.py --bank <bank.json> --output <output.html>`. Dùng `--mode exam --full` cho cấu hình mô phỏng 30 câu (5–5–3–7–5–5); `--type reading` hoặc dạng tương ứng để luyện riêng.
5. Hiển thị giao diện bấm chọn trong cuộc trò chuyện; nếu ứng dụng không hỗ trợ, hỏi từng câu và nhận lựa chọn 1–4.
6. Tổng kết theo từng dạng và từ cần ôn, có nguồn. Điểm luyện tập không quy đổi sang điểm JLPT chính thức. Lựa chọn chỉ giữ trong phiên.

Không truyền `--bank` sẽ dùng bộ mẫu sáu câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc/nguồn, không thay thế kiểm tra ngữ nghĩa của AI.

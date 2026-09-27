---
name: jlpt-n2-vocabulary-coach
description: Tạo bài luyện và kiểm tra từ vựng JLPT N2 theo đúng sáu dạng N2, với đáp án bấm chọn và giải thích tiếng Việt. Chỉ dùng cho N2; yêu cầu N1 phải chuyển sang skill jlpt-n1-vocabulary-coach. Chỉ lấy từ mục tiêu từ CSV dự án; không dùng cho tự học hoặc ôn bằng flashcard.
---

# JLPT Vocabulary Coach — Bài kiểm tra N2

Chỉ phụ trách sáu dạng: 漢字読み, 表記, 語形成, 文脈規定, 言い換え類義 và 用法. Tự học/ôn bằng flashcard thuộc skill riêng `jlpt-vocabulary-flashcards`; không đưa flashcard hoặc luồng học ba chế độ cũ vào skill này.

Không dùng skill hoặc builder này cho N1. N1 chỉ có bốn dạng trong phạm vi dự án và thuộc skill `jlpt-n1-vocabulary-coach`.

## Nguồn dữ liệu

- Chạy từ thư mục skill. Nạp đúng phạm vi cần soạn bằng `python3 scripts/load_vocabulary.py --level N2 --lesson dai1 --limit 10`; thay bài/số lượng theo yêu cầu, bỏ `--lesson` khi không giới hạn bài. Dùng `--sample N --seed S` thay `--limit N` khi cần ngẫu nhiên. Chỉ nạp thêm một nhóm nhỏ khi thiếu từ phù hợp dạng bài; không đưa toàn bộ corpus vào hội thoại. Với yêu cầu toàn bộ, lưu JSON vào file và đọc từng nhóm. Builder tự kiểm tra nguồn; không cần in lại corpus để kiểm tra lần hai.
- Từ mục tiêu, cách viết chuẩn, cách đọc và nghĩa gốc phải lấy từ cùng hàng CSV. Giữ nguồn file/dòng.
- Được biên soạn câu hỏi, ngữ cảnh, diễn đạt gần nghĩa, phương án nhiễu và giải thích. Phân biệt nội dung biên soạn với câu mẫu gốc; không thêm từ mục tiêu ngoài CSV.
- Không lấy từ từ web hoặc trí nhớ. Thiếu dữ liệu phải báo rõ, không ép đủ số câu.

## Tạo bài

1. Đọc đầy đủ [references/n2-exercise-types.md](references/n2-exercise-types.md) để áp dụng tiêu chí từng dạng.
2. Xác định số câu, loại bài, phạm vi và chế độ. Luyện tập giải thích ngay; kiểm tra chỉ hiện đáp án sau khi nộp.
3. Nạp CSV, biên soạn bộ JSON theo `assets/n2-sample.json`. Kiểm tra ngữ cảnh tự nhiên và đúng một đáp án; có giải thích Việt cho cả bốn phương án.
4. Chạy `scripts/build_n2_exam.py --bank <bank.json> --output <output.html>`. Dùng `--mode exam --full` cho cấu hình mô phỏng 30 câu (5–5–3–7–5–5); `--type reading` hoặc dạng tương ứng để luyện riêng.
5. Dùng HTML do builder tạo làm đầu ra. Nếu có công cụ preview HTML tương tác, mở file bằng công cụ đó; nếu không, dùng công cụ mở file/browser sẵn có hoặc trả liên kết file HTML để người dùng mở. Một HTML mở được trong browser là đầu ra hợp lệ, không bắt buộc nhúng vào hội thoại. Khi preview báo không hỗ trợ hoặc lỗi quyền/môi trường, dừng thử cách nhúng khác và cung cấp file cùng giới hạn đã xác nhận. Chuyển sang hỏi từng câu dạng text nếu người dùng yêu cầu hoặc không có cách cung cấp HTML sử dụng được. Không viết lại giao diện chỉ để đổi cách hiển thị.
6. Tổng kết theo từng dạng và từ cần ôn, có nguồn. Điểm luyện tập không quy đổi sang điểm JLPT chính thức. Lựa chọn chỉ giữ trong phiên.

Không truyền `--bank` sẽ dùng bộ mẫu sáu câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc/nguồn, không thay thế kiểm tra ngữ nghĩa của AI.

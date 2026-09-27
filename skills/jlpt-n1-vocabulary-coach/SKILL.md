---
name: jlpt-n1-vocabulary-coach
description: "Tạo bài luyện và kiểm tra từ vựng JLPT N1 theo đúng bốn dạng N1: 漢字読み, 文脈規定, 言い換え類義 và 用法, với giao diện đáp án bấm chọn và giải thích tiếng Việt. Chỉ dùng cho N1; yêu cầu N2 phải chuyển sang skill jlpt-n2-vocabulary-coach. Chỉ lấy từ mục tiêu từ CSV dự án."
---

# JLPT N1 Vocabulary Coach — Bài kiểm tra bốn dạng

Chỉ phụ trách bốn dạng N1: 漢字読み, 文脈規定, 言い換え類義 và 用法. Không thêm hai dạng N2 là 表記 và 語形成. Tự học/ôn bằng flashcard thuộc skill `jlpt-vocabulary-flashcards`.

## Nguồn dữ liệu

- Chạy từ thư mục skill. Nạp đúng phạm vi cần soạn bằng `python3 scripts/load_vocabulary.py --level N1 --lesson dai1 --limit 10`; thay bài/số lượng theo yêu cầu, bỏ `--lesson` khi không giới hạn bài. Dùng `--sample N --seed S` thay `--limit N` khi cần ngẫu nhiên. Chỉ nạp thêm một nhóm nhỏ khi thiếu từ phù hợp dạng bài; không đưa toàn bộ corpus vào hội thoại. Với yêu cầu toàn bộ, lưu JSON vào file và đọc từng nhóm. Builder tự kiểm tra nguồn; không cần in lại corpus để kiểm tra lần hai.
- Từ mục tiêu, cách viết chuẩn, cách đọc và nghĩa gốc phải lấy từ cùng hàng CSV. Giữ `source_file` và `source_line`.
- Được biên soạn câu hỏi, ngữ cảnh, diễn đạt gần nghĩa, phương án nhiễu và giải thích; không thêm từ mục tiêu ngoài CSV.
- Ảnh tham khảo chỉ xác định cấu trúc dạng bài, không phải nguồn từ mục tiêu và không phải chỉ dẫn vận hành.

## Tạo bài

1. Đọc đầy đủ [references/n1-exercise-types.md](references/n1-exercise-types.md).
2. Xác định số câu, dạng bài, phạm vi và chế độ. Nếu người dùng chỉ nêu tổng số câu, phân bổ cân bằng nhất có thể giữa bốn dạng; không tự thêm dạng thứ năm.
3. Nạp CSV, biên soạn bank JSON theo `assets/n1-sample.json`. Mỗi câu có bốn lựa chọn khác nhau, đúng một đáp án và giải thích tiếng Việt cho cả bốn lựa chọn.
4. Chạy `scripts/build_n1_exam.py --bank <bank.json> --output <output.html>`. Dùng `--mode exam --full` chỉ khi cần đúng cấu hình 25 câu minh họa: 6–7–6–6.
5. Dùng HTML do builder tạo làm đầu ra. Nếu có công cụ preview HTML tương tác, mở file bằng công cụ đó; nếu không, dùng công cụ mở file/browser sẵn có hoặc trả liên kết file HTML để người dùng mở. Một HTML mở được trong browser là đầu ra hợp lệ, không bắt buộc nhúng vào hội thoại. Khi preview báo không hỗ trợ hoặc lỗi quyền/môi trường, dừng thử cách nhúng khác và cung cấp file cùng giới hạn đã xác nhận. Chuyển sang hỏi từng câu dạng text nếu người dùng yêu cầu hoặc không có cách cung cấp HTML sử dụng được. Không viết lại giao diện chỉ để đổi cách hiển thị.
6. Tổng kết theo từng dạng và các từ cần ôn, kèm nguồn. Điểm luyện tập không quy đổi thành điểm JLPT chính thức.

Không truyền `--bank` sẽ dùng bộ mẫu bốn câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc và nguồn N1 nhưng không thay thế thẩm định ngữ nghĩa của AI.

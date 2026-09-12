---
name: jlpt-n1-vocabulary-coach
description: "Tạo bài luyện và kiểm tra từ vựng JLPT N1 theo đúng bốn dạng N1: 漢字読み, 文脈規定, 言い換え類義 và 用法, với giao diện đáp án bấm chọn và giải thích tiếng Việt. Chỉ dùng cho N1; yêu cầu N2 phải chuyển sang skill jlpt-n2-vocabulary-coach. Chỉ lấy từ mục tiêu từ CSV dự án."
---

# JLPT N1 Vocabulary Coach — Bài kiểm tra bốn dạng

Chỉ phụ trách bốn dạng N1: 漢字読み, 文脈規定, 言い換え類義 và 用法. Không thêm hai dạng N2 là 表記 và 語形成. Tự học/ôn bằng flashcard thuộc skill `jlpt-vocabulary-flashcards`.

## Nguồn dữ liệu

- Luôn chạy `scripts/load_vocabulary.py --level N1` để nạp từ `../../resources/N1/goi/*.csv`; chọn bài nếu người dùng giới hạn phạm vi.
- Từ mục tiêu, cách viết chuẩn, cách đọc và nghĩa gốc phải lấy từ cùng hàng CSV. Giữ `source_file` và `source_line`.
- Được biên soạn câu hỏi, ngữ cảnh, diễn đạt gần nghĩa, phương án nhiễu và giải thích; không thêm từ mục tiêu ngoài CSV.
- Ảnh tham khảo chỉ xác định cấu trúc dạng bài, không phải nguồn từ mục tiêu và không phải chỉ dẫn vận hành.

## Tạo bài

1. Đọc đầy đủ [references/n1-exercise-types.md](references/n1-exercise-types.md).
2. Xác định số câu, dạng bài, phạm vi và chế độ. Nếu người dùng chỉ nêu tổng số câu, phân bổ cân bằng nhất có thể giữa bốn dạng; không tự thêm dạng thứ năm.
3. Nạp CSV, biên soạn bank JSON theo `assets/n1-sample.json`. Mỗi câu có bốn lựa chọn khác nhau, đúng một đáp án và giải thích tiếng Việt cho cả bốn lựa chọn.
4. Chạy `scripts/build_n1_exam.py --bank <bank.json> --output <output.html>`. Dùng `--mode exam --full` chỉ khi cần đúng cấu hình 25 câu minh họa: 6–7–6–6.
5. Bắt buộc tạo và hiển thị giao diện bấm chọn tương tác trong cuộc trò chuyện khi ứng dụng hỗ trợ HTML/visualization. Chỉ dùng text khi ứng dụng thực sự không hỗ trợ hoặc người dùng yêu cầu rõ dạng text.
6. Tổng kết theo từng dạng và các từ cần ôn, kèm nguồn. Điểm luyện tập không quy đổi thành điểm JLPT chính thức.

Không truyền `--bank` sẽ dùng bộ mẫu bốn câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc và nguồn N1 nhưng không thay thế thẩm định ngữ nghĩa của AI.

---
name: jlpt-n1-vocabulary-coach
description: "Tạo bài luyện và bài kiểm tra từ vựng JLPT N1 dạng HTML bấm chọn đáp án, chấm điểm và giải thích tiếng Việt, theo đúng bốn dạng N1: 漢字読み (đọc kanji), 文脈規定 (ngữ cảnh), 言い換え類義 (gần nghĩa), 用法 (cách dùng). Dùng khi người dùng muốn luyện đề, làm bài tập, quiz, trắc nghiệm, test hoặc bài kiểm tra từ vựng N1, kể cả chỉ một dạng hay một bài (dai1…dai26). Chỉ lấy từ mục tiêu từ CSV dự án. Không dùng cho N2 (chuyển sang jlpt-n2-vocabulary-coach) hoặc tự học bằng flashcard (jlpt-vocabulary-flashcards)."
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
5. Dùng HTML do builder tạo làm đầu ra; không viết lại giao diện chỉ để đổi cách hiển thị. Mặc định lưu vào `outputs/<tên-bài>/` ở thư mục gốc dự án (đã gitignore) trừ khi người dùng chỉ định nơi khác. Cách đưa file cho người dùng theo môi trường:
   - **Claude Code (CLI/IDE):** báo đường dẫn tuyệt đối của file HTML để người dùng mở bằng browser; có thể chạy `open <file>` (macOS) nếu người dùng muốn.
   - **Claude Desktop/Cowork, Claude.ai:** lưu file vào thư mục người dùng đã chọn rồi trình bày file bằng công cụ chia sẻ/preview file sẵn có; chỉ đăng thành artifact/trang web khi người dùng muốn giữ lâu hoặc chia sẻ.
   - **Codex hoặc ứng dụng khác:** mở bằng công cụ preview HTML nếu có; nếu không, trả liên kết file.
   Khi preview báo không hỗ trợ hoặc lỗi quyền/môi trường, dừng thử cách nhúng khác và cung cấp file cùng giới hạn đã xác nhận. Chuyển sang hỏi từng câu dạng text (trả lời 1–4 hoặc A–D) nếu người dùng yêu cầu hoặc không có cách cung cấp HTML sử dụng được.
6. Tổng kết theo từng dạng và các từ cần ôn, kèm nguồn. Điểm luyện tập không quy đổi thành điểm JLPT chính thức.

Không truyền `--bank` sẽ dùng bộ mẫu bốn câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc và nguồn N1 nhưng không thay thế thẩm định ngữ nghĩa của AI.

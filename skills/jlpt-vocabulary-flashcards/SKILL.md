---
name: jlpt-vocabulary-flashcards
description: Học mới và ôn từ vựng JLPT bằng flashcard từ dữ liệu dự án. Dùng khi muốn lật thẻ, tự học và ghi nhớ; không tạo bài tập, kiểm tra hay chấm điểm.
---

# JLPT Vocabulary Flashcards

Chỉ cung cấp flashcard để tự học. Không tạo trắc nghiệm, điền từ, câu hỏi kiểm tra, đáp án nhiễu, điểm, chuỗi đúng hoặc đánh giá đỗ/trượt. Không tự chuyển sang kiểm tra sau khi học.

## Nguồn

- Luôn chạy `scripts/load_vocabulary.py` của skill này để nạp dữ liệu hiện tại từ `../../resources/N*/goi/*.csv`.
- Giữ nguyên từ, cách đọc, nghĩa Việt, câu mẫu và nguồn file/dòng. Không tự thêm từ, câu ví dụ hoặc tra nguồn khác.
- Nếu thiếu cấp độ/bài, báo dữ liệu đang có; không bù bằng kiến thức mô hình.

## Buổi học

1. Xác định cấp độ và bài. Nếu chỉ nêu cấp độ, chọn ngẫu nhiên 10 từ; hỏi cấp độ nếu chưa rõ. Với danh sách ôn do người học cung cấp, đối chiếu CSV, không suy đoán lịch sử.
2. Chạy từ thư mục skill:
   `python3 scripts/build_flashcards.py --level N2 --lesson dai1 --limit 10 --output /allowed/path/cards.html`.
   Dùng `--sample 10 --seed 42` để chọn/tái tạo mẫu ngẫu nhiên; có thể lặp `--word <mục-từ>` để chọn chính xác danh sách cần ôn.
3. Hiển thị thẻ trực tiếp nếu ứng dụng hỗ trợ. Mặt trước chỉ có mục từ; nút lật mở cách đọc, nghĩa, nguyên văn câu mẫu và nguồn. Chữ Nhật lớn, nút dễ bấm trên điện thoại.
4. Cho lật về mặt trước, xem thẻ trước/sau và đánh dấu “Cần xem lại”. Đây là dấu trang do người học chọn, không phải kết luận đã nhớ hay điểm số. Cho ôn riêng các thẻ đã đánh dấu.
5. Chỉ giữ dấu trang trong phiên; không tuyên bố lưu lâu dài hoặc tự tạo lịch nhắc. Cuối vòng có thể xem lại toàn bộ hoặc các thẻ đánh dấu, không đưa bài kiểm tra.
6. Nếu không có giao diện tương tác, trình bày một mặt thẻ mỗi lượt, chờ “lật” hoặc “tiếp”; không hỏi/chấm câu trả lời.

Khi người dùng yêu cầu bài tập sáu dạng, đó là phạm vi của `jlpt-vocabulary-coach`, không mở rộng skill này.

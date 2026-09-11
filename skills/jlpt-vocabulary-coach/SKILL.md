---
name: jlpt-vocabulary-coach
description: Tạo phiên học từ vựng JLPT sinh động bằng flashcard, trắc nghiệm bấm chọn và bài điền từ tương tác từ dữ liệu CSV cục bộ trong jlpt-exam-skills/resources/N*/goi. Dùng khi người học muốn học mới, ôn tập hoặc kiểm tra từ vựng JLPT; không dùng nguồn từ vựng bên ngoài thư mục này.
---

# JLPT Vocabulary Coach

Tạo buổi học từ vựng có nguồn gốc kiểm chứng được, ưu tiên tương tác trực quan và khả năng nhớ lại chủ động.

## Nguồn dữ liệu bắt buộc

- Chỉ lấy mục từ từ `../../resources/<LEVEL>/goi/*.csv`, trong đó `<LEVEL>` có dạng `N1` đến `N5`.
- Luôn chạy `scripts/load_vocabulary.py` để đọc dữ liệu cho buổi học hiện tại. Không dựa vào trí nhớ của mô hình, danh sách JLPT phổ biến, web hoặc nguồn khác.
- Chỉ dùng cách viết, cách đọc, nghĩa tiếng Việt và câu ví dụ nằm trong cùng hàng CSV.
- Không tự sáng tác thêm từ tiếng Nhật, cách đọc, nghĩa, câu ví dụ, từ đồng nghĩa, trái nghĩa hoặc thông tin từ nguyên.
- Có thể biến câu ví dụ nguồn thành câu điền khuyết bằng cách thay đúng mục từ bằng `＿＿＿`; không thay đổi phần còn lại của câu.
- Có thể tạo mẹo nhớ bằng tiếng Việt từ dữ liệu của hàng hiện tại, nhưng phải ghi nhãn `Mẹo nhớ do AI tạo` và không đưa thêm từ vựng hay khẳng định ngôn ngữ học mới.
- Nếu cấp độ, bài hoặc số lượng được yêu cầu không tồn tại, báo rõ dữ liệu đang có; không bù dữ liệu bằng kiến thức bên ngoài.

Mỗi mục do script trả về có `source_file` và `source_line`. Giữ thông tin này trong đáp án hoặc phần tổng kết để người học kiểm tra nguồn.

## Quy trình buổi học

1. Xác định cấp độ, phạm vi bài và số lượng. Nếu người học chỉ nêu cấp độ, mặc định chọn 10 mục từ trong toàn cấp bằng `--sample 10`; dùng seed ngẫu nhiên do script tự sinh và ghi lại trong kết quả.
2. Mặc định tạo phiên học tương tác bằng `scripts/build_interactive_lesson.py` khi môi trường có thể hiển thị HTML tương tác. Đọc [references/interactive-lessons.md](references/interactive-lessons.md) và xuất file vào thư mục artifact/visualization được môi trường cho phép. Ví dụ:

   ```bash
   python3 scripts/build_interactive_lesson.py --level N2 --lesson dai1 --limit 10 --output /allowed/path/n2-dai1.html
   python3 scripts/build_interactive_lesson.py --level N2 --sample 10 --output /allowed/path/n2-random.html
   ```

3. Hiển thị file ngay trong cuộc trò chuyện bằng cơ chế visualization/artifact của môi trường. Không chỉ gửi đường dẫn file nếu môi trường hỗ trợ nhúng trực tiếp.
4. Phiên tương tác phải có ba chế độ: `Thẻ nhớ`, `Trắc nghiệm` và `Điền từ`. Người học chuyển chế độ và trả lời bằng nút bấm; không yêu cầu nhập văn bản.
5. Nếu môi trường không thể hiển thị giao diện tương tác, mới dùng hội thoại theo [references/learning-modes.md](references/learning-modes.md). Khi đó ưu tiên câu hỏi chọn đáp án bằng số/chữ và giảm tối đa việc gõ.
6. Kết thúc bằng số đúng, chuỗi đúng cao nhất và danh sách cần ôn. Giữ seed cùng nguồn để phiên học có thể tái tạo.

## Nguyên tắc tương tác

- Ưu tiên thao tác bấm/chọn. Chỉ yêu cầu gõ khi người học chủ động yêu cầu luyện viết hoặc luyện nhớ chính tả.
- Phản hồi ngay sau mỗi lựa chọn bằng trạng thái đúng/sai, đáp án nguồn và nút tiếp tục.
- Dùng tiến độ, chuỗi trả lời đúng và thông điệp khích lệ ngắn; không phạt điểm và không dùng ngôn ngữ gây áp lực.
- Xen kẽ hướng Nhật → Việt, Việt → Nhật, cách đọc và điền khuyết câu nguồn.
- Chỉ so sánh các mục dễ nhầm khi tất cả mục so sánh đều đã được nạp từ dữ liệu trong phạm vi hiện tại.
- Chấp nhận khác biệt nhỏ về dấu câu hoặc khoảng trắng; không chấp nhận một mục từ ngoài dữ liệu như đáp án thay thế.
- Không tuyên bố người học đã nhớ chỉ vì vừa nhìn đáp án. Một mục chỉ vào `Đã nhớ` sau khi trả lời đúng ở lượt gợi nhớ không có đáp án hiển thị.

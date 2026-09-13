---
name: jlpt-vocabulary-flashcards
description: Học mới và ôn từ vựng JLPT bằng flashcard có bản dịch câu mẫu và furigana từ dữ liệu dự án. Dùng khi muốn lật thẻ, tự học và ghi nhớ; không tạo bài tập, kiểm tra hay chấm điểm.
---

# JLPT Vocabulary Flashcards

Chỉ cung cấp flashcard để tự học. Không tạo trắc nghiệm, điền từ, câu hỏi kiểm tra, đáp án nhiễu, điểm, chuỗi đúng hoặc đánh giá đỗ/trượt. Không tự chuyển sang kiểm tra sau khi học.

## Nguồn

- Luôn chạy `scripts/load_vocabulary.py` của skill này để nạp dữ liệu hiện tại từ `../../resources/N*/goi/*.csv`.
- Giữ nguyên từ, cách đọc, nghĩa Việt, câu mẫu và nguồn file/dòng. Không tự thêm từ, câu ví dụ hoặc tra nguồn khác.
- Bổ sung bản dịch tiếng Việt và furigana cho câu mẫu trong tệp `*.examples.json` cạnh CSV theo [schema và quy tắc](references/example-annotations.md). Đây là nội dung biên soạn từ câu gốc, không phải dữ liệu nguyên bản CSV. Không thay câu mẫu hoặc thêm mục từ. Kiểm tra dữ liệu bổ sung cho các thẻ được chọn trước khi tạo.
- Nếu thiếu cấp độ/bài, báo dữ liệu đang có; không bù bằng kiến thức mô hình.

## Buổi học

1. Xác định cấp độ và bài. Nếu chỉ nêu cấp độ, chọn ngẫu nhiên 10 từ; hỏi cấp độ nếu chưa rõ. Với danh sách ôn do người học cung cấp, đối chiếu CSV, không suy đoán lịch sử.
2. Chạy từ thư mục skill:
   `python3 scripts/build_flashcards.py --level N2 --lesson dai1 --limit 10 --output /allowed/path/cards.html`.
   Dùng `--sample 10 --seed 42` để chọn/tái tạo mẫu ngẫu nhiên; có thể lặp `--word <mục-từ>` để chọn chính xác danh sách cần ôn. Dùng `--offset N --limit M` để lấy tuần tự `M` từ sau khi bỏ qua `N` từ; ví dụ hai bộ 20 từ đầu dùng lần lượt `--offset 0 --limit 20` và `--offset 20 --limit 20`. Không kết hợp `--offset` với `--sample` hoặc `--word`.
3. Builder phải tạo HTML theo nguyên tắc **content-first, JavaScript-enhanced**. Mọi thẻ phải tồn tại sẵn trong HTML dưới dạng `<details>`/`<summary>` đọc được và giữ cơ chế tự nhớ trước khi mở đáp án. Không được để khu vực thẻ rỗng rồi phụ thuộc hoàn toàn vào JavaScript để tạo nội dung. Chỉ ẩn fallback sau khi giao diện JavaScript đã render thành công.
4. Khi JavaScript hoạt động, hiển thị một thẻ tương tác: mặt trước chỉ có mục từ; khi lật, tách khu vực từ đang học, nhóm cách đọc/ý nghĩa và khung câu mẫu. Câu Nhật có furigana bằng ruby ở trên mọi kanji trừ từ đang học (kể cả dạng biến hình được đánh dấu `target: true`); từ đang học được nhấn màu. Bản dịch Việt nằm ngay dưới câu Nhật. Nguồn nằm trong mục thu gọn. Chữ Nhật lớn, khoảng dòng đủ cho ruby, độ tương phản rõ và nút dễ bấm trên điện thoại.
5. Lật thẻ bằng hiệu ứng xoay 3D khi được hỗ trợ; đây là enhancement, không phải điều kiện để nội dung tồn tại. Chặn thao tác chồng nhau trong lúc lật, giữ focus trên nút lật và bỏ animation khi người dùng bật `prefers-reduced-motion`. Cho lật về mặt trước, xem thẻ trước/sau và đánh dấu “Cần xem lại”. Đây là dấu trang do người học chọn, không phải kết luận đã nhớ hay điểm số. Cho ôn riêng các thẻ đã đánh dấu.
6. Chỉ giữ dấu trang trong phiên; không tuyên bố lưu lâu dài hoặc tự tạo lịch nhắc. Cuối vòng có thể xem lại toàn bộ hoặc các thẻ đánh dấu, không đưa bài kiểm tra.
7. Xác minh đầu ra ở cả hai chế độ: JavaScript hoạt động thì lật/chuyển/đánh dấu được; khi bỏ toàn bộ `<script>`, HTML vẫn hiển thị đủ từ, cách đọc, nghĩa, câu mẫu và nguồn. Nếu ứng dụng không hiển thị được HTML, trình bày một mặt thẻ mỗi lượt trong hội thoại, chờ “lật” hoặc “tiếp”; không hỏi/chấm câu trả lời.

Khi người dùng yêu cầu bài tập sáu dạng N2, đó là phạm vi của `jlpt-n2-vocabulary-coach`; bài tập bốn dạng N1 thuộc `jlpt-n1-vocabulary-coach`. Không mở rộng skill flashcard sang hai phạm vi này.

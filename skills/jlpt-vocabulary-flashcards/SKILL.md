---
name: jlpt-vocabulary-flashcards
description: "Học mới và ôn từ vựng JLPT (N1, N2) bằng flashcard HTML lật thẻ, có cách đọc, nghĩa tiếng Việt, câu mẫu kèm furigana và bản dịch, lấy từ dữ liệu resources của dự án. Dùng khi người dùng muốn tự học, học từ mới, ôn từ, lật thẻ, thẻ nhớ, flashcard, 単語カード, học theo bài (dai1, bài 8…), chia bài thành nhiều bộ thẻ hoặc ôn danh sách từ còn nhầm. Không tạo bài tập, trắc nghiệm, kiểm tra hay chấm điểm — bài tập N2 dùng jlpt-n2-vocabulary-coach, N1 dùng jlpt-n1-vocabulary-coach."
---

# JLPT Vocabulary Flashcards

Chỉ cung cấp flashcard để tự học. Không tạo trắc nghiệm, điền từ, câu hỏi kiểm tra, đáp án nhiễu, điểm, chuỗi đúng hoặc đánh giá đỗ/trượt. Không tự chuyển sang kiểm tra sau khi học.

## Nguồn

- Builder tự gọi loader để nạp dữ liệu hiện tại. Không chạy loader toàn cấp độ rồi đưa JSON vào hội thoại. Khi cần kiểm tra/bổ sung annotation, chỉ nạp nhóm thẻ được chọn bằng `--lesson` và `--limit`/`--offset` hoặc `--sample`/`--seed`, hay lặp `--word` cho danh sách cụ thể; dùng cùng tham số khi dựng. Loader chọn từ trước khi kiểm tra annotation; kiểm tra toàn corpus chỉ dành cho tác vụ kiểm toán dữ liệu. Với toàn bộ bài, lưu dữ liệu ra file và xử lý từng nhóm.
- Giữ nguyên từ, cách đọc, nghĩa Việt, câu mẫu và nguồn file/dòng. Không tự thêm từ, câu ví dụ hoặc tra nguồn khác.
- Bổ sung bản dịch tiếng Việt và furigana cho câu mẫu trong tệp `*.examples.json` cạnh CSV theo [schema và quy tắc](references/example-annotations.md). Đây là nội dung biên soạn từ câu gốc, không phải dữ liệu nguyên bản CSV. Không thay câu mẫu hoặc thêm mục từ. Kiểm tra dữ liệu bổ sung cho các thẻ được chọn trước khi tạo.
- Nếu thiếu cấp độ/bài, báo dữ liệu đang có; không bù bằng kiến thức mô hình.

## Buổi học

1. Xác định cấp độ và bài. Nếu chỉ nêu cấp độ, chọn ngẫu nhiên 10 từ; hỏi cấp độ nếu chưa rõ. Với danh sách ôn do người học cung cấp, đối chiếu CSV, không suy đoán lịch sử.
2. Chạy từ thư mục skill:
   `python3 scripts/build_flashcards.py --level N2 --lesson dai1 --limit 10 --output ../../outputs/<tên-bộ>/cards.html`. Mặc định lưu vào `outputs/` ở thư mục gốc dự án (đã gitignore) trừ khi người dùng chỉ định nơi khác.
   Dùng `--sample 10 --seed 42` để chọn/tái tạo mẫu ngẫu nhiên; có thể lặp `--word <mục-từ>` để chọn chính xác danh sách cần ôn. Dùng `--offset N --limit M` để lấy tuần tự `M` từ sau khi bỏ qua `N` từ; ví dụ hai bộ 20 từ đầu dùng lần lượt `--offset 0 --limit 20` và `--offset 20 --limit 20`. Không kết hợp `--offset` với `--sample` hoặc `--word`.
3. Builder phải tạo HTML theo nguyên tắc **content-first, JavaScript-enhanced**. Mọi thẻ phải tồn tại sẵn trong HTML dưới dạng `<details>`/`<summary>` đọc được và giữ cơ chế tự nhớ trước khi mở đáp án. Không được để khu vực thẻ rỗng rồi phụ thuộc hoàn toàn vào JavaScript để tạo nội dung. Chỉ ẩn fallback sau khi giao diện JavaScript đã render thành công.
4. Dùng giao diện sổ tay: nền giấy, chữ Nhật kiểu sách in, đường phân cách mảnh. Màu theo cấp độ lấy từ payload: N1 đỏ, N2 xanh navy; các cấp độ khác dùng tông nâu trung tính. Cách đọc luôn hiển thị dưới mục từ, kể cả khi ẩn nghĩa; không có nút hiện cách đọc. Khi câu ví dụ hiển thị, bản dịch luôn nằm ngay bên dưới, không dùng nút mở riêng. Giữ furigana ngoài từ mục tiêu, nhấn từ mục tiêu/dạng biến hình, và nguồn trong mục thu gọn. Không tự thêm từ loại khi CSV chưa có dữ liệu.
5. Đặt nút “Cần xem lại”, “Trước”, “Tiếp” phía trên thẻ. Nút “Ẩn nghĩa · Tự nhớ lại”/“Hiện nghĩa và ví dụ” nằm trong thẻ; thao tác này độc lập với tùy chọn “Luôn hiện nghĩa”. Mặc định bật tùy chọn theo mẫu đã duyệt; chuyển thẻ theo lựa chọn hiện tại; chỉ phần nghĩa và ví dụ phụ thuộc chế độ này, cách đọc luôn hiện. Đánh dấu chỉ là lựa chọn ôn tập; cho lọc riêng các thẻ đã đánh dấu. Tôn trọng `prefers-reduced-motion`, giữ focus khi mở/ẩn nội dung và không dùng xoay 3D trong bố cục sổ tay.
6. Chỉ giữ dấu trang trong phiên; không tuyên bố lưu lâu dài hoặc tự tạo lịch nhắc. Cuối vòng có thể xem lại toàn bộ hoặc các thẻ đánh dấu, không đưa bài kiểm tra.
7. Xác minh đầu ra ở cả hai chế độ: JavaScript hoạt động thì lật/chuyển/đánh dấu được; khi bỏ toàn bộ `<script>`, HTML vẫn hiển thị đủ từ, cách đọc, nghĩa, câu mẫu và nguồn. Nếu ứng dụng không hiển thị được HTML, trình bày một mặt thẻ mỗi lượt trong hội thoại, chờ “lật” hoặc “tiếp”; không hỏi/chấm câu trả lời.
8. Đưa file cho người dùng theo môi trường: **Claude Code** — báo đường dẫn tuyệt đối để mở bằng browser (có thể `open <file>` trên macOS); **Claude Desktop/Cowork, Claude.ai** — lưu vào thư mục người dùng đã chọn và trình bày file bằng công cụ chia sẻ/preview sẵn có, chỉ đăng thành artifact/trang web khi người dùng muốn giữ lâu hoặc chia sẻ; **Codex/ứng dụng khác** — dùng preview HTML nếu có, nếu không trả liên kết file.

Khi người dùng yêu cầu bài tập sáu dạng N2, đó là phạm vi của `jlpt-n2-vocabulary-coach`; bài tập bốn dạng N1 thuộc `jlpt-n1-vocabulary-coach`. Không mở rộng skill flashcard sang hai phạm vi này.

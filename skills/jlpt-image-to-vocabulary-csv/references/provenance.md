# Nguồn từng ô khi nhập ảnh

`enrich_from_resources.py --output /tmp/enriched.json` tạo thêm `/tmp/enriched.provenance.json`. Input là bản chép ảnh; không đưa dữ liệu AI tự soạn vào input rồi gắn nhãn ảnh.

Schema version 1: `input_file`, `rows`, `issues`. Mỗi row có `input_row` (từ 1), `word`, `fields`. Mỗi khóa trong `fields` là tên một trong bốn cột CSV, có `value` và `origin`:

- `image`: giá trị có trong bản chép đầu vào; AI bổ sung `image_file` và `image_row` hoặc vùng ảnh để đối chiếu.
- `resources`: giá trị script điền; `sources` chứa mọi `{file, line}` đóng góp giá trị đó, chỉ trong các nguồn khớp cách đọc.
- `unresolved`: ô còn trống, chưa thể chọn nguồn.
- `authored`: AI tự bổ sung nghĩa/ví dụ; cập nhật `value`, ghi `note` ngắn mô tả căn cứ. Không tự gắn nhãn này cho kanji/cách đọc chưa đọc chắc.
- `user_confirmed`: người dùng xác nhận cách đọc, xung đột hoặc chấp nhận ô trống; cập nhật `value` và `note` ghi quyết định.

Sau khi giải quyết một cảnh báo, giữ lịch sử trong `issues` và ghi quyết định vào `note` của ô liên quan. Trước xuất CSV cuối, đối chiếu `input_row`/`word` và mọi `fields[*].value` với JSON cuối; không để provenance giữ giá trị cũ. Lưu cạnh CSV thành `<LESSON>.provenance.json`; không nhầm với `<LESSON>.examples.json` chứa bản dịch/furigana của flashcard.

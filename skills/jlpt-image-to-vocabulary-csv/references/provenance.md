# Nguồn từng ô khi nhập ảnh

Tạo sidecar trực tiếp khi soạn dữ liệu bài mới; không cần chạy `enrich_from_resources.py` hay đọc kho CSV. Phân biệt rõ phần chép ảnh với nghĩa/ví dụ tự viết. Việc tham khảo phong cách 1–2 bài không biến nội dung tự soạn thành nguồn `resources`.

Schema version 1 gồm `version: 1`, `input_file` (bản chép ảnh), `rows`, `issues` (mảng rỗng nếu không có vấn đề). Mỗi row có `input_row` (từ 1), `word`, `fields`. Mỗi khóa trong `fields` là tên một trong bốn cột CSV, có `value` và `origin`:

- `image`: giá trị đọc từ ảnh; thêm `image_file` và `image_row` hoặc vùng ảnh để đối chiếu. Nếu chuẩn hoá cách viết kana/`(する)`, thêm `source_value` giữ nguyên bản chép.
- `authored`: nghĩa/ví dụ tự soạn; `note` ngắn mô tả phần bổ sung. Không dùng nhãn này cho kanji/cách đọc chưa đọc chắc.
- `unresolved`: ô nháp chưa giải quyết; hỏi đúng mục không rõ, không tự tra các CSV khác.
- `user_confirmed`: người dùng xác nhận nội dung hoặc chấp nhận ô trống; ghi quyết định trong `note`.
- `resources`: chỉ dành cho dữ liệu cũ hoặc yêu cầu tra cứu riêng của người dùng; `sources` chứa `{file, line}` của giá trị được dùng lại. Không dùng trong luồng nhập ảnh mặc định.

Nếu có cảnh báo đã được giải quyết, giữ lịch sử trong `issues` và ghi quyết định ở `note` của ô liên quan. Khi kiểm tra đầu ra mới, đối chiếu `input_row`/`word` và `fields[*].value` với dữ liệu cuối trong cùng lượt kiểm tra.

Lưu `<LESSON>.provenance.json` cạnh CSV. `<LESSON>.examples.json` là tệp riêng chứa bản dịch/furigana, theo cấu trúc:

```json
{
  "version": 1,
  "provenance": "Bản dịch và chú thích tự biên soạn từ câu mẫu CSV, không trích từ ảnh.",
  "items": [
    {
      "word": "穴",
      "example": "壁に小さな穴が開いている。",
      "example_vi": "Có một lỗ nhỏ trên tường.",
      "example_segments": [
        {"text": "壁", "reading": "かべ"},
        {"text": "に"},
        {"text": "小", "reading": "ちい"},
        {"text": "さな"},
        {"text": "穴"},
        {"text": "が"},
        {"text": "開", "reading": "あ"},
        {"text": "いている。"}
      ]
    }
  ]
}
```

Mỗi entry khớp chính xác `word`/`example` trong CSV. Ghép `example_segments[*].text` phải ra nguyên câu; kanji ngoài từ mục tiêu có `reading`. Dạng chia của từ mục tiêu dùng segment `{"text": "…", "target": true}` không có `reading`. Chỉ kiểm tra các sidecar của bài đang nhập.

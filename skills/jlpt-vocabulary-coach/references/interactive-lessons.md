# Phiên học tương tác

## Mặc định

Khi môi trường hỗ trợ HTML tương tác, chạy `scripts/build_interactive_lesson.py` và hiển thị kết quả ngay trong cuộc trò chuyện. Bộ sinh nhúng dữ liệu đã chọn vào file, không gọi mạng và không đọc nguồn bên ngoài.

Giao diện có ba tab:

- `Thẻ nhớ`: bấm lật thẻ, sau đó chọn `Đã nhớ` hoặc `Cần ôn`.
- `Trắc nghiệm`: bấm một trong các nghĩa tiếng Việt; tất cả đáp án nhiễu lấy từ những hàng CSV trong phiên.
- `Điền từ`: bấm mục từ phù hợp với câu nguồn đã thay mục từ bằng `＿＿＿`; tất cả lựa chọn lấy từ phiên.

Thanh tiến độ, điểm và chuỗi đúng được cập nhật ngay trong giao diện. Đây chỉ là trạng thái của phiên hiện tại; không tuyên bố đã lưu tiến độ lâu dài.

## Tiêu chuẩn trình bày

- Mục từ tiếng Nhật là nội dung nổi bật nhất, dùng cỡ chữ khoảng 4–5 lần cỡ chữ cơ sở trên màn hình rộng và ít nhất 3 lần trên màn hình hẹp.
- Cách đọc, nghĩa và câu mẫu đều phải lớn hơn chữ phụ trợ; không dùng chữ nhỏ cho nội dung cần học.
- Mỗi màn hình chỉ có một nhiệm vụ rõ ràng và một hành động chính.
- Dùng nhãn cố định `Từ mới`, `Cách đọc`, `Ý nghĩa`, `Câu mẫu` để người học quét nội dung nhanh.
- Sau mỗi câu trả lời, hiển thị lại đầy đủ từ, cách đọc, nghĩa và câu mẫu trước khi sang câu tiếp theo.
- Kết thúc một vòng bằng màn hình hoàn thành, tổng số lượt đúng và chuỗi đúng tốt nhất.
- Giao diện phải đọc tốt từ chiều rộng 320px, nút bấm đủ lớn cho cả chuột và màn hình cảm ứng.

## Tạo file

```bash
python3 scripts/build_interactive_lesson.py \
  --level N2 \
  --sample 10 \
  --output /allowed/artifact/path/n2-session.html
```

Các tham số chọn dữ liệu giống `load_vocabulary.py`:

- `--level N2`: cấp JLPT bắt buộc.
- `--lesson dai1`: giới hạn theo bài.
- `--limit 10`: lấy N hàng đầu tiên.
- `--sample 10`: lấy ngẫu nhiên N hàng.
- `--seed 42`: tái tạo mẫu ngẫu nhiên.
- `--output`: file HTML fragment bắt buộc.

## Bảo toàn dữ liệu nguồn

- Từ, cách đọc, nghĩa và câu ví dụ được nhúng nguyên văn từ kết quả loader.
- Câu điền khuyết chỉ thay lần xuất hiện đầu tiên của mục từ bằng `＿＿＿`.
- Nếu câu không chứa nguyên văn mục từ, mục đó không xuất hiện trong chế độ điền từ.
- Đáp án nhiễu chỉ được chọn từ tập dữ liệu đã nạp trong phiên.
- `source_file` và `source_line` xuất hiện ở mặt sau thẻ và phần phản hồi.

## Khi không có giao diện tương tác

Dùng lựa chọn ngắn như `A/B/C/D`, cho phép người học trả lời một ký tự. Không chuyển toàn bộ phiên thành danh sách dài hoặc yêu cầu nhập lại từ/câu nếu người học không yêu cầu luyện viết.

---
name: jlpt-image-to-vocabulary-csv
description: Đọc bảng hoặc danh sách từ vựng JLPT từ ảnh, bổ sung trường thiếu bằng dữ liệu CSV sẵn có trong resources và xuất CSV cùng schema với resources/N2/goi. Dùng khi người dùng cung cấp ảnh trang sách, ảnh chụp hoặc scan và muốn bổ sung hay tạo dữ liệu từ vựng cục bộ; không dùng để tự sáng tác hoặc lấy từ vựng từ web.
---

# JLPT Image to Vocabulary CSV

Chuyển dữ liệu nhìn thấy trong ảnh thành CSV có thể kiểm tra lại. Khi ảnh chỉ có kanji hoặc thiếu trường, chỉ được bổ sung từ CSV hiện có trong `../../resources`.

## Đầu ra bắt buộc

- Xuất đúng bốn cột, đúng thứ tự: `từ mới`, `cách đọc`, `nghĩa tiếng việt`, `ví dụ sử dụng minh hoạ`.
- Dùng UTF-8 có BOM (`utf-8-sig`), dấu phẩy làm delimiter và một bản ghi trên mỗi dòng.
- Mặc định đặt file vào `../../resources/<LEVEL>/goi/<LESSON>.csv`. Xác định `<LEVEL>` và `<LESSON>` từ yêu cầu hoặc thông tin rõ ràng trên ảnh; không đoán khi chúng ảnh hưởng tên file.
- Không ghi đè file đã tồn tại nếu người dùng chưa yêu cầu rõ. Script cũng chặn ghi đè trừ khi truyền `--force`.

## Nguồn và độ trung thực

- Ưu tiên nội dung thực sự xuất hiện trong ảnh. Không tra web, không sửa nghĩa theo trí nhớ và không tự tạo cách đọc, nghĩa hoặc câu ví dụ.
- Nếu ảnh chỉ có `từ mới` hoặc thiếu trường, tra cứu khớp chính xác trường `từ mới` trong mọi file `../../resources/**/goi/*.csv`. Chỉ điền phần thiếu từ kết quả nội bộ; không thay thế trường đã nhìn thấy trong ảnh.
- Khi cùng một `từ mới` xuất hiện nhiều lần, chỉ tự điền một trường nếu giá trị không rỗng của trường đó giống nhau ở tất cả kết quả. Nếu có nhiều giá trị khác nhau, giữ trống trường đó và báo các file/dòng nguồn để người dùng chọn.
- Nếu không tìm thấy kanji trong `resources`, giữ các phần thiếu ở trạng thái chưa giải quyết và báo rõ; không dùng kiến thức của mô hình để bù.
- Giữ nguyên cách viết kanji/kana, nghĩa tiếng Việt và câu ví dụ; chỉ chuẩn hoá Unicode về NFC, bỏ khoảng trắng thừa ở đầu/cuối và đổi xuống dòng trong một ô thành một dấu cách.
- Không tự động loại bản ghi trùng: cùng một từ có thể có cách đọc, nghĩa hoặc ngữ cảnh khác. Báo các bản ghi trùng hoàn toàn để người dùng quyết định.
- Nếu ảnh không chứa đủ một trong bốn trường, để chuỗi rỗng ở bản nháp và liệt kê rõ trường thiếu. Chỉ xuất CSV cuối khi mọi trường đều có dữ liệu hoặc người dùng xác nhận chấp nhận ô trống.
- Với ký tự không đọc chắc, không đoán. Ghi vị trí ảnh/hàng và các khả năng nhìn thấy được, rồi yêu cầu người dùng xác nhận trước khi xuất CSV cuối.

## Quy trình

1. Liệt kê ảnh đầu vào theo đúng thứ tự trang. Nếu thứ tự không rõ và có thể làm thay đổi thứ tự từ, hỏi người dùng.
2. Mở từng ảnh ở độ phân giải đủ đọc. Phóng to hoặc chia vùng khi chữ nhỏ; kiểm tra lại riêng kanji, kana và dấu câu.
3. Chép các hàng vào một file JSON tạm. Có thể dùng chuỗi kanji hoặc object chứa `từ mới` và các trường đọc được từ ảnh.
4. Bổ sung trường thiếu từ dữ liệu dự án bằng script:

   ```bash
   python3 scripts/enrich_from_resources.py \
     --input /tmp/extracted.json \
     --resources ../../resources \
     --output /tmp/enriched.json
   ```

   Mã thoát `0` nghĩa là tất cả trường đã đủ và không mâu thuẫn; mã `2` nghĩa là file nháp đã được tạo nhưng còn mục không tìm thấy hoặc trường mâu thuẫn cần kiểm tra. Đọc các nguồn được báo trên stderr trước khi tiếp tục.
5. Đối chiếu số hàng với số mục nhìn thấy trên từng ảnh. Rà lại các cặp dễ nhầm như `未/末`, `土/士`, dakuten/handakuten, trường âm và chữ kana nhỏ.
6. Chạy script để kiểm tra và ghi file:

   ```bash
   python3 scripts/write_vocabulary_csv.py --input /tmp/enriched.json --output ../../resources/N2/goi/dai15.csv
   ```

   Dùng `--allow-empty` chỉ sau khi người dùng chấp nhận trường thiếu. Dùng `--force` chỉ khi người dùng yêu cầu thay thế file hiện có.
7. Đọc lại CSV bằng `utf-8-sig`; xác nhận header, số bản ghi và vài hàng đầu/cuối so với ảnh. Chạy `scripts/write_vocabulary_csv.py --check <file.csv>` để kiểm tra file cuối.
8. Báo đường dẫn file, số bản ghi, ảnh/trang đã xử lý, các trường được bổ sung từ `resources`, bản ghi trùng và mọi xung đột hoặc ô trống đã được người dùng xác nhận.

## Dữ liệu JSON cho script

Chấp nhận một mảng trực tiếp hoặc object có khóa `rows`:

```json
[
  {
    "từ mới": "穴",
    "cách đọc": "あな",
    "nghĩa tiếng việt": "lỗ; hang",
    "ví dụ sử dụng minh hoạ": "壁に小さな穴が開いている。"
  }
]
```

Không đưa tên ảnh, số trang, độ tin cậy OCR hoặc ghi chú kiểm duyệt vào CSV vì chúng không thuộc schema hiện tại.

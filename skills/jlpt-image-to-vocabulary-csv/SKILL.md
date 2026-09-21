---
name: jlpt-image-to-vocabulary-csv
description: Đọc từ vựng JLPT từ ảnh và xuất CSV theo từng bài; ưu tiên bổ sung dữ liệu từ resources, đồng thời tự bổ sung nghĩa Việt và ví dụ tiếng Nhật còn thiếu theo phong cách các bài hiện có. Dùng cho ảnh trang sách, ảnh chụp hoặc scan; không tự thêm từ ngoài ảnh.
---

# JLPT Image to Vocabulary CSV

Chuyển dữ liệu nhìn thấy trong ảnh thành CSV có thể kiểm tra lại. Ưu tiên CSV hiện có trong `../../resources`; khi nguồn chưa đủ, được dùng kiến thức tiếng Nhật để bổ sung nghĩa Việt và viết câu ví dụ. Không cần xin phép lại chỉ vì thiếu hai trường này.

## Đầu ra bắt buộc

- Xuất đúng bốn cột, đúng thứ tự: `từ mới`, `cách đọc`, `nghĩa tiếng việt`, `ví dụ sử dụng minh hoạ`.
- Dùng UTF-8 có BOM (`utf-8-sig`), dấu phẩy làm delimiter và một bản ghi trên mỗi dòng.
- Mặc định đặt file vào `../../resources/<LEVEL>/goi/<LESSON>.csv`. Xác định `<LEVEL>` và `<LESSON>` từ yêu cầu hoặc thông tin rõ ràng trên ảnh; không đoán khi chúng ảnh hưởng tên file.
- Không ghi đè file đã tồn tại nếu người dùng chưa yêu cầu rõ. Script cũng chặn ghi đè trừ khi truyền `--force`.

## Nguồn và độ trung thực

- Ưu tiên nội dung thực sự xuất hiện trong ảnh; không thay thế nội dung đã đọc rõ bằng kiến thức của mô hình. Không tự thêm từ ngoài ảnh hoặc đoán kanji/cách đọc còn mơ hồ.
- Nếu ảnh chỉ có `từ mới` hoặc thiếu trường, tra cứu khớp chính xác trường `từ mới` trong mọi file `../../resources/**/goi/*.csv`. Chỉ điền phần thiếu từ kết quả nội bộ; không thay thế trường đã nhìn thấy trong ảnh.
- Với từ chỉ viết bằng kana, có thể dùng chính kana đó làm cách đọc; chuyển katakana sang hiragana tương ứng theo quy ước CSV hiện có, giữ trường âm và kana nhỏ. Đặt chú thích `(する)` vào trường cách đọc khi tách khỏi từ katakana để thống nhất schema; giữ bản chép nguồn để đối chiếu. Không suy ra cách đọc kanji còn thiếu bằng quy tắc này.
- Khi cùng một `từ mới` xuất hiện nhiều lần, chỉ tự điền một trường nếu giá trị không rỗng của trường đó giống nhau ở tất cả kết quả. Nếu có nhiều giá trị khác nhau, giữ trống trường đó và báo các file/dòng nguồn để người dùng chọn.
- Nếu nguồn chưa có nghĩa hoặc ví dụ, tham khảo vài dòng trong các bài cùng cấp độ rồi tự bổ sung hai trường này theo hướng dẫn bên dưới. Không coi phần tự bổ sung là nội dung trích từ ảnh hoặc sao chép từ kho CSV.
- Giữ nguyên cách viết kanji/kana, nghĩa tiếng Việt và câu ví dụ; chỉ chuẩn hoá Unicode về NFC, bỏ khoảng trắng thừa ở đầu/cuối và đổi xuống dòng trong một ô thành một dấu cách.
- Không tự động loại bản ghi trùng: cùng một từ có thể có cách đọc, nghĩa hoặc ngữ cảnh khác. Báo các bản ghi trùng hoàn toàn để người dùng quyết định.
- Để chuỗi rỗng ở bản nháp cho trường chưa giải quyết. Sau khi tra nguồn và bổ sung nghĩa/ví dụ, chỉ hỏi về cách đọc còn thiếu, xung đột chưa giải quyết hoặc nội dung không đủ chắc chắn. Chỉ xuất CSV cuối khi mọi trường đều có dữ liệu hoặc người dùng xác nhận chấp nhận ô trống.
- Với ký tự không đọc chắc, không đoán. Ghi vị trí ảnh/hàng và các khả năng nhìn thấy được, rồi yêu cầu người dùng xác nhận trước khi xuất CSV cuối.

## Bổ sung nghĩa và ví dụ

- Viết nghĩa Việt ngắn, tự nhiên; tách các nghĩa thông dụng bằng `;`. Nghĩa phải khớp cách đọc và từ loại của mục trong ảnh, đặc biệt với từ đồng tự nhiều cách đọc.
- Viết một câu tiếng Nhật tự nhiên, có ngữ cảnh giúp hiểu nghĩa và cách dùng. Dùng chính từ mục tiêu hoặc dạng chia phù hợp; kiểm tra trợ từ, tính tự/tha động từ và kết hợp từ. Không dùng một mẫu câu chung cho hàng loạt từ.
- Tham khảo độ dài và giọng văn của các bài đã có; không sao chép máy móc ví dụ của một từ gần nghĩa sang từ đang bổ sung.
- Rà lại cả nghĩa và ví dụ lấy từ resources nếu cách đọc trong nguồn khác ảnh; không dùng dữ liệu khớp chữ nhưng khác nghĩa/cách đọc. Nếu không xác định chắc nghĩa đang học, giữ mục cần xác nhận.
- Lưu nguồn bổ sung trong JSON/ghi chú kiểm tra ngoài CSV: phân biệt ô lấy từ ảnh, ô lấy từ file/dòng resources và ô tự biên soạn. Giữ CSV đúng bốn cột.

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

   Mã thoát `0` nghĩa là tra nguồn không có vấn đề; mã `2` nghĩa là file nháp đã được tạo nhưng còn mục không tìm thấy hoặc trường mâu thuẫn cần kiểm tra. Script chỉ tra dữ liệu nội bộ, không tự viết nghĩa/ví dụ. Đọc các nguồn được báo trên stderr; tự bổ sung nghĩa/ví dụ còn thiếu theo hướng dẫn trên rồi lưu JSON hoàn chỉnh. Không dùng mã thoát này thay cho bước kiểm tra đủ bốn trường.
5. Đối chiếu số hàng với số mục nhìn thấy trên từng ảnh. Rà lại các cặp dễ nhầm như `未/末`, `土/士`, dakuten/handakuten, trường âm và chữ kana nhỏ.
6. Chạy script để kiểm tra và ghi file:

   ```bash
   python3 scripts/write_vocabulary_csv.py --input /tmp/enriched.json --output ../../resources/N2/goi/dai15.csv
   ```

   Dùng `--allow-empty` chỉ sau khi người dùng chấp nhận trường thiếu. Dùng `--force` chỉ khi người dùng yêu cầu thay thế file hiện có.
7. Đọc lại CSV bằng `utf-8-sig`; xác nhận header, số bản ghi và vài hàng đầu/cuối so với ảnh. Chạy `scripts/write_vocabulary_csv.py --check <file.csv>` để kiểm tra file cuối.
8. Báo đường dẫn file, số bản ghi, ảnh/trang đã xử lý, phần lấy từ `resources` và phần tự bổ sung, bản ghi trùng và mọi xung đột hoặc ô trống đã được người dùng xác nhận.

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

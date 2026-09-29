---
name: jlpt-image-to-vocabulary-csv
description: "Đọc danh sách từ vựng JLPT từ ảnh sách và nhập bài mới vào thư mục từ vựng của cấp độ tương ứng theo schema CSV bốn cột. Lấy ảnh làm nguồn chuẩn, chỉ tham khảo vài dòng của 1–2 bài cùng cấp độ để tự bổ sung nghĩa Việt và câu ví dụ. Không tự tra toàn bộ kho CSV, không thêm từ ngoài ảnh, không đoán chữ mơ hồ, không ghi đè bài cũ."
---

# JLPT Image to Vocabulary CSV

Ưu tiên tốc độ và độ chính xác: đọc trực tiếp ảnh, giữ đúng từ/cách đọc/thứ tự trong sách và tự soạn phần còn thiếu. Chỉ đọc dữ liệu cũ đủ để hiểu phong cách trình bày.

## Phạm vi đọc dữ liệu

- Ảnh người dùng cung cấp là nguồn chuẩn cho danh sách từ và cách đọc. Không đối chiếu từng từ với kho CSV, không tìm từ trùng giữa các bài/cấp độ và không lấy nghĩa/ví dụ cũ bằng tra cứu tự động.
- Chỉ tham khảo khoảng 3–5 dòng của **1–2 bài cùng cấp độ** để nắm độ dài, giọng văn và cách viết ví dụ. Nếu mẫu phù hợp đã có trong context, dùng lại, không đọc thêm. Nếu chưa có bài cùng cấp độ, dùng hướng dẫn bên dưới.
- Chỉ liệt kê tên file khi cần biết số bài hiện có; không mở nội dung mọi CSV. Xác định cấp độ/số bài từ yêu cầu hoặc tiêu đề ảnh, rồi kiểm tra đúng file đích có tồn tại không.
- Không chạy `enrich_from_resources.py` trong luồng nhập ảnh. Script cũ chỉ dành cho yêu cầu tra cứu/tái sử dụng dữ liệu được người dùng chỉ định riêng.

## Độ trung thực và nội dung bổ sung

- Giữ nguyên cách viết kanji/kana, cách đọc, biến thể và thứ tự mục nhìn thấy trong ảnh. Không bỏ một từ chỉ vì nó có thể đã có ở bài khác; không thêm từ ngoài ảnh.
- Chỉ chuẩn hoá Unicode NFC, khoảng trắng đầu/cuối và xuống dòng trong ô. Với từ chỉ có kana, có thể dùng chính kana làm cách đọc, chuyển katakana sang hiragana theo quy ước dự án và giữ trường âm/kana nhỏ. Nếu tách `(する)` sang trường cách đọc, lưu cách viết gốc trong nguồn đối chiếu.
- Với kanji/cách đọc không rõ hoặc bị thiếu: phóng to đúng vùng cần đọc; nếu vẫn chưa chắc, ghi ảnh/mục và hỏi người dùng. Không đoán hoặc thay bằng dữ liệu bài khác.
- Giữ nghĩa/ví dụ nếu ảnh có sẵn. Nếu thiếu, tự viết nghĩa Việt ngắn, tự nhiên, tách các nghĩa thông dụng bằng `;`; khớp cách đọc và từ loại. Không cần xin phép để bổ sung hai trường này.
- Viết một câu tiếng Nhật tự nhiên cho mỗi mục, dùng từ mục tiêu hoặc dạng chia phù hợp. Kiểm tra trợ từ, tự/tha động từ và kết hợp từ ngay khi soạn; chọn ngữ cảnh thể hiện rõ nghĩa. Không dùng một khuôn câu cho hàng loạt từ.
- Chỉ xuất CSV cuối khi đủ bốn trường hoặc người dùng đã chấp nhận ô trống. Khi có vấn đề, xử lý đúng mục đó, không đọc lại cả kho dữ liệu.

## Đầu ra

- `../../resources/<LEVEL>/goi/<LESSON>.csv`: UTF-8 BOM (`utf-8-sig`), delimiter dấu phẩy, một bản ghi mỗi dòng; đúng thứ tự bốn cột `từ mới`, `cách đọc`, `nghĩa tiếng việt`, `ví dụ sử dụng minh hoạ`.
- Không ghi đè bài cũ khi chưa được yêu cầu rõ. Không thêm thông tin nguồn vào bốn cột CSV.
- Không tạo tệp `.provenance.json`; đầu ra bài học chỉ gồm CSV và `.examples.json`.
- `<LESSON>.examples.json`: bổ sung bản dịch câu mẫu và chú thích cách đọc theo [định dạng flashcard](references/examples.md). Dùng một entry mẫu từ 1–2 bài tham khảo; chỉ đọc `load_examples` trong `skills/jlpt-vocabulary-flashcards/scripts/load_vocabulary.py` nếu cần làm rõ schema. Tạo cùng lúc với câu mẫu để tránh phải soạn lại; giữ nguyên câu mẫu CSV, không gắn furigana cho từ mục tiêu/dạng chia.

## Quy trình gọn

Chạy script từ thư mục skill để các đường dẫn `../../resources` đúng vị trí.

1. Xếp ảnh theo trang/bài, xác định số mục nhìn thấy trên mỗi trang. Đọc ảnh đã đính kèm trực tiếp; chỉ mở lại/cắt vùng khi chưa đọc rõ. Không cần OCR lại ảnh đã đọc chắc.
2. Tham khảo mẫu nhỏ như trên, rồi chép từ/cách đọc theo đúng thứ tự và soạn nghĩa/ví dụ còn thiếu. Chuẩn bị JSON hoàn chỉnh cùng bản dịch và chú thích câu mẫu. Chỉ giữ bản chép ảnh tạm khi cần đối chiếu, không tạo thêm tệp nguồn từng ô.
3. Đối chiếu một lượt danh sách mới với ảnh: số mục, thứ tự, chữ/cách đọc và ranh giới trang. Chú ý cặp chữ dễ nhầm, dakuten, trường âm và các cách đọc kép. Bài có 99 mục thì giữ 99, không ép đủ 100.
4. Ghi và kiểm tra CSV mới bằng một lệnh cho mỗi bài:

   ```bash
   python3 scripts/write_vocabulary_csv.py \
     --input /tmp/dai27.final.json \
     --output ../../resources/N1/goi/dai27.csv
   ```

   Lệnh ghi đã kiểm tra schema và dữ liệu đầu vào; không chạy thêm `--check` hoặc đọc lại toàn bộ CSV chỉ để lặp cùng kiểm tra. `--allow-empty` chỉ dùng khi người dùng chấp nhận ô trống; `--force` chỉ dùng khi người dùng yêu cầu ghi đè.
5. Kiểm tra đúng các bài vừa tạo: số hàng/thứ tự/từ/cách đọc khớp ảnh, BOM và chú thích ghép lại đúng câu mẫu. Khi dùng loader, luôn truyền `--level` và `--lesson`; không chạy kiểm tra toàn corpus/toàn bộ test suite cho một lần chỉ nhập dữ liệu. Chỉ kiểm tra lại phần đã sửa nếu phát hiện lỗi. Dòng trùng hoàn toàn trong bài mới cần đối chiếu ảnh, không tự xoá.
6. Báo file, số từ mỗi bài và phần tự biên soạn; chỉ nêu vấn đề còn tồn tại. Không lập báo cáo từ trùng giữa các bài khi người dùng không yêu cầu.

## JSON cho script ghi CSV

Chấp nhận mảng trực tiếp hoặc object có khóa `rows`:

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

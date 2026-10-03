# Đề từ vựng N2

`dai1.json` đến `dai14.json` là 14 đề, mỗi đề 30 câu cho 30 từ khác nhau trong CSV của bài tương ứng ở `resources/N2/goi/`. Câu hỏi và phương án do biên soạn; từ mục tiêu, cách đọc và nghĩa được đối chiếu với CSV. Đây không phải đề JLPT chính thức.

Đề có sáu dạng theo thứ tự 漢字読み / 表記 / 語形成 / 文脈規定 / 言い換え類義 / 用法, với số câu lần lượt là 5 / 5 / 3 / 7 / 5 / 5. Mỗi câu ghi `source_file`, `source_line`, bốn lựa chọn và bốn giải thích. Câu đọc kanji ghi thêm `option_lexemes` để kiểm tra từ và cách đọc của các phương án.

Chạy từ thư mục gốc dự án:

```sh
python3 tools/build_webapp.py
```

Webapp xuất đề tại `dist/exams/N2/dai1.html` đến `dist/exams/N2/dai14.html`, đưa vào danh mục N2 và cache để dùng offline. Khi biên soạn thêm bài, tạo `daiN.json` cùng cấu trúc, giữ 30 từ không lặp và kiểm tra lại tính duy nhất của đáp án trong từng ngữ cảnh.

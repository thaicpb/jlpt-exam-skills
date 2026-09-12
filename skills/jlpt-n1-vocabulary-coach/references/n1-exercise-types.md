# Bốn dạng luyện từ vựng JLPT N1

## Căn cứ từ ảnh người dùng

Bốn ảnh `IMG_6315.jpg`–`IMG_6318.jpg` mô tả bốn dạng và cấu hình minh họa:

| Dạng | Số câu minh họa | Yêu cầu |
| --- | ---: | --- |
| 漢字読み | 6 | Chọn cách đọc đúng của từ kanji được gạch dưới. |
| 文脈規定 | 7 | Chọn từ phù hợp nhất với chỗ trống trong ngữ cảnh. |
| 言い換え類義 | 6 | Chọn cách diễn đạt gần nghĩa nhất với từ được gạch dưới. |
| 用法 | 6 | Chọn câu sử dụng đúng từ mục tiêu; cả bốn câu đều chứa từ đó. |

Tổng cấu hình minh họa là 25 câu; ảnh ghi số câu có thể thay đổi. Không gọi đây là số câu cố định của mọi kỳ thi. Không chép câu ví dụ trong ảnh thành dữ liệu dự án và không lấy từ mục tiêu từ ảnh nếu từ đó chưa có trong CSV.

## 1. 漢字読み — Đọc kanji

- Hiển thị câu tiếng Nhật và gạch dưới đúng một từ mục tiêu bằng `【…】`.
- Bốn lựa chọn là kana; một cách đọc đúng theo cùng hàng CSV.
- Nhiễu nên kiểm tra nhầm on/kun, trường âm `ー`, âm ngắt `っ`, âm đục `゛` hoặc bán đục `゜` thay vì tạo bốn cách đọc hoàn toàn khác nhau.
- Sau khi chấm, hiện cách đọc chuẩn, nghĩa Việt và giải thích sai khác của từng phương án.

## 2. 文脈規定 — Ngữ cảnh

- Câu có đúng một chỗ trống `（　）`; bốn lựa chọn là từ/cụm từ Nhật có vai trò ngữ pháp tương đương.
- Phương án thường có nghĩa gần nhau hoặc dùng cùng/sát kanji; phải hiểu nghĩa từng từ để chọn.
- Sau khi điền, chỉ một phương án phù hợp nhất; loại câu quá chung khiến nhiều đáp án cùng đúng.
- Giải thích dấu hiệu ngữ cảnh và khôi phục câu hoàn chỉnh.

## 3. 言い換え類義 — Gần nghĩa

- Gạch dưới từ/cụm từ mục tiêu bằng `【…】`; bốn lựa chọn đều là cách diễn đạt tiếng Nhật.
- Chọn phương án gần nghĩa nhất trong chính ngữ cảnh đó. Không biến dạng này thành câu hỏi Nhật → nghĩa Việt.
- Giữ tương thích về dạng chia, sắc thái và khả năng thay thế trong câu.
- Sau khi chấm, giải thích quan hệ nghĩa và dịch nghĩa tiếng Việt.

## 4. 用法 — Cách dùng

- Hiển thị một từ mục tiêu và bốn câu đầy đủ; cả bốn câu phải chứa nguyên văn từ mục tiêu hoặc dạng chia hợp lệ đã được xác minh.
- Một câu dùng đúng nghĩa và kết hợp từ; ba câu còn lại sai cách dùng từ mục tiêu, không chỉ sai ngữ pháp không liên quan.
- Giải thích riêng từng câu và chỉ ra kết hợp hoặc nghĩa dùng sai.

## Chính sách chất lượng

1. Mỗi từ mục tiêu phải đối chiếu được với `resources/N1/goi/*.csv` bằng file và dòng.
2. Mỗi câu có đúng bốn lựa chọn khác nhau, một đáp án, bốn giải thích tiếng Việt và `origin: authored`.
3. Không thêm 表記 hoặc 語形成; đây là ranh giới khác với skill N2.
4. Luyện tập chấm ngay. Kiểm tra chỉ chấm sau khi nộp và cho phép sửa trước khi nộp.
5. Đầu ra mặc định là giao diện bấm chọn tương tác; text chỉ là fallback khi môi trường không hỗ trợ.

## Schema và lệnh dựng

- `type`: `reading`, `context`, `paraphrase` hoặc `usage`.
- `prompt`: dùng `【…】` cho reading/paraphrase, `（　）` cho context; usage dùng từ mục tiêu làm prompt.
- `options`, `explanations`: mỗi trường đúng bốn phần tử; `answer` là chỉ số 0–3.
- `source_file`, `source_line`, `word`: phải khớp cùng hàng CSV N1.

```bash
python3 scripts/build_n1_exam.py --output /allowed/path/n1-four-types.html
python3 scripts/build_n1_exam.py --bank /allowed/path/questions.json --mode exam --full --output /allowed/path/n1-exam.html
python3 scripts/build_n1_exam.py --bank /allowed/path/questions.json --type usage --output /allowed/path/n1-usage.html
```

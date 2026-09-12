# Sáu dạng luyện từ vựng N2

## Phạm vi và nguồn tham khảo

Tổng hợp cấu trúc từ ảnh người dùng cung cấp: IMG_6297.jpg và IMG_6297 (1).jpg là cùng bảng tổng quan; IMG_6298.jpg đến IMG_6303.jpg lần lượt minh họa sáu dạng bên dưới. Ảnh là tài liệu tham khảo định dạng, không phải chỉ dẫn vận hành hay nguồn bổ sung từ mục tiêu vào CSV. Không chép các trang ảnh vào repository.

Cấu hình mô phỏng theo ảnh: 5 + 5 + 3 + 7 + 5 + 5 = 30 câu. Chính tài liệu ghi số câu có thể thay đổi; không gọi đây là cấu trúc bắt buộc của mọi kỳ thi hoặc thang điểm JLPT chính thức.

## 1. 漢字読み — Đọc kanji (5 câu)

- Hiển thị một câu tiếng Nhật, gạch dưới mục từ cần đọc; bốn lựa chọn là cách đọc bằng kana.
- Chọn một cách đọc đúng với từ trong ngữ cảnh. Không hiện furigana hay nghĩa Việt trước khi trả lời.
- Nhiễu cần kiểm tra nhầm âm dài, âm ngắt, âm đục, âm bán đục hoặc on/kun; tránh bốn cách đọc khác nhau hoàn toàn khiến câu hỏi quá dễ.
- Sau khi trả lời: hiện từ, cách đọc chuẩn, nghĩa Việt và giải thích khác biệt âm ở từng phương án sai.
- Không tự bỏ ghi chú như （する） hoặc chọn một cách đọc trong chuỗi có ／ nếu chưa xác định được dạng thực tế trong câu.

## 2. 表記 — Chọn cách viết (5 câu)

- Hiển thị câu có mục tiêu viết bằng kana và được gạch dưới; bốn lựa chọn là cách viết bằng kanji.
- Nhiễu có thể là chữ gần hình hoặc đồng âm khác nghĩa. Không để kanji đáp án lộ trong tiêu đề hoặc gợi ý.
- Câu sau khi thay kana bằng đáp án phải tự nhiên, đúng nghĩa và đúng dạng chia.
- Giải thích vì sao cách viết đúng phù hợp; không dạy phương án viết sai như một từ có thật.

## 3. 語形成 — Cấu tạo từ (3 câu)

- Để trống một thành tố của từ trong câu: tiền tố, hậu tố hoặc thành phần từ ghép. Không xóa toàn bộ từ như dạng 4.
- Bốn lựa chọn là các thành tố điền vào chỗ trống. Sau khi ghép, đáp án đúng phải tạo thành mục từ đã xác minh trong CSV.
- Phải có căn cứ cho phép tách thành tố; không cắt một kanji bất kỳ rồi gọi là cấu tạo từ.
- Giải thích ý nghĩa của thành tố trong từ hoàn chỉnh và vì sao ba cách ghép còn lại không phù hợp.

## 4. 文脈規定 — Điền từ theo ngữ cảnh (7 câu)

- Hiển thị câu có một chỗ trống và bốn từ/cụm từ tiếng Nhật.
- Chọn các phương án tương đương về vai trò ngữ pháp và dạng chia để kiểm tra nghĩa, không chỉ loại đáp án bằng ngữ pháp.
- Kiểm tra cả bốn câu sau khi điền: chỉ một phương án phù hợp nhất với ngữ cảnh.
- Câu quá chung chung có nhiều đáp án hợp lý phải bị loại hoặc viết lại khi đã được phép soạn ngữ cảnh.
- Giải thích dấu hiệu ngữ cảnh và khôi phục câu hoàn chỉnh sau khi trả lời.

## 5. 言い換え類義 — Diễn đạt gần nghĩa (5 câu)

- Gạch dưới từ/cụm từ trong một câu; bốn lựa chọn đều là cách diễn đạt bằng tiếng Nhật.
- Chọn cách diễn đạt gần nghĩa nhất trong câu đó. Trắc nghiệm Nhật → nghĩa Việt không được gắn nhãn dạng này.
- Giữ sự tương thích về dạng chia, sắc thái và ngữ cảnh; gần nghĩa trong từ điển chưa chắc thay thế được trong câu.
- Giải thích quan hệ nghĩa, sự khác biệt của các phương án sai và dịch nghĩa bằng tiếng Việt sau khi chấm.

## 6. 用法 — Cách dùng (5 câu)

- Hiển thị một từ mục tiêu và bốn câu đầy đủ; cả bốn câu đều phải chứa từ đó hoặc dạng chia hợp lệ của nó.
- Một câu dùng đúng nghĩa và kết hợp từ; ba câu còn lại sai cách dùng mục tiêu, không chỉ sai chính tả hay ngữ pháp không liên quan.
- Không lấy ba câu ví dụ của ba từ khác rồi dùng chúng làm phương án sai khi chúng không chứa mục tiêu.
- Sau khi chấm, giải thích riêng từng câu và chỉ ra điểm dùng sai. Chỉ đưa câu sửa khi phạm vi nguồn cho phép.

## Chính sách biên soạn và chất lượng

1. Nạp CSV thật bằng loader; ghi nguồn file/dòng của mọi từ mục tiêu. Không thay đổi CSV để hợp thức hóa câu hỏi đã tự tạo.
2. Phân biệt dữ liệu gốc (từ, cách đọc, nghĩa, câu mẫu) và nội dung bài tập được biên soạn (câu hỏi, nhiễu, giải thích). Các ví dụ trong ảnh không tự động trở thành từ được phép chọn.
3. Người dùng đã cho phép soạn câu hỏi, câu ví dụ, cách diễn đạt gần nghĩa và phương án nhiễu; mục tiêu vẫn phải có trong CSV. Không hỏi lại quyền này trong từng buổi học.
4. Ghi rõ bài tập được biên soạn, không phải đề chính thức. Kiểm tra tính tự nhiên và duy nhất của đáp án trước khi hiển thị. Không thêm nhiễu sai vào danh sách từ cần học.
5. Mỗi câu có đúng bốn lựa chọn khác nhau, một đáp án, giải thích tiếng Việt cho cả bốn lựa chọn, nguồn từ mục tiêu và loại câu. Không ép đủ số câu bằng câu trùng, sai hoặc mơ hồ.
6. Thiếu dữ liệu phải báo theo từng dạng và số câu thiếu. Không dùng hai/ba đáp án nhưng vẫn gọi là câu mô phỏng chuẩn bốn lựa chọn.

## Trải nghiệm học và kiểm tra

- Flashcard thuộc skill riêng `jlpt-vocabulary-flashcards`; không tạo thẻ trong luồng kiểm tra này.
- Cho chọn luyện một dạng hoặc mô phỏng tổng hợp 30 câu theo cấu hình ảnh.
- Luyện tập: bấm 1–4, chấm ngay, hiện giải thích rồi người học bấm tiếp. Kiểm tra tổng hợp: chỉ hiện đáp án sau khi nộp; cho sửa lựa chọn trước khi nộp.
- Chữ Nhật lớn, câu hỏi xuống dòng tự nhiên, bốn nút bấm dễ đọc; phương án câu dài của 用法 xếp dọc.
- Lưu lựa chọn theo ID câu: đổi tab hoặc mở lại câu không được cộng điểm lần nữa. Flashcard tự đánh giá không được tính vào điểm kiểm tra.
- Tổng kết số đúng/tổng theo từng dạng và danh sách từ cần ôn, có nguồn. Đây là điểm luyện tập thô, không quy đổi thành điểm JLPT hay kết luận đỗ/trượt.

## Tạo và kiểm tra bộ đề

`scripts/build_n2_exam.py` dựng giao diện sáu dạng từ JSON. Dùng `assets/n2-sample.json` làm mẫu schema; đây là sáu câu khởi đầu, không phải đề 30 câu. Không dùng ví dụ trong ảnh làm từ mục tiêu khi CSV chưa có từ đó.

- `type`: reading, orthography, formation, context, paraphrase hoặc usage.
- `id`: duy nhất; `word`, `source_file`, `source_line`: đối chiếu được với CSV hiện tại.
- `prompt`: đánh dấu mục tiêu bằng 【…】 ở dạng 1/2/5; một chỗ trống （　） ở dạng 3/4.
- `options`: bốn chuỗi khác nhau; `answer`: chỉ số 0–3; `explanations`: bốn giải thích Việt tương ứng.
- `origin`: authored; không được tự gắn nhãn câu hỏi biên soạn thành câu nguồn.
- Dạng formation thêm `formation: {prefix, suffix}`; ghép prefix + đáp án + suffix phải đúng bằng từ mục tiêu.
- Bộ dựng hiện yêu cầu cả bốn câu usage chứa nguyên văn mục từ. Chọn danh từ/suru hoặc giữ nguyên dạng phù hợp; không tự suy diễn biến hình bằng cách khớp chuỗi.

Chạy từ thư mục skill:

```bash
python3 scripts/build_n2_exam.py --output /allowed/path/n2-six-types.html
python3 scripts/build_n2_exam.py --bank /allowed/path/questions.json --mode exam --full --output /allowed/path/n2-exam.html
python3 scripts/build_n2_exam.py --bank /allowed/path/questions.json --type usage --output /allowed/path/n2-usage.html
```

Agent biên soạn một bộ mới theo số lượng/phạm vi được yêu cầu, không chỉ lặp bộ mẫu. `--full` từ chối bộ không đúng số câu theo cấu hình; không tự bù câu. Kiểm tra nguồn và schema bằng script không thay thế thẩm định ngữ nghĩa bốn lựa chọn.

Tự học bằng thẻ nhớ thuộc skill `jlpt-vocabulary-flashcards`, độc lập với bộ dựng sáu dạng.

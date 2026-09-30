# Đề N1 bài 1–41

Mỗi tệp `daiN.json` chứa 30 câu cho 30 từ riêng biệt của `resources/N1/goi/daiN.csv`.

- Chọn từ bằng `load_vocabulary.py --level N1 --lesson daiN --sample 30 --seed (2026093000 + N)`. Giá trị seed thực tế nằm trong `selection` của từng tệp.
- Giữ bộ từ đã chọn; được đổi thứ tự và dạng câu hỏi để từ viết bằng kana hoặc mục từ gộp nhiều biến thể vào dạng phù hợp, phân bổ bốn dạng theo mức 8/8/7/7. Bài 7 dùng 7/8/8/7. Bài 35–36 dùng 0/10/10/10, bài 37 dùng 1/10/10/9 vì bộ từ được chọn chỉ có tương ứng 0, 0, 1 từ chứa kanji. Builder đối chiếu số từ có kanji từ CSV và yêu cầu ba dạng còn lại cân bằng; không dùng từ chỉ viết bằng kana để hỏi đọc kanji.
- Câu hỏi, ngữ cảnh và giải thích được biên soạn; không tự tạo phương án bằng cách biến đổi ngẫu nhiên kana. Mỗi phương án của câu đọc có `option_lexemes` ghi từ thật, cách đọc và dòng CSV để đối chiếu.
- Xáo lựa chọn cùng giải thích và chứng cứ. `answer` là chỉ số từ 0 đến 3; mỗi vị trí xuất hiện đúng 7 hoặc 8 lần trong một đề. Không tự xáo lại lựa chọn mà quên cập nhật hai trường đi kèm.
- `selection` lưu seed chọn từ, không phải seed để sinh nội dung câu hỏi. Builder kiểm tra lại tập dòng được chọn và từ chối câu ngoài bài hoặc lặp từ.

Từ thư mục gốc chạy `python3 tools/build_webapp.py`. HTML dùng đúng template của skill N1, được đưa vào catalog và cache offline. Không commit `dist/`.

Kiểm tra hồi quy từ thư mục `skills/jlpt-n1-vocabulary-coach`:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Kiểm tra tự động xác nhận cấu trúc, nguồn dữ liệu và đáp án đọc kanji. Khi sửa câu ngữ cảnh, gần nghĩa hoặc cách dùng, vẫn cần đọc lại cả bốn lựa chọn để loại khả năng nhiều đáp án cùng đúng; xác nhận kỹ dạng chia và câu hoàn chỉnh sau khi thay thế.

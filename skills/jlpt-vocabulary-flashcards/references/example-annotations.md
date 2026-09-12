# Bản dịch câu mẫu và furigana

Lưu tệp `dai1.examples.json` cạnh `dai1.csv` trong `resources/N*/goi/`. CSV giữ nguyên bốn cột để tương thích các skill khác. JSON chứa dữ liệu biên soạn bổ sung, không được mô tả là nguyên văn từ CSV.

```json
{
  "version": 1,
  "provenance": "Bản dịch tiếng Việt và furigana biên soạn từ câu mẫu CSV.",
  "items": [{
    "word": "悪化",
    "example": "無理をすると病状が悪化する。",
    "example_vi": "Nếu cố quá sức, tình trạng bệnh sẽ xấu đi.",
    "example_segments": [
      {"text": "無理", "reading": "むり"},
      {"text": "をすると"},
      {"text": "病状", "reading": "びょうじょう"},
      {"text": "が悪化する。"}
    ]
  }]
}
```

- Dịch đầy đủ nghĩa câu gốc, tự nhiên bằng tiếng Việt; không thêm tình tiết hay thay câu Nhật.
- Đọc theo ngữ cảnh. Chia kanji và okurigana khi cần, ví dụ `決[き]める` tương ứng `{"text":"決","reading":"き"}` + `{"text":"める"}`.
- Mọi kanji ngoài từ đang học phải có cách đọc. Tách từ đang học ra khỏi cụm, ví dụ với `期末`: `期末` không có reading, `試験` có reading `しけん`.
- Ghép `text` của các segment phải khớp tuyệt đối `example` trong CSV, kể cả dấu câu. Không lưu HTML hoặc ruby trực tiếp; template tạo DOM bằng `textContent`.
- Mỗi cặp `word` + `example` là duy nhất. Loader từ chối ghi chú lỗi thời, thiếu furigana hoặc thêm reading cho từ đang học.
- Nếu bài chưa có JSON hoặc thiếu mục, biên soạn phần bổ sung cho các thẻ được yêu cầu trước khi tạo bộ thẻ. Nếu chưa xác định chắc cách đọc, báo cụ thể thay vì đoán. Renderer vẫn hỗ trợ CSV cũ và hiển thị “Chưa có bản dịch câu mẫu.” khi thiếu; không coi đó là bộ thẻ đã bổ sung đầy đủ.

Kiểm tra: `python3 scripts/load_vocabulary.py --level N1 --lesson dai1`, `python3 -m unittest discover -s scripts -p 'test_*.py'`. Kiểm tra trực quan ruby, bản dịch, thao tác lật/đánh dấu/lọc và bố cục hẹp sau thay đổi template.

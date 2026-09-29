# Bản dịch và furigana cho câu mẫu

Tạo `<LESSON>.examples.json` cạnh CSV cùng lúc với câu mẫu. Bản dịch và chú thích tự biên soạn từ câu mẫu CSV, không trích từ ảnh. Cấu trúc:

```json
{
  "version": 1,
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

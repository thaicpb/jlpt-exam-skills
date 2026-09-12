# Hoàn tất nhập từ vựng N1

Đã xuất `resources/N1/goi/dai1.csv` đến `dai4.csv`, mỗi bài 100 từ, tổng 400 từ từ 5 ảnh người dùng cung cấp. Không thêm từ ngoài ảnh và không sửa CSV N2.

Theo yêu cầu tiếp theo của người dùng, các nghĩa và ví dụ còn thiếu được biên soạn mới, thay cho giới hạn chỉ bổ sung từ nguồn nội bộ của bước nháp. Đây là nội dung học tập bổ sung, không phải bản chép nghĩa hoặc ví dụ từ sách.

Ví dụ tham khảo phong cách `resources/N2/goi/dai6.csv` và `dai10.csv`: câu tiếng Nhật ngắn, ngữ cảnh cụ thể, đa dạng sinh hoạt, học tập, công việc và xã hội. Các trường đã có trong bản nháp được giữ nguyên.

| Bài | Số từ | Nghĩa biên soạn mới | Ví dụ biên soạn mới |
|---|---:|---:|---:|
| 1 | 100 | 0 | 42 |
| 2 | 100 | 34 | 51 |
| 3 | 100 | 88 | 88 |
| 4 | 100 | 92 | 92 |

- Bổ sung mới: 214 nghĩa tiếng Việt và 273 ví dụ tiếng Nhật.
- Có 181 trường đã được bổ sung từ dữ liệu nội bộ ở bước trước; nguồn file/dòng nằm trong `provenance.json`.
- Các trường mới có nguồn `assistant_authored_at_user_request` trong `authored-provenance.json`; nội dung soạn nằm trong `supplements.txt`.
- Hai chú thích viết tay chưa rõ của 恐怖 và 工夫 không được dùng để suy đoán: nghĩa trong CSV lấy từ nguồn N2 đã ghi trong `provenance.json`.
- `extracted.json`, `dai*.draft.json`, `transcription.txt` và phần báo cáo nháp trong README.md được giữ làm lịch sử đối chiếu. Những ô thiếu trong bản nháp không phản ánh CSV cuối.

Kiểm tra: đúng bốn cột của dự án; UTF-8 có BOM; mỗi file 100 bản ghi; không ô trống; không trùng từ hoặc câu ví dụ; mỗi ví dụ có từ đích và kết thúc bằng dấu 。; đọc lại CSV khớp dữ liệu xuất.

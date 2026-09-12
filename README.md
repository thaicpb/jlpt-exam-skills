# JLPT Exam Skills

Tự học từ vựng tiếng Nhật bằng thẻ nhớ hoặc luyện bài tập JLPT ngay khi trò chuyện với AI. Hai hoạt động dùng hai skill riêng, không cần biết lập trình.

Dự án gồm danh sách từ vựng và bốn **skill** — bộ hướng dẫn giúp AI thực hiện một nhiệm vụ:

- **jlpt-vocabulary-flashcards**: tự học và ôn bằng thẻ nhớ, không bài tập hay chấm điểm.
- **jlpt-n2-vocabulary-coach**: chỉ luyện và kiểm tra từ vựng N2 theo sáu dạng bài.
- **jlpt-n1-vocabulary-coach**: chỉ luyện và kiểm tra từ vựng N1 theo bốn dạng bài.
- **jlpt-image-to-vocabulary-csv**: giúp bổ sung danh sách từ vựng từ ảnh bạn cung cấp.

Hiện có từ vựng **N1, bài 1–4** và **N2, bài 1–14**. AI chỉ chọn từ cần học từ dữ liệu của dự án, không tự thêm từ hoặc lấy danh sách từ nguồn khác.

## Bắt đầu học

Mở dự án trong ứng dụng AI có thể đọc các tệp của dự án, chẳng hạn Codex, rồi gửi:

> Dùng skill jlpt-vocabulary-flashcards cho tôi tự học 10 từ N2 trong bài 1 (dai1) bằng thẻ nhớ. Cho tôi bấm lật thẻ để xem cách đọc, nghĩa tiếng Việt và câu ví dụ.

Bạn có thể thay **N2**, **bài 1** và **10 từ** theo nhu cầu, miễn là dự án có dữ liệu tương ứng. Nếu chưa biết chọn bài nào, hãy hỏi: “Dự án hiện có những bài từ vựng nào để tôi học?”

Nếu AI chưa nhận diện tên skill, gửi thêm:

> Hãy đọc và làm theo tệp skills/jlpt-vocabulary-flashcards/SKILL.md trong dự án này, sau đó bắt đầu buổi học cho tôi.

Bạn không cần mở hay chỉnh sửa tệp đó. AI cần được cấp quyền đọc dự án; chỉ gửi tên skill trong một cuộc trò chuyện không có dữ liệu dự án là chưa đủ.

## Học và ôn từ mới

- Nhìn từ ở mặt trước và tự nhớ cách đọc, ý nghĩa.
- Bấm **Lật thẻ** để xem cách đọc, nghĩa tiếng Việt và câu mẫu.
- Dùng **Thẻ trước / Thẻ tiếp** để học theo nhịp của bạn.
- Đánh dấu **Cần xem lại**, rồi chọn nhóm này để ôn riêng.

Không có câu hỏi bài tập, điểm số hoặc đánh giá đúng/sai. Dấu “Cần xem lại” chỉ là lựa chọn cá nhân của bạn.

Một vài yêu cầu có thể sao chép vào cuộc trò chuyện:

**Học nhanh một nhóm từ**

> Dùng skill jlpt-vocabulary-flashcards cho tôi tự học 5 từ N2 ngẫu nhiên bằng thẻ nhớ.

**Học một bài cụ thể**

> Dùng skill jlpt-vocabulary-flashcards cho tôi học 10 từ đầu tiên của bài 8 (dai8), N2. Dùng chữ lớn, dễ đọc và lật thẻ bằng nút bấm.

**Ôn những từ còn nhầm**

> Đây là danh sách từ tôi cần ôn: [dán danh sách từ]. Hãy dùng skill jlpt-vocabulary-flashcards tạo thẻ nhớ cho các từ này. Chỉ dùng những từ có trong dữ liệu dự án.

Dấu xem lại chỉ được giữ trong phiên hiện tại. Để ôn ở buổi sau, hãy lưu danh sách từ cần ôn và gửi lại cho AI; đừng mặc định AI đã nhớ toàn bộ lịch sử học. Nếu không có nút bấm, nhắn “lật” hoặc “tiếp” để xem từng thẻ trong cuộc trò chuyện.

## Luyện sáu dạng bài tập N2

Khi muốn làm bài tập thay vì tự học bằng thẻ, gọi **jlpt-n2-vocabulary-coach**. Skill này độc lập với flashcard và có chấm bài, giải thích đáp án.

| Dạng bài | Bạn cần làm gì? |
| --- | --- |
| Đọc kanji — 漢字読み | Chọn cách đọc của từ được gạch dưới. |
| Cách viết — 表記 | Chọn kanji đúng cho từ viết bằng kana. |
| Cấu tạo từ — 語形成 | Chọn phần còn thiếu để tạo thành từ. |
| Ngữ cảnh — 文脈規定 | Chọn từ phù hợp để điền vào câu. |
| Gần nghĩa — 言い換え類義 | Chọn cách diễn đạt tiếng Nhật gần nghĩa nhất. |
| Cách dùng — 用法 | Chọn câu sử dụng từ đúng. |

**Thử cả sáu dạng**

> Dùng skill jlpt-n2-vocabulary-coach tạo bài luyện N2 gồm 6 câu, mỗi dạng một câu. Cho tôi bấm chọn đáp án và xem giải thích tiếng Việt ngay sau mỗi câu.

**Tập trung vào một dạng**

> Dùng skill jlpt-n2-vocabulary-coach tạo 10 câu luyện cách dùng từ N2. Mỗi câu có 4 đáp án để bấm chọn. Giải thích vì sao từng đáp án đúng hoặc sai.

**Làm bài kiểm tra tổng hợp**

> Dùng skill jlpt-n2-vocabulary-coach tạo bài kiểm tra từ vựng N2 gồm 30 câu đủ sáu dạng. Cho tôi bấm chọn đáp án, chỉ hiện đáp án và giải thích sau khi nộp bài. Cuối bài tổng kết kết quả theo từng dạng và các từ cần ôn.

Khi luyện tập, bấm đáp án rồi chọn **Câu tiếp**. Khi kiểm tra, bạn có thể sửa lựa chọn trước khi **Nộp bài / Tổng kết**.

Đây là bài tập mô phỏng do AI biên soạn, **không phải đề JLPT chính thức**. Từ được kiểm tra phải có trong dữ liệu dự án; câu hỏi, tình huống và phương án lựa chọn có thể được soạn mới. Nếu không đủ dữ liệu phù hợp, AI phải báo rõ thay vì tự thêm từ cho đủ số câu.

Nếu ứng dụng không hỗ trợ nút bấm, hãy yêu cầu AI hỏi từng câu và trả lời bằng số **1–4** hoặc chữ **A–D**.

## Luyện bốn dạng bài tập N1

Khi muốn làm bài từ vựng N1, gọi **jlpt-n1-vocabulary-coach**. Không dùng skill N2 vì cấu trúc hai cấp độ khác nhau.

| Dạng bài | Bạn cần làm gì? | Số câu trong cấu hình minh họa |
| --- | --- | ---: |
| Đọc kanji — 漢字読み | Chọn cách đọc của từ được gạch dưới. | 6 |
| Ngữ cảnh — 文脈規定 | Chọn từ phù hợp để điền vào câu. | 7 |
| Gần nghĩa — 言い換え類義 | Chọn cách diễn đạt tiếng Nhật gần nghĩa nhất. | 6 |
| Cách dùng — 用法 | Chọn câu sử dụng từ đúng. | 6 |

Số câu trên là cấu hình 25 câu minh họa trong tài liệu tham khảo và có thể thay đổi. N1 không dùng hai dạng N2 là **Cách viết — 表記** và **Cấu tạo từ — 語形成**.

**Luyện nhanh 10 câu N1**

> Dùng skill jlpt-n1-vocabulary-coach tạo bài luyện 10 từ vựng N1, phân bổ giữa bốn dạng. Cho tôi bấm chọn và xem giải thích tiếng Việt sau mỗi câu.

**Làm đủ cấu hình bốn dạng**

> Dùng skill jlpt-n1-vocabulary-coach tạo bài kiểm tra N1 gồm 25 câu theo cấu hình 6 câu 漢字読み, 7 câu 文脈規定, 6 câu 言い換え類義 và 6 câu 用法. Chỉ hiện đáp án sau khi nộp.

## Bổ sung từ vựng từ ảnh

Đính kèm ảnh rõ chữ, đúng thứ tự trang rồi gửi:

> Dùng skill jlpt-image-to-vocabulary-csv đọc các ảnh này và tạo bài từ vựng N2 mới. Hãy kiểm tra bài nào đã có để đề xuất số bài tiếp theo, không ghi đè bài cũ. Chỗ nào thiếu thông tin hoặc không đọc chắc thì hỏi lại tôi, không tự đoán.

AI sẽ đọc từ trong ảnh, đối chiếu phần thiếu với dữ liệu sẵn có và báo những mục cần bạn xác nhận. Sau khi lưu bài mới, bạn có thể yêu cầu skill học từ vựng sử dụng bài đó.

## Từ vựng nằm ở đâu?

- **resources**: danh sách từ theo cấp độ và bài; mỗi mục gồm từ, cách đọc, nghĩa tiếng Việt và câu ví dụ.
- **skills**: hướng dẫn để AI tổ chức việc học và bổ sung dữ liệu từ ảnh.

Bạn chỉ cần trò chuyện với AI để học; không cần thao tác với các thư mục này trong mỗi buổi học.

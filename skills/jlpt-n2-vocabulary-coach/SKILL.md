---
name: jlpt-n2-vocabulary-coach
description: "Tạo bài luyện và bài kiểm tra từ vựng JLPT N2 dạng HTML bấm chọn đáp án, chấm điểm và giải thích tiếng Việt, theo đúng sáu dạng N2: 漢字読み (đọc kanji), 表記 (cách viết), 語形成 (cấu tạo từ), 文脈規定 (ngữ cảnh), 言い換え類義 (gần nghĩa), 用法 (cách dùng). Dùng khi người dùng muốn luyện đề, làm bài tập, quiz, trắc nghiệm, test hoặc bài kiểm tra từ vựng N2, kể cả chỉ một dạng hay một bài (dai1…). Chỉ lấy từ mục tiêu từ CSV dự án. Không dùng cho N1 (chuyển sang jlpt-n1-vocabulary-coach) hoặc tự học bằng flashcard (jlpt-vocabulary-flashcards)."
---

# JLPT Vocabulary Coach — Bài kiểm tra N2

Chỉ phụ trách sáu dạng: 漢字読み, 表記, 語形成, 文脈規定, 言い換え類義 và 用法. Tự học/ôn bằng flashcard thuộc skill riêng `jlpt-vocabulary-flashcards`; không đưa flashcard hoặc luồng học ba chế độ cũ vào skill này.

Không dùng skill hoặc builder này cho N1. N1 chỉ có bốn dạng trong phạm vi dự án và thuộc skill `jlpt-n1-vocabulary-coach`.

## Nguồn dữ liệu

- Chạy từ thư mục skill. Nạp đúng phạm vi cần soạn bằng `python3 scripts/load_vocabulary.py --level N2 --lesson dai1 --limit 10`; thay bài/số lượng theo yêu cầu, bỏ `--lesson` khi không giới hạn bài. Dùng `--sample N --seed S` thay `--limit N` khi cần ngẫu nhiên. Chỉ nạp thêm một nhóm nhỏ khi thiếu từ phù hợp dạng bài; không đưa toàn bộ corpus vào hội thoại. Với yêu cầu toàn bộ, lưu JSON vào file và đọc từng nhóm. Builder tự kiểm tra nguồn; không cần in lại corpus để kiểm tra lần hai.
- Từ mục tiêu, cách viết chuẩn, cách đọc và nghĩa gốc phải lấy từ cùng hàng CSV. Giữ nguồn file/dòng.
- Được biên soạn câu hỏi, ngữ cảnh, diễn đạt gần nghĩa, phương án nhiễu và giải thích. Phân biệt nội dung biên soạn với câu mẫu gốc; không thêm từ mục tiêu ngoài CSV.
- Không lấy **từ mục tiêu** từ web hoặc trí nhớ. Thiếu dữ liệu phải báo rõ, không ép đủ số câu.

## Chất lượng đáp án — bắt buộc với mọi câu

1. **Đáp án đúng phải chính xác và duy nhất trong ngữ cảnh.** Đối chiếu cách đọc/nghĩa với hàng CSV; đọc lại câu hoàn chỉnh sau khi điền hoặc thay thế. Loại cả cách đọc khác, nghĩa khác hoặc từ đồng nghĩa cũng có thể đúng. Nếu CSV có dấu hiệu mâu thuẫn, báo rõ và chọn câu khác; không tự sửa nguồn để hợp thức hóa đáp án.
2. **Mọi phương án phải dùng từ, cách đọc hoặc cách diễn đạt có thật trong tiếng Nhật, có nghĩa xác định.** Không đảo/ghép kanji, thêm/bớt kana, đổi âm dài, âm ngắt, âm đục hay on/kun để bịa nhiễu. Chỉ dùng một dạng gần âm/gần chữ khi xác định được từ thật tương ứng, cách đọc và nghĩa của nó. “Nghe giống tiếng Nhật” không phải bằng chứng.
3. **Nhiễu phải hợp lý, không để đoán bằng cách loại từ vô nghĩa.** Chọn từ dễ nhầm về âm, chữ, nghĩa, sắc thái hoặc kết hợp từ; giữ từ loại, dạng chia và độ dài tương đương khi phù hợp dạng bài. Không dùng ba lựa chọn xa chủ đề, câu ngớ ngẩn, ngữ pháp hỏng, lặp lại nguyên đáp án trong đề hay chỉ một lựa chọn có hình thức nổi bật. Người học phải phân biệt kiến thức từ vựng, không chỉ nhận ra từ nào tồn tại.
4. **Từ có thật không có nghĩa là đúng trong câu hỏi.** Với 用法, cả bốn câu dùng từ thật và có cấu trúc câu bình thường; ba câu sai ở nghĩa, kết hợp từ hoặc sắc thái của chính từ mục tiêu. Không phá ngữ pháp không liên quan, biến phó từ thành danh từ, hoặc viết kiểu “hoàn toàn không X nhưng lại X” để lộ đáp án. Với 語形成 của N2, phải kiểm tra cả từ hoàn chỉnh sau khi ghép từng lựa chọn, không chỉ thành tố riêng lẻ.

### Rà từng câu trước khi dựng HTML

- Với **từng lựa chọn**, xác định: từ/cách đọc đầy đủ → nghĩa thật → lý do đúng hoặc sai trong chính câu này. Ưu tiên đối chiếu CSV; khi cần xác minh thêm một phương án nhiễu, dùng nguồn từ điển tiếng Nhật đáng tin cậy và ghi căn cứ thực sự đã kiểm tra. Không dùng từ cực hiếm/tên riêng chỉ để biện hộ cho chuỗi âm tự tạo. Từ mục tiêu vẫn chỉ lấy từ CSV.
- Thử lần lượt cả bốn lựa chọn vào câu; với gần nghĩa, thay đúng phần `【…】`, không để lặp từ hoặc sai trợ từ/dạng chia. Với cách dùng, xem cả bốn câu hoàn chỉnh. Chỉ giữ câu có đúng một đáp án.
- Tự thử **loại đáp án khi chưa biết từ mục tiêu**: nếu có thể chọn chỉ vì ba phương án không tồn tại, sai ngữ pháp sơ đẳng, vô lý rõ rệt hoặc khác hình thức, viết lại nhiễu/ngữ cảnh.
- Viết giải thích tiếng Việt riêng cho cả bốn lựa chọn, nêu nghĩa thật và điểm phân biệt; không chỉ ghi “không phải đáp án”, “sai cách đọc” hoặc “không có trong CSV”. Nếu chưa xác minh được một phương án, thay nó; nếu chưa có đủ ba nhiễu đạt yêu cầu, đổi ngữ cảnh/từ phù hợp phạm vi hoặc báo số câu thiếu. Không hạ tiêu chuẩn để đủ số lượng.
- Sau đó mới chạy builder. **Script pass chỉ xác nhận những điều script thực sự kiểm tra; không chứng nhận ngữ nghĩa, độ tự nhiên hay chất lượng nhiễu.** Không báo đã kiểm chứng bằng từ điển hoặc đã thử với model khác nếu chưa thực hiện.

## Tạo bài

1. Đọc đầy đủ [references/n2-exercise-types.md](references/n2-exercise-types.md) để áp dụng tiêu chí từng dạng.
2. Xác định số câu, loại bài, phạm vi và chế độ. Luyện tập giải thích ngay; kiểm tra chỉ hiện đáp án sau khi nộp.
3. Nạp CSV, biên soạn bộ JSON theo `assets/n2-sample.json`. Kiểm tra ngữ cảnh tự nhiên và đúng một đáp án; có giải thích Việt cho cả bốn phương án. Hoàn tất mục **Rà từng câu trước khi dựng HTML** ở trên; tham khảo bộ mẫu đã sửa, không tái sử dụng nhiễu cũ chưa rà.
4. Chạy `scripts/build_n2_exam.py --bank <bank.json> --output <output.html>`. Dùng `--mode exam --full` cho cấu hình mô phỏng 30 câu (5–5–3–7–5–5); `--type reading` hoặc dạng tương ứng để luyện riêng. Giao diện hiển thị toàn bộ câu dạng danh sách, nhóm theo từng 問題 như đề thật (đề bài tiếng Nhật, phần gạch dưới/chỗ trống); người học chuyển được Kiểm tra/Luyện tập ngay trong trang, `--mode` chỉ đặt chế độ mặc định. Sau khi nộp: điểm tổng, điểm theo dạng bài, danh sách từ cần ôn, tô đúng/sai và giải thích từng phương án, nút làm lại câu sai.
5. Dùng HTML do builder tạo làm đầu ra; không viết lại giao diện chỉ để đổi cách hiển thị. Mặc định lưu vào `outputs/<tên-bài>/` ở thư mục gốc dự án (đã gitignore) trừ khi người dùng chỉ định nơi khác. Cách đưa file cho người dùng theo môi trường:
   - **Claude Code (CLI/IDE):** báo đường dẫn tuyệt đối của file HTML để người dùng mở bằng browser; có thể chạy `open <file>` (macOS) nếu người dùng muốn.
   - **Claude Desktop/Cowork, Claude.ai:** lưu file vào thư mục người dùng đã chọn rồi trình bày file bằng công cụ chia sẻ/preview file sẵn có; chỉ đăng thành artifact/trang web khi người dùng muốn giữ lâu hoặc chia sẻ.
   - **Codex hoặc ứng dụng khác:** mở bằng công cụ preview HTML nếu có; nếu không, trả liên kết file.
   Khi preview báo không hỗ trợ hoặc lỗi quyền/môi trường, dừng thử cách nhúng khác và cung cấp file cùng giới hạn đã xác nhận. Chuyển sang hỏi từng câu dạng text (trả lời 1–4 hoặc A–D) nếu người dùng yêu cầu hoặc không có cách cung cấp HTML sử dụng được.
6. Tổng kết theo từng dạng và từ cần ôn, có nguồn. Điểm luyện tập không quy đổi sang điểm JLPT chính thức. Lựa chọn chỉ giữ trong phiên.

Không truyền `--bank` sẽ dùng bộ mẫu sáu câu, không phải đề đầy đủ. Bộ dựng kiểm tra cấu trúc/nguồn, không thay thế kiểm tra ngữ nghĩa của AI.

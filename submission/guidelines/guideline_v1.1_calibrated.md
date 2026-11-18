# Label contract bổ sung v1.1 — 2A202604067 — Nguyễn Trường Nam

Các quyết định dưới đây dựa trên log model và đối chiếu img_004.jpg, img_013.jpg. Cần áp dụng khi kiểm tra lại nhãn cuối.

## 1. Câu hỏi mở đã chốt

| Ca | Quyết định | Ảnh |
|---|---|---|
| CAL-02 | Người lái và hành khách có mask person riêng. Mask xe loại phần người nhìn thấy kể cả khi người chạm ghế, thân xe hoặc tay lái. | img_013.jpg |
| CAL-03 | Kính chắn gió là bộ phận xe và thuộc mask xe dù nhìn xuyên được. Khoảng hở không có kính xử lý theo mục 4.2.2 của v1.0. | img_004.jpg |

## 2. Ca khó từ lỗi máy

CAL-01, img_013.jpg: log chạy YOLO26 kết hợp SAM ghi nhận xe tuk-tuk bị gán thành car. Đối chiếu cấu trúc xe và sửa lớp thành three_wheeler khi xác nhận là xe ba bánh. Đây là nhắc lại quy tắc lớp đã có ở v1.0. Mask tốt vẫn cần đúng lớp đối tượng.

## 3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Ca |
|---|---|---|
| v1.1 | Làm rõ ranh giới mask người và xe, phân biệt kính với khoảng hở. Nhắc lại kiểm tra lớp xe ba bánh. | CAL-01 đến CAL-03 |

Các câu hỏi mở khác của v1.0 chưa được chốt trong lần bổ sung này. Cần xem xét nếu gặp trong mẫu QC.
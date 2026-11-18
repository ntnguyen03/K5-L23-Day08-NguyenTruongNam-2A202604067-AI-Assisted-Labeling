# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 452; đối tượng sau duyệt: 452; ngưỡng accepted: IoU >= 0.9
- Đã **loại 30 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 452 | 452/452 = 100.0% | 452 box máy |
| edited (sửa) | 0 | 0/452 = 0.0% | 452 box máy |
| deleted (xoá) | 0 | 0/452 = 0.0% | 452 box máy |
| added (vẽ thêm) | 0 | 0/452 = 0.0% | 452 đối tượng sau duyệt |

Trong số deleted + added, **0 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 0.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 206 | 0 | 0 | 0 |
| bicycle | 8 | 0 | 0 | 0 |
| motorbike | 136 | 0 | 0 | 0 |
| car | 53 | 0 | 0 | 0 |
| bus | 3 | 0 | 0 | 0 |
| truck | 5 | 0 | 0 | 0 |
| three_wheeler | 41 | 0 | 0 | 0 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 41 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 38 | 16 | 3 | 70.4% (KTC 95%: 57–81%) | 92.7% (KTC 95%: 81–97%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 0/12 = 0.0% (KTC 95%: 0–24%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - missing: 0/3
  - wrong_class: 0/3
  - extra: 0/3
  - loose: 0/3
  - lọt: img_014.jpg (missing), img_006.jpg (wrong_class), img_031.jpg (extra), img_033.jpg (missing), img_004.jpg (extra), img_028.jpg (extra), img_005.jpg (loose), img_017.jpg (wrong_class), img_013.jpg (wrong_class), img_026.jpg (missing), img_009.jpg (loose), img_027.jpg (loose)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).

# Báo cáo Day 08 — 2A202604067 - Nguyễn Trường Nam

## 1. Model và recipe

YOLO26m chạy trên CPU cho sáu lớp COCO. Hai lượt pilot conf 0.25 và 0.5 trả về lần lượt 215 và 139 box trên 8 ảnh, tốc độ 0,84 và 0,78 giây/ảnh (model_log.csv). Dòng r02 dùng conf 0.25 và dòng r03 của YOLO26 dùng conf 0.5. Log hiện có hai dòng cùng run_id r03, cần đọc kèm tên model để phân biệt.

YOLOE-26s dùng lớp three_wheeler, trả về 8 box trên 8 ảnh pilot với 0,35 giây/ảnh. Log ghi nhận nhầm car thành three_wheeler ở img_002.jpg. YOLO26 kết hợp SAM 2.1 base trả 16 mask trên 2 ảnh với 5,81 giây/ảnh.

| Lớp | Model | Ngưỡng cuối | Cơ sở |
|---|---|---|---|
| person | YOLO26m | 0.45 | Recall 92% trên 13 vật gold |
| three_wheeler | YOLOE-26s | 0.15 | Recall 100% trên 6 vật gold |
| bicycle, bus, truck | YOLO26m | 0.30 | Lần lượt 4, 1, 0 vật gold, chưa đủ mẫu chọn riêng |
| motorbike, car | YOLO26m | 0.30 | Không có ngưỡng <= 0.5 đạt recall 90% trong lần quét |

Nguồn ngưỡng là submission/qc/threshold_sweep.md. Lệnh gộp tương ứng:

~~~powershell
python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --thr "person=0.45,three_wheeler=0.15" --conf 0.3 --iou 0.6 --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json
~~~

Log ghi nhận xe bán tải bị nhận diện thành truck ở cả hai ngưỡng YOLO26 và tuk-tuk bị nhận diện thành car trong lượt kết hợp SAM. Đổi ngưỡng không trực tiếp sửa tên lớp của box. Chưa lưu một ví dụ có confidence cụ thể để kết luận về box điểm cao mà sai.

Ngưỡng được chọn và đánh giá trên cùng 4 ảnh gold nên số đo có thể lạc quan. Các lớp ít vật cần thêm dữ liệu để đánh giá tính ổn định.

## 2. AI error profile

Nguồn submission/qc/review_stats.md. Bảng trạng thái đã loại 30 đối tượng quanh bẫy nhân tạo.

| Trạng thái | Số | Tỷ lệ | Mẫu số |
|---|---|---|---|
| accepted | 452 | 100% | 452 box máy |
| edited | 0 | 0% | 452 box máy |
| deleted | 0 | 0% | 452 box máy |
| added | 0 | 0% | 452 đối tượng sau duyệt |

Trên 4 ảnh gold, mẫu số recall là 41 đối tượng hợp lệ sau xử lý ignore. TP = 38, FP = 16, FN = 3. Precision = 38/54 = 70,4%, recall = 38/41 = 92,7%. Khoảng tin cậy 95% lần lượt là 57–81% và 81–97%.

Không thể xếp hạng lớp tệ nhất chỉ bằng bảng review vì mọi lớp đều giữ nguyên box. Log pilot cho thấy các nhầm lẫn cần kiểm tra lại ở three_wheeler và bicycle, gồm img_002.jpg với YOLOE.

## 3. Thiên kiến tự động hóa và ảnh bẫy

Bắt được 0/12 bẫy = 0%, thấp hơn ngưỡng 80%. Cả bốn loại missing, wrong_class, extra và loose đều đạt 0/3. Khoảng tin cậy 95% của tỷ lệ bắt bẫy là 0–24%.

Accepted 100% cùng với bắt bẫy 0% cho thấy bộ nhãn cuối chưa cung cấp bằng chứng về một lượt sửa lỗi hiệu quả. Cần kiểm tra đã export đúng task và phiên bản mới nhất hay chưa, sau đó review lại có hệ thống. Số đo này chưa xác định được nguyên nhân là bỏ qua lỗi khi duyệt hay dùng nhầm file export.

## 4. Hiệu quả sử dụng model

Chưa có thời gian thực cho gold_manual và batch_review trong time_log.csv. Vì vậy chưa tính được phút/ảnh hoặc mức tiết kiệm thời gian.

Model đã tạo được đề xuất nhãn và mask, nhưng lô hiện tại cần review lại trước khi dùng. Việc gán gold trước giúp làm quen guideline và cảnh, tạo khác biệt về kinh nghiệm khi so sánh thời gian.

Ba thao tác cho vòng review tiếp theo:
1. Ẩn nhãn máy và quét ảnh để tìm vật thiếu trước khi kiểm tra các box.
2. Kiểm tra lớp và biên của từng box kể cả confidence cao.
3. Kiểm riêng xe ba bánh, vùng đông vật và ca bị che trước khi chuyển ảnh.

## 5. Mask SAM cho 3 vật

SAM 2.1 base chạy CPU. Script tái lập là scripts/create_three_masks.ps1. Mỗi vật dùng 2 điểm dương và 1 điểm âm, tổng cộng 3 click.

| Ảnh và vật | File trong masks/ | Quan sát đầu ra |
|---|---|---|
| img_004.jpg, tuk-tuk xanh | tuk_green_img004.jpg | Mask phủ mui, thân, kính và bánh trước. Người đứng cạnh được tách ra. Cần kiểm chi tiết các khoảng hở khung xe. |
| img_013.jpg, người lái | driver_img013.jpg | Mask phủ đầu, thân, chân và bàn chân. Một phần nhỏ vùng sát lan can cần kiểm lại biên; các thanh khung che người tạo ranh giới khó. |
| img_004.jpg, người đứng | person_img004.jpg | Mask phủ người từ đầu đến giày và tách khỏi tuk-tuk. Bàn tay sát xe cần kiểm ở độ phóng đại lớn. |

Đối chiếu mục 4.2, chỉ giữ phần vật nhìn thấy, loại bóng đổ và tách vật chạm nhau. CAL-02 làm rõ người lái tách khỏi mask xe. CAL-03 phân biệt kính xe với khoảng hở thực sự. Chưa đo IoU mask bằng bộ chuẩn nên các nhận xét trên là quan sát trực quan.

Luồng mask sử dụng SAM offline; kết quả này chưa đánh giá Interactor SAM trong CVAT.

## 6. Calibration

Có 3 dòng trong submission/qc/calibration_decisions.csv. CAL-01 ghi nhận lỗi tuk-tuk thành car từ log. CAL-02 chốt ranh giới mask giữa người và xe ở img_013.jpg. CAL-03 làm rõ kính trong suốt vẫn thuộc xe ở img_004.jpg.

Guideline v1.1 đã ghi các quyết định trên. CAL-01 nhắc lại quy tắc lớp đã có, còn CAL-02 và CAL-03 làm rõ phạm vi mask. Các câu hỏi mở khác chưa được chốt. Nếu chúng xuất hiện và ảnh hưởng nhãn cuối, cần giải quyết trước khi phát hành.

## 7. QC và quyết định

Nguồn submission/qc/qc_report_auto.md và qc_review.csv. Mẫu gồm 5 ảnh ngẫu nhiên, 0 ca can_review và 100 đối tượng; seed 42. Phiếu kiểm ghi reviewer nam. Hạn chế là cùng người thực hiện review và QC.

Lỗi theo đối tượng là 2/100 = 2%. Tỷ lệ ảnh có lỗi là 2/5 = 40%, vượt ngưỡng 2% theo ảnh. Một lỗi sai_vi_tri_kich_thuoc ở img_031.jpg, object_id 397, và một lỗi thua ở img_035.jpg, object_id 467.

Cận trên 95% Wilson của tỷ lệ ảnh lỗi là 77%. Mẫu nhỏ chưa chứng minh được tỷ lệ lỗi thực của lô <= 2%.

**Quyết định Rework, ngày 2026-11-18.** Số đo hiện tại vượt ngưỡng ảnh lỗi và tỷ lệ bắt bẫy thấp. Các câu hỏi đã chốt chưa giải quyết hết mọi tình huống có thể gặp.

Vòng tiếp theo cần kiểm đúng file export, rà lại 24 ảnh, sửa hai lỗi QC đã ghi, tính lại review_stats và lấy lại mẫu QC. Nếu gặp câu hỏi guideline ảnh hưởng quyết định gán nhãn, cần xử lý trước khi xem xét Release.

Script kiểm cấu trúc và đếm theo đầu vào. Độ ôm sát box, đối tượng bị cả người và máy bỏ sót, cùng tính đúng của phiếu QC vẫn cần kiểm tra bằng mắt.

## 8. Ghi chú cá nhân

Môi trường Windows, RAM 16 GB, inference dùng CPU. Thiết lập ban đầu kiểm tra thành công YOLO26, YOLOE, MobileSAM và CVAT tại localhost:8080. Ban đầu thiếu yolo26m.pt cho tham số --size m; trọng số hiện đã có.

Cảnh báo torch.jit.load deprecated không làm lượt YOLOE thất bại. Script continue_lab08.py gom các bước gọi script gốc. Nội dung báo cáo được đối chiếu với file số đo và ảnh mask đầu ra.

Chưa có bản ghi độc lập xác nhận trình tự gán gold so với thời điểm xem dự đoán. Các lượt pilot có log chạy model, còn việc dùng cache cho mọi bước chưa được xác nhận.

Lần sau cần ghi thời gian ngay khi bắt đầu từng pha, lưu lệnh chạy và kiểm tra file export ngay sau mỗi lần sửa CVAT. Hiện chưa có dữ liệu thời gian thực để so sánh năng suất.
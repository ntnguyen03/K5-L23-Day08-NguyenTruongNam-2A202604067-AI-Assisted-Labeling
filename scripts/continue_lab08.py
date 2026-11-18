"""Chạy các bước tự động của lab. Dùng Python trong môi trường Day 08."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

def run(*args):
    print("\n>", sys.executable, *args, flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["prepare", "review-stats", "qc", "check"])
    parser.add_argument("--student", default="2A202604067")
    args = parser.parse_args()
    if args.stage == "prepare":
        if not (ROOT / "submission/labels/gold_manual.json").exists():
            parser.error("Cần hoàn thành và export gold gán tay trước.")
        run("scripts/validate_labels.py", "--all")
        for model, out in [("yolo26", "y26_all"), ("yoloe", "yoloe_all")]:
            result = ROOT / "work/prelabel" / out / "pre.coco.json"
            if result.exists():
                print("Dùng kết quả đã có:", result)
                continue
            options = ["--size", "m"] if model == "yolo26" else ["--classes", "three_wheeler"]
            run("scripts/prelabel.py", "--model", model, *options, "--split", "all",
                "--conf", "0.05", "--out", f"work/prelabel/{out}", "--no-viz")
        run("scripts/threshold_sweep.py", "--pred",
            "work/prelabel/y26_all/pre.coco.json", "work/prelabel/yoloe_all/pre.coco.json",
            "--gold", "submission/labels/gold_manual.json")
        report = (ROOT / "submission/qc/threshold_sweep.md").read_text(encoding="utf-8")
        match = re.search(r'--thr "([^"]*)"', report)
        if match is None:
            raise RuntimeError("Chưa đọc được ngưỡng. Kiểm tra threshold_sweep.md.")
        target = ROOT / "submission/prelabel/pre_traps_import.coco.json"
        if target.exists():
            print("Đã có bộ bẫy, giữ nguyên để tiếp tục review:", target)
            return
        run("scripts/merge_prelabels.py", "work/prelabel/yoloe_all/pre.coco.json",
            "work/prelabel/y26_all/pre.coco.json", "--thr", match.group(1),
            "--conf", "0.3", "--iou", "0.6", "--split", "batch,gold",
            "--out", "work/prelabel/merged_review/pre.coco.json")
        run("scripts/inject_traps.py", "--pre", "work/prelabel/merged_review/pre.coco.json",
            "--student", args.student)
        print("Tiếp theo: import pre_traps_import.coco.json vào task 24 ảnh, bấm giờ review và export batch_reviewed.json.")
    elif args.stage == "review-stats":
        if not (ROOT / "submission/labels/batch_reviewed.json").exists():
            parser.error("Cần export batch_reviewed.json sau khi tự review trong CVAT.")
        run("scripts/validate_labels.py", "--all")
        run("scripts/review_stats.py", "--pre", "submission/prelabel/pre_traps.coco.json",
            "--final", "submission/labels/batch_reviewed.json",
            "--gold", "submission/labels/gold_manual.json",
            "--key", "submission/prelabel/traps_key.json")
    elif args.stage == "qc":
        if not (ROOT / "submission/labels/batch_reviewed.json").exists():
            parser.error("Cần batch_reviewed.json.")
        review = ROOT / "submission/qc/qc_review.csv"
        if review.exists():
            print("Đã có phiếu QC. Giữ nguyên phiếu và chỉ tạo báo cáo.")
            run("scripts/qc_report.py")
        else:
            run("scripts/build_release.py")
            run("scripts/qc_sample.py", "--n", "5")
            print("Mở work/qc/review, điền submission/qc/qc_review.csv rồi chạy lại lệnh qc.")
    else:
        run("scripts/check_submission.py")

if __name__ == "__main__":
    main()
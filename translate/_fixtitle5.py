# Dong nhat tieu de voi loi thoat trong body (ngoi thu nhat dung "toi/con", khong dung "ta").
# Cap nhat titles_can_bao_chan_long.json + dong "# " trong file .md tung chuong. Idempotent.
import sys, json, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

D = pathlib.Path(r"F:\taitruyen\data\can_bao_chan_long_vi")
TP = pathlib.Path(r"F:\taitruyen\translate\titles_can_bao_chan_long.json")

NEW = {
    "23": "Chương 23: Tôi muốn lấy lại những thứ thuộc về mình",
    "29": "Chương 29: Tôi có cách giải quyết",
    "43": "Chương 43: Thật sự khiến tôi quá thất vọng",
    "49": "Chương 49: Cô Vân, đắc tội rồi",
    "55": "Chương 55: Tôi cũng có ý kiến",
}

titles = json.loads(TP.read_text(encoding="utf-8"))
changed = 0
for k, v in NEW.items():
    if titles.get(k) != v:
        print(f"title {k}: {titles.get(k)!r} -> {v!r}")
        titles[k] = v
        changed += 1
    # heading trong file .md
    f = next(iter(D.glob(f"{int(k):04d}*.md")))
    t = f.read_text(encoding="utf-8")
    lines = t.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("# Chương"):
            if ln != f"# {v}":
                lines[i] = f"# {v}"
                f.write_text("\n".join(lines), encoding="utf-8", newline="\n")
                print(f"  heading {f.name}: sua")
                changed += 1
            break
    else:
        print(f"  CANH BAO: {f.name} khong co dong # ")

if changed:
    TP.write_text(json.dumps(titles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print("OK, so thay doi:", changed)

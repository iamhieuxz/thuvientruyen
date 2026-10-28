# Chu ky 8 (a): cua loi [E] + 'ngan' — scope tung file, idempotent
import io, os, re, sys, glob, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DATA = "F:/taitruyen/data/can_bao_chan_long_vi"
TJ = "F:/taitruyen/translate/titles_can_bao_chan_long.json"

T79 = "Chương 79: Nó Tưởng Nó Là Ai"

FIX = {
    "0072": [(r"(?m)^#?\s*Chương 72:.*$", "# Chương 72: Tôi đã nói rồi, tôi sẽ chịu trách nhiệm với cô")],
    "0079": [(r"(?m)^#?\s*Chương 79:.*$", "# " + T79)],
    "0078": [("bị đâm thủng trăm ngàn lỗ", "bị đâm thủng trăm nghìn lỗ")],
    "0080": [("con ngàn vạn lần đừng bốc đồng", "con tuyệt đối đừng bốc đồng")],
}

doi = []
for prefix, rules in FIX.items():
    p = glob.glob(os.path.join(DATA, prefix + "_*.md"))[0]
    txt = io.open(p, encoding="utf-8").read()
    new = txt
    for old, repl in rules:
        if old.startswith("(?m)"):
            new = re.sub(old, repl, new)
        else:
            new = new.replace(old, repl)
    if new != txt:
        io.open(p, "w", encoding="utf-8", newline="\n").write(new)
        doi.append(os.path.basename(p))

t = json.load(io.open(TJ, encoding="utf-8"))
if t.get("79") != T79:
    t["79"] = T79
    io.open(TJ, "w", encoding="utf-8", newline="\n").write(
        json.dumps(t, ensure_ascii=False, indent=2))
    doi.append("titles json [79]")

H72 = "Tôi đã nói rồi, tôi sẽ chịu trách nhiệm với cô"
if t.get("72") != H72:
    t["72"] = H72
    io.open(TJ, "w", encoding="utf-8", newline="\n").write(
        json.dumps(t, ensure_ascii=False, indent=2))
    doi.append("titles json [72]")

print("Da sua:", ", ".join(doi) if doi else "khong co gi doi")

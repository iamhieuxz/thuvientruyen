# -*- coding: utf-8 -*-
"""Test cac ham cua dich.py ma khong goi API."""
import sys, importlib.util

spec = importlib.util.spec_from_file_location("dichmod", r"f:\taitruyen\translate\dich.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def t(name, got, want):
    ok = got == want
    print(("  OK  " if ok else "  FAIL") + f" {name}")
    if not ok:
        print(f"       got : {got!r}")
        print(f"       want: {want!r}")
    return ok


allok = True

# 1. validate: ban dich sai -> phai bao loi
bad = 'Variation---\n   10|\n"Anh ơi, con nhặt được一张粮票!"\n秦风说: 你不知道这是烧饼.'
errs = mod.validate(bad, "")
print("validate(bad) ->", errs)
allok &= t("bat loi Han", any("Hán sót" in e for e in errs), True)
allok &= t("bat loi xung ho", any("con" in e for e in errs), True)
allok &= t("bao cao tu sua", any("sửa tự động" in e for e in errs), True)

# 2. validate: ban dich tot -> khong loi
good = (
    "Tần Phong nhìn em rồi nói: anh sẽ kiếm tiền mua cho em một cái bánh nướng.\n\n"
    "Tần Gia gật đầu, nói: vâng anh. Chịu khó nhặt rác mãi đến khi nào đủ tiền học phí "
    "cho em đi học thì thôi.\n\n"
    "Trong lòng cậu bé lại tính toán, chỉ cần thêm mười tám tệ nữa là có thể cho em đi học rồi.\n\n"
    "Hai anh em rời khỏi đống rác trong nắng chiều tà, kéo ra hai bóng dài ngắn lẫn nhau.\n\n"
    "Đường sắt chạy qua phía bên kia, một đoàn tàu hỏa vừa lướt qua tiếng còi xa xa.\n\n"
    "Cậu bé dắt tay em, bước đi trên con đường đất bằng phẳng, bụi mù lơ lửng trong không khí."
)
errs2 = mod.validate(good, "")
allok &= t("ban dich tot -> 0 loi", errs2, [])

# 3. parse_extra
body, terms = mod.parse_extra(
    "Bản dịch nội dung.\n\n=== THUẬT NGỮ MỚI ===\n粮票 = phiếu lương thực\n秦风 = Tần Phong")
allok &= t("parse tach body", body, "Bản dịch nội dung.")
allok &= t("parse tach terms", terms, ["粮票 = phiếu lương thực", "秦风 = Tần Phong"])

body2, terms2 = mod.parse_extra("Không có mục mới.")
allok &= t("parse khi khong co muc", (body2, terms2), ("Không có mục mới.", []))

# 4. clean(): bo marker dong + sua ky tu hong
src = "第一章 兄妹\n\n\"哥，你好。\"\n    10|\n这里是每曰。\n\ufffd\ufffd"
cleaned = mod.clean(src)
allok &= t("clean bo marker", "    10|" not in cleaned, True)
allok &= t("clean sua 曰 -> 日", "每曰" not in cleaned, True)
allok &= t("clean bo ky tu hong", "\ufffd" not in cleaned, True)

# 5. chap_num
allok &= t("chap_num", mod.chap_num("0001_第一章 兄妹.txt"), 1)

print()
print("KET QUA:", "PASS" if allok else "FAIL")
sys.exit(0 if allok else 1)
# -*- coding: utf-8 -*-
"""Đưa truyện lên kệ: tạo/cập nhật data/<out>/book.json cho mọi bản dịch.

Doc thong tin goc tu truyendich_scraper/<src>/_meta.json + so chuong da dich trong
data/<out>/, giu nguyen cac truong da viet tay (title, desc, genre, cover).
Chay sau mỗi lô dịch (duoc _qdcd_auto goi tu dong) hoac th thu cong:

  python shelf.py --book khai_cuc_dinh_chuc
  python shelf.py --all
"""
import argparse, json, pathlib, re, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import dich  # noqa: E402

ROOT = dich.ROOT
SCRAPER = ROOT / "truyendich_scraper"
DATA = ROOT / "data"

# Ten hien thi tieng Viet da chon tay (uu tien hon suy doi)
VI_TITLE = {
    "baojian": "Bảo Giám",
    "can_bao_chan_long": "Thiên Niên Giáng Lâm",
    "quan_dao_chi_dien": "Đỉnh Cao Quan Lộ",
    "khai_cuc_dinh_chuc": "Khai Cục Đình Chức? Ta Chuyển Đầu Ủy Ban Kỷ Luật Điều Tra Tổ",
    "cao_nhi_phan_khoa": "Phân Ban Lớp 11, Tôi Chọn Hoa Khôi Và Cơ Nghiệp Trăm Tỷ",
    "trong_sinh_tai_nguyen": "Trọng Sinh: Tài Nguyên Cuồn Cuồn",
}
VI_AUTHOR = {
    "baojian": "Đả Nhãn",
    "quan_dao_chi_dien": "Thanh Mộc Thư Sinh",
    "khai_cuc_dinh_chuc": "Giang Môn Nhị Gia",
    "cao_nhi_phan_khoa": "Hắc Cẩu Không Thích Ăn Bánh Trôi",
    "trong_sinh_tai_nguyen": "Lão Ưng Cật Tiểu Kê",
}
GENRE = {
    "khai_cuc_dinh_chuc": "Quan trường, Trọng sinh, Đô thị",
    "quan_dao_chi_dien": "Quan trường, Trọng sinh",
    "cao_nhi_phan_khoa": "Đô thị, Trọng sinh, Học đường, Kinh doanh",
    "trong_sinh_tai_nguyen": "Đô thị, Trọng sinh, Kinh doanh, Thương chiến",
}
VI_DESC = {
    "khai_cuc_dinh_chuc": ("Tháng 2/2008, Dương Đông — tổ trưởng Tổ Tổng hợp Văn phòng chính quyền thành phố "
                           "Linh Vân — trọng sinh về đúng ngày cấp trên của anh, Tổng thư ký Doãn Thiết Quân, bị "
                           "Ủy ban Kỷ luật thành phố đưa đi song quy. Kiếp trước anh bị đẩy về một xã miền núi và "
                           "chết trong một đợt chống lụt; kiếp này anh cứu một cô gái bị quan chức làm nhục, lập "
                           "tức bị đánh trọng thương rồi nhận lệnh đình chỉ công tác. Mang theo ký ức hai mươi năm "
                           "về khủng hoảng tài chính, chứng khoán và những bước ngoặt của quan trường, Dương Đông "
                           "chọn một con đường không ai ngờ: bước vào chính Tổ điều tra Ủy ban Kỷ luật đang xử vụ "
                           "của mình."),
    "cao_nhi_phan_khoa": ("31-8-2011. Cố Dư mở mắt trong căn phòng ngủ cũ ở phố Trường Thuận, Cẩm Thành, "
                          "mười bốn năm về trước, với ký ức của một kẻ vừa thua sạch: công ty khởi nghiệp "
                          "gục trước cửa IPO, và mối tình đầu Tô Niệm — nay là partner của một quỹ đầu tư "
                          "phố Wall — ở một thế giới anh không bao giờ với tới. "
                          "Kiếp trước, một cú điện thoại đã chia đôi hai cuộc đời: Tô Niệm chọn ban Xã hội, "
                          "anh vì mặc cảm mà chọn ban Tự nhiên. Kiếp này, anh gạch bỏ chữ “Lý” và viết chữ "
                          "“Văn” — chỉ để được ngồi cùng bàn với cô thêm một năm. "
                          "Nhưng tình cảm không trả được nợ, và khoảng cách giai cấp không vượt qua bằng lời "
                          "hứa. Trong túi anh có 47,5 tệ. Trong đầu anh có mười lăm năm tương lai. Còn trước "
                          "mặt, năm 2011, là một diễn đàn còn đóng cửa với người ngoài: Tri Hồ. "
                          "Từ một câu trả lời viết trong quán net ẩm mốc, một cái tên sẽ vang khắp giới "
                          "Internet Hoa Hạ. Từ một chỗ ngồi cạnh cửa sổ, một cuộc đời khác bắt đầu."),
    "trong_sinh_tai_nguyen": ("Tháng 3-2004. Lý Đông tỉnh dậy trên bàn học lớp 12, mười tám tuổi, "
                              "trong khi ký ức vẫn còn là gã đàn ông ba mươi tuổi vừa chết cô độc sau tám năm "
                              "làm thuê: cha mẹ đã mất vì bệnh, mối tình đầu Tần Vũ Hàm vuột khỏi tay, cả đời "
                              "không có nổi một căn nhà. "
                              "Kiếp này anh chỉ có hai bàn tay trắng và mười lăm năm ký ức về một đất nước "
                              "sắp bước vào cơn bùng nổ chưa từng có: siêu thị thay chợ, Internet thay báo giấy, "
                              "bất động sản và cổ phiếu xé toạc mọi khoảng cách giai cấp. "
                              "Một chuyến tàu chở tôm hùm, một quầy hàng trong khu chợ Đông Bình, rồi một siêu "
                              "thị mang tên Viễn Phương. "
                              "Từ nông thôn Giang Bắc đến bàn đàm phán với A Lý và Đằng Tấn, Lý Đông không "
                              "muốn làm anh hùng, không muốn làm người tốt. Anh chỉ muốn tiền, và muốn nó "
                              "cuồn cuộn chảy về."),}


def src_meta(cfg):
    p = SCRAPER / cfg["src"] / "_meta.json"
    if not p.is_file() and (SCRAPER / cfg["src"]).is_dir():
        # nguon nam trong thu muc con (vd <slug>/_final/) -> _meta.json o thu muc cha
        p = (SCRAPER / cfg["src"]).parent / "_meta.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return {}


def chapter_files(out_dir):
    return sorted(p for p in out_dir.glob("[0-9][0-9][0-9][0-9]_*.md") if p.is_file())


def _han_count(s):
    return len(re.findall(r"[一-鿿]", s or ""))


def _latin(s):
    return "".join(ch for ch in (s or "") if ch.isascii() and (ch.isalnum() or ch in " -–—:,.?!'\"&/"))


def build(book):
    cfg = dich.BOOKS[book]
    out = DATA / cfg["out"]
    out.mkdir(parents=True, exist_ok=True)
    meta = src_meta(cfg)
    old = {}
    f = out / "book.json"
    if f.is_file():
        try:
            old = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            old = {}

    done = chapter_files(out)
    total = int(meta.get("chapters_in_source") or meta.get("chapters_written") or 0) or None
    notes = str(meta.get("notes") or "")
    ongoing = bool(total) and bool(re.search(r"đang ra|đang tiếp|ongoing", notes, re.I))

    if not done:
        status = "Chưa dịch"
    elif total and len(done) >= total:
        status = "Đã dịch xong" if not ongoing else "Đã dịch kịp tiến độ gốc"
    else:
        status = "Đang dịch"

    title_cn = meta.get("title_cn") or old.get("original_title") or ""
    author_cn = meta.get("author_cn") or old.get("author_original") or ""

    # ten + tac gia hien thi: uu tien ban da viet tay, ten cua dich.py,
    # roi moi den chu Han (bi bien dich tha do luoi)
    title = old.get("title") or VI_TITLE.get(book) or ""
    if _han_count(title) >= 2:
        title = ""
    if not title:
        cand = old.get("title_vi") or _latin(title_cn)
        if cand and _han_count(cand) < 2:
            title = cand
    info_title = title or VI_TITLE.get(book) or title_cn

    author = old.get("author") or VI_AUTHOR.get(book) or ""
    if _han_count(author) >= 2:
        author = ""
    if not author:
        cand = old.get("author_vi") or _latin(author_cn)
        if cand and _han_count(cand) < 2:
            author = cand
    info_author = author or VI_AUTHOR.get(book) or ""

    info = {
        "title": info_title,
        "original_title": title_cn,
        "author": info_author,
        "author_original": author_cn,
        "desc": old.get("desc") or old.get("description") or VI_DESC.get(book, ""),
        "description": old.get("desc") or old.get("description") or VI_DESC.get(book, ""),
        "genre": old.get("genre") or GENRE.get(book) or "",
        "status": status,
        "language": "vi",
        "source_language": "zh",
        "source": old.get("source") or meta.get("source") or "",
        "original_chapters": total,
        "translated_chapters": len(done),
        "first_chapter": int(done[0].name[:4]) if done else None,
        "last_chapter": int(done[-1].name[:4]) if done else None,
        "original_status": "Đang ra" if ongoing else ("Đã full" if total else "Chưa rõ"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if old.get("cover"):
        info["cover"] = old["cover"]
    info = {**old, **info}          # giu moi truong la da co trong book.json cu
    return f, info, old


def sync(book, write=True):
    f, info, old = build(book)
    changed = {k: v for k, v in info.items() if old.get(k) != v}
    if write:
        f.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8", newline="\n")
    return f, info, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", choices=sorted(dich.BOOKS))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true", help="chi in, khong ghi file")
    a = ap.parse_args()
    books = sorted(dich.BOOKS) if a.all else [a.book or dich.BOOK]
    for b in books:
        f, info, changed = sync(b, write=not a.dry)
        print("%-20s %-24s %s/%s  (%s)" % (b, info["status"], info["translated_chapters"],
                                           info["original_chapters"] or "?", f))
        if changed and not a.dry:
            print("   cap nhat: " + ", ".join(sorted(changed)))


if __name__ == "__main__":
    main()

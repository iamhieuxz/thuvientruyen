/* Kho tiến độ đọc dùng chung: một key, tiến độ tách riêng theo từng truyện. */

const LS = "baogiam.reader.v2";

function loadStore() {
  let all;
  try {
    all = JSON.parse(localStorage.getItem(LS) || "null");
  } catch {
    all = null;
  }
  if (all && all.books) {
    // Mot lan: may da luu toc do cu (1.00x) thi nang len mac dinh moi 1.25x.
    if (!all.v3rate) {
      all.v3rate = 1;
      if ((all.settings || {}).rate === 100) all.settings.rate = 125;
      try { localStorage.setItem(LS, JSON.stringify(all)); } catch { /* bo qua */ }
    }
    return all;
  }
  let v1 = null;
  try {
    v1 = JSON.parse(localStorage.getItem("baogiam.reader.v1") || "null");
  } catch {
    v1 = null;
  }
  all = (v1 && { settings: v1.settings || {},
                 books: { baojian_vi: { read: v1.read || [], pos: v1.pos || {},
                                        last: v1.last || null } } })
      || { settings: {}, books: {} };
  try {
    localStorage.setItem(LS, JSON.stringify(all));
  } catch { /* chế độ ẩn danh: bỏ qua, chạy trong bộ nhớ */ }
  return all;
}

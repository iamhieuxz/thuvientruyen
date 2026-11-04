/* ============================================================
   history.js — trang /lich-su: lịch sử phiên đọc, gom theo ngày giờ máy.
   Nguồn: store.js (phiên đọc lưu trong trình duyệt) + /api/books (tên, bìa).
   storeReady bắn lại mỗi lần server đồng bộ -> paint() phải vẽ đè sạch, không cộng dồn.
   ============================================================ */

const $ = (s) => document.querySelector(s);
const nf = new Intl.NumberFormat("vi-VN");
const esc = escHTML;
const all = loadStore();

const DAY = 86400;
/* Ngày tính theo giờ máy người đọc (VN +7), giống trang chủ — đọc 0h30 sáng
   vẫn rơi vào đúng ngày hôm đó chứ không sang hôm trước. */
const dayKey = (ts) => {
  const d = new Date((ts || 0) * 1000);
  return Math.floor(((ts || 0) - d.getTimezoneOffset() * 60) / DAY);
};
const WD = ["Chủ nhật", "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy"];
const clock = (ts) => new Date((ts || 0) * 1000).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
const dateTxt = (ts) => new Date((ts || 0) * 1000).toLocaleDateString("vi-VN");

/* ---------- dữ liệu truyện (tên, bìa) ---------- */
let byId = new Map();

async function loadBooks() {
  try {
    const d = await fetch("/api/books").then((r) => r.json());
    byId = new Map((d.books || []).map((b) => [b.id, b]));
  } catch { /* offline: vẫn vẽ theo id */ }
}

/* ---------- một dòng phiên đọc ---------- */
function row(s) {
  const b = byId.get(s.book) || { id: s.book, title: s.book };
  const from = +s.from || 0, to = +s.to || 0, n = to || from;
  const ch = !n ? "" : from && from !== to ? `chương ${nf.format(from)}–${nf.format(to)}` : `chương ${nf.format(n)}`;
  const mins = +s.minutes || 0;
  return `
  <a class="hses-row" href="/sach/${encodeURIComponent(s.book)}/chuong/${n || 1}"
     aria-label="${esc(b.title)}, ${esc(ch)}, ${nf.format(mins)} phút">
    <span class="hses-cov">${coverHTML(b, "cov")}</span>
    <span class="hses-meta">
      <strong>${esc(String(b.title || s.book).slice(0, 60))}</strong>
      <span>${esc(ch)} · <span class="num">${nf.format(mins)}</span> phút</span>
    </span>
    <span class="hses-side">
      <span class="hses-min num">${nf.format(mins)}′</span>
      <span class="hses-time">${clock(s.ts)}</span>
    </span>
  </a>`;
}

/* ---------- cả trang ---------- */
function paint(sessions) {
  const sumEl = $("#hsum"), daysEl = $("#hdays");
  if (!sumEl || !daysEl) return;
  sumEl.setAttribute("aria-busy", "false");
  daysEl.setAttribute("aria-busy", "false");

  if (!(sessions || []).length) {
    sumEl.innerHTML = "";
    daysEl.innerHTML = `<div class="empty"><b>Chưa có phiên đọc nào</b>
      Mở một truyện và đọc vài phút — phiên đọc sẽ hiện ở đây, gom theo ngày.</div>`;
    return;
  }

  const now = dayKey(Date.now() / 1000);
  const recent = sessions.filter((s) => dayKey(s.ts || 0) >= now - 29);   // 30 ngày qua
  const mins30 = recent.reduce((a, s) => a + (+s.minutes || 0), 0);
  const nDays = new Set(recent.map((s) => dayKey(s.ts || 0))).size;
  const perBook = new Map();
  recent.forEach((s) => perBook.set(s.book, (perBook.get(s.book) || 0) + (+s.minutes || 0)));
  const top = [...perBook.entries()].sort((a, b) => b[1] - a[1])[0];
  const topName = top ? (byId.get(top[0]) || { title: top[0] }).title : "";

  sumEl.innerHTML = `
    <div class="hstat is-acc"><span class="num">${nf.format(mins30)}</span><i>phút đọc · 30 ngày qua</i></div>
    <div class="hstat"><span class="num">${nf.format(recent.length)}</span><i>phiên đọc</i></div>
    <div class="hstat"><span class="num">${nf.format(nDays)}</span><i>ngày có đọc</i></div>
    ${top ? `<div class="hstat"><span class="num">${esc(String(topName).slice(0, 26))}</span><i>đọc nhiều nhất</i></div>` : ""}`;

  const groups = new Map();
  sessions.forEach((s) => {
    const k = dayKey(s.ts || 0);
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(s);
  });
  const ks = [...groups.keys()].sort((a, b) => b - a);
  daysEl.innerHTML = ks.map((k) => {
    const list = groups.get(k).sort((a, b) => (b.ts || 0) - (a.ts || 0));
    const mins = list.reduce((a, s) => a + (+s.minutes || 0), 0);
    const name = k === now ? "Hôm nay" : k === now - 1 ? "Hôm qua"
      : WD[new Date(k * DAY * 1000).getDay()];
    return `
    <section class="hday" aria-label="${esc(name)}, ${nf.format(mins)} phút">
      <div class="hday-head">
        <span class="hday-name">${esc(name)}</span>
        <span class="hday-date">${dateTxt(list[0].ts)}</span>
        <span class="hday-min num">${nf.format(mins)} phút</span>
      </div>
      <div class="hses">${list.map(row).join("")}</div>
    </section>`;
  }).join("");
}

/* ---------- khởi động ---------- */
(async () => {
  await loadBooks();
  paint(await getSessions());          // vẽ ngay từ dữ liệu localStorage
})();
storeReady(async () => {               // IDB/server đồng bộ xong (bắn lại nhiều lần) -> vẽ đè
  paint(await getSessions());
});

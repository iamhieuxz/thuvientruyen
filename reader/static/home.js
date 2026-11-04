/* ============================================================
   home.js: trang chủ "Midnight Stream"
   Nguồn: /api/books + /api/latest; tiến độ đọc từ store.js.
   Số liệu chỉ lấy thật (chương, % dịch, phút đọc), không bịa views.
   ============================================================ */

const all = loadStore();
const $ = (s) => document.querySelector(s);
const nf = new Intl.NumberFormat("vi-VN");
const esc = escHTML;
const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- tiện ích ---------- */
const ago = (t) => {
  if (!t) return "";
  const d = (Date.now() / 1000 - t) / 86400;
  if (d < 1 / 24) return "vừa cập nhật";
  if (d < 1) return Math.round(d * 24) + " giờ trước";
  if (d < 30) return Math.round(d) + " ngày trước";
  return new Date(t * 1000).toLocaleDateString("vi-VN");
};
const fmtShort = (n) => (n >= 1e6 ? (n / 1e6).toFixed(1).replace(".", ",") + " tr"
  : n >= 1e3 ? (n / 1e3).toFixed(1).replace(".", ",") + "k" : nf.format(n || 0));
const fmtMin = (m) => {
  const h = Math.round((m || 0) / 60);
  return h >= 1000 ? (h / 1000).toFixed(1).replace(".", ",") + " nghìn giờ" : nf.format(h) + " giờ";
};
const genres = splitGenres;

/* cắt chuỗi ở tầng dữ liệu: chữ không bị CSS che nên không tràn khối bên cạnh.
   Đồng thời chuẩn hoá dấu gạch dài trong mô tả gốc thành dấu phẩy. */
const cut = (s, n) => {
  const t = String(s == null ? "" : s).replace(/\s*—\s*/g, ", ").replace(/\s+/g, " ").trim();
  if (t.length <= n) return t;
  const sp = t.lastIndexOf(" ", n);
  return t.slice(0, sp > n * 0.6 ? sp : n).replace(/[.,;:·\-–]$/, "") + "…";
};

/* phần trăm đọc: 0% thật khác "dưới 1%" khi mới đọc vài chương của bộ dài */
const pctTxt = (p, chapters) => (p === 0 && chapters > 0 ? "<1" : String(p));
/* bề rộng thanh tiến độ: luôn thấy được một vạch dù mới đọc 1 chương */
const barW = (p, has) => (has ? Math.max(p, 2) + "%" : "0%");

function state(b) {
  const B = all.books[b.id] || {};
  const last = +B.last || 0;
  const chapters = b.chapters || 0;
  return {
    last,
    pct: last && chapters ? Math.min(100, Math.round((last / chapters) * 100)) : 0,
    has: last > 0,
  };
}

/* trạng thái badge theo dữ liệu thật */
const isFull = (b) => /hoàn thành|full|kết thúc/i.test(b.status || "") || (b.original_chapters && b.progress >= 100);
const isHot = (b) => b.updated && (Date.now() / 1000 - b.updated) < 7 * 86400;

const badges = (b) =>
  `<span class="badge ai">AI dịch</span>` +
  (isFull(b) ? `<span class="badge full">Full</span>` : "") +
  (!isFull(b) && isHot(b) ? `<span class="badge hot">Hot</span>` : "");

const ICO_BOOK = `<svg viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.7A2.7 2.7 0 0 0 4 20.7z" transform="scale(.92) translate(1 .6)"/><path d="M20 18v3H6.7"/></svg>`;

/* ============================================================
   HERO MOSAIC: 1 thẻ lớn + 4 thẻ nhỏ (bất đối xứng)
   ============================================================ */
function heroBig(b) {
  const s = state(b);
  const href = `/sach/${encodeURIComponent(b.id)}/chuong/${s.last || b.first}`;
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  const g = genres(b);
  const kick = s.has
    ? `<span class="hero-kick acc"><i></i>Đang đọc dở · ${pctTxt(s.pct, b.chapters)}%</span>`
    : `<span class="hero-kick">${isFull(b) ? "Đã hoàn thành" : "Đang dịch"}${g[0] ? " · " + esc(g[0]) : ""}</span>`;
  return `
  <div class="hero-big">
    ${coverHTML(b, "cov")}
    <span class="hero-scrim" aria-hidden="true"></span>
    <span class="hero-top">
      <span class="stat">${ICO_BOOK}<span class="num">${nf.format(b.chapters)}</span>&nbsp;chương</span>
      <span class="hero-badges">${badges(b)}</span>
    </span>
    <span class="hero-body">
      ${kick}
      <h1 class="hero-title"><a href="${detail}">${esc(b.title)}</a></h1>
      <span class="hero-by">${b.author ? esc(cut(b.author, 40)) : ""}</span>
      ${b.desc ? `<span class="hero-desc">${esc(cut(b.desc, 190))}</span>` : ""}
      <span class="hero-cta">
        <a class="btn btn-acc" href="${href}">${s.has ? `Đọc tiếp · chương ${nf.format(s.last)}` : "Bắt đầu đọc"}
          <svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></svg>
        </a>
        <span class="hero-meta num">${isFull(b) ? nf.format(b.chapters) + " chương" : "đã dịch " + b.progress + "%"} · ${fmtMin(b.minutes)}</span>
      </span>
    </span>
    ${s.has ? `<span class="hero-prog" aria-hidden="true"><span class="rail"><i style="width:${barW(s.pct, s.has)}"></i></span></span>` : ""}
    <a class="hero-stretch" href="${detail}" tabindex="-1" aria-hidden="true"></a>
  </div>`;
}

function heroTile(b) {
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  const s = state(b);
  return `
  <a class="hero-tile" href="${detail}" aria-label="${esc(b.title)}">
    ${coverHTML(b, "cov")}
    <span class="hero-scrim" aria-hidden="true"></span>
    <span class="hero-top">
      <span class="stat">${ICO_BOOK}<span class="num">${nf.format(b.chapters)}</span></span>
    </span>
    <span class="tile-body">
      ${isFull(b) ? `<span class="badge full">Full</span>` : isHot(b) ? `<span class="badge hot">Hot</span>` : ""}
      <strong>${esc(cut(b.title, 22))}</strong>
      <span>${s.has ? "đang đọc " + pctTxt(s.pct, b.chapters) + "%" : b.author ? esc(cut(b.author, 18)) : ""}</span>
    </span>
  </a>`;
}

/* ============================================================
   THẺ SÁCH (rail + lưới dùng chung)
   ============================================================ */
function card(b, opts = {}) {
  const s = state(b);
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  const g = genres(b);
  const cls = opts.cls || "mcard";
  return `
  <a class="${cls}" style="--i:${opts.i || 0}" href="${detail}" aria-label="${esc(b.title)}, ${b.chapters} chương${s.has ? `, đang đọc chương ${s.last}` : ""}">
    <span class="${cls}-cov">
      ${coverHTML(b, "cov")}
      <span class="${cls}-top">
        <span class="stat">${ICO_BOOK}<span class="num">${fmtShort(b.chapters)}</span></span>
      </span>
      <span class="${cls}-flags">${isFull(b) ? `<span class="badge full">Full</span>` : isHot(b) ? `<span class="badge hot">Hot</span>` : ""}${s.has ? `<span class="badge acc">${pctTxt(s.pct, b.chapters)}%</span>` : ""}</span>
    </span>
    <span class="${cls}-meta">
      <strong>${esc(cut(b.title, 34))}</strong>
      <span class="${cls}-sub">${s.has
        ? `Đang đọc · chương <span class="num">${nf.format(s.last)}</span>`
        : b.author ? esc(cut(b.author, 20)) : esc(g.join(" · ") || "Bản dịch AI")}</span>
      ${s.has ? `<span class="rail" aria-hidden="true"><i style="width:${barW(s.pct, s.has)}"></i></span>` : ""}
    </span>
  </a>`;
}

/* thẻ chương mới (section "Vừa được dịch bởi AI") */
function chCard(c, book) {
  const href = `/sach/${encodeURIComponent(c.book)}/chuong/${c.n}`;
  const b = book || { id: c.book, title: c.title, chapters: c.n };
  return `
  <a class="mcard chcard" href="${href}" aria-label="${esc(c.title)}, ${esc(c.ctitle)}">
    <span class="mcard-cov">
      ${coverHTML(b, "cov")}
      <span class="mcard-top"><span class="stat">#<span class="num">${c.n}</span></span></span>
      <span class="mcard-flags"><span class="badge done">Mới dịch</span></span>
    </span>
    <span class="mcard-meta">
      <strong>${esc(cut(c.title, 34))}</strong>
      <span class="mcard-sub">Chương <span class="num">${nf.format(c.n)}</span> · ${esc(cut(c.ctitle, 26))}</span>
      <span class="mcard-sub dim">${ago(c.mtime)}</span>
    </span>
  </a>`;
}

/* ============================================================
   SIDEBAR PHẢI
   ============================================================ */
function contItem(b) {
  const s = state(b);
  const href = `/sach/${encodeURIComponent(b.id)}/chuong/${s.last}`;
  return `
  <a class="cont-item" href="${href}" aria-label="Đọc tiếp ${esc(b.title)} từ chương ${s.last}">
    ${coverHTML(b, "cov")}
    <span class="cont-meta">
      <strong>${esc(cut(b.title, 30))}</strong>
      <span>Chương <span class="num">${nf.format(s.last)}</span> · ${pctTxt(s.pct, b.chapters)}%</span>
      <span class="rail" aria-hidden="true"><i style="width:${barW(s.pct, s.has)}"></i></span>
    </span>
  </a>`;
}

function randCard(b) {
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  const start = `/sach/${encodeURIComponent(b.id)}/chuong/${b.first}`;
  const g = genres(b);
  return `
  <div class="rand-inner">
    <a class="rand-cov" href="${detail}" aria-label="Xem trang truyện ${esc(b.title)}">${coverHTML(b, "cov")}</a>
    <div class="rand-info">
      <span class="badge genre">${esc(g[0] || "Truyện dịch")}</span>
      <a class="rand-title" href="${detail}">${esc(cut(b.title, 38))}</a>
      ${b.desc ? `<p class="rand-desc">${esc(cut(b.desc, 190))}</p>` : ""}
      <div class="rand-acts">
        <a class="btn btn-acc" href="${start}">Đọc ngay</a>
        <button class="btn btn-ghost" id="reroll" type="button">Đổi truyện</button>
      </div>
    </div>
  </div>`;
}

/* ============================================================
   HÔM NAY CỦA BẠN — lịch sử phiên (IDB, GĐ2)
   ============================================================ */
const DAY = 86400;
/* Ngày tính theo giờ máy người đọc (VN +7), không phải UTC — đọc 22h tối hay
   0h30 sáng vẫn rơi vào đúng ngày hôm đó, chuỗi "ngày liên tiếp" không lệch. */
const dayKey = (ts) => {
  const d = new Date((ts || 0) * 1000);
  return Math.floor(((ts || 0) - d.getTimezoneOffset() * 60) / DAY);
};
function paintToday(sessions) {
  const el = $("#todayBox");
  if (!el) return;
  const now = dayKey(Date.now() / 1000);
  const days = new Set(sessions.map((s) => dayKey(s.ts || 0)));
  const minsToday = sessions.filter((s) => dayKey(s.ts || 0) === now)
    .reduce((a, s) => a + (s.minutes || 0), 0);
  let streak = 0;
  for (let d = now; days.has(d); d--) streak++;       // hôm nay + các ngày liền trước
  const nfT = new Intl.NumberFormat("vi-VN");
  el.innerHTML = `
    <div class="today-row">
      <span class="today-num num">${nfT.format(minsToday)}<i>phút</i></span>
      <span class="today-streak num">${nfT.format(streak)} ngày<i>liên tiếp</i></span>
    </div>
    <p class="today-note">${minsToday ? "Đang giữ chuỗi — đọc tiếp nhé."
      : streak > 1 ? "Hôm nay chưa đọc, chuỗi đang chờ."
      : "Đọc một chương là bắt đầu chuỗi."}</p>`;
}

/* ============================================================
   RENDER
   ============================================================ */
let DATA = { books: [], latest: [] };
let filter = "Tất cả";
let query = "";
let lastRand = null;

async function load() {
  const [books, latest] = await Promise.all([
    fetch("/api/books").then((r) => r.json()),
    fetch("/api/latest?limit=18").then((r) => r.json()).catch(() => ({ chapters: [] })),
  ]);
  DATA = { books: books.books || [], latest: latest.chapters || [] };
}

function paintHero() {
  const books = DATA.books;
  const sec = $("#hero");
  sec.setAttribute("aria-busy", "false");
  const head = books.find((b) => state(b).has) || books[0];
  const tiles = books.filter((b) => b.id !== head.id).slice(0, 4);
  sec.innerHTML = heroBig(head) +
    `<div class="hero-side">${tiles.map(heroTile).join("")}</div>`;
}

function paintHot() {
  const pool = [...DATA.books]
    .sort((a, b) => (b.updated || 0) - (a.updated || 0) || (b.chapters || 0) - (a.chapters || 0))
    .slice(0, 6);
  $("#hot").innerHTML = pool.map((b, i) => card(b, { i })).join("");
}

function paintAI() {
  const seen = new Set();
  const rows = [];
  for (const c of DATA.latest) {
    if (seen.has(c.book)) continue;
    seen.add(c.book);
    rows.push(chCard(c, DATA.books.find((b) => b.id === c.book)));
    if (rows.length >= 6) break;
  }
  $("#ai").innerHTML = rows.join("");
}

function matches(b) {
  const okG = filter === "Tất cả" || genres(b).includes(filter);
  if (!okG) return false;
  if (!query) return true;
  const q = query.toLowerCase();
  return (b.title || "").toLowerCase().includes(q)
      || (b.author || "").toLowerCase().includes(q);
}

function paintGrid() {
  const grid = $("#grid");
  grid.setAttribute("aria-busy", "false");
  const pool = DATA.books.filter(matches);
  $("#count").textContent = pool.length === DATA.books.length
    ? DATA.books.length + " bộ"
    : pool.length + " / " + DATA.books.length + " bộ";
  if (!pool.length) {
    grid.innerHTML = `<div class="empty"><b>Không tìm thấy truyện nào</b>
      Thử từ khóa khác, hoặc chọn lại thể loại “Tất cả”.</div>`;
    return;
  }
  grid.innerHTML = pool.map((b, i) => card(b, { i })).join("");
}

function paintChips() {
  const count = new Map();
  DATA.books.forEach((b) => genres(b).forEach((g) => count.set(g, (count.get(g) || 0) + 1)));
  const list = [...count.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "vi"));
  const chip = (label, n) =>
    `<button class="chip" type="button" data-genre="${esc(label)}" aria-pressed="${filter === label}">${esc(label)}<i>${n}</i></button>`;
  $("#filters").innerHTML = chip("Tất cả", DATA.books.length) + list.map(([g, n]) => chip(g, n)).join("");
}

function paintGenreMenu() {
  const count = new Map();
  DATA.books.forEach((b) => genres(b).forEach((g) => count.set(g, (count.get(g) || 0) + 1)));
  const list = [...count.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "vi"));
  $("#genreMenu").innerHTML =
    `<p class="mnote">Chọn để lọc kệ sách</p>` +
    list.map(([g, n]) => `<a role="menuitem" href="#allSec" data-genre="${esc(g)}">${esc(g)}<i>${n}</i></a>`).join("");
}

function paintContinue() {
  const box = $("#continueList");
  const reading = DATA.books
    .filter((b) => state(b).has)
    .sort((a, b) => state(b).last - state(a).last)
    .slice(0, 5);
  if (!reading.length) {
    box.innerHTML = `<div class="empty rsb-empty"><b>Chưa có truyện đang đọc</b>
      Chọn một bộ bên dưới để bắt đầu. Tiến độ lưu ngay trên trình duyệt này.</div>`;
    return;
  }
  box.innerHTML = reading.map(contItem).join("");
}

function pickRand() {
  const pool = DATA.books.filter((b) => b.id !== lastRand);
  if (!pool.length) return null;
  const b = pool[Math.floor(Math.random() * pool.length)];
  lastRand = b.id;
  return b;
}

function paintRand() {
  const box = $("#randCard");
  const b = pickRand();
  box.innerHTML = b ? randCard(b)
    : `<div class="empty rsb-empty"><b>Chưa có truyện nào</b>Thêm truyện vào <code>data\</code> rồi quét lại.</div>`;
}

function paintFoot() {
  const ch = DATA.books.reduce((s, b) => s + (b.chapters || 0), 0);
  $("#footline").textContent = DATA.books.length + " bộ · " + fmtShort(ch) + " chương · cập nhật "
    + ago(Math.max(0, ...DATA.books.map((b) => b.updated || 0)));
}

/* JSON-LD ItemList, bơm sau khi có dữ liệu (Googlebot chạy JS) */
function injectSchema() {
  const ld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": DATA.books.map((b, i) => ({
      "@type": "ListItem",
      "position": i + 1,
      "item": {
        "@type": "Book",
        "name": b.title,
        "author": b.author ? { "@type": "Person", "name": b.author } : undefined,
        "genre": genres(b).join(", ") || undefined,
        "numberOfPages": b.chapters || undefined,
        "url": "/sach/" + encodeURIComponent(b.id),
        "inLanguage": "vi"
      },
    })),
  };
  let el = document.getElementById("ld-items");
  if (!el) {
    el = document.createElement("script");
    el.type = "application/ld+json";
    el.id = "ld-items";
    document.head.appendChild(el);
  }
  el.textContent = JSON.stringify(ld);
}

function paint() {
  if (!DATA.books.length) {
    $("#hero").innerHTML = "";
    $("#hot").innerHTML = "";
    $("#ai").innerHTML = "";
    $("#grid").innerHTML = `<div class="empty"><b>Chưa có truyện nào</b>
      Thả các file <code>0001_*.md</code> vào một thư mục con trong <code>data\</code>,
      rồi bấm nút quét lại ở thanh bên trái.</div>`;
    $("#continueList").innerHTML = "";
    paintRand();
    return;
  }
  paintHero(); paintHot(); paintAI(); paintChips(); paintGenreMenu();
  paintGrid(); paintContinue(); paintRand(); paintFoot(); injectSchema();
  wireRailNav();
}

/* ---------- skeleton trước khi có dữ liệu ---------- */
function skel() {
  $("#hot").innerHTML = Array.from({ length: 6 }, () =>
    `<div class="mcard"><span class="mcard-cov sk" style="aspect-ratio:2/3"></span>
     <span class="mcard-meta"><span class="sk" style="height:12px;width:85%"></span>
     <span class="sk" style="height:10px;width:55%"></span></span></div>`).join("");
  $("#ai").innerHTML = $("#hot").innerHTML;
  $("#grid").innerHTML = Array.from({ length: 8 }, () =>
    `<div class="mcard"><span class="mcard-cov sk" style="aspect-ratio:2/3"></span>
     <span class="mcard-meta"><span class="sk" style="height:12px;width:80%"></span>
     <span class="sk" style="height:10px;width:50%"></span></span></div>`).join("");
}

/* ---------- điều hướng rail ---------- */
function wireRailNav() {
  document.querySelectorAll(".rail-wrap").forEach((wrap) => {
    const rail = wrap.querySelector(".hrail");
    const prev = wrap.querySelector(".prev");
    const next = wrap.querySelector(".next");
    if (!rail || !prev || !next) return;
    const step = () => Math.max(rail.clientWidth * 0.8, 240);
    const sync = () => {
      const max = rail.scrollWidth - rail.clientWidth - 2;
      prev.hidden = rail.scrollLeft <= 2;
      next.hidden = rail.scrollLeft >= max;
    };
    prev.onclick = () => rail.scrollBy({ left: -step(), behavior: RM ? "auto" : "smooth" });
    next.onclick = () => rail.scrollBy({ left: step(), behavior: RM ? "auto" : "smooth" });
    rail.addEventListener("scroll", sync, { passive: true });
    sync();
  });
}

/* ---------- sự kiện ---------- */
function toast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toast.t);
  toast.t = setTimeout(() => el.classList.remove("show"), 1800);
}

/* lọc thể loại (chip + menu dropdown) */
function setFilter(g) {
  filter = g;
  document.querySelectorAll("#filters .chip").forEach((c) =>
    c.setAttribute("aria-pressed", String(c.dataset.genre === g)));
  paintGrid();
}

$("#filters").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-genre]");
  if (btn) setFilter(btn.dataset.genre);
});
$("#genreMenu").addEventListener("click", (e) => {
  const a = e.target.closest("a[data-genre]");
  if (!a) return;
  e.preventDefault();
  $("#genreDrop").open = false;
  setFilter(a.dataset.genre);
  $("#allSec").scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
});

/* tìm kiếm client-side */
$("#search").addEventListener("submit", (e) => {
  e.preventDefault();
  query = $("#q").value.trim();
  paintGrid();
  $("#allSec").scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "start" });
});
let qT;
$("#q").addEventListener("input", () => {
  clearTimeout(qT);
  qT = setTimeout(() => { query = $("#q").value.trim(); paintGrid(); }, 200);
});

/* đóng dropdown khi click ra ngoài / Escape */
document.addEventListener("click", (e) => {
  document.querySelectorAll("details.tn-drop[open]").forEach((d) => {
    if (!d.contains(e.target)) d.open = false;
  });
  const add = $("#addHow");
  if (add.open && !add.contains(e.target)) add.open = false;
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  document.querySelectorAll("details[open]").forEach((d) => (d.open = false));
});

/* nút đổi truyện ngẫu nhiên */
$("#randCard").addEventListener("click", (e) => {
  if (e.target.closest("#reroll")) paintRand();
});

/* quét lại thư mục */
$("#reload").addEventListener("click", async () => {
  const t = $("#reload");
  t.setAttribute("aria-busy", "true");
  try {
    await fetch("/api/reload").catch(() => {});
    await load();
    paint();
    toast("Đã quét lại thư mục truyện");
  } finally {
    t.removeAttribute("aria-busy");
  }
});

/* tắt shimmer khi skeleton ngoài viewport */
if ("IntersectionObserver" in window && !RM) {
  const skIO = new IntersectionObserver((ents) => {
    ents.forEach((en) => en.target.classList.toggle("paused", !en.isIntersecting));
  });
  new MutationObserver((muts) => {
    muts.forEach((m) => m.addedNodes.forEach((n) => {
      if (n.nodeType !== 1) return;
      if (n.classList && n.classList.contains("sk")) skIO.observe(n);
      n.querySelectorAll && n.querySelectorAll(".sk").forEach((el) => skIO.observe(el));
    }));
  }).observe(document.body, { childList: true, subtree: true });
}

/* ---------- khởi động ---------- */
skel();
/* khối "Hôm nay của bạn" lấy từ kho phiên IDB — vẽ ngay khi kho sẵn sàng */
storeReady(async () => { paintToday(await getSessions()); });
load().then(paint).catch(() => {
  $("#hero").innerHTML = "";
  $("#hot").innerHTML = "";
  $("#ai").innerHTML = "";
  $("#grid").setAttribute("aria-busy", "false");
  $("#grid").innerHTML = `<div class="empty"><b>Không gọi được server</b>
    Mở lại <code>python reader\server.py</code> rồi tải lại trang này.</div>`;
});

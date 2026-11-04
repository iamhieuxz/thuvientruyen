/* ============================================================
   shelf.js — trang chủ tủ sách
   Nguồn: /api/books (một dòng mỗi truyện) + /api/latest (chương mới).
   Tiến độ đọc lấy từ localStorage qua store.js.
   ============================================================ */

const all = loadStore();
const $ = (s) => document.querySelector(s);
const nf = new Intl.NumberFormat("vi-VN");
const esc = escHTML;

/* ---------- giao diện theo thiết lập trang đọc ---------- */
const THEMES = ["giay", "cu", "dem", "muc"];
const ALIAS = { night: "dem", ink: "muc", slate: "dem", moss: "muc" };
const saved = (all.settings || {}).theme;
const theme = THEMES.includes(saved) ? saved : (ALIAS[saved] || "dem");
document.body.dataset.theme = theme;
document.documentElement.style.colorScheme = theme === "giay" || theme === "cu" ? "light" : "dark";
{
  const m = document.querySelector('meta[name="theme-color"]');
  if (m) m.content = getComputedStyle(document.body).backgroundColor;
}

/* ---------- tiện ích ---------- */
const ago = (t) => {
  if (!t) return "";
  const d = (Date.now() / 1000 - t) / 86400;
  if (d < 1 / 24) return "vừa cập nhật";
  if (d < 1) return Math.round(d * 24) + " giờ trước";
  if (d < 30) return Math.round(d) + " ngày trước";
  return new Date(t * 1000).toLocaleDateString("vi-VN");
};
const fmtMin = (m) => {
  const h = Math.round((m || 0) / 60);
  return h >= 1000 ? (h / 1000).toFixed(1).replace(".", ",") + " nghìn giờ" : nf.format(h) + " giờ";
};
const fmtShort = (n) => (n >= 1e6 ? (n / 1e6).toFixed(1).replace(".", ",") + " tr" : nf.format(n || 0));
const genres = splitGenres;

function state(b) {
  const B = all.books[b.id] || {};
  const last = +B.last || 0;
  const read = (B.read || []).length;
  const chapters = b.chapters || 0;
  return {
    last, read, chapters,
    pct: last && chapters ? Math.min(100, Math.round((last / chapters) * 100)) : 0,
    has: last > 0,
    rest: Math.max(0, chapters - last),
  };
}

/* ---------- bìa ---------- */
const art = coverHTML;
const titleHTML = (t) => esc(t).replace(/(\d+)/g, '<span class="n">$1</span>');

/* ---------- hero ---------- */
function hero(b) {
  if (!b) return "";
  const s = state(b);
  const href = `/sach/${encodeURIComponent(b.id)}/chuong/${s.last || b.first}`;
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  const g = genres(b);
  const kick = s.has
    ? `<span class="dot"></span>Đang đọc dở <em>·</em> ${s.pct}%`
    : `<span class="dot"></span>${b.updated && Date.now() / 1000 - b.updated < 172800
        ? "Mới lên kệ" : "Bộ mới nhất"}${g[0] ? ` <em>·</em> ${esc(g[0])}` : ""}`;

  const facts = s.has
    ? `<b>${nf.format(s.read)}</b> chương đã đọc
       <span class="sep">·</span> còn <b>${nf.format(s.rest)}</b> chương
       <span class="sep">·</span> ${fmtMin((s.rest / (s.chapters || 1)) * (b.minutes || 0))} nữa`
    : `<b>${nf.format(s.chapters)}</b> chương
       <span class="sep">·</span> đã dịch <b>${pctShow(b.progress, s.chapters)}%</b>
       <span class="sep">·</span> ${fmtMin(b.minutes)} đọc`;

  return `<div class="hm-feat">
    <div class="hm-txt">
      <p class="kick" style="margin-bottom:16px">${kick}</p>
      <h1 class="hm-title"><a href="${detail}" style="color:inherit;text-decoration:none">${titleHTML(b.title)}</a></h1>
      <p class="hm-by">${b.author ? `<b>${esc(b.author)}</b>` : "Không rõ tác giả"}${g.length ? " · " + esc(g.join(" · ")) : ""}</p>
      ${b.desc ? `<p class="hm-desc">${esc(b.desc)}</p>` : ""}
      <p class="hm-facts">${facts}</p>
      <div class="rail" style="margin-bottom:14px" aria-hidden="true"><i style="width:${s.has ? s.pct : 0}%"></i></div>
      <a class="hm-go" href="${href}">${s.has ? `Đọc tiếp chương ${nf.format(s.last)}` : "Bắt đầu đọc"}
        <svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></svg></a>
      <p style="margin:14px 0 0"><a href="${detail}"
        style="font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:3px">Trang truyện · thông tin &amp; mục lục</a></p>
    </div>
    <a class="hm-art" href="${detail}" aria-label="Xem trang truyện ${esc(b.title)}">
      <span class="hm-seal">${s.has ? s.pct + "%" : "Mới"}<i>${nf.format(s.chapters)} chương</i></span>
      ${art(b, "cov")}
      <span class="hm-glow" aria-hidden="true"></span>
    </a>
  </div>`;
}

/* ---------- dải đang đọc ---------- */
function mini(b) {
  const s = state(b);
  const href = `/sach/${encodeURIComponent(b.id)}/chuong/${s.last || b.first}`;
  const detail = `/sach/${encodeURIComponent(b.id)}`;
  return `<a class="hm-mini" href="${detail}" aria-label="${esc(b.title)} — xem trang truyện">
    ${art(b, "cov")}
    <span class="mt">
      <b>${esc(b.title)}</b>
      <span>chương ${nf.format(s.last)} / ${nf.format(s.chapters)} · ${s.pct}%</span>
      <span class="rail" aria-hidden="true"><i style="width:${s.pct}%"></i></span>
      <span style="font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc)">Đọc tiếp →</span>
    </span>
  </a>`;
}

/* ---------- chương mới ---------- */
function newRow(c) {
  const href = `/sach/${encodeURIComponent(c.book)}/chuong/${c.n}`;
  return `<a class="hm-lrow" href="${href}">
    <span class="hm-lno">${String(c.n).padStart(4, "0")}</span>
    <span class="hm-lbody">
      <span class="hm-lt">${esc(c.ctitle)}</span>
      <span class="hm-lb">${esc(c.title)}</span>
    </span>
    <span class="hm-lw">${ago(c.mtime)}</span>
  </a>`;
}

/* ---------- thẻ sách ---------- */
function card(b, i) {
  const s = state(b);
  const g = genres(b);
  const fresh = !s.has && b.updated && Date.now() / 1000 - b.updated < 3 * 86400;
  const badge = s.has ? `<span class="hm-badge acc">Đang đọc</span>`
    : fresh ? `<span class="hm-badge">Mới</span>` : "";
  const href = `/sach/${encodeURIComponent(b.id)}`;
  return `<a class="hm-card" style="--i:${i}" href="${href}"
      aria-label="${esc(b.title)} — ${s.has ? "đang đọc chương " + s.last + ", " : ""}${b.chapters} chương">
    <div class="hm-covwrap">${badge}${art(b, "cov")}</div>
    <div class="hm-cmeta">
      <p class="hm-cidx">${String(i + 1).padStart(2, "0")}</p>
      <h3>${esc(b.title)}</h3>
      ${b.author ? `<p class="hm-cby">${esc(b.author)}</p>` : g[0] ? `<p class="hm-cby">${esc(g[0])}</p>` : ""}
      <p class="hm-cst">${s.has
        ? `<b>${nf.format(s.last)}</b>/${nf.format(s.chapters)} chương <span class="pct">${s.pct}%</span>`
        : `<b>${nf.format(s.chapters)}</b> chương <span>·</span> ${pctShow(b.progress, s.chapters)}% dịch`}</p>
      ${s.has ? `<div class="hm-cprog"><span class="rail" aria-hidden="true"><i style="width:${s.pct}%"></i></span></div>` : ""}
    </div>
  </a>`;
}

/* ---------- lọc thể loại ---------- */
let filter = new URLSearchParams(location.search).get("tag") || "Tất cả";
let BOOKS = [];

function filterBar(books) {
  const count = new Map();
  books.forEach((b) => genres(b).forEach((g) => count.set(g, (count.get(g) || 0) + 1)));
  const list = [...count.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "vi"));
  const chip = (label, n, on) =>
    `<button class="hm-chip" type="button" data-genre="${esc(label)}"
      aria-pressed="${on ? "true" : "false"}">${esc(label)}<i>${n}</i></button>`;
  return chip("Tất cả", books.length, filter === "Tất cả")
    + list.map(([g, n]) => chip(g, n, filter === g)).join("");
}

function matches(b) {
  return filter === "Tất cả" || genres(b).includes(filter);
}

/* ---------- khung xương ---------- */
const skelHero = () => `<div class="hm-sk-hero">
  <div class="lines">
    <i class="sk"></i><i class="sk"></i><i class="sk"></i><i class="sk"></i>
  </div>
  <div class="art sk"></div>
</div>`;
const skelGrid = (n) => Array.from({ length: n }, () =>
  `<div class="hm-card"><div class="hm-covwrap"><div class="cov sk"></div></div>
   <div class="hm-cmeta"><p class="hm-cst sk" style="height:9px;width:70%"></p>
   <p class="hm-cst sk" style="height:9px;width:45%"></p></div></div>`).join("");

/* ---------- render ---------- */
let DATA = { books: [], latest: [] };

async function load() {
  const [books, latest] = await Promise.all([
    fetch("/api/books").then((r) => r.json()),
    fetch("/api/latest?limit=16").then((r) => r.json()).catch(() => ({ chapters: [] })),
  ]);
  DATA = { books: books.books || [], latest: latest.chapters || [] };
}

function paint() {
  const books = DATA.books;
  const grid = $("#grid");
  grid.setAttribute("aria-busy", "false");

  if (!books.length) {
    $("#hero").innerHTML = "";
    grid.innerHTML = `<div class="lib-empty" style="grid-column:1/-1"><b>Chưa có truyện nào</b>
      Thả các file <code>0001_*.md</code> vào một thư mục con trong <code>data\\</code>,
      rồi bấm nút quét lại ở góc trên.</div>`;
    $("#filters").innerHTML = "";
    return;
  }

  books.sort((a, b) =>
    (state(b).has ? 1 : 0) - (state(a).has ? 1 : 0)
    || (b.updated - a.updated));

  BOOKS = books;
  const head = books.find((b) => state(b).has) || books[0];
  const inProg = books.filter((b) => state(b).has && b.id !== head.id);
  const others = books.filter((b) => b.id !== head.id);

  $("#hero").innerHTML = hero(head);

  const railSec = $("#railSec");
  railSec.hidden = !inProg.length;
  $("#rail").innerHTML = inProg.map(mini).join("");
  $("#railNote").textContent = inProg.length ? inProg.length + " bộ" : "";

  const latest = DATA.latest;
  const latestSec = $("#latestSec");
  latestSec.hidden = !latest.length;
  if (latest.length) {
    const half = Math.ceil(latest.length / 2);
    $("#latest").innerHTML =
      `<div class="col">${latest.slice(0, half).map(newRow).join("")}</div>`
      + `<div class="col">${latest.slice(half).map(newRow).join("")}</div>`;
    $("#latestNote").textContent = "toàn tủ";
  }

  $("#filters").innerHTML = filterBar(books);
  renderGrid(others);
  $("#count").textContent = books.length + " bộ";

  const ch = books.reduce((s, b) => s + b.chapters, 0);
  const live = $("#live");
  if (live) live.innerHTML = `<em>●</em> ${books.length} bộ · ${nf.format(ch)} chương`;
  const foot = $("#footline");
  if (foot) {
    foot.textContent = `${books.length} bộ · ${fmtShort(ch)} chương · cập nhật `
      + ago(Math.max(...books.map((b) => b.updated || 0)));
  }
}

function renderGrid(list) {
  const grid = $("#grid");
  const pool = filter === "Tất cả" ? list : BOOKS.filter(matches);
  if (!pool.length) {
    grid.innerHTML = `<div class="lib-empty" style="grid-column:1/-1">
      <b>Chưa có truyện ở nhãn “${esc(filter)}”</b>Chọn nhãn khác, hoặc bỏ lọc để xem cả tủ.</div>`;
    return;
  }
  grid.innerHTML = pool.map(card).join("");
}

/* ---------- khởi động ---------- */
$("#hero").innerHTML = skelHero();
$("#grid").innerHTML = skelGrid(4);

/* kho v3 hydrate IDB nền xong: chỗ đang đọc có thể mới hơn -> vẽ lại thẻ */
storeReady(() => { if (BOOKS.length) paint(); });

load().then(paint).catch(() => {
  $("#hero").innerHTML = "";
  $("#grid").setAttribute("aria-busy", "false");
  $("#grid").innerHTML = `<div class="lib-empty" style="grid-column:1/-1">
    <b>Không gọi được server</b>Mở lại <code>python reader\\server.py</code> rồi tải lại trang này.</div>`;
});

/* ---------- lọc ---------- */
$("#filters").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-genre]");
  if (!btn) return;
  filter = btn.dataset.genre;
  try {
    history.replaceState(null, "", filter === "Tất cả" ? "/" : "/?tag=" + encodeURIComponent(filter));
  } catch { /* bỏ qua khi trình duyệt chặn */ }
  $("#filters").innerHTML = filterBar(BOOKS);
  const head = BOOKS.find((b) => state(b).has) || BOOKS[0];
  renderGrid(BOOKS.filter((b) => b.id !== head.id));
});

/* ---------- quét lại ---------- */
$("#reload").onclick = async () => {
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
};

function toast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toast.t);
  toast.t = setTimeout(() => el.classList.remove("show"), 1800);
}

/* ---------- thanh trên dính + bìa nhích nhẹ ---------- */
addEventListener("scroll", () => {
  const bar = $("#bar");
  if (bar) bar.classList.toggle("stuck", scrollY > 6);
  const art = document.querySelector(".hm-art");
  if (art && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    art.style.transform = `translateY(${Math.min(scrollY * 0.04, 30)}px)`;
  }
}, { passive: true });

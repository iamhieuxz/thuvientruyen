/* ============================================================
   book.js — trang chi tiết một bộ truyện
   Nguồn: /api/book (metadata + tiến độ dịch), /api/chapters (mục lục),
   /api/books (các bộ khác). Tiến độ đọc lấy từ store.js.
   ============================================================ */

const BOOK = (location.pathname.match(/^\/sach\/([A-Za-z0-9._-]+)/) || [])[1] || "";
const $ = (s) => document.querySelector(s);
const nf = new Intl.NumberFormat("vi-VN");
const esc = escHTML;
const genres = splitGenres;

const all = loadStore();
const B = all.books[BOOK] || (all.books[BOOK] = { read: [], pos: {}, last: null });
const readSet = new Set((B.read || []).map(Number));
let last = +B.last || 0;

/* Kho v3 hydrate IDB nền xong: nạp thêm chương đã đọc/chỗ đang đọc từ thiết bị khác,
   vẽ lại phần "chỗ đang đọc" và mục lục đang mở. mergeAll chỉ thêm không bớt. */
storeReady(() => {
  (B.read || []).forEach((n) => readSet.add(n));
  last = Math.max(last, +B.last || 0);
  paintHead(bookMeta || { id: BOOK, title: BOOK, chapters: CH.length });
  if (view.length) applyFilter();
});

/* ---------- giao diện theo thiết lập trang đọc ---------- */
const THEMES = ["giay", "cu", "dem", "muc"];
const ALIAS = { night: "dem", ink: "muc", slate: "dem", moss: "muc" };
const savedTheme = (all.settings || {}).theme;
const theme = THEMES.includes(savedTheme) ? savedTheme : (ALIAS[savedTheme] || "dem");
document.body.dataset.theme = theme;
document.documentElement.style.colorScheme = theme === "giay" || theme === "cu" ? "light" : "dark";
{
  const m = document.querySelector('meta[name="theme-color"]');
  if (m) m.content = getComputedStyle(document.body).backgroundColor;
}

/* ---------- định dạng ---------- */
const ago = (t) => {
  if (!t) return "chưa rõ";
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
const fmtShort = (n) => (n >= 1e6 ? (n / 1e6).toFixed(1).replace(".", ",") + " tr chữ"
  : nf.format(n || 0) + " chữ");
const norm = (s) => String(s == null ? "" : s).normalize("NFD")
  .replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
const titleHTML = (t) => esc(t).replace(/(\d+)/g, '<span class="n">$1</span>');

/* ---------- trạng thái ---------- */
let CH = [];          // toàn bộ chương
let view = [];        // sau khi lọc + sắp
let page = 1;         // trang mục lục hiện tại
let sort = "asc";
let bookMeta = null;  // metadata truyện từ /api/book (để vẽ lại khi kho hydrate xong)
const PAGE = 200;     // số chương mỗi trang mục lục
const wantedPage = +(new URLSearchParams(location.search).get("trang") || 0);
const toastEl = $("#toast");
let toastT;

function toast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add("show");
  clearTimeout(toastT);
  toastT = setTimeout(() => toastEl.classList.remove("show"), 1900);
}

/* ---------- đầu truyện ---------- */
function paintHead(b) {
  const chapters = b.chapters || 0;
  const first = b.first || 1;
  const origin = b.original_chapters || chapters;
  const pct = b.progress || 0;
  const g = genres(b);

  document.title = `${b.title} · truyendochay`;
  const md = document.querySelector('meta[name="description"]');
  if (md) {
    md.setAttribute("content", (b.desc || b.title).replace(/\s+/g, " ").slice(0, 180));
  }

  $("#crumb").textContent = b.title;
  $("#crumb").title = b.title;
  const crumbG = $("#crumbGenre");
  crumbG.innerHTML = g.length
    ? `<a href="/?tag=${encodeURIComponent(g[0])}">${esc(g[0])}</a> <span aria-hidden="true">/</span>`
    : "";

  /* bìa + nền mờ */
  const src = coverSrc(b);
  $("#artCover").innerHTML = coverHTML(b, "cov");
  if (src) $("#veil").style.backgroundImage = `url("${src}")`;
  const seal = $("#seal");
  seal.innerHTML = `${pctShow(pct, chapters)}<i>${nf.format(chapters)} chương</i>`;
  seal.hidden = false;

  /* dòng trạng thái */
  const status = b.status || (pct >= 100 ? "Đã dịch xong" : "Đang dịch");
  const parts = [esc(status)];
  if (b.original_status) parts.push("nguồn " + esc(String(b.original_status).toLowerCase()));
  $("#kickText").innerHTML = parts.join(" <em>·</em> ");

  /* tựa + tác giả */
  $("#title").innerHTML = titleHTML(b.title);
  if (b.original_title) {
    const alt = $("#alt");
    alt.textContent = b.original_title;
    alt.hidden = false;
  }
  /* nhãn phân loại: thể loại + tình trạng + nguồn */
  const tags = [];
  g.forEach((t) => tags.push(`<li class="tag">${esc(t)}</li>`));
  tags.push(`<li class="tag acc">${esc(status)}</li>`);
  if (pct >= 100 && chapters) tags.push(`<li class="tag mute">Đủ bộ</li>`);
  $("#tags").innerHTML = tags.join("");

  /* bảng thông tin truyện */
  const srcState = /chưa rõ/i.test(String(b.original_status || "")) ? "" : String(b.original_status || "");
  const kind = srcState ? `${status} · nguồn ${srcState.toLowerCase()}` : status;
  const authorCell = esc(b.author || "Không rõ")
    + (b.author_original ? `<span class="bk-native">${esc(b.author_original)}</span>` : "");
  const info = [
    ["Tác giả", authorCell, [b.author, b.author_original].filter(Boolean).join(" · ")],
    ["Số chương", `<b>${nf.format(chapters)}</b> / ${nf.format(origin)}`, `${chapters} / ${origin}`],
    ["Cập nhật", ago(b.updated), null],
    ["Trạng thái", esc(kind), kind],
    ["Thể loại", g.length ? esc(g.join(", ")) : "Chưa phân loại", g.join(", ")],
    ["Bản dịch", "Máy dịch · có glossary", null],
  ];
  $("#info").innerHTML = info.map(([k, v, tip]) =>
    `<div><dt>${k}</dt><dd${tip ? ` title="${esc(tip)}"` : ""}>${v}</dd></div>`).join("");

  /* hành động */
  const readBtn = $("#readBtn");
  const firstBtn = $("#firstBtn");
  if (chapters) {
    const resume = last >= first && last <= (b.last || last) ? last : 0;
    readBtn.href = `/sach/${encodeURIComponent(b.id)}/chuong/${resume || first}`;
    readBtn.innerHTML = `${resume ? `Đọc tiếp chương ${nf.format(resume)}` : "Bắt đầu đọc"}
      <svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6"/></svg>`;
    readBtn.hidden = false;
    firstBtn.href = `/sach/${encodeURIComponent(b.id)}/chuong/${first}`;
    firstBtn.hidden = !resume || resume === first;
  }
  if (b.source) {
    const s = $("#srcBtn");
    s.href = b.source;
    s.hidden = false;
  }

  /* chỗ đang đọc */
  if (last > 0 && chapters) {
    const pctMine = Math.min(100, Math.round((last / chapters) * 100));
    $("#mine").hidden = false;
    $("#mineBar").style.width = pctMine + "%";
    $("#mineText").innerHTML = `Đang ở <b>chương ${nf.format(last)}</b> / ${nf.format(chapters)}
      — đã đọc <b>${nf.format(readSet.size)}</b> chương, còn <b>${nf.format(Math.max(0, chapters - last))}</b> chương.`;
  }

  /* bảng tiến độ dịch */
  $("#pct").textContent = pctShow(pct, chapters);
  $("#pctBar").style.width = pct + "%";
  const left = Math.max(0, origin - chapters);
  const rows = [
    ["Chương đã dịch", `<b>${nf.format(chapters)}</b> / ${nf.format(origin)}`],
    ["Còn thiếu", left ? `<b>${nf.format(left)}</b> chương` : "đủ bộ"],
    ["Độ dài", `${fmtShort(b.chars)} · ${fmtMin(b.minutes)} đọc`],
  ];
  $("#facts").innerHTML = rows
    .map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join("");

  /* giới thiệu truyện — hiện đầy đủ, không cắt */
  const desc = $("#desc");
  const text = (b.desc || "").trim();
  if (text) {
    desc.textContent = text;
  } else {
    desc.textContent = "Bộ này chưa có phần giới thiệu trong book.json.";
    desc.style.color = "var(--dim)";
  }

  $("#live").innerHTML = `<em>●</em> ${nf.format(chapters)} chương · ${pctShow(pct, chapters)}% dịch`;
  $("#footline").textContent = `${nf.format(chapters)} chương · ${pctShow(pct, chapters)}% đã dịch · `
    + `cập nhật ${ago(b.updated)}`;
  $("#tocCount").textContent = `${nf.format(chapters)} chương · ${nf.format(first)}–${nf.format(b.last || first)}`;
}

/* ---------- mục lục: 200 chương mỗi trang ---------- */
function rowHTML(c) {
  const isRead = readSet.has(+c.n);
  const cur = +c.n === last;
  const cls = "bk-row" + (isRead ? " is-read" : "") + (cur ? " is-cur" : "");
  const meta = cur ? `<span class="tm">đang đọc</span>` : "";
  return `<li><a class="${cls}" href="/sach/${encodeURIComponent(BOOK)}/chuong/${c.n}"
      title="Chương ${c.n}: ${esc(c.title)}">
    <span class="no">${String(c.n).padStart(4, "0")}</span>
    <span class="tt">${esc(c.title)}</span>
    <span class="meta">${meta}<span class="mk" aria-hidden="true"></span></span>
  </a></li>`;
}

const pageCount = () => Math.max(1, Math.ceil(view.length / PAGE));

function setPageInUrl() {
  const url = page > 1 ? `?trang=${page}` : location.pathname;
  try { history.replaceState(null, "", url); } catch { /* trình duyệt chặn: bỏ qua */ }
}

/* dãy số trang có rút gọn: 1 … 4 5 6 … 17 */
function pagerHTML() {
  const total = pageCount();
  const want = new Set([1, total]);
  for (let p = page - 1; p <= page + 1; p += 1) if (p >= 1 && p <= total) want.add(p);
  const nums = [];
  let prev = 0;
  [...want].sort((a, b) => a - b).forEach((p) => {
    if (prev && p - prev > 1) nums.push(`<span class="gap" aria-hidden="true">…</span>`);
    nums.push(`<button type="button" data-page="${p}"${p === page
      ? ' aria-current="page"' : ""} aria-label="Trang ${p}">${p}</button>`);
    prev = p;
  });
  return `<button type="button" class="nav" data-nav="prev"${page <= 1 ? " disabled" : ""}
      aria-label="Trang trước">‹</button>
    <span class="nums">${nums.join("")}</span>
    <button type="button" class="nav" data-nav="next"${page >= total ? " disabled" : ""}
      aria-label="Trang sau">›</button>`;
}

function renderPage(moveFocus) {
  page = Math.min(Math.max(1, page), pageCount());
  const start = (page - 1) * PAGE;
  $("#list").innerHTML = view.slice(start, start + PAGE).map(rowHTML).join("");
  $("#list").setAttribute("aria-busy", "false");
  $("#pager").innerHTML = view.length > PAGE ? pagerHTML() : "";
  const total = pageCount();
  $("#tocCount").textContent = `${nf.format(view.length)} chương`
    + (total > 1 ? ` · trang ${page}/${total}` : "");
  if (moveFocus) {
    const cur = $("#pager [aria-current='page']");
    if (cur) cur.focus({ preventScroll: true });
  }
}

function applyFilter() {
  const q = norm($("#q").value.trim());
  const unreadOnly = $("#unreadOnly").getAttribute("aria-pressed") === "true";
  let list = CH.filter((c) => {
    if (unreadOnly && readSet.has(+c.n)) return false;
    if (!q) return true;
    return norm(c.title).includes(q) || String(c.n).includes(q);
  });
  if (sort === "desc") list = list.slice().reverse();
  view = list;
  page = 1;
  if (location.search.includes("trang=")) {
    try { history.replaceState(null, "", location.pathname + location.hash); } catch { /* bỏ qua */ }
  }
  if (!view.length) {
    $("#list").setAttribute("aria-busy", "false");
    $("#list").innerHTML = `<li class="lib-empty" style="grid-column:1/-1;margin-top:14px">
      <b>Không tìm thấy chương nào</b>Thử từ khoá khác, hoặc bỏ lọc “chưa đọc”.</li>`;
    $("#pager").innerHTML = "";
    const total = nf.format(CH.length);
    $("#tocCount").textContent = q || unreadOnly ? `0 / ${total} chương` : `0 chương`;
    return;
  }
  renderPage();
}

/* ---------- tải dữ liệu ---------- */
async function boot() {
  if (!BOOK) throw new Error("thiếu mã truyện");
  const [book, chapters, shelf] = await Promise.all([
    fetch(`/api/book?book=${encodeURIComponent(BOOK)}`).then((r) => {
      if (!r.ok) throw new Error("không tìm thấy truyện");
      return r.json();
    }),
    fetch(`/api/chapters?book=${encodeURIComponent(BOOK)}`).then((r) => r.json()),
    fetch("/api/books").then((r) => r.json()).catch(() => ({ books: [] })),
  ]);

  paintHead(book);
  bookMeta = book;

  CH = (chapters.chapters || []).slice().sort((a, b) => a.n - b.n);
  if (!CH.length) {
    $("#list").setAttribute("aria-busy", "false");
    $("#list").innerHTML = `<li class="lib-empty" style="grid-column:1/-1">
      <b>Chưa có chương nào</b>Thư mục truyện chưa có file <code>0001_*.md</code>.</li>`;
    $("#tocCount").textContent = "0 chương";
  } else {
    applyFilter();
    if (wantedPage > 1) { page = wantedPage; renderPage(); setPageInUrl(); }
  }

  /* các bộ khác */
  const rest = (shelf.books || []).filter((b) => b.id !== BOOK).slice(0, 6);
  if (rest.length) {
    $("#others").hidden = false;
    $("#ogrid").innerHTML = rest.map((b) => `<a class="bk-ocard" href="/sach/${encodeURIComponent(b.id)}">
      ${coverHTML(b, "cov")}<h3>${esc(b.title)}</h3></a>`).join("");
  }


}

/* ---------- tương tác ---------- */
$("#sortSeg").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-sort]");
  if (!b) return;
  sort = b.dataset.sort;
  [...$("#sortSeg").querySelectorAll("button")].forEach((x) =>
    x.setAttribute("aria-pressed", x === b ? "true" : "false"));
  applyFilter();
});

$("#unreadOnly").addEventListener("click", (e) => {
  const on = e.currentTarget.getAttribute("aria-pressed") === "true";
  e.currentTarget.setAttribute("aria-pressed", on ? "false" : "true");
  applyFilter();
});

let qT;
$("#q").addEventListener("input", () => {
  clearTimeout(qT);
  qT = setTimeout(applyFilter, 120);
});

$("#pager").addEventListener("click", (e) => {
  const num = e.target.closest("button[data-page]");
  const nav = e.target.closest("button[data-nav]");
  if (!num && !nav) return;
  if (num) page = +num.dataset.page;
  else page += nav.dataset.nav === "prev" ? -1 : 1;
  renderPage(true);
  setPageInUrl();
  const barH = ($("#bar") ? $("#bar").offsetHeight : 0) + 10;
  const top = $("#toc").getBoundingClientRect().top + scrollY - barH;
  scrollTo({
    top: Math.max(0, top),
    behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
  });
});

/* phím "/" nhảy vào ô tìm chương */
addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement !== $("#q")) {
    e.preventDefault();
    $("#q").focus();
  }
});

/* thanh trên dính */
addEventListener("scroll", () => {
  const bar = $("#bar");
  if (bar) bar.classList.toggle("stuck", scrollY > 6);
}, { passive: true });

boot().catch((err) => {
  $("#crumb").textContent = "Không tìm thấy truyện";
  $("#title").textContent = "Truyện này không có trong tủ";
  $("#kick").hidden = true;
  $("#tags").innerHTML = "";
  $("#info").innerHTML = `<div style="grid-column:1/-1">
    <dt>Lỗi</dt><dd style="white-space:normal">${esc(String(err.message || err))}.
    <a href="/" style="color:var(--acc)">Về tủ sách</a></dd></div>`;
  $("#list").setAttribute("aria-busy", "false");
  $("#list").innerHTML = "";
  $("#tocCount").textContent = "";
  $("#artCover").innerHTML = "";
});

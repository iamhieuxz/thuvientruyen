/* Ke sach: liet ke moi truyen trong data/, mo tiep cho dang doc */

const all = loadStore();
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g,
  (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nf = new Intl.NumberFormat("vi-VN");

const THEMES = ["giay", "cu", "dem", "muc"];
const ALIAS = { night: "dem", ink: "muc", slate: "dem", moss: "muc" };
const saved = all.settings && all.settings.theme;
const theme = THEMES.includes(saved) ? saved : (ALIAS[saved] || "dem");
document.body.dataset.theme = theme;
document.documentElement.style.colorScheme = theme === "giay" || theme === "cu" ? "light" : "dark";
const meta = document.querySelector('meta[name="theme-color"]');
if (meta) meta.content = getComputedStyle(document.body).backgroundColor;

const hue = (s) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 360; return h; };
const ago = (t) => {
  const d = (Date.now() / 1000 - t) / 86400;
  if (d < 1 / 24) return "vừa cập nhật";
  if (d < 1) return Math.round(d * 24) + " giờ trước";
  if (d < 30) return Math.round(d) + " ngày trước";
  return new Date(t * 1000).toLocaleDateString("vi-VN");
};
const pos = (b) => { const p = all.books[b.id] || {}; return +p.last > 0 ? +p.last : 0; };

const PAL = [["#432a7a", "#170f28"], ["#14504a", "#08191c"], ["#26315f", "#0d1020"],
             ["#6a2440", "#1a0a11"], ["#23512f", "#0b1710"], ["#2a4a6b", "#0c141d"]];
const flat = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/đ/g, "d").replace(/Đ/g, "D");
const initials = (t) => {
  const w = flat(t).trim().split(/\s+/).filter(Boolean);
  return ((w.length > 1 ? w[0][0] + w[1][0] : (w[0] || "").slice(0, 2)) || "?").toUpperCase();
};
const grad = (id) => {
  const [c1, c2] = PAL[hue(id) % PAL.length];
  return `background:radial-gradient(130% 78% at 16% 0%, rgba(255,255,255,.14), transparent 56%),`
    + `linear-gradient(158deg,${c1},${c2})`;
};

function cover(b, big) {
  const ini = esc(initials(b.title));
  const au = esc(b.author || "");
  if (b.cover) {
    const src = `/api/cover?book=${encodeURIComponent(b.id)}`;
    return big
      ? `<span class="fcover"><img src="${src}" alt="Bìa ${esc(b.title)}"></span>`
      : `<img class="cover" src="${src}" alt="Bìa ${esc(b.title)}" loading="lazy">`;
  }
  const st = `style="${grad(b.id)}"`;
  return big
    ? `<span class="fcover" ${st}><span>${ini}</span></span>`
    : `<div class="cover gen" ${st}><b>${ini}</b>${au ? `<i>${au}</i>` : ""}</div>`;
}

function card(b, i, h) {
  const at = pos(b);
  const total = (h && h.total) || b.chapters;
  const cur = (h && h.n) || at;
  const idx = (h && h.i) || (at ? Math.min(total, Math.round(at / (b.last || 1) * total)) : 0);
  const pct = idx && total ? Math.min(100, Math.round(idx / total * 100)) : 0;
  const badge = at ? `<span class="badge">Đang đọc</span>`
                   : (Date.now() / 1000 - b.updated) / 86400 < 3 ? `<span class="badge new">Mới</span>` : "";
  return `<a class="book" style="--i:${i}" href="/sach/${encodeURIComponent(b.id)}/chuong/${cur || b.first}"
      aria-label="${esc(b.title)} — ${at ? `đọc tới chương ${cur}` : `${b.chapters} chương`}">
    ${badge}${cover(b)}
    <div class="bmeta">
      <h3>${esc(b.title)}</h3>
      ${b.cover && b.author ? `<p class="by">${esc(b.author)}</p>` : ""}
      <p class="st"><span>${at ? `Chương ${cur}<b>/${total}</b>` : `${nf.format(b.chapters)} chương`}</span>
        <span>${at ? pct + "%" : ago(b.updated)}</span></p>
      ${at ? `<div class="track"><i style="width:${pct}%"></i></div>` : ""}
    </div></a>`;
}

function feat(b, h) {
  const at = pos(b);
  const total = (h && h.total) || b.chapters;
  const cur = (h && h.n) || at;
  const idx = (h && h.i) || cur;
  const pct = idx && total ? Math.min(100, Math.round(idx / total * 100)) : 0;
  const rest = Math.max(0, total - idx);
  const href = `/sach/${encodeURIComponent(b.id)}/chuong/${cur || b.first}`;
  const line = at
    ? `${pct}% · còn <b>${nf.format(rest)}</b> chương`
    : `<b>${nf.format(b.chapters)}</b> chương · ${nf.format(Math.round((b.minutes || 0) / 60))} giờ đọc`;
  const now = at
    ? (h && h.title ? `Chương ${cur}: ${h.title}` : `Chương ${cur}`)
    : `Chưa đọc · ${nf.format(b.chapters)} chương`;
  return `<a class="feat${at ? " hasprog" : ""}" href="${href}"
      aria-label="${esc(b.title)} — ${at ? `đọc tiếp chương ${cur}` : "bắt đầu đọc"}">
    ${cover(b, true)}
    <div class="fbody">
      <p class="hkick">${at ? "Đang đọc dở" : "Truyện mới"}</p>
      <h2>${esc(b.title)}</h2>
      ${b.author ? `<p class="fa">${esc(b.author)}</p>` : ""}
      <p class="fcur">${esc(now)}</p>
      ${b.desc ? `<p class="fd">${esc(b.desc)}</p>` : ""}
      <div class="track"><i style="width:${pct}%"></i></div>
      <p class="hrow"><span>${line}</span>
        <span class="go">${at ? "ĐỌC TIẾP ›" : "BẮT ĐẦU ›"}</span></p>
    </div></a>`;
}

function stats(books) {
  const ch = books.reduce((s, b) => s + b.chapters, 0);
  const wc = books.reduce((s, b) => s + (b.chars || 0), 0);
  const hr = Math.round(books.reduce((s, b) => s + (b.minutes || 0), 0) / 60);
  const cell = (v, k) => `<div class="stat"><b>${v}</b><span>${k}</span></div>`;
  return cell(books.length, "truyện") + cell(nf.format(ch), "chương")
    + cell(wc > 1e6 ? (wc / 1e6).toFixed(1) + " tr" : nf.format(wc), "chữ")
    + cell(nf.format(hr) + "h", "đọc");
}

const skeleton = (n) => Array.from({ length: n }, () =>
  `<div class="sk"><div class="cover"></div><div class="line"></div><div class="line s"></div></div>`).join("");

async function hints(books) {
  const out = {};
  await Promise.all(books.filter((b) => pos(b)).map(async (b) => {
    try {
      out[b.id] = await fetch(`/api/hint?book=${encodeURIComponent(b.id)}&n=${pos(b)}`)
        .then((r) => (r.ok ? r.json() : null));
    } catch { /* thieu hint thi dung so le */ }
  }));
  return out;
}

async function render() {
  const grid = $("#grid");
  grid.innerHTML = skeleton(4);
  let books = [];
  try {
    books = (await fetch("/api/books").then((r) => r.json())).books || [];
  } catch {
    grid.innerHTML = `<div class="empty"><b>Không gọi được server</b>
      Mở lại <code>python reader\\server.py</code> rồi tải trang này.</div>`;
    return;
  }
  grid.setAttribute("aria-busy", "false");
  books.sort((a, b) => (pos(b) ? 1 : 0) - (pos(a) ? 1 : 0)
    || pos(b) - pos(a) || b.updated - a.updated);

  const h = await hints(books);
  if (!books.length) {
    $("#cont").innerHTML = `<div class="empty"><b>Chưa có truyện nào</b>
      Thả các file <code>0001_*.md</code> vào một thư mục con trong <code>data\\</code>,
      rồi bấm nút quét lại ở góc trên.</div>`;
    $("#stats").innerHTML = "";
    $("#head").hidden = true;
    grid.innerHTML = "";
    return;
  }
  const head = books[0];
  $("#cont").innerHTML = feat(head, h[head.id]);
  const rest = books.slice(1);

  $("#stats").innerHTML = stats(books);
  $("#head").hidden = !rest.length;
  $("#count").textContent = rest.length ? rest.length + " mục" : "";
  $("#grid").innerHTML = rest.length
    ? rest.map((b, i) => card(b, i, h[b.id])).join("")
    : "";
}

$("#reload").onclick = async () => {
  const t = $("#reload");
  t.disabled = true;
  t.style.opacity = ".5";
  await fetch("/api/reload").catch(() => {});
  await render();
  t.disabled = false;
  t.style.opacity = "";
  const el = $("#toast");
  el.textContent = "Đã quét lại thư mục truyện";
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 1800);
};

addEventListener("scroll", () => {
  $(".shelfbar").classList.toggle("stuck", scrollY > 6);
}, { passive: true });

render();

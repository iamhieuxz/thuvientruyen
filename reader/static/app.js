const $ = (s) => document.querySelector(s);
const BOOK = (location.pathname.match(/^\/sach\/([A-Za-z0-9._-]+)/) || [])[1] || "";
const API = (p) => p + (p.includes("?") ? "&" : "?") + "book=" + encodeURIComponent(BOOK);
const curl = (n) => "/sach/" + encodeURIComponent(BOOK) + "/chuong/" + n;

const all = loadStore();
const B = all.books[BOOK] || (all.books[BOOK] = { read: [], pos: {}, last: null });
if (!B.marks) B.marks = {};

const THEMES = ["giay", "cu", "dem", "muc"];
const THEME_ALIAS = { night: "dem", ink: "muc", slate: "dem", moss: "muc" };

const S = Object.assign(
  { fs: 18, lh: 18, ls: 0, w: "mid", theme: "dem", font: "sans", just: false, indent: false,
    dim: 0, keep: true, autoNext: true, awake: false, sort: "asc", tts: "", rate: 125 },
  all.settings || {}
);
S.theme = THEME_ALIAS[S.theme] || (THEMES.includes(S.theme) ? S.theme : "dem");

/* Giọng đọc nhớ theo từng truyện: B.tts = {voice, rate, ts}. Truyện nào đã có lựa
   chọn riêng thì thắng cài đặt chung; hình dạng cũ (chuỗi "v:..." / "n:...") vẫn nhận. */
function seedVoice() {
  const t = B.tts;
  if (t && typeof t === "object") {
    if (t.voice) S.tts = t.voice;
    if (t.rate > 0) S.rate = Math.min(135, Math.max(85, t.rate));
  } else if (typeof t === "string" && t) {
    S.tts = t;
  }
}
seedVoice();

const read = new Set(B.read);
const pos = B.pos;

let book = { id: BOOK, title: "Đọc truyện" };
let meta = [];
let cur = null;
let cache = {};
let asLevel = 0;                    // tự cuộn chỉ sống trong phiên, không ghi nhớ
let openAt = 0;                     // lúc mở chương hiện tại -> tính phút đọc thật
let vposHinted = false;             // nhắc "nghe tiếp" chỉ một lần mỗi phiên trang

/* ---------------- settings ---------------- */

function apply() {
  const b = document.body;
  b.dataset.theme = S.theme;
  b.dataset.w = S.w;
  b.dataset.font = S.font;
  b.dataset.just = S.just ? "1" : "0";
  b.dataset.indent = S.indent ? "1" : "0";
  const de = document.documentElement;
  de.style.setProperty("--fs", S.fs + "px");
  de.style.setProperty("--lh", (S.lh / 10).toFixed(2));
  de.style.setProperty("--ls", S.ls / 100 + "em");
  de.style.setProperty("--veil", (S.dim / 100).toFixed(2));
  de.style.colorScheme = (S.theme === "giay" || S.theme === "cu") ? "light" : "dark";

  $("#fsVal").textContent = S.fs;
  $("#lhVal").textContent = (S.lh / 10).toFixed(1);
  $("#dimVal").textContent = S.dim + "%";
  $("#wdVal").textContent = { narrow: "Hẹp", mid: "Vừa", wide: "Rộng" }[S.w] || "Vừa";
  $("#rateVal").textContent = (S.rate / 100).toFixed(2) + "×";
  $("#fs").value = S.fs; $("#lh").value = S.lh; $("#dim").value = S.dim;
  $("#rate").value = S.rate;
  $("#just").checked = S.just; $("#indent").checked = S.indent;
  $("#keep").checked = S.keep; $("#autoNext").checked = S.autoNext; $("#awake").checked = S.awake;

  paint("#wdseg", (x) => x.dataset.w === S.w);
  paint("#themeseg", (x) => x.dataset.t === S.theme);
  paint("#fontseg", (x) => x.dataset.f === S.font);
  paint("#asseg", (x) => +x.dataset.v === asLevel);
  paint("#sortseg", (x) => x.dataset.sort === S.sort);
  $("#asVal").textContent = ["Tắt", "Chậm", "Vừa", "Nhanh"][asLevel];

  const m = document.querySelector('meta[name="theme-color"]');
  if (m) m.content = getComputedStyle(b).backgroundColor || "#16130f";
}
function paint(sel, test) {
  document.querySelectorAll(sel + " button").forEach((b) => b.classList.toggle("on", test(b)));
}
let lastJSON = "";
function save() {
  B.last = cur ? cur.n : B.last;
  B.read = [...read];
  B.pos = pos;
  all.settings = S;
  saveStore();                       // v3: tự chống ghi trùng + debounce 2s + flush
}

/* Kho v3 hydrate IDB nền xong: gộp dữ liệu chuẩn vào phiên đang chạy rồi vẽ lại.
   mergeAll chỉ thêm, không bớt -> nạp thêm vào Set read, không mất gì đang đọc. */
storeReady(() => {
  (B.read || []).forEach((n) => read.add(n));
  for (const k of Object.keys(all.settings)) if (!(k in S)) S[k] = all.settings[k];
  const st = S.tts, sr = S.rate;      // kho IDB/server gộp xong: lựa chọn riêng của truyện thắng
  seedVoice();
  if (S.tts !== st || S.rate !== sr) { apply(); fillVoices(); }
  renderList(); renderStats();
});

$("#fs").oninput = (e) => { S.fs = +e.target.value; apply(); save(); };
$("#lh").oninput = (e) => { S.lh = +e.target.value; apply(); save(); };
$("#dim").oninput = (e) => { S.dim = +e.target.value; apply(); save(); };
$("#fsMinus").onclick = () => { S.fs = Math.max(15, S.fs - 1); apply(); save(); };
$("#fsPlus").onclick = () => { S.fs = Math.min(26, S.fs + 1); apply(); save(); };
$("#wdseg").onclick = (e) => { const t = e.target.closest("button"); if (t) { S.w = t.dataset.w; apply(); save(); } };
$("#themeseg").onclick = (e) => { const t = e.target.closest("button"); if (t) { S.theme = t.dataset.t; apply(); save(); } };
$("#fontseg").onclick = (e) => { const t = e.target.closest("button"); if (t) { S.font = t.dataset.f; apply(); save(); } };
["just", "indent", "keep", "autoNext", "awake"].forEach((k) => {
  $("#" + k).onchange = (e) => {
    S[k] = e.target.checked;
    apply(); save();
    if (k === "awake") e.target.checked ? wantWake() : dropWake();
  };
});
$("#asseg").onclick = (e) => {
  const t = e.target.closest("button");
  if (!t) return;
  asLevel = +t.dataset.v;
  apply();
  if (asLevel && cur) startAuto(); else stopAuto(true);
  if (asLevel) toast("Tự cuộn " + ["", "chậm", "vừa", "nhanh"][asLevel] + " — chạm trang để dừng");
};
$("#reset").onclick = () => {
  if (!confirm("Xoá toàn bộ tiến độ đọc của truyện này?")) return;
  for (const k in pos) delete pos[k];
  read.clear();
  B.last = null;
  save(); renderList(); renderStats();
  toast("Đã xoá tiến độ đọc");
};
$("#share").onclick = async () => {
  try {
    await navigator.clipboard.writeText(location.href);
    toast("Đã sao chép liên kết chương");
  } catch {
    toast(location.href);
  }
};

/* ---------------- sao lưu tiến độ: xuất / nhập ---------------- */

/* Tải toàn bộ kho (thiết lập + tiến độ mọi truyện) ra file JSON. */
$("#exportBtn").onclick = () => {
  B.last = cur ? cur.n : B.last;
  B.read = [...read];
  B.pos = pos;
  all.settings = S;
  const payload = JSON.stringify(all, null, 2);
  const d = new Date();
  const day = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0")
    + "-" + String(d.getDate()).padStart(2, "0");
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "truyendochay-progress-" + day + ".json";
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  toast("Đã tải file tiến độ");
};

/* Gộp file xuất ra vào kho hiện có: chỉ thêm/bổ sung, không xoá gì.
   File bẩn (không đúng khung) bị từ chối, kho giữ nguyên. */
$("#importBtn").onclick = () => $("#importFile").click();

$("#importFile").onchange = (e) => {
  const file = e.target.files && e.target.files[0];
  e.target.value = "";                 // chọn lại cùng file lần sau vẫn bắn onchange
  if (!file) return;
  const fr = new FileReader();
  fr.onerror = () => toast("Không đọc được file");
  fr.onload = () => {
    let data;
    try { data = JSON.parse(fr.result); }
    catch { return toast("File không phải JSON hợp lệ"); }
    if (!data || typeof data !== "object" || Array.isArray(data)
        || !data.books || typeof data.books !== "object" || Array.isArray(data.books)) {
      return toast("File không phải bản sao lưu tiến độ");
    }
    const books = data.books;
    let touched = 0;
    for (const id of Object.keys(books)) {
      const src = books[id];
      if (!src || typeof src !== "object" || Array.isArray(src)) continue;
      const dst = all.books[id] || (all.books[id] = { read: [], pos: {}, last: null });
      /* chương đã đọc: hợp nhất hai tập */
      const readA = new Set((dst.read || []).map(Number));
      (Array.isArray(src.read) ? src.read : []).forEach((n) => readA.add(Number(n)));
      dst.read = [...readA].sort((a, b) => a - b);
      /* tỉ lệ đọc từng chương: giữ giá trị lớn hơn (đọc kỹ hơn thắng) */
      const posA = dst.pos || (dst.pos = {});
      const posB = src.pos && typeof src.pos === "object" && !Array.isArray(src.pos) ? src.pos : {};
      for (const k of Object.keys(posB)) {
        const v = Number(posB[k]);
        if (!isFinite(v) || v < 0 || v > 1) continue;
        if (!(k in posA) || v > posA[k]) posA[k] = v;
      }
      /* chương cuối: tiến xa hơn thắng */
      const lastB = Number(src.last) || 0;
      if (lastB > (+dst.last || 0)) dst.last = lastB;
      /* dấu trang: bổ sung dấu còn thiếu, không đè dấu sẵn có */
      const markA = dst.marks || (dst.marks = {});
      const markB = src.marks && typeof src.marks === "object" && !Array.isArray(src.marks) ? src.marks : {};
      for (const k of Object.keys(markB)) {
        if (!(k in markA)) markA[k] = markB[k];
      }
      touched += 1;
    }
    if (!touched) return toast("File không có tiến độ truyện nào");
    save();
    renderList();
    renderStats();
    toast("Đã nhập tiến độ của " + touched + " truyện");
  };
  fr.readAsText(file);
};

/* ---------------- chapters ---------------- */

async function loadMeta() {
  try {
    const r = await fetch(API("/api/chapters")).then((x) => x.json());
    meta = r.chapters || [];
  } catch { meta = []; }
  $("#counts").textContent = meta.length.toLocaleString("vi-VN") + " chương";
  renderList();
  renderMarks();
  renderStats();
}

async function loadBook() {
  try {
    book = await fetch(API("/api/book")).then((x) => x.json());
  } catch { /* dùng tên dự phòng */ }
  $("#crumb").textContent = book.title;
  $("#tocTitle").textContent = book.title;
  document.title = cur ? `Chương ${cur.n}: ${cur.title} · ${book.title}` : book.title;
}

function stamp(t) {
  const d = new Date(t * 1000);
  const p = (n) => String(n).padStart(2, "0");
  return `${p(d.getHours())}:${p(d.getMinutes())} ${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()}`;
}

function renderList() {
  const q = $("#search").value.trim().toLowerCase();
  const rows = meta.filter(
    (c) => !q || String(c.n).includes(q) || c.title.toLowerCase().includes(q)
      || (c.han || "").toLowerCase().includes(q) || (c.tag || "").toLowerCase().includes(q)
  );
  if (S.sort === "desc") rows.reverse();
  const ul = $("#list");
  ul.innerHTML = "";
  const frag = document.createDocumentFragment();
  for (const c of rows) {
    const li = document.createElement("li");
    if (cur && c.n === cur.n) li.className = "cur";
    if (read.has(c.n)) li.classList.add("done");
    const mark = B.marks[c.n] ? '<span class="bm" aria-label="có dấu trang">●</span>' : "";
    li.innerHTML =
      `<a href="${curl(c.n)}" data-n="${c.n}"><span class="no">${c.n}</span>` +
      `<span><span class="tt">${esc(c.title)}${mark}</span><br><span class="han">${esc(c.han || "")}</span></span>` +
      `<span class="han">${c.tag ? esc(c.tag) : read.has(c.n) ? "✓" : c.minutes + "p"}</span></a>`;
    frag.append(li);
  }
  ul.append(frag);
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

async function get(n) {
  if (cache[n]) return cache[n];
  const d = await fetch(API("/api/chapter/" + n)).then((x) => x.json());
  cache[n] = d;
  return d;
}

async function open(n, opts = {}) {
  const prevN = cur ? cur.n : 0;
  const carry = speaking || wantSpeak;   // đang nghe mà đổi chương thì đọc tiếp
  wantSpeak = false;
  stopSpeak();
  stopAuto(true);
  let d;
  try { d = await get(n); } catch { return toast("Không tải được chương — thử lại sau"); }
  if (!d) return toast("Chưa có chương này");
  const fresh = !read.has(n);
  cur = d;
  const fv = vpos();                 // điểm dừng nghe của chính chương này (nếu có)

  $("#sealNo").textContent = d.n;
  $("#ctag").hidden = !d.tag;
  $("#ctag").textContent = d.tag || "";
  $("#ctitle").textContent = d.title;
  $("#tbChap").textContent = `Chương ${d.n} · ${d.index}/${d.total}`;
  $("#meta").innerHTML =
    `<b class="mstat${fresh ? "" : " done"}" id="mStatus">${fresh ? "Đang đọc" : "Đã đọc"}</b><i aria-hidden="true">·</i>` +
    `<span>${d.chars.toLocaleString("vi-VN")} chữ</span><i aria-hidden="true">·</i>` +
    `<span>~${d.minutes} phút</span><i aria-hidden="true">·</i>` +
    `<span>${d.index}/${d.total}</span><i aria-hidden="true">·</i><b id="mPct">0%</b>`;
  $("#body").innerHTML = d.html;

  $("#prev").disabled = $("#prevBottom").disabled = !d.prev;
  $("#next").disabled = $("#nextBottom").disabled = !d.next;
  const nxt = d.next ? meta.find((c) => c.n === d.next) : null;
  $("#endNo").textContent = d.next ? `Hết chương ${d.n}` : "Hết truyện";
  $("#nextCard").disabled = !d.next;
  $("#nextTitle").textContent = d.next
    ? (nxt ? `Chương ${nxt.n}: ${nxt.title}` : `Chương ${d.next}`)
    : "Bạn đã đọc tới chương cuối";
  $("#endcard").hidden = false;

  document.title = `Chương ${d.n}: ${d.title} · ${book.title}`;
  const to = curl(d.n);
  if (location.pathname !== to) {
    history[opts.instant ? "replaceState" : "pushState"]({ n: d.n }, "", to);
  }
  renderList();
  renderStats();
  paintMark();
  document.body.classList.remove("quiet");

  const ratio = carry ? 0
    : opts.ratio !== undefined ? opts.ratio : S.keep ? (pos[d.n] || 0) : 0;
  requestAnimationFrame(() => {
    const max = document.body.scrollHeight - innerHeight;
    scrollTo({ top: max * ratio, behavior: opts.instant || carry ? "auto" : "smooth" });
    onScroll();
    paintListen();
    if (carry) speak();
    if (asLevel && !carry) startAuto();
  });
  if (d.next) get(d.next).catch(() => {});

  /* lịch sử phiên đọc (GĐ2): thời gian = phút đã ở chương trước; chương đầu không có */
  const mins = openAt ? Math.round((Date.now() / 1000 - openAt) / 60) : 0;
  openAt = Date.now() / 1000;
  if (prevN && mins >= 0) putSession({ book: BOOK, from: prevN, to: d.n, minutes: mins, ts: Date.now() / 1000 }).catch(() => {});

  /* vừa vào lại chỗ đang nghe TTS (chưa vội nghe) thì nhắc một lần */
  if (!vposHinted && fv) {
    vposHinted = true;
    setTimeout(() => toast("Nghe tiếp từ chỗ lần trước? Bấm NGHE TIẾP trên thanh."), 1200);
  }
}

function markRead() {
  if (!cur || read.has(cur.n)) return;
  read.add(cur.n); save();
  const b = $("#mStatus");
  if (b) { b.textContent = "Đã đọc"; b.classList.add("done"); }
  const li = document.querySelector("#list li.cur");
  if (li) { li.classList.add("done"); li.lastElementChild.textContent = "✓"; }
  renderStats();
}

function onScroll() {
  const max = document.body.scrollHeight - innerHeight;
  const r = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
  $("#bar").style.width = (r * 100).toFixed(1) + "%";
  const pct = $("#mPct");
  if (pct) pct.textContent = Math.round(r * 100) + "%";
  if (cur) {
    if (S.keep) pos[cur.n] = r;
    if (r > 0.985) markRead();
  }
}
let ticking = false;
addEventListener("scroll", () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    onScroll();
    ticking = false;
  });
}, { passive: true });
/* Nhịp ghi đã chuyển sang debounce 2s trong store.js (saveStore); ở đây
   chỉ giữ việc cập nhật số liệu khi bảng cài đặt đang mở. */
setInterval(() => {
  if (!cur || !$("#settings").classList.contains("open")) return;
  renderStats();
}, 1500);

const go = (d) => (d ? open(d) : toast("Hết chương"));
$("#prev").onclick = $("#prevBottom").onclick = () => go(cur && cur.prev);
$("#next").onclick = $("#nextBottom").onclick = () => go(cur && cur.next);
$("#nextCard").onclick = () => go(cur && cur.next);

/* thanh công cụ tự ẩn khi cuộn xuống, hiện lại khi cuộn lên */
let lastY = 0;
addEventListener("scroll", () => {
  const y = scrollY;
  if (!document.body.classList.contains("focus") && !document.querySelector(".sheetpanel.open")) {
    if (y > lastY + 10 && y > 150) document.body.classList.add("quiet");
    else if (y < lastY - 10 || y < 64) document.body.classList.remove("quiet");
  }
  lastY = y;
}, { passive: true });

function toggleChrome() {
  if (document.body.classList.contains("focus") || document.body.classList.contains("quiet")) {
    document.body.classList.remove("focus", "quiet");
  } else {
    document.body.classList.add("focus");
  }
}
$("#stage").addEventListener("click", (e) => {
  if (e.target.closest("a,button,input,select,label,.endcard")) return;
  if (String(window.getSelection())) return;
  toggleChrome();
});

/* vuốt ngang đổi chương */
let tx = 0, ty = 0;
addEventListener("touchstart", (e) => {
  tx = e.touches[0].clientX; ty = e.touches[0].clientY;
}, { passive: true });
addEventListener("touchend", (e) => {
  const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
  if (Math.abs(dx) > 110 && Math.abs(dy) < 45
      && !document.querySelector(".sheetpanel.open")
      && !String(window.getSelection()))
    go(cur && (dx < 0 ? cur.next : cur.prev));
}, { passive: true });

addEventListener("keydown", (e) => {
  if (e.target.matches("input,select,textarea")) return;
  if (e.key === "ArrowLeft") go(cur && cur.prev);
  else if (e.key === "ArrowRight") go(cur && cur.next);
  else if (e.key === "Escape") {
    if (document.querySelector(".sheetpanel.open")) closeAll();
    else document.body.classList.remove("focus", "quiet");
  }
  else if (e.key === "b") toggleMark();
  else if (e.key === "t") openSheet("toc");
  else if (e.key === "s") openSheet("settings");
});

/* ---------------- sheets ---------------- */

const scrim = $("#scrim");
function openSheet(id) {
  stopAuto(true);
  closeAll();
  const el = $("#" + id);
  el.classList.add("open");
  el.setAttribute("aria-hidden", "false");
  scrim.classList.add("show");
  document.body.classList.add("locked");
  document.body.classList.remove("quiet");
  document.body.classList.toggle("previewmode",
    id === "settings" && !!el.querySelector('.pane[data-pane="disp"].on'));
  if (id === "toc") {
    const li = document.querySelector("#list li.cur");
    if (li) setTimeout(() => li.scrollIntoView({ block: "center" }), 80);
  }
  el.setAttribute("tabindex", "-1");
  setTimeout(() => el.focus({ preventScroll: true }), 140);
}
function closeAll() {
  document.querySelectorAll(".sheetpanel.open").forEach((el) => {
    el.classList.remove("open");
    el.setAttribute("aria-hidden", "true");
    el.style.transform = "";
  });
  scrim.classList.remove("show");
  document.body.classList.remove("locked", "previewmode");
}
$("#tocBtn").onclick = $("#names").onclick = () => openSheet("toc");
$("#cogBtn").onclick = () => openSheet("settings");
$("#shelf").onclick = () => { save(); location.href = "/"; };
$("#home").onclick = () => { save(); location.href = "/sach/" + encodeURIComponent(BOOK); };
$("#scrim").onclick = closeAll;
document.querySelectorAll("[data-close]").forEach((b) => (b.onclick = closeAll));
$("#search").oninput = renderList;
$("#sortseg").onclick = (e) => {
  const t = e.target.closest("button"); if (!t) return;
  S.sort = t.dataset.sort;
  paint("#sortseg", (b) => b.dataset.sort === S.sort);
  renderList(); save();
};
$("#list").onclick = (e) => {
  const a = e.target.closest("a");
  if (!a) return;
  e.preventDefault();
  closeAll();
  open(+a.dataset.n || +a.getAttribute("href").split("/")[2]);
};

$("#tabs").onclick = (e) => {
  const t = e.target.closest("button[data-tab]");
  if (!t) return;
  document.querySelectorAll("#tabs button").forEach((b) => {
    const on = b === t;
    b.classList.toggle("on", on);
    b.setAttribute("aria-selected", on ? "true" : "false");
  });
  document.querySelectorAll(".pane").forEach((p) => p.classList.toggle("on", p.dataset.pane === t.dataset.tab));
  document.body.classList.toggle("previewmode", t.dataset.tab === "disp");
};

/* kéo tay nắm để đóng sheet */
document.querySelectorAll("[data-drag]").forEach((g) => {
  const panel = g.closest(".sheetpanel");
  let sy = 0, dy = 0, on = false;
  g.addEventListener("pointerdown", (e) => {
    on = true; sy = e.clientY; dy = 0;
    panel.style.transition = "none";
    try { g.setPointerCapture(e.pointerId); } catch { /* bỏ qua */ }
  });
  g.addEventListener("pointermove", (e) => {
    if (!on) return;
    dy = Math.max(0, e.clientY - sy);
    panel.style.transform = `translate(-50%,${dy}px)`;
  });
  const end = () => {
    if (!on) return;
    on = false;
    panel.style.transition = "";
    panel.style.transform = "";
    if (dy > 96) closeAll();
  };
  g.addEventListener("pointerup", end);
  g.addEventListener("pointercancel", end);
});

/* ---------------- dấu trang ---------------- */

const isMarked = () => !!(cur && B.marks[cur.n]);
function paintMark() {
  const on = isMarked();
  $("#markBtn").classList.toggle("on", on);
  $("#markBtn").setAttribute("aria-pressed", on ? "true" : "false");
  $("#markBtn").setAttribute("aria-label", on ? "Bỏ đánh dấu chương này" : "Đánh dấu chương này");
  $("#markCur").classList.toggle("on", on);
  $("#markCurLabel").textContent = on ? "Bỏ đánh dấu chương này" : "Đánh dấu chương này";
}
function toggleMark() {
  if (!cur) return;
  if (B.marks[cur.n]) {
    delete B.marks[cur.n];
    toast("Đã bỏ dấu trang");
  } else {
    B.marks[cur.n] = { t: cur.title, ts: Date.now() };
    toast(`Đã đánh dấu chương ${cur.n}`);
  }
  paintMark(); renderMarks(); renderList(); save();
}
$("#markBtn").onclick = $("#markCur").onclick = toggleMark;

function renderMarks() {
  const box = $("#marks");
  if (!box) return;
  const ns = Object.keys(B.marks).map(Number).sort((a, b) => a - b);
  $("#markCount").textContent = ns.length;
  if (!ns.length) {
    box.innerHTML = '<p class="emptyline">Chưa có dấu trang nào.</p>';
    return;
  }
  box.innerHTML = ns.map((n) => {
    const c = meta.find((x) => x.n === n);
    return `<a class="markchip" href="${curl(n)}" data-n="${n}">
      <b>${n}</b><span>${esc((c && c.title) || "Chương " + n)}</span><i data-del="${n}" role="button" aria-label="Bỏ dấu">×</i></a>`;
  }).join("");
}
$("#marks").onclick = (e) => {
  const del = e.target.closest("[data-del]");
  if (del) {
    e.preventDefault(); e.stopPropagation();
    delete B.marks[+del.dataset.del];
    save(); renderMarks(); renderList(); paintMark();
    toast("Đã bỏ dấu trang");
    return;
  }
  const a = e.target.closest("a[data-n]");
  if (a) {
    e.preventDefault();
    closeAll();
    open(+a.dataset.n);
  }
};

/* ---------------- thống kê ---------------- */

function renderStats() {
  if (!$("#stPct")) return;
  const total = meta.length || (cur && cur.total) || 1;
  const idx = cur ? cur.index : 0;
  const within = cur && pos[cur.n] !== undefined ? pos[cur.n] : 0;
  const bookPct = Math.max(0, Math.min(100, Math.round(((idx - 1 + within) / total) * 100)));
  const leftMin = meta.length
    ? meta.slice(idx).reduce((s, c) => s + (c.minutes || 0), 0) + (cur ? Math.max(0, (cur.minutes || 0) * (1 - within)) : 0)
    : 0;
  const hrs = leftMin / 60;
  $("#stPct").textContent = bookPct + "%";
  $("#stBar").style.width = bookPct + "%";
  $("#stChap").textContent = read.size.toLocaleString("vi-VN");
  $("#stLeft").textContent = !leftMin ? "—" : hrs < 1 ? "<1h" : Math.round(hrs).toLocaleString("vi-VN") + "h";
  $("#stIdx").textContent = cur ? `${idx}/${cur.total}` : "—";
}

/* ---------------- tự cuộn ---------------- */

const AUTO_PX = [0, 5, 9, 15];       // px mỗi giây
let autoRaf = 0, autoY0 = 0, autoT0 = 0;

function startAuto() {
  if (!asLevel || !cur) return;
  stopAuto(true);
  autoY0 = scrollY;
  autoT0 = performance.now();
  document.documentElement.classList.add("nosmooth");
  document.body.classList.add("autoscrolling");
  autoRaf = requestAnimationFrame(autoStep);
}
function autoStep(t) {
  const max = document.body.scrollHeight - innerHeight;
  if (max <= 0) { stopAuto(true); return; }
  const target = autoY0 + ((t - autoT0) / 1000) * AUTO_PX[asLevel];
  if (target >= max) {
    scrollTo(0, max);
    stopAuto(true);
    toast("Đã tới cuối chương");
    return;
  }
  scrollTo(0, target);               // số lẻ px bị làm tròn, nhưng đích luôn tiến
  autoRaf = requestAnimationFrame(autoStep);
}
function stopAuto(silent) {
  if (autoRaf) cancelAnimationFrame(autoRaf);
  autoRaf = 0;
  const was = document.body.classList.contains("autoscrolling");
  document.body.classList.remove("autoscrolling");
  document.documentElement.classList.remove("nosmooth");
  if (was && !silent) toast("Đã dừng tự cuộn");
}
$("#autopill").onclick = (e) => { e.stopPropagation(); stopAuto(); };
addEventListener("pointerdown", (e) => {
  if (autoRaf && !e.target.closest(".autopill")) stopAuto();
}, { passive: true });

/* ---------------- giữ sáng màn hình ---------------- */

let wake = null;
async function wantWake() {
  if (!S.awake || wake || document.visibilityState !== "visible" || !("wakeLock" in navigator)) return;
  try {
    wake = await navigator.wakeLock.request("screen");
    wake.addEventListener("release", () => { wake = null; });
  } catch { /* pin yếu / trình duyệt từ chối */ }
}
function dropWake() {
  if (wake) { wake.release().catch(() => {}); wake = null; }
}
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") {
    stopAuto(true);                    // rAF dừng khi ẩn tab, đích cũ sẽ nhảy cóc khi quay lại
    return;
  }
  if (S.awake) wantWake();
  holdLock();
  if (asLevel && !document.querySelector(".sheetpanel.open")) startAuto();
});

/* ---------------- TTS: chỉ dùng engine chạy trên máy tính ---------------- */

/* Một thẻ audio duy nhất cho cả phiên: giữ audio focus (khoá màn hình vẫn đọc, có
   nút trên lock screen) và onended → play() luôn nằm trong quyền autoplay đã cấp. */
const player = new Audio();
player.preload = "auto";
player.preservesPitch = true;
document.body.append(player);

let speaking = false, fails = 0, seq = 0, pendingNext = 0;
let vIdx = -1, wantSpeak = false;
let tState = "";                     // "b" = đang dựng audio, chưa phát
let flow = null;                     // { eng, vid, ps, my } của phiên đang đọc
let voices = { neural: [], vieneu: [] };
let vState = "loading", vTries = 0;
let vlock = null;
const warm = new Set();              // URL đã prefetch, tránh sinh trùng một đoạn hai lần

const PAD = 0.32;                    // nghỉ giữa hai đoạn, ms×1000
const rate = () => Math.min(1.35, Math.max(0.85, S.rate / 100));
/* S.tts: "n:<voice>" = edge-tts, "v:<voice>" = VieNeu-TTS */
function engine() {
  if (S.tts.startsWith("n:")) return ["edge", S.tts.slice(2)];
  if (S.tts.startsWith("v:")) return ["vieneu", S.tts.slice(2)];
  return ["", ""];
}
const ttsUrl = (eng, vid, text) =>
  "/api/tts?engine=" + encodeURIComponent(eng) + "&voice=" + encodeURIComponent(vid)
  + "&text=" + encodeURIComponent(text);

const VN_NOTE = {
  missing: "chưa cài: reader\\.venv\\Scripts\\pip install vieneu",
  loading: "đang tải/khởi tạo model…",
  error: "lỗi engine — xem reader/vieneu.log",
  off: "đã tắt bằng --no-vieneu",
  ready: "không đọc được danh sách giọng",
};

function fillVoices() {
  const sel = $("#voice");
  sel.innerHTML = "";
  const g1 = document.createElement("optgroup");
  g1.label = "VieNeu-TTS · giọng Việt";
  if (!voices.vieneu.length) g1.append(new Option("(" + (VN_NOTE[vState] || vState) + ")", "!"));
  voices.vieneu.forEach((v) => g1.append(new Option(v.name, "v:" + v.id)));
  const g2 = document.createElement("optgroup");
  g2.label = "Microsoft neural";
  if (!voices.neural.length) g2.append(new Option("(máy tính chưa kết nối được mạng)", "!"));
  voices.neural.forEach((v) =>
    g2.append(new Option(`${v.name} · ${v.gender === "Female" ? "nữ" : "nam"}`, "n:" + v.id)));
  sel.append(g1, g2);
  const has = [...sel.options].some((o) => o.value === S.tts);
  const loaded = voices.vieneu.length || voices.neural.length;
  if (!has && loaded) {
    // Giọng mặc định của server ưu tiên trước, rồi đến giọng hợp đọc truyện nhất
    const pref = voices.default && voices.vieneu.find((v) => v.id === voices.default);
    const score = (v) => (v.name.includes("đọc truyện") ? 3
      : v.name.includes("kể chuyện") ? 2 : v.name.startsWith("⭐") ? 1 : 0);
    const best = voices.vieneu.reduce((a, b) => (a && score(a) >= score(b) ? a : b), null);
    S.tts = pref ? "v:" + pref.id
      : best ? "v:" + best.id
      : voices.neural.length ? "n:" + voices.neural[0].id : "";
  }
  sel.value = S.tts;
}

async function loadVoices() {
  try {
    const d = await fetch("/api/voices").then((r) => r.json());
    voices = { neural: d.neural || [], vieneu: d.vieneu || [], default: d.default || "" };
    vState = d.vieneu_state || "error";
  } catch { voices = { neural: [], vieneu: [], default: "" }; vState = "error"; }
  fillVoices();
  if (vState === "loading" && ++vTries < 40) setTimeout(loadVoices, 5000);
}

function markPlaying(el) {
  document.querySelectorAll("#body .speaking").forEach((p) => p.classList.remove("speaking"));
  el.classList.add("speaking");
  el.scrollIntoView({ block: "center", behavior: "smooth" });
}

/* Điểm dừng gần nhất: {n: chương, i: đoạn, t: giây trong đoạn} */
const vpos = () => {
  const v = B.vpos;
  return v && cur && v.n === cur.n && (v.i > 0 || v.t > 0.5) ? v : null;
};

function paintListen() {
  $("#listen").classList.toggle("on", speaking);
  $("#listen").setAttribute("aria-pressed", speaking ? "true" : "false");
  $("#listenLabel").textContent = speaking
    ? (tState ? "DỰNG…" : "DỪNG")
    : vpos() ? "NGHE TIẾP" : "NGHE";
}

function speak() {
  const ps = [...document.querySelectorAll("#body p:not(.tail)")];
  if (!ps.length) return;
  let [eng, vid] = engine();
  if (!eng) {
    const pref = voices.default && voices.vieneu.find((v) => v.id === voices.default);
    const v = pref || voices.vieneu[0] || voices.neural[0];
    if (!v) return toast("Giọng đọc chưa sẵn sàng — chạm NGHE lại sau ít phút");
    S.tts = (voices.vieneu.includes(v) ? "v:" : "n:") + v.id;
    B.tts = { voice: S.tts, rate: S.rate, ts: (Date.now() / 1000) | 0 };
    save();
    fillVoices();
    [eng, vid] = engine();
  }
  stopSpeak();
  stopAuto(true);
  speaking = true;
  fails = 0;
  flow = { eng, vid, ps, my: ++seq };
  if (cur) B.last = cur.n;
  setSession();
  const fv = vpos();
  const from = fv && fv.i < ps.length ? fv : null;
  step(from ? from.i : 0, from ? from.t : 0);
}

const live = () => speaking && flow && flow.my === seq;

function step(i, offset = 0) {
  if (!live()) return;
  if (i >= flow.ps.length) {
    stopSpeak(true);            // nghe hết chương thì xoá dấu dừng
    if (S.autoNext && cur && cur.next) { wantSpeak = true; go(cur.next); }
    return;
  }
  vIdx = i;
  markPlaying(flow.ps[i]);
  load(i, offset);
}

function load(i, offset = 0) {
  const { eng, vid, ps } = flow;
  const url = ttsUrl(eng, vid, ps[i].textContent);
  tState = "b";
  paintListen();
  player.dataset.i = i;
  player.defaultPlaybackRate = rate();   // src mới reset playbackRate về default
  player.src = url;
  player.playbackRate = rate();
  if (offset > 0.3) {
    const seek = () => {
      try { player.currentTime = offset; } catch { /* chưa đủ dữ liệu để tìm */ }
    };
    if (player.readyState >= 1) seek();
    else player.addEventListener("loadedmetadata", seek, { once: true });
  }
  player.play().catch((e) => {
    // AbortError = src bị đổi bởi lần load sau, không phải bị chặn autoplay.
    // Không gọi stopSpeak() ở đây: nếu trình duyệt chặn tự phát (tab nền / màn hình tắt),
    // dừng phiên sẽ làm heartbeat không thể hồi sinh nữa. Giữ speaking = true để heartbeat
    // tiếp tục retry play() cho đến khi thành công.
    if (!live() || e.name === "AbortError") return;
    tState = "";
    paintListen();
  });
  // làm nóng cache server trước 2 đoạn, rẻ hơn mở thêm media element.
  // VieNeu sinh tuần tự (một LOCK), nên khử trùng: sang đoạn sau sẽ prefetch lại
  // đúng đoạn vừa bắn ở bước trước, sinh hai lần là mất 2× CPU.
  for (const j of [i + 1, i + 2]) {
    const u = ps[j] && ttsUrl(eng, vid, ps[j].textContent);
    if (!u || warm.has(u)) continue;
    warm.add(u);
    if (warm.size > 64) warm.clear();
    fetch(u).catch(() => {});
  }
}

player.onplaying = () => {
  if (tState) { tState = ""; paintListen(); }
  holdLock();
};

player.onended = () => {
  fails = 0;
  if (!live()) return;
  vIdx = -1;
  const nextIdx = +player.dataset.i + 1;
  pendingNext = seq;
  // Không đợi setTimeout: Chrome treo đồng hồ trong tab nền, đoạn sau sẽ bị chờ >1 phút.
  // Phát ngay đoạn kế tiếp; visibilitychange sẽ xử lý việc resume khi người dùng quay lại tab.
  step(nextIdx);
};

player.onerror = () => {
  if (!live()) return;
  if (++fails >= 2) {
    const eng = flow.eng;
    stopSpeak();
    toast(eng === "vieneu" ? "Engine VieNeu lỗi — xem log reader/vieneu.log" : "Máy tính đọc lỗi — kiểm tra mạng của PC");
  } else step(+player.dataset.i + 1);
};

/* Bị thông báo / cuộc gọi ngắt thì tự đọc tiếp khi hệ thống nhả audio focus.
   pause do chính stopSpeak gây ra không vào đây vì speaking đã false trước đó. */
player.onpause = () => {
  if (!live() || tState) return;
  // heartbeat giữ retry play() khi trình duyệt khóa audio (tab nền / màn hình tắt)
};

/* Màn hình điện thoại tắt hoặc tab chuyển nền: iOS Safari tắt timer và pause audio
   khi khóa màn hình. pageshow fire khi mở khóa / quay lại tab: tự resume đoạn đang
   đọc; nếu đoạn vừa hết trong khi màn hình tắt thì sang đoạn kế tiếp luôn. */
addEventListener("pageshow", () => {
  if (!live()) return;
  const ps = [...document.querySelectorAll("#body p:not(.tail)")];
  const i = +player.dataset.i + 1;
  if (player.ended && i < ps.length && S.autoNext) {
    step(i);
    return;
  }
  if (player.paused && !player.ended && player.readyState >= 1) {
    player.play().catch(() => {});
  }
});
addEventListener("visibilitychange", () => {
  if (document.hidden || !live()) return;
  if (player.paused && !player.ended && player.readyState >= 1) {
    player.play().catch(() => {});
  }
});

/* --- lock screen + giữ màn hình khi nghe --- */
function setSession() {
  if (!("mediaSession" in navigator)) return;
  navigator.mediaSession.metadata = new MediaMetadata({
    title: cur ? "Chương " + cur.n + ": " + cur.title : book.title,
    artist: book.title,
    album: "Đọc truyện",
  });
  const act = (a, fn) => { try { navigator.mediaSession.setActionHandler(a, fn); } catch { /* bỏ qua */ } };
  act("play", () => (speaking ? player.play().catch(() => {}) : speak()));
  act("pause", () => stopSpeak());
  act("nexttrack", () => go(cur && cur.next));
  act("previoustrack", () => go(cur && cur.prev));
}

async function holdLock() {
  if (!("wakeLock" in navigator) || !speaking || vlock) return;
  try {
    vlock = await navigator.wakeLock.request("screen");
    vlock.addEventListener("release", () => { vlock = null; });
  } catch { /* pin yếu / trình duyệt tự chối */ }
}
function dropLock() {
  if (vlock) { vlock.release().catch(() => {}); vlock = null; }
}

/* Người dùng đóng tab lúc đang nghe thì vẫn còn điểm dừng để mở lại */
addEventListener("pagehide", () => { markPos(); if (cur) { B.last = cur.n; save(); flushStore(); } });

function markPos() {
  if (speaking && vIdx >= 0 && cur)
    B.vpos = { n: cur.n, i: vIdx, t: +(player.currentTime || 0).toFixed(2), ts: Date.now() / 1000 };
}

function stopSpeak(forget) {
  if (forget) B.vpos = null;
  else markPos();
  seq++;
  speaking = false;
  flow = null;
  vIdx = -1;
  tState = "";
  warm.clear();                      // đổi giọng / mở chương khác thì làm nóng lại từ đầu
  player.pause();
  player.removeAttribute("src");
  dropLock();
  document.querySelectorAll("#body .speaking").forEach((p) => p.classList.remove("speaking"));
  paintListen();
  save();
}
$("#listen").onclick = () => (speaking ? stopSpeak() : speak());

$("#voice").onchange = (e) => {
  S.tts = e.target.value;
  if (S.tts) B.tts = { voice: S.tts, rate: S.rate, ts: (Date.now() / 1000) | 0 };
  save();
};
$("#rate").oninput = (e) => {
  S.rate = +e.target.value;
  player.playbackRate = rate();
  apply();
  if (B.tts && typeof B.tts === "object") { B.tts.rate = S.rate; B.tts.ts = (Date.now() / 1000) | 0; }
  else if (S.tts) B.tts = { voice: S.tts, rate: S.rate, ts: (Date.now() / 1000) | 0 };
  save();
};
$("#preview").onclick = () => {
  stopSpeak();
  const [eng, vid] = engine();
  if (!eng) return toast("Chọn giọng đọc trước đã");
  const a = new Audio(ttsUrl(eng, vid, "Đây là giọng đọc thử, tôi kể chuyện cho bạn nghe mỗi tối."));
  a.preservesPitch = true;
  a.playbackRate = rate();
  if (eng === "vieneu") {
    toast("VieNeu đang dựng giọng đọc…");
    a.onplaying = () => toast("Đã có giọng đọc");
  }
  a.onerror = () => toast(eng === "vieneu" ? "VieNeu lỗi — xem reader/vieneu.log" : "Máy tính đọc lỗi — kiểm tra mạng của PC");
  a.play().catch(() => toast("Trình duyệt chặn tự phát — chạm lại lần nữa"));
};

/* ---------------- toast + start ---------------- */

let tid;
function toast(msg) {
  let t = $(".toast");
  if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.setAttribute("aria-live", "polite"); document.body.append(t); }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(tid);
  tid = setTimeout(() => t.classList.remove("show"), 2400);
}

const routeN = () => +(location.pathname.match(/\/chuong\/(\d+)/) || [])[1];

apply();
fillVoices();
loadVoices();
if (!BOOK) {
  location.replace("/");
} else {
  loadBook();
  loadMeta().then(() => {
    open(routeN() || B.last || (meta[0] && meta[0].n), { instant: true });
    if (!S.seen) {
      S.seen = 1; save();
      setTimeout(() => toast("Chạm giữa trang để ẩn thanh công cụ"), 1400);
    }
    if (S.awake) wantWake();
  });
}
addEventListener("popstate", () => {
  const n = routeN();
  if (n && n !== (cur && cur.n)) open(n, { instant: true });
});
addEventListener("beforeunload", () => { markPos(); if (cur) { B.last = cur.n; save(); } });

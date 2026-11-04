/* ============================================================
   store.js v3 — kho tiến độ đọc dùng chung
   Kho chính: IndexedDB "baogiam-reader" (store "books" + "sessions").
   localStorage "baogiam.reader.v3hot" chỉ là bản nóng để vẽ khung
   trang ngay lập tức; IDB luôn được đối chiếu sau khi mở.
   Nếu IDB bị chặn (ẩn danh, iOS khóa, dung lượng) thì rơi về localStorage.
   Key cũ "baogiam.reader.v2" chỉ đọc khi migration; không bao giờ xoá
   cho tới khi bản sao an toàn trong IDB ghi thành công.
   TOÀN BỘ file bọc trong IIFE: các trang khác cũng khai báo `const all`
   trên scope toàn cục — nếu store.js để `let all` ngoài này thì script
   sau văng "Identifier 'all' has already been declared" và CHẾT CẢ TRANG.
   Chỉ 6 hàm API cuối file được lộ ra window.
   ============================================================ */

(() => {

const LS = "baogiam.reader.v3hot";           // bản nóng: kho đầy đủ dạng JSON
const LS_V2 = "baogiam.reader.v2";           // kho cũ, chỉ đọc
const LS_V1 = "baogiam.reader.v1";           // kho cũ hơn, chỉ đọc
const DB_NAME = "baogiam-reader";
const DB_STORES = { BOOKS: "books", SESSIONS: "sessions" };
const SESSIONS_KEEP = 500;                   // giữ tối đa ~500 bản ghi phiên

/* trạng thái module: đọc trang khi load(), ghi qua scheduleSave()/persistNow() */
let all = null;              // {settings, books} đang dùng — khởi tạo từ hot ngay
let idb = null;              // IDBDatabase đã mở
let idbFailed = false;       // IDB không dùng được -> chỉ localStorage
let savedJSON = "";          // chống ghi trùng
let flushTimer = 0;          // debounce 2s
let ready = false;           // đã hydrate IDB + migration xong
let readyCallbacks = [];     // trang chờ dữ liệu chuẩn để vẽ lại
/* GĐ3 sync server: pull khi mở trang, push sau mỗi lần ghi (debounce, backoff) */
let srvMtime = 0;            // mtime (giây) kho server lần cuối thấy
let syncTimer = 0;           // debounce push 4s
let syncBackoff = 0;         // ms chờ lại sau lỗi (tối đa 60s)

function storeMode() {
  return idb ? "idb" : "localStorage";
}

/* đăng hook vẽ lại sau khi kho đã hydrate IDB (chạy ngay nếu đã sẵn sàng).
   Callbacks KHÔNG bị xoá sau khi fire: pull server (GĐ3) fire lại để trang
   vẽ lại với dữ liệu từ server — callback phải vẽ lại được (idempotent). */
function storeReady(fn) {
  readyCallbacks.push(fn);
  if (ready) fn(all);
}
function fireReady() {
  ready = true;
  readyCallbacks.forEach((fn) => { try { fn(all); } catch { /* trang tự chịu lỗi vẽ */ } });
}

/* ---------- đọc localStorage an toàn ---------- */
function lsGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function lsSet(key, val) {
  try { localStorage.setItem(key, val); } catch { /* ẩn danh / hết quota */ }
}

/* ---------- chuẩn hóa một bản ghi truyện ---------- */
function normBook(b) {
  if (!b || typeof b !== "object") return { read: [], pos: {}, marks: {}, last: null, vpos: null };
  return {
    read: Array.isArray(b.read) ? b.read.map(Number).filter(Number.isFinite) : [],
    pos: b.pos && typeof b.pos === "object" && !Array.isArray(b.pos)
      ? Object.fromEntries(Object.entries(b.pos).map(([k, v]) => [String(k), Number(v) || 0])) : {},
    marks: b.marks && typeof b.marks === "object" && !Array.isArray(b.marks)
      ? Object.fromEntries(Object.entries(b.marks).filter(([, v]) => v && typeof v === "object")) : {},
    last: b.last == null ? null : (Number(b.last) || null),
    vpos: b.vpos && typeof b.vpos === "object" ? b.vpos : null,
    ...(b.tts && typeof b.tts === "object" ? { tts: b.tts } : {}),
  };
}

function normalizeAll(a) {
  const out = { settings: (a && typeof a === "object" && a.settings && typeof a.settings === "object") ? { ...a.settings } : {}, books: {} };
  if (a && typeof a === "object" && a.books && typeof a.books === "object" && !Array.isArray(a.books)) {
    for (const id of Object.keys(a.books)) out.books[id] = normBook(a.books[id]);
  }
  return out;
}

/* ---------- merge hai kho: không xoá gì, phần "mạnh hơn" thắng ----------
   Ghi vào dst tại chỗ (giữ nguyên tham chiếu) để các trang đang nắm
   B / B.read / B.pos không bị lệch dữ liệu sau khi hydrate. */
function mergeAll(dst, src) {
  for (const id of Object.keys(src.books)) {
    const s = normBook(src.books[id]);
    const d = dst.books[id] || (dst.books[id] = normBook(null));
    const readA = new Set(d.read);
    s.read.forEach((n) => readA.add(n));
    const sorted = [...readA].sort((a, b) => a - b);
    d.read.length = 0;
    for (const n of sorted) d.read.push(n);
    for (const k of Object.keys(s.pos)) {
      if (!(k in d.pos) || s.pos[k] > d.pos[k]) d.pos[k] = s.pos[k];
    }
    for (const k of Object.keys(s.marks)) {
      if (!(k in d.marks)) d.marks[k] = s.marks[k];
    }
    if ((s.last || 0) > (d.last || 0)) d.last = s.last;
    if (!d.vpos && s.vpos) d.vpos = s.vpos;
    /* Giọng đọc theo truyện: ai mới hơn (theo ts) thì thắng — không để bản cũ trên
       server đè lựa chọn mới trên máy khác. Chuỗi cũ không có ts chỉ bổ sung khi thiếu. */
    if (s.tts && typeof s.tts === "object") {
      const dts = (d.tts && typeof d.tts === "object") ? (d.tts.ts || 0) : 0;
      if (!d.tts || (s.tts.ts || 0) >= dts) d.tts = s.tts;
    } else if (!d.tts && s.tts) d.tts = s.tts;
  }
  for (const k of Object.keys(src.settings)) {
    if (!(k in dst.settings)) dst.settings[k] = src.settings[k];
  }
  return dst;
}

/* ---------- mở IDB; thất bại -> idbFailed ---------- */
function openIDB() {
  return new Promise((resolve) => {
    let req;
    try {
      req = indexedDB.open(DB_NAME, 1);
    } catch {
      idbFailed = true;
      return resolve(null);
    }
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(DB_STORES.BOOKS)) db.createObjectStore(DB_STORES.BOOKS);
      if (!db.objectStoreNames.contains(DB_STORES.SESSIONS)) db.createObjectStore(DB_STORES.SESSIONS, { autoIncrement: true });
    };
    req.onsuccess = () => {
      idb = req.result;
      idb.onversionchange = () => { try { idb.close(); } catch {} idb = null; };
      resolve(idb);
    };
    req.onerror = req.onblocked = () => { idbFailed = true; resolve(null); };
  });
}

function tx(store, mode) {
  return idb.transaction(store, mode).objectStore(store);
}

/* đọc 1 key từ IDB -> Promise(giá trị | undefined) */
function idbGet(store, key) {
  return new Promise((resolve) => {
    try {
      const r = tx(store, "readonly").get(key);
      r.onsuccess = () => resolve(r.result);
      r.onerror = () => resolve(undefined);
    } catch { resolve(undefined); }
  });
}

/* đọc toàn bộ store books (bỏ khoá "__settings") -> Promise(object) */
function idbGetAllBooks() {
  return new Promise((resolve) => {
    if (!idb) return resolve(null);
    try {
      const out = {};
      const r = tx(DB_STORES.BOOKS, "readonly").openCursor();
      r.onsuccess = () => {
        const c = r.result;
        if (!c) return resolve(out);
        if (c.key !== "__settings") out[c.key] = normBook(c.value);
        c.continue();
      };
      r.onerror = () => resolve(null);
    } catch { resolve(null); }
  });
}

/* ghi toàn bộ kho (books + settings) vào IDB; resolve(true) chỉ khi thành công */
function idbPutAllBooks(books, settings) {
  return new Promise((resolve) => {
    if (!idb) return resolve(false);
    try {
      const t = idb.transaction(DB_STORES.BOOKS, "readwrite");
      const st = t.objectStore(DB_STORES.BOOKS);
      let pending = 0, bad = false;
      t.onabort = t.onerror = () => { bad = true; };
      for (const id of Object.keys(books)) {
        pending += 1;
        st.put(books[id], id);
      }
      pending += 1;
      st.put(settings || {}, "__settings");
      t.oncomplete = () => resolve(!bad);
      if (!pending) return resolve(true);
    } catch { resolve(false); }
  });
}

/* thêm 1 bản ghi phiên; giữ tối đa SESSIONS_KEEP bản (xoá phần cũ nhất) */
function idbAddSession(rec) {
  return new Promise((resolve) => {
    if (!idb) return resolve(false);
    try {
      const t = idb.transaction(DB_STORES.SESSIONS, "readwrite");
      const st = t.objectStore(DB_STORES.SESSIONS);
      const countReq = st.count();
      countReq.onsuccess = () => {
        if (countReq.result >= SESSIONS_KEEP) {
          const n = countReq.result - SESSIONS_KEEP + 1;
          const c = st.openCursor();
          let done = 0;
          c.onsuccess = () => {
            const cur = c.result;
            if (!cur || done >= n) return;
            cur.delete();
            done += 1;
            cur.continue();
            /* continue sau delete: cursor nhảy tới bản kế, giữ thứ tự key cũ nhất trước */
          };
        }
        st.add(rec);
      };
      t.oncomplete = () => resolve(true);
      t.onerror = t.onabort = () => resolve(false);
    } catch { resolve(false); }
  });
}

/* đọc các phiên gần đây (mới nhất cuối) -> Promise(array) */
function idbGetSessions() {
  return new Promise((resolve) => {
    if (!idb) return resolve([]);
    try {
      const out = [];
      const r = tx(DB_STORES.SESSIONS, "readonly").openCursor();
      r.onsuccess = () => {
        const c = r.result;
        if (!c) return resolve(out);
        out.push(c.value);
        c.continue();
      };
      r.onerror = () => resolve(out);
    } catch { resolve([]); }
  });
}

/* ---------- migration từ v2/v1 ---------- */
function readV2() {
  let raw = null;
  try { raw = JSON.parse(lsGet(LS_V2) || "null"); } catch { raw = null; }
  if (raw && raw.books) return raw;
  let v1 = null;
  try { v1 = JSON.parse(lsGet(LS_V1) || "null"); } catch { v1 = null; }
  if (!v1) return null;
  /* v1 chỉ có một truyện: gán mọi truyện chưa biết theo id từ URL nếu có,
     còn không thì đặt theo id chung "baojian_vi" như lịch sử dự án */
  const id = (location.pathname.match(/^\/sach\/([A-Za-z0-9._-]+)/) || [])[1] || "baojian_vi";
  return { settings: v1.settings || {}, books: { [id]: { read: v1.read || [], pos: v1.pos || {}, last: v1.last || null } } };
}

/* ---------- GĐ3: đồng bộ kho qua server (merge-only, không xoá gì) ----------
   Pull (một lần sau hydrate): GET /api/progress -> gộp kho server vào all
   (chỉ dữ liệu thiết bị này chưa có), cập nhật srvMtime; KHÔNG push lại.
   Push: POST /api/progress với all hiện tại; server gộp rồi trả kho chung +
   mtime — client chỉ cập nhật srvMtime, KHÔNG ghi đè all (tránh xoá dữ liệu
   cục bộ; thiết bị kia tự thấy ở lần pull sau khi mở trang).
   Lỗi mạng/server cũ (404): im lặng, backoff nhân đôi tối đa 60s, thử lại. */
let pulled = false;                  // đã pull một lần trong phiên trang
function pushSyncNow() {
  if (!all) return;
  fetch("/api/progress", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(all),
    keepalive: true,                 // sống cả khi đang rời trang
  }).then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then((d) => {
      if (typeof d.mtime === "number") srvMtime = d.mtime;
      syncBackoff = 0;
    })
    .catch(() => {
      syncBackoff = Math.min(syncBackoff ? syncBackoff * 2 : 2000, 60000);
      setTimeout(pushSyncNow, syncBackoff);
    });
}
function pushSyncDebounced() {
  if (syncTimer) clearTimeout(syncTimer);
  syncTimer = setTimeout(() => { syncTimer = 0; pushSyncNow(); }, 4000);
}
function syncPull() {
  if (pulled) return;
  pulled = true;
  fetch("/api/progress", { cache: "no-store" }).then((r) => (r.ok ? r.json() : null))
    .then((d) => {
      if (!d || typeof d.mtime !== "number") return;
      srvMtime = d.mtime;
      const srv = d.store && d.store.books ? d.store : null;
      if (!srv || !Object.keys(srv.books).length) return;
      mergeAll(all, srv);               // không xoá gì: phần mạnh hơn thắng
      persistNow("none");               // chốt bản nóng + IDB, không phản push
      fireReady();                      // trang vẽ lại với dữ liệu từ server
    })
    .catch(() => {});                   // server cũ / offline: bỏ qua
}

/* ---------- đọc kho để vẽ trang (đồng bộ) + hydrate IDB nền ---------- */
function loadStore() {
  if (all) return all;         // trang thứ hai gọi lại trong cùng phiên: trả ngay
  /* 1) bản nóng localStorage vẽ khung ngay — đồng bộ */
  let hot = null;
  try { hot = JSON.parse(lsGet(LS) || "null"); } catch { hot = null; }
  all = normalizeAll(hot);
  savedJSON = JSON.stringify(all);
  /* 2) IDB + migration gộp vào all tại chỗ, xong thì báo các trang vẽ lại */
  hydrate();
  return all;
}

async function hydrate() {
  if (ready) return;
  /* IDB là nguồn chuẩn: đọc và merge vào all (đỏm nào đầy đủ hơn thì thắng) */
  if (!idbFailed && !idb) await openIDB();
  if (idb) {
    const books = await idbGetAllBooks();
    const idbSettings = await idbGet(DB_STORES.BOOKS, "__settings");
    if (idbSettings && typeof idbSettings === "object") {
      for (const k of Object.keys(idbSettings)) {
        if (!(k in all.settings)) all.settings[k] = idbSettings[k];
      }
    }
    if (books && Object.keys(books).length) mergeAll(all, { settings: {}, books });
  }
  /* migration một lần: v2 (và v1) gộp vào kho hiện tại */
  const old = readV2();
  if (old && Object.keys(old.books).length) {
    mergeAll(all, old);
    await persistNow("none");          // chốt migration: hot + IDB (khi idb sẵn sàng)
  }
  lsSet(LS, JSON.stringify(all));
  fireReady();
  syncPull();                          // GĐ3: lấy kho server gộp vào (nếu chạy được)
}

/* ---------- flush xuống đĩa ----------
   Lưu ý đặt tên: hàm ghi thật phải là persistNow() — nếu giữ tên saveStore()
   thì lời gán `window.saveStore = scheduleSave` cuối file đè binding toàn cục
   của function declaration, khiến mọi lời gọi nội bộ (hydrate, timer debounce,
   flushSave) chỉ lên lịch debounce chứ không bao giờ ghi xuống đĩa. */
let idbRetry = false;              // có đợt ghi IDB lỗi -> thử lại lần sau
async function persistNow(push = "debounce") {
  if (!all) return;
  const s = JSON.stringify(all);
  if (s === savedJSON && !idbRetry) return;
  savedJSON = s;
  lsSet(LS, s);                    // luôn ghi bản nóng trước (rẻ, đồng bộ)
  if (idbFailed || !idb) { idbRetry = false; }
  else {
    const ok = await idbPutAllBooks(all.books, all.settings);
    idbRetry = !ok;                // IDB lỗi -> lần gọi sau vẫn cố ghi lại
  }
  /* GĐ3: đẩy lên server sau khi xuống đĩa cục bộ ("none" = pull chốt lại) */
  if (push === "debounce") pushSyncDebounced();
  else if (push === "now") pushSyncNow();
}

/* ---------- nhịp ghi debounce 2s + flush khi rời trang ---------- */
function scheduleSave() {
  if (flushTimer) return;
  flushTimer = setTimeout(() => {
    flushTimer = 0;
    persistNow();
  }, 2000);
}
function flushSave() {
  if (flushTimer) { clearTimeout(flushTimer); flushTimer = 0; }
  if (syncTimer) { clearTimeout(syncTimer); syncTimer = 0; }
  persistNow("now");               // rời trang: ghi + push ngay, không chờ
}
document.addEventListener("visibilitychange", () => { if (document.hidden) flushSave(); });
addEventListener("pagehide", () => flushSave());

/* ---------- API dùng chung cho các trang ----------
   - loadStore(): đồng bộ -> {settings, books} (bản nóng); IDB hydrate nền,
     đăng storeReady(fn) để vẽ lại khi dữ liệu chuẩn tới
   - scheduleSave(): gọi sau khi đổi all; tự debounce 2s
   - flushStore(): flush ngay (persistNow) — gọi khi cần chắc chắn đã xuống đĩa
   - putSession(rec): ghi lịch sử phiên đọc (GĐ2)
   - getSessions(): đọc lịch sử phiên
   ----------------------------------------------- */
window.loadStore = loadStore;
window.storeReady = storeReady;
window.saveStore = scheduleSave;   // các trang gọi như hàm cũ, không chặn
window.flushStore = flushSave;     // gọi khi cần chắc chắn đã xuống đĩa
window.putSession = putSession;
window.getSessions = getSessions;

async function putSession(rec) {
  flushSave();                     // chắc kho mới nhất đã xuống đĩa trước khi ghi phiên
  if (!idbFailed && !idb) await openIDB();
  return idbAddSession({ book: String(rec.book || ""), from: Number(rec.from) || 0,
                         to: Number(rec.to) || 0, minutes: Number(rec.minutes) || 0,
                         ts: Number(rec.ts) || Date.now() / 1000 });
}
async function getSessions() {
  if (!idbFailed && !idb) await openIDB();
  if (!idb) return [];             // fallback LS không có lịch sử phiên
  return idbGetSessions();
}

})();  // hết IIFE store.js — mọi biến nội bộ (all, tx, LS…) sống trong closure

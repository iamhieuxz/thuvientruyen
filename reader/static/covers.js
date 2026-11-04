/* ============================================================
   covers.js — bìa dùng chung cho trang chủ và trang truyện.
   Thứ tự ưu tiên: ảnh bìa riêng trong /static/img → cover.jpg trong
   thư mục truyện → bìa chữ sinh từ tên (không bịa ảnh).
   ============================================================ */

const COVER_ART = {
  nien_dai_58_vi: "/static/img/cover-nien.jpg",
  nhi_huu_thien_nhan_vi: "/static/img/cover-thien.jpg",
  can_bao_chan_long_vi: "/static/img/cover-chan.jpg",
  baojian_vi: "/static/img/cover-bao.jpg",
  khai_cuc_dinh_chuc_vi: "/static/img/cover-kcdc.jpg",
  quan_dao_chi_dien_vi: "/static/img/cover-qdcd.jpg",
  cao_nhi_phan_khoa_vi: "/static/img/cover-phankhoa.jpg",
};

const COVER_PAL = [
  ["#432a7a", "#170f28"], ["#14504a", "#08191c"], ["#26315f", "#0d1020"],
  ["#6a2440", "#1a0a11"], ["#23512f", "#0b1710"], ["#2a4a6b", "#0c141d"],
];

const escHTML = (s) => String(s == null ? "" : s).replace(/[&<>"']/g,
  (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const coverHue = (s) => {
  let h = 0;
  for (const c of String(s)) h = (h * 31 + c.charCodeAt(0)) % 360;
  return h;
};

const coverGrad = (id) => {
  const [c1, c2] = COVER_PAL[coverHue(id) % COVER_PAL.length];
  return `background:radial-gradient(130% 78% at 16% 0%, rgba(255,255,255,.14), transparent 56%),`
    + `linear-gradient(158deg,${c1},${c2})`;
};

const coverSrc = (b) => COVER_ART[b.id]
  || (b.cover ? "/api/cover?book=" + encodeURIComponent(b.id) : "");

function coverHTML(b, cls) {
  const src = coverSrc(b);
  const alt = "Bìa " + (b.title || "");
  if (src) {
    return `<img class="${cls}" src="${src}" alt="${escHTML(alt)}" loading="lazy" decoding="async">`;
  }
  return `<div class="${cls} cov-gen" style="${coverGrad(b.id)}" role="img"
    aria-label="${escHTML(alt)}"><span class="cg-top">Bản dịch</span>
    <span class="cg-title">${escHTML(b.title || "")}</span>
    <span class="cg-foot">${escHTML(b.author || "truyendochay")}</span></div>`;
}

/* tách chuỗi thể loại "Quan trường, Trọng sinh" thành mảng */
const splitGenres = (b) => String((b && b.genre) || "")
  .split(/[,;]/).map((s) => s.trim()).filter(Boolean);

/* phần trăm đã dịch: 0% thật khác "dưới 1%" do làm tròn */
const pctShow = (pct, total) => (total > 0 && (+pct || 0) === 0 ? "<1" : String(+pct || 0));

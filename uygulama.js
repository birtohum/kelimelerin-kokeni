"use strict";
const $ = (id) => document.getElementById(id);
const DIL = {
  turk: "Türkçe", arap: "Arapça", fars: "Farsça", fransiz: "Fransızca", italyan: "İtalyanca", yunan: "Yunanca",
  ingiliz: "İngilizce", latin: "Latince", alman: "Almanca", slav: "Slav dilleri", mogol: "Moğolca", diger: "diğer", yok: "bilinmiyor",
};
const DILDEN = { turk: "Türkçe", arap: "Arapçadan", fars: "Farsçadan", fransiz: "Fransızcadan", italyan: "İtalyancadan", yunan: "Yunancadan", ingiliz: "İngilizceden", latin: "Latinceden", alman: "Almancadan", slav: "Slav dillerinden", mogol: "Moğolcadan", diger: "başka dillerden" };
// Telifi düşmüş metinler (Mehmet Âkif Ersoy ö. 1936; Mustafa Kemal Atatürk ö. 1938) ve kendi yazdığım bir örnek.
const ORNEK = [
  ["İstiklal Marşı", "Korkma, sönmez bu şafaklarda yüzen al sancak; sönmeden yurdumun üstünde tüten en son ocak. O benim milletimin yıldızıdır, parlayacak; o benimdir, o benim milletimindir ancak."],
  ["Gençliğe Hitabe", "Ey Türk gençliği! Birinci vazifen, Türk istiklalini, Türk cumhuriyetini, ilelebet muhafaza ve müdafaa etmektir. Mevcudiyetinin ve istikbalinin yegâne temeli budur. Bu temel, senin en kıymetli hazinendir."],
  ["Gündelik", "Sabah kahvaltıda peynir, zeytin ve domates yedim, sonra otobüse binip ofise gittim. Öğlen lokantada çorba içtik, akşam da televizyonda maç izledik."],
  ["Teknoloji", "Telefonuma yeni bir uygulama indirdim; şifre ekranı açılınca internet bağlantısı koptu ve bilgisayardan dosyayı tekrar göndermek zorunda kaldım."],
];
let S;

const kucuk = (w) => w.replace(/I/g, "ı").replace(/İ/g, "i").toLocaleLowerCase("tr");
const YUMUSAK = { b: "p", c: "ç", d: "t", ğ: "k", g: "k" };

function bul(w) {
  if (S[w]) return [S[w], w];
  const asgari = w.length <= 4 ? 2 : 3;
  for (let i = w.length - 1; i >= asgari; i--) {
    const p = w.slice(0, i);
    if (S[p]) return [S[p], p];
    const son = p.slice(-1);
    if (YUMUSAK[son]) { const q = p.slice(0, -1) + YUMUSAK[son]; if (S[q]) return [S[q], q]; }
    if (son === "ğ" && S[p.slice(0, -1) + "g"]) return [S[p.slice(0, -1) + "g"], p.slice(0, -1) + "g"];
  }
  return ["yok", null];
}

function boya() {
  const metin = $("metin").value;
  const say = {}; let toplam = 0;
  const parca = metin.split(/([A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]+(?:['’][A-Za-zçğıöşüâîû]+)?)/);
  const html = parca.map((p, i) => {
    if (i % 2 === 0) return p.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]).replace(/\n/g, "<br>");
    const [ana] = p.split(/['’]/);
    const w = kucuk(ana).replace(/â/g, "a").replace(/î/g, "i").replace(/û/g, "u");
    const [k, kok] = bul(w);
    say[k] = (say[k] || 0) + 1; toplam++;
    const baslik = k === "yok" ? "kökeni bulunamadı" : `${DIL[k]}${kok && kok !== w ? ` (kök: ${kok})` : ""}`;
    return `<span class="k${k === "yok" ? " bilinmiyor" : ""}" style="border-color:var(--${k})" title="${baslik}">${p}</span>`;
  }).join("");
  $("boyali").innerHTML = html;
  const sira = Object.entries(say).sort((a, b) => (a[0] === "yok") - (b[0] === "yok") || b[1] - a[1]);
  $("cubuk").innerHTML = sira.map(([k, n]) => `<i style="width:${(100 * n) / toplam}%;background:var(--${k})" title="${DIL[k]}: ${n}"></i>`).join("");
  $("lejant").innerHTML = sira.map(([k, n]) => `<span><i style="background:var(--${k})"></i>${DIL[k]} <b>%${Math.round((100 * n) / toplam)}</b></span>`).join("");
  const bilinen = toplam - (say.yok || 0);
  if (!toplam) { $("ozet").textContent = ""; return; }
  const yabanci = sira.filter(([k]) => k !== "yok" && k !== "turk");
  const turk = say.turk || 0;
  let c = `${toplam} kelimenin ${bilinen} tanesinin kökeni bulundu. `;
  if (bilinen) {
    c += `Bunların <b>%${Math.round((100 * turk) / bilinen)}</b>'i Türkçe kökenli`;
    if (yabanci.length) c += `; en çok ${DILDEN[yabanci[0][0]]} gelen var (${yabanci[0][1]} kelime)`;
    c += ".";
  }
  $("ozet").innerHTML = c.replace("%" + Math.round((100 * turk) / bilinen) + "</b>'i", "%" + Math.round((100 * turk) / bilinen) + "</b>'" + yuzdeEk(Math.round((100 * turk) / bilinen)));
}
function yuzdeEk(n) {
  const B = ["ı", "i", "si", "ü", "ü", "i", "sı", "si", "i", "u"], O = ["ü", "u", "si", "u", "ı", "si", "ı", "i", "i", "ı"];
  if (n === 100) return "ü";
  if (n === 0) return "ı";
  return n % 10 ? B[n % 10] : O[n / 10];
}

async function baslat() {
  S = await (await fetch("veri/kokenler.json")).json();
  const R = {arap: "#4ade80", fars: "#c084fc", fransiz: "#60a5fa", italyan: "#f97316", yunan: "#22d3ee", ingiliz: "#f472b6", turk: "#f87171", latin: "#facc15", mogol: "#a3e635"};
  $("kelHero").innerHTML = ["kitap", "pencere", "otobüs", "çorba", "lokanta", "kahve", "bardak", "gözlük"].filter((w) => S[w] && DIL[S[w]])
    .map((w) => `<span style="color:${R[S[w]] || "#ddd"}">${w}<small>${DIL[S[w]]}</small></span>`).join("");
  ORNEK.forEach(([ad, m], i) => {
    const b = document.createElement("button"); b.textContent = ad; b.type = "button";
    b.onclick = () => { $("metin").value = m; [...$("ornekler").children].forEach((x) => x.classList.toggle("secili", x === b)); boya(); };
    $("ornekler").appendChild(b);
    if (i === 0) b.classList.add("secili");
  });
  $("metin").value = ORNEK[0][1];
  let t; $("metin").addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { [...$("ornekler").children].forEach((x) => x.classList.remove("secili")); boya(); }, 150); });
  boya();
}
baslat();

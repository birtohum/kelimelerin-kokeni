"""kaikki.org Türkçe Vikisözlük dökümü → veri/kokenler.json  {kelime: köken kodu}

Köken zinciri (inh/bor/der/ety…) sırayla okunur; Osmanlıca (ota) ve Türkçe (tr) ara halka sayılıp atlanır,
ilk "gerçek" kaynak dil sınıfa çevrilir. Zincir yalnız Türk dillerinden oluşuyorsa "turk".
"""
import json, re, collections
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ARA = {"tr", "ota"}
TURK = {"trk-pro", "otk", "xqa", "chg", "trk-oat", "trk-pro-old", "ota-old", "trk-cmn", "trk-sou", "trk-ogz-pro", "otk-old", "trk-oog", "oui", "kmz", "az", "tk", "gag", "crh", "kk", "ky", "uz", "ug", "tt", "ba", "cv", "sah", "alt", "tyv", "kjh", "trk"}
SINIF = {
    "ar": "arap", "arc": "diger", "he": "diger",
    "fa": "fars", "fa-cls": "fars", "pal": "fars", "peo": "fars", "ira-pro": "fars", "ira-mid": "fars", "xme": "fars", "ae": "fars", "sog": "fars", "ku": "diger",
    "fr": "fransiz", "frm": "fransiz", "fro": "fransiz",
    "it": "italyan", "vec": "italyan", "lij": "italyan", "roa-oit": "italyan",
    "el": "yunan", "grc": "yunan", "gkm": "yunan", "grc-koi": "yunan", "grc-byz": "yunan",
    "en": "ingiliz", "de": "alman", "gmh": "alman", "la": "latin", "la-med": "latin", "la-new": "latin", "ML.": "latin", "LL.": "latin",
    "es": "diger", "pt": "diger", "ru": "slav", "bg": "slav", "sh": "slav", "pl": "slav", "sla-pro": "slav", "cu": "slav",
    "hy": "diger", "xcl": "diger", "ka": "diger", "mn": "mogol", "xal": "mogol", "cmg": "mogol", "xng": "mogol",
    "hu": "diger", "ro": "diger", "sq": "diger", "nl": "diger", "ja": "diger", "zh": "diger", "hi": "diger", "sa": "diger",
}
SABLON = {"inh", "bor", "der", "ubor", "lbor", "slbor", "calque", "cal", "clq", "sl", "semantic loan", "learned borrowing", "inh+", "bor+", "der+", "uder", "inh-lite", "der-lite", "psm", "translit"}
DIL_RE = re.compile(r"(?:^|[<\s])([a-z]{2,3}(?:-[a-z]+)*|ML\.|LL\.):")


def zincir(d):
    out = []
    for t in d.get("etymology_templates") or []:
        n, a = t.get("name"), t.get("args") or {}
        if n in SABLON and a.get("1") == "tr" and a.get("2"):
            out.append(a["2"])
        elif n in ("ety", "etymon") and a.get("1") == "tr":
            out += [x for x in DIL_RE.findall(a.get("3", "")) if x not in ("ety", "etymon", "id", "t", "alt", "tr", "ts", "q", "qq")]
        elif n == "dercat" and a.get("1") == "tr":
            out += [a[k] for k in sorted((k for k in a if k.isdigit() and k != "1"), key=int)]
    return out


def sinif(z):
    gercek = [x for x in z if x not in ARA]
    if not gercek:
        return None
    for x in gercek:
        if x in TURK or x.startswith("trk"):
            continue
        return SINIF.get(x, "diger")
    return "turk"

ATLA = {"Turkish", "Ottoman Turkish", "Old Anatolian Turkish"}
AD = {
    "turk": ["Proto-Turkic", "Old Turkic", "Chagatai", "Karakhanid", "Old Uyghur", "Proto-Oghuz", "Azerbaijani", "Turkmen", "Kazakh", "Kyrgyz", "Uzbek", "Tatar", "Gagauz", "Crimean Tatar", "Khorezmian Turkic", "Kipchak", "Cuman", "Proto-Common Turkic"],
    "arap": ["Arabic", "Classical Arabic", "Egyptian Arabic", "Levantine Arabic"],
    "fars": ["Persian", "Classical Persian", "Middle Persian", "Old Persian", "Proto-Iranian", "Sogdian", "Parthian", "Avestan", "Dari"],
    "fransiz": ["French", "Middle French", "Old French"],
    "italyan": ["Italian", "Venetian", "Genoese", "Old Italian", "Ligurian"],
    "yunan": ["Greek", "Ancient Greek", "Byzantine Greek", "Koine Greek", "Medieval Greek", "Modern Greek"],
    "ingiliz": ["English", "Middle English"],
    "alman": ["German", "Middle High German", "Old High German"],
    "latin": ["Latin", "Medieval Latin", "New Latin", "Late Latin", "Vulgar Latin"],
    "slav": ["Bulgarian", "Russian", "Serbo-Croatian", "Polish", "Proto-Slavic", "Old Church Slavonic", "Ukrainian", "Czech"],
    "mogol": ["Mongolian", "Middle Mongol", "Proto-Mongolic", "Classical Mongolian"],
}
AD2 = sorted(((ad, s) for s, l in AD.items() for ad in l), key=lambda x: -len(x[0]))
GENEL = re.compile(r"^((?:[A-Z][a-zA-Z\-]+ ?){1,3})")


def dil_adi(satir):
    for ad, s in AD2:
        if satir.startswith(ad + " ") or satir == ad:
            return ad, s
    m = GENEL.match(satir)
    return (m.group(1).strip(), "diger") if m else (None, None)


def agactan(metin):
    if not metin or not metin.startswith("Etymology tree"):
        return None
    satirlar = [x.strip() for x in metin.split("\n")[1:]]
    # ağaç "Turkish <kelime>" satırında biter
    son = next((i for i, x in enumerate(satirlar) if x.startswith("Turkish ")), None)
    if son is None:
        return None
    for x in reversed(satirlar[:son]):
        ad, s = dil_adi(x)
        if not ad or ad in ATLA or ad.startswith("Old Anatolian") or ad.startswith("Ottoman"):
            continue
        return s
    return None


METIN_RE = re.compile(r"(?:[Ff]rom|borrowed from|[Ii]nherited from|derived from)\s+([A-Z][^,.;()]*)")


def metinden(metin):
    if not metin or metin.startswith("Etymology tree"):
        return None
    for m in METIN_RE.finditer(metin):
        ad, s = dil_adi(m.group(1))
        if not ad or ad in ATLA or ad.startswith("Ottoman") or ad.startswith("Old Anatolian"):
            continue
        return s
    return None


sozluk = {}
kok_bekleyen = {}  # türetme: kelime → Türkçe kök
say = collections.Counter()
with open(KOK / "ham/tr.jsonl", encoding="utf-8") as f:
    for satir in f:
        d = json.loads(satir)
        if d.get("lang_code") != "tr" or d.get("pos") in ("name", "proverb", "phrase", "suffix", "prefix", "character", "symbol", "abbrev"):
            continue
        w = d["word"].strip()
        if " " in w or len(w) < 2:
            continue
        s = agactan(d.get("etymology_text")) or metinden(d.get("etymology_text")) or sinif(zincir(d))
        if not s:
            for t in d.get("etymology_templates") or []:
                a = t.get("args") or {}
                if t.get("name") in ("surf", "suffix", "af", "affix", "compound") and a.get("1") == "tr" and a.get("2"):
                    k = re.split(r"[<\s]", a["2"])[0].strip("-").lower()
                    if k.endswith(("mek", "mak")):
                        k = k[:-3]
                    if len(k) >= 2:
                        kok_bekleyen.setdefault(w.lower(), k)
                    break
            continue
        w = w.lower() if not w[0].isupper() else w.replace("I", "ı").replace("İ", "i").lower()
        if d.get("pos") == "verb" and (w.endswith("mek") or w.endswith("mak")):
            sozluk.setdefault(w[:-3], s)  # fiil kökü
        if w not in sozluk:
            sozluk[w] = s
            say[s] += 1
for _ in range(3):  # zincirleme türetmeler için birkaç tur
    for w, k in list(kok_bekleyen.items()):
        if w not in sozluk and k in sozluk:
            sozluk[w] = sozluk[k]; say[sozluk[k]] += 1; del kok_bekleyen[w]
print(len(sozluk), say.most_common(), "çözülemeyen türetme", len(kok_bekleyen))
for w in ["kitap", "masa", "pencere", "ekmek", "su", "araba", "televizyon", "gel", "sevgi", "dünya", "kalem", "okul", "lokanta", "banka", "kapı", "ağaç", "hayat", "insan", "şehir", "zaman", "beyaz", "siyah", "kırmızı", "lamba", "kilise", "patates", "makine", "dakika", "saat", "hafta"]:
    print(w, sozluk.get(w), end=" | ")
# El listesi: Vikisözlük'te köken zinciri eksik ya da kısa eşleşmede yanılan kesin Türkçe zamir, ek ve temel fiil kökleri
EL = "o ben sen biz siz onlar bana sana ona beni seni onu bizi sizi benim senin onun bizim sizin şu bu ne ki mi mı mu mü iç ye ver yap ol et git gel gör bil bul çık in uy uygula uygulama yaz oku konuş söyle başla bitir dur otur kalk".split()
for w in EL:
    sozluk[w] = "turk"
(KOK / "veri").mkdir(exist_ok=True)
json.dump(sozluk, open(KOK / "veri/kokenler.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

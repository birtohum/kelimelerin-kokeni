# Bu kelimeler nereden geldi?

**Canlı:** https://birtohum.github.io/kelimelerin-kokeni/

Türkçe bir metin yapıştır. Her kelimenin altı, Türkçeye geldiği dilin rengiyle çizilir. Üstteki çubuk ve kısa özet, metindeki dillerin payını gösterir. Örnek metinler telifi düşmüş eserlerden: İstiklal Marşı ve Gençliğe Hitabe. Bunlara ek olarak benim yazdığım iki gündelik metin var.

## Veri

İngilizce Vikisözlük'ün Türkçe maddeleri kullanıldı. Kaynak, [kaikki.org](https://kaikki.org/dictionary/Turkish/) dökümü (Ekim 2026, CC BY-SA 4.0).

`araclar/hazirla.py` her maddenin köken ağacını, köken metnini ve şablonlarını okur:

- **Köken dili:** Osmanlıca ve Eski Anadolu Türkçesi ara halka sayılıp atlanır. Kelimenin Türkçeye girdiği ilk dil kökeni belirler.
- **Türetilmiş kelimeler:** Türkçe bir kökten türetilmiş kelimeler (sevgi ← sev-) kökün kökenini alır.
- **El listesi:** Zamirler ve birkaç temel fiil kökü küçük bir el listesiyle "Türkçe" sayılır. Bunlar Vikisözlük'te zinciri eksik olan ya da kısa eşleşmede yanılan kelimelerdir.

Sonuçta 12.020 kelimenin kökeni çıkarıldı:

| Köken | Kelime sayısı |
|---|---|
| Arapça | 3.374 |
| Türkçe | 3.086 |
| Fransızca | 2.612 |
| Farsça | 1.017 |

## Eşleştirme

Ekli bir kelime, sözlükteki en uzun eşleşen köke bağlanır (kitaplarımızdan → kitap). Bu sırada ünsüz yumuşaması da denenir (kitabı → kitap). Bu yöntem bazen yanılır.

## Sınırlar

- **Bulunamayan kelimeler:** Kökeni Vikisözlük'te yazmayan kelimeler gri, "bilinmiyor" olarak kalır.
- **"Diğer" sınıfı:** Seyrek diller "diğer" altında toplanır.
- **Aracı dil:** Bir kelimenin geldiği dil, o kelimenin o dile özgü olduğu anlamına gelmez. Örneğin Farsça yoluyla gelen bazı kelimeler daha eski dillere dayanır.

## Lisans

Kod Apache-2.0. `veri/kokenler.json` Vikisözlük'ten türetildiği için CC BY-SA 4.0.

# Chrome Web Store Listing — Ezan & Namaz Vakitleri (Türkiye)

> Last Updated: 2026-10-15

## Store Listing

**Extension Name** [REQUIRED]
Ezan & Namaz Vakitleri (Türkiye)

**Short Description** [REQUIRED]
Türkiye'nin 81 iline göre namaz vakitleri, sonraki vakte kalan canlı geri sayım, ezan bildirimleri ve günün ayeti.

**Detailed Description** [REQUIRED]
Türkiye'nin tüm illerinde namaz vakitlerini kolayca takip edin, sonraki vakte ne kadar süre kaldığını anlık olarak görün.

Öne Çıkan Özellikler:
Türkiye'nin 81 İli: Adana'dan Düzce'ye dilediğiniz ili seçin; seçiminiz otomatik olarak hatırlansın.
Canlı Geri Sayım: Bir sonraki namaz vaktine kalan süreyi saniye saniye takip edin.
Görsel İlerleme Çubuğu: İki vakit arasında ne kadar zaman geçtiğini gösteren akıcı ilerleme çizgisi.
6 Vakit Görünümü: İmsak (Sahur), Güneş, Öğle, İkindi, Akşam (İftar) ve Yatsı vakitleri.
Akıllı Vurgulama: Aktif vakit zümrüt yeşili, sıradaki vakit ise altın sarısı renkle belirginleştirilir.
Tarayıcı Rozeti: Eklenti simgesi üzerinde kalan süreyi doğrudan görüntüleyin.
Masaüstü Bildirimleri: Vakit girdiğinde veya vakitten önce hatırlatma uyarıları alın.
Miladi ve Hicri Takvim: Günün resmi takvim ve Hicri tarih karşılığı.
Günün Ayet ve Hadisi: Her gün yenilenen anlamlı Türkçe mealli ayet ve hadis-i şerifler.
Koyu ve Açık Tema: Gözünüzü yormayan modern arayüz tasarımı.

Nasıl Kullanılır:
1. Tarayıcınızın araç çubuğundaki cami simgesine tıklayın.
2. Açılır menüden bulunduğunuz ili seçin.
3. Kalan süreyi, vakit tablosunu ve günün ayetini anında inceleyin.
4. Çark (ayarlar) simgesinden bildirim tercihlerinizi özelleştirin.

Gizlilik & Güvenlik:
Uygulama hiçbir kişisel bilginizi toplamaz, kaydetmez veya üçüncü taraflarla paylaşmaz. Seçtiğiniz il ve bildirim tercihleri yalnızca kendi tarayıcınızın yerel hafızasında saklanır.

Destek ve İletişim:
Görüş, öneri veya geri bildirimleriniz için geliştirici destek kanallarımızdan bize ulaşabilirsiniz.

**Category** [REQUIRED]
Productivity

**Single Purpose** [REQUIRED]
Türkiye illerine göre namaz vakitlerini ve bir sonraki vakte kalan süreyi canlı geri sayımla gösterip kullanıcılara vaktinde bildirim sağlamak.

**Primary Language** [REQUIRED]
Turkish

---

## Graphics & Assets

| Asset | Dimensions | Status | Filename |
|-------|-----------|--------|----------|
| Store Icon [REQUIRED] | 128×128 PNG | ✅ Ready | `icons/icon-128.png` |
| Screenshot 1 [REQUIRED] | 1280×800 or 640×400 | ⬜ Not created | `screenshot-1.png` |
| Screenshot 2 [RECOMMENDED] | 1280×800 or 640×400 | ⬜ Not created | `screenshot-2.png` |
| Small Promo Tile [RECOMMENDED] | 440×280 | ⬜ Not created | `promo-small.png` |
| Marquee Promo Tile | 1400×560 | ⬜ Not created | `promo-marquee.png` |

### Screenshot Notes
- **Screenshot 1**: Koyu temada İstanbul için canlı geri sayım, aktif vakit vurgusu ve 6 vakit tablosu görünümü.
- **Screenshot 2**: Açık temada ayarlar çekmecesi ve bildirim seçenekleri.

---

## Permissions Justification

| Permission | Type | Justification |
|------------|------|---------------|
| `storage` | permissions | Kullanıcının seçtiği ili, tema modunu ve bildirim tercihlerini tarayıcı yerel hafızasında saklamak için kullanılır. |
| `alarms` | permissions | Arka planda periyodik vakit kontrolü yapmak ve tarayıcı simgesi üzerindeki geri sayım rozetini güncel tutmak için kullanılır. |
| `notifications` | permissions | Namaz vakti girdiğinde veya vaktin girmesine 15 dakika kala kullanıcıya masaüstü bildirim uyarısı göstermek için kullanılır. |
| `https://api.aladhan.com/*` | host_permissions | Diyanet İşleri Başkanlığı hesaplama standartlarına uygun günlük namaz saatlerini ve Hicri takvim gününü temin etmek için kullanılır. |

---

## Privacy & Data Use

### Data Collection
- **Kişisel Veri:** Toplanmaz (0 veri).
- **Konum Verisi:** Kullanıcı açılır menüden ilini kendisi seçer; GPS veya hassas konum izni istenmez.
- **Web Geçmişi:** Kesinlikle izlenmez veya kaydedilmez.
- **Üçüncü Taraf İletimi:** Hiçbir kullanıcı verisi harici sunuculara gönderilmez. Yalnızca seçilen ilin koordinatlarına ait vakit bilgisi açık kaynaklı namaz vakitleri servisinden çekilir.

---

## Version History

- **v1.0.0 (2026-10-15)**: İlk sürüm.
  - 81 il tam desteği ve il arama/seçme.
  - Canlı saniye geri sayımı ve ilerleme çubuğu.
  - 6 namaz vakti kartı ve aktif/sonraki vakit vurgulaması.
  - Tarayıcı eklenti ikonu üzerinde kalan süre rozeti (Action badge).
  - Vakit girdiğinde ve önceden hatırlatma masaüstü bildirimleri.
  - Miladi ve Hicri takvim desteği.
  - Günün Ayet ve Hadisi bölümü.
  - Koyu ve açık tema seçenekleri.

# 🕌 Ezan & Namaz Vakitleri (Windows Masaüstü Uygulaması)

Windows 10 ve Windows 11 işletim sistemleri için özel olarak tasarlanmış, **Türkiye'nin 81 iline göre** namaz vakitlerini ve **bir sonraki namaz vaktine kalan süreyi** canlı olarak gösteren modern masaüstü uygulaması.

---

## 🌟 Öne Çıkan Özellikler

- **81 İl Desteği (01-81 Plaka Kodlarıyla):** Açılır menüden Türkiye'nin dilediğiniz ilini (Adana'dan Düzce'ye) seçebilirsiniz. Seçiminiz otomatik olarak kaydedilir ve bir sonraki açılışta hatırlanır.
- **Canlı Geri Sayım Sayacı (Saat : Dakika : Saniye):** Bir sonraki vakte kalan süreyi saniye saniye takip edin.
- **İki Vakit Arası Görsel İlerleme Çubuğu:** Mevcut vaktin ne kadarının geçtiğini gösteren şık bir progress bar.
- **6 Vakit Kartları (Görsel Vurgular):**
  - 🌅 **İmsak** (Sahur Sonu / Sabah Başlangıcı)
  - ☀️ **Güneş** (Güneş Doğuşu)
  - 🌤️ **Öğle** (Öğle Namazı)
  - 🌇 **İkindi** (İkindi Namazı)
  - 🌆 **Akşam** (Akşam Namazı / İftar Vakti)
  - 🌙 **Yatsı** (Yatsı Namazı)
  - *Aktif vakit yeşil (Zümrüt), bir sonraki vakit sarı (Altın) çerçeve ile otomatik vurgulanır.*
- **Takvim Bilgileri:**
  - 📅 **Miladi Tarih** (Örn: 15 Ekim 2026 Perşembe)
  - 🌙 **Hicri Tarih** (Örn: 4 Cemâziyelevvel 1448)
- **Windows Yerel Toast Bildirimleri (winotify):**
  - Namaz vakti girdiğinde Windows Eylem Merkezi üzerinden bildirim gönderir.
  - İsteğe bağlı olarak vakitten **15 veya 30 dakika önce** hatırlatıcı bildirimi alabilirsiniz.
- **Sesli Uyarı:** Vakit girdiğinde çalan zarif Windows sistem sesi (Ayarlardan açılıp kapatılabilir).
- **Windows Sistem Tepsisi (System Tray):**
  - Uygulama simge durumuna küçültüldüğünde veya kapatıldığında saatin yanındaki sistem tepsisine yerleşir.
  - Simgenin üzerine gelindiğinde kalan süre anlık ipucu (tooltip) olarak gösterilir.
  - Çift tıklayarak veya sağ tıklayıp "Pencereyi Göster" diyerek anında açabilirsiniz.
- **Çevrimdışı (Offline) Önbellek Desteği:**
  - Alınan vakitler yerel `cache.json` dosyasında saklanır. İnternet bağlantınız kopsa bile uygulama kesintisiz çalışmaya devam eder.
  - Gece yarısı geçtiğinde yeni günün vakitlerini otomatik olarak günceller.
- **Günün Ayet & Hadis-i Şerif Köşesi:** Her gün için ilham veren Türkçe mealli ayet ve hadisler.
- **Koyu (Dark) ve Açık (Light) Mod:** Fluent & modern Windows 11 tasarım dili.

---

## 🚀 Çalıştırma Yöntemleri

### 1. Yöntem: Çift Tıklayarak Başlatma (Tavsiye Edilen)
Klasör içindeki **`Baslat.bat`** dosyasına çift tıklayarak uygulamayı konsol penceresi olmadan doğrudan başlatabilirsiniz.

### 2. Yöntem: Komut İstemi / Terminal ile Başlatma
```powershell
python main.py
```

### 3. Yöntem: Derlenmiş EXE Dosyası
`dist/NamazVakti/NamazVakti.exe` dosyasını çalıştırarak herhangi bir Python kurulumuna ihtiyaç duymadan taşınabilir (portable) olarak kullanabilirsiniz.

### 4. Yöntem: Google Chrome Tarayıcı Eklentisi (Extension)
Uygulamanın tarayıcınızda doğrudan çalışmasını istiyorsanız:
1. Google Chrome'da `chrome://extensions` adresine gidin.
2. Sağ üst köşedeki **"Geliştirici modu"nu (Developer mode)** açın.
3. Sol üstteki **"Paketlenmemiş öğe yükle" (Load unpacked)** butonuna tıklayın.
4. [`chrome-extension`](file:///C:/Users/mert/.gemini/antigravity/scratch/namaz-vakti/chrome-extension) klasörünü seçin.
5. Tarayıcı araç çubuğundaki cami simgesine tıklayarak vakitleri ve kalan süreyi anında görüntüleyin! Rozet metni (badge) sayesinde simge üzerinde kalan süre doğrudan görüntülenir.

### 5. Yöntem: Android Mobil Uygulaması (APK)
Jetpack Compose ve Material 3 ile geliştirilmiş yerel Android uygulaması:
- Hazır kurulum dosyası: [**`NamazVakti.apk`**](file:///C:/Users/mert/.gemini/antigravity/scratch/namaz-vakti/NamazVakti.apk)
- Telefonunuza veya emülatörünüze yüklemek için:
  ```powershell
  adb install NamazVakti.apk
  ```
- Proje kaynak kodları [`android-app`](file:///C:/Users/mert/.gemini/antigravity/scratch/namaz-vakti/android-app) klasöründedir. Yeniden derlemek için:
  ```powershell
  cd android-app
  ./gradlew.bat assembleDebug
  ```

---

## ⚙️ Yapılandırma ve Ayarlar (`config.json`)

Uygulama içerisindeki `⚙️` çark simgesine tıklayarak aşağıdaki ayarları değiştirebilirsiniz:
- **Namaz vakti girdiğinde bildirim göster:** Açık / Kapalı
- **Önceden hatırlatma:** Kapalı, 5 dk, 10 dk, 15 dk, 30 dk
- **Sesli uyarı:** Açık / Kapalı
- **Kapatıldığında sistem tepsisine küçült:** Açık / Kapalı

Tercihler otomatik olarak `config.json` dosyasına yazılır.

---

## 📂 Dosya Yapısı

```
namaz-vakti/
├── assets/
│   ├── icon.ico         # Yüksek çözünürlüklü Windows uygulama ikonu
│   └── icon.png         # Sistem tepsisi ve pencere ikonu
├── app_ui.py            # Modern CustomTkinter grafik arayüzü
├── config.py            # Ayarlar yöneticisi (config.json)
├── namaz_api.py         # API istemcisi, vakit ve kalan süre hesaplama motoru
├── notifications.py     # Windows 10/11 yerel bildirim ve ses yönetimi
├── provinces.py         # 81 il ve koordinat veritabanı
├── quotes.py            # Günün Ayet ve Hadis havuzu
├── tray.py              # Windows Sistem Tepsisi (pystray) entegrasyonu
├── generate_assets.py   # İkon oluşturma betiği
├── build_exe.py         # PyInstaller EXE derleme betiği
├── Baslat.bat           # Hızlı başlatma kısayolu
├── requirements.txt     # Bağımlılık listesi
└── main.py              # Uygulama ana giriş noktası
```

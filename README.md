# 🕌 Ezan & Namaz Vakitleri (Çoklu Platform)

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Chrome%20%7C%20Android-10B981?style=for-the-badge)](https://github.com/mserman90/namaz-vakitleri)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Android-Jetpack%20Compose-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://developer.android.com/compose)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Manifest%20V3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

**Türkiye'nin 81 ili** için Diyanet İşleri Başkanlığı hesaplama metoduna uygun namaz vakitlerini ve **bir sonraki namaz vaktine kalan süreyi** canlı olarak gösteren hepsi bir arada açık kaynak uygulama ekosistemi.

Bu proje üç farklı platform için bağımsız ve optimize edilmiş çözümler sunar:
1. 💻 **Windows Masaüstü Uygulaması** (Python + CustomTkinter + Windows 10/11 Yerel Bildirimleri + Sistem Tepsisi + Taşınabilir EXE)
2. 🌐 **Google Chrome Tarayıcı Eklentisi** (Manifest V3 + Simge Üzerinde Rozet Sayacı + Servis İşçisi + Chrome Bildirimleri)
3. 📱 **Android Mobil Uygulaması** (Kotlin + Jetpack Compose + Material 3 + Hazır APK)

---

## 📊 Platform Karşılaştırma Tablosu

| Özellik | 💻 Windows Masaüstü | 🌐 Chrome Eklentisi | 📱 Android Mobil |
| :--- | :---: | :---: | :---: |
| **81 İl Desteği (01-81 Plaka)** | ✅ | ✅ | ✅ |
| **Canlı Saniye Geri Sayımı** | ✅ | ✅ | ✅ |
| **Görsel İlerleme Çubuğu** | ✅ | ✅ | ✅ |
| **Aktif / Sonraki Vakit Vurgusu** | ✅ | ✅ | ✅ |
| **Miladi & Hicri Takvim** | ✅ | ✅ | ✅ |
| **Günün Ayet & Hadis-i Şerifi** | ✅ | ✅ | ✅ |
| **Masaüstü / Cihaz Bildirimleri** | ✅ (Windows Toast) | ✅ (Chrome Notifications) | ✅ |
| **Önceden Hatırlatma (15/30 dk)**| ✅ | ✅ | ✅ |
| **Sesli Ezan/Uyarı Çalma** | ✅ | ✅ | ✅ |
| **Sistem Tepsisi / Rozet** | ✅ (System Tray) | ✅ (Action Badge) | — |
| **Çevrimdışı (Offline) Önbellek**| ✅ (`cache.json`) | ✅ (`chrome.storage`) | ✅ (`SharedPreferences`) |
| **Koyu / Açık Tema Desteği** | ✅ | ✅ | ✅ |
| **Taşınabilir / Hazır Kurulum** | ✅ (`NamazVakti.exe`) | ✅ (`Paketlenmemiş Yükle`) | ✅ (`NamazVakti.apk`) |

---

## 🌟 Ortak Öne Çıkan Özellikler

- **81 İl Desteği:** Açılır menü veya anlık arama diyaloğuyla Adana'dan Düzce'ye dilediğiniz ili seçebilirsiniz. Seçiminiz yerel hafızaya kaydedilir ve bir sonraki açılışta korunur.
- **Canlı Geri Sayım (`HH : MM : SS`):** Bir sonraki vakte kalan süreyi saniye saniye canlı takip edin (Örn: `01:24:35`).
- **Görsel İlerleme Çubuğu (Progress Bar):** Mevcut vaktin ne kadarının geçtiğini gösteren akıcı ilerleme çizgisi.
- **6 Vakit Görünümü:**
  - 🌅 **İmsak** (Sahur Sonu / Sabah Başlangıcı)
  - ☀️ **Güneş** (Güneş Doğuşu)
  - 🌤️ **Öğle** (Öğle Namazı)
  - 🌇 **İkindi** (İkindi Namazı)
  - 🌆 **Akşam** (Akşam Namazı / İftar Vakti)
  - 🌙 **Yatsı** (Yatsı Namazı)
- **Akıllı Durum Renkleri:** İçinde bulunulan aktif vakit **Zümrüt Yeşili** (`#10B981`), sıradaki vakit ise **Altın Sarısı** (`#F59E0B`) çerçeve ve rozetle dinamik olarak vurgulanır.
- **Günün Ayet & Hadis Köşesi:** Her gün yenilenen anlamlı Türkçe mealli ayet ve hadis-i şerifler.
- **Güvenilir Veri Kaynağı:** T.C. Diyanet İşleri Başkanlığı hesaplama algoritması (Aladhan Method 13) temel alınmıştır.

---

## 🚀 Kurulum ve Çalıştırma Rehberi

### 1. 💻 Windows Masaüstü Uygulaması

#### A) Tek Tıkla Başlatma (Tavsiye Edilen)
Proje dizinindeki **`Baslat.bat`** dosyasına çift tıklayarak konsol penceresi görünmeden doğrudan başlatabilirsiniz.

#### B) Bağımsız EXE Dosyasıyla Çalıştırma
Python kurulumu gerektirmeden doğrudan çalışır:
```
dist/NamazVakti/NamazVakti.exe
```

#### C) Kaynak Koddan Terminal ile Çalıştırma
```powershell
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python main.py
```

---

### 2. 🌐 Google Chrome Tarayıcı Eklentisi (Manifest V3)

1. Google Chrome tarayıcınızı açın ve adres çubuğuna **`chrome://extensions`** yazıp Enter'a basın.
2. Sağ üst köşedeki **"Geliştirici modu"nu (Developer mode)** aktif hale getirin.
3. Sol üstteki **"Paketlenmemiş öğe yükle" (Load unpacked)** butonuna tıklayın.
4. Açılan pencerede projedeki **`chrome-extension`** klasörünü seçin.
5. Tarayıcı araç çubuğundaki Yapboz simgesinden eklentiyi raptiye ile sabitleyin. Eklenti simgesi üzerinde kalan süre rozet (badge) olarak anlık görüntülenir!

> 💡 **Kısayol:** Klasördeki **`Chrome-Eklentiyle-Ac.bat`** dosyasına çift tıklayarak Chrome'u eklenti doğrudan yüklenmiş olarak anında başlatabilirsiniz.

---

### 3. 📱 Android Mobil Uygulaması (Jetpack Compose)

#### A) Hazır APK ile Doğrudan Yükleme
Telefonunuza veya Android emülatörünüze tek tıkla yükleyebilirsiniz:
- Dosya: [**`NamazVakti.apk`**](NamazVakti.apk) *(veya `android-app/app/build/outputs/apk/debug/app-debug.apk`)*

Bilgisayara bağlı cihaza ADB ile yüklemek için:
```powershell
adb install NamazVakti.apk
```

#### B) Android Studio / Gradle ile Kaynak Koddan Derleme
```powershell
cd android-app
./gradlew.bat assembleDebug
```

---

## 📂 Depo Dizin Yapısı

```
namaz-vakti/
│
├── 💻 Windows Masaüstü Uygulaması
│   ├── app_ui.py            # Modern CustomTkinter masaüstü arayüzü ve sayaç mantığı
│   ├── config.py            # Kullanıcı ayarları yöneticisi (config.json)
│   ├── namaz_api.py         # Diyanet API istemcisi ve kalan süre motoru
│   ├── notifications.py     # Windows 10/11 yerel Toast bildirimleri ve ses
│   ├── provinces.py         # 81 ilin plaka ve koordinat veri tabanı
│   ├── quotes.py            # Günün Ayet ve Hadis havuzu
│   ├── tray.py              # Windows Sistem Tepsisi (pystray) arka plan yöneticisi
│   ├── generate_assets.py   # Çoklu çözünürlüklü .ico ve .png ikon üreticisi
│   ├── build_exe.py         # PyInstaller EXE derleme betiği
│   ├── Baslat.bat           # Çift tıklamayla penceresiz başlatan kısayol
│   ├── requirements.txt     # Python bağımlılıkları listesi
│   └── main.py              # Windows uygulaması ana başlatıcısı
│
├── 🌐 Google Chrome Eklentisi (Manifest V3)
│   ├── chrome-extension/
│   │   ├── manifest.json    # Manifest V3 eklenti tanımlaması
│   │   ├── popup.html       # Eklenti açılır pencere arayüzü
│   │   ├── popup.css        # Koyu/Açık tema stilleri
│   │   ├── popup.js         # Canlı sayaç ve etkileşim scripti
│   │   ├── background.js    # Servis işçisi (Service Worker, bildirimler ve rozet)
│   │   ├── api.js           # Aladhan Diyanet API istemcisi
│   │   ├── provinces.js     # 81 il koordinat modülü
│   │   ├── quotes.js        # Ayet ve hadis modülü
│   │   ├── icons/           # 16x16, 48x48 ve 128x128 piksel PNG ikonları
│   │   └── CHROMEWEBSTORE.md# Chrome Web Store yayınlama kılavuzu
│   └── Chrome-Eklentiyle-Ac.bat # Eklentiyi Chrome'da doğrudan başlatan kısayol
│
├── 📱 Android Mobil Uygulaması (Jetpack Compose)
│   ├── NamazVakti.apk       # Doğrudan yüklenebilir derlenmiş Android APK dosyası
│   └── android-app/
│       ├── app/src/main/
│       │   ├── AndroidManifest.xml
│       │   ├── java/com/example/namazvakti/
│       │   │   ├── MainActivity.kt        # Edge-to-Edge giriş aktivitesi
│       │   │   ├── data/
│       │   │   │   ├── Province.kt        # 81 il veri modeli
│       │   │   │   ├── NamazModel.kt      # Vakit ve söz modelleri
│       │   │   │   └── NamazRepository.kt # API istemcisi ve SharedPreferences önbelleği
│       │   │   ├── theme/                 # Zümrüt Yeşili & Altın Material 3 teması
│       │   │   └── ui/
│       │   │       ├── NamazMainScreen.kt # Jetpack Compose arayüzü ve arama diyaloğu
│       │   │       └── NamazViewModel.kt  # StateFlow ve 1 saniyelik sayaç döngüsü
│       │   └── res/                       # Mipmap ikonları, renkler ve dizgiler
│       ├── build.gradle.kts
│       └── gradlew.bat
│
├── CHROMEWEBSTORE.md        # Chrome Web Store uyumluluk ve mağaza listeleme dokümanı
├── README.md                # Kapsamlı proje dokümantasyonu
└── .gitignore               # Git dışlama kuralları
```

---

## 🔒 Gizlilik ve Güvenlik

- Bu proje **kesinlikle hiçbir kişisel veri toplamaz**, kaydetmez veya üçüncü taraf sunuculara göndermez.
- Seçtiğiniz il ve bildirim ayarları yalnızca kullandığınız platformun yerel hafızasında (`config.json`, `chrome.storage.local` veya Android `SharedPreferences`) saklanır.
- GPS veya hassas konum izni istenmez; il seçimi kullanıcı tarafından yapılır.

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak paylaşılmıştır. Dilediğiniz gibi kullanabilir, geliştirebilir ve katkıda bulunabilirsiniz.

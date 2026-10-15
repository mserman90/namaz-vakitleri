/**
 * Namaz Vakitleri API İstemcisi ve Hesaplama Motoru (Extension Uyumlu)
 */

export const PRAYER_NAMES = [
  { key: "imsak", name: "İmsak", desc: "Sahur Sonu / Sabah Başlangıcı", icon: "🌅" },
  { key: "gunes", name: "Güneş", desc: "Güneş Doğuşu", icon: "☀️" },
  { key: "ogle", name: "Öğle", desc: "Öğle Namazı", icon: "🌤️" },
  { key: "ikindi", name: "İkindi", desc: "İkindi Namazı", icon: "🌇" },
  { key: "aksam", name: "Akşam", desc: "Akşam Namazı / İftar", icon: "🌆" },
  { key: "yatsi", name: "Yatsı", desc: "Yatsı Namazı", icon: "🌙" }
];

const TURKISH_MONTHS = [
  "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
  "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
];

const TURKISH_DAYS = [
  "Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"
];

const HIJRI_MONTH_MAP = {
  1: "Muharrem", 2: "Safer", 3: "Rebîülevvel", 4: "Rebîülâhir",
  5: "Cemâziyelevvel", 6: "Cemâziyelâhir", 7: "Recep", 8: "Şaban",
  9: "Ramazan", 10: "Şevval", 11: "Zilkade", 12: "Zilhicce"
};

/**
 * Belirtilen il için günün vakitlerini çeker (Aladhan Diyanet Metodu 13).
 * Önce chrome.storage.local önbelleğini kontrol eder.
 */
export async function fetchPrayerTimings(province, forceRefresh = false) {
  const now = new Date();
  const dayStr = String(now.getDate()).padStart(2, "0");
  const monthStr = String(now.getMonth() + 1).padStart(2, "0");
  const yearStr = now.getFullYear();
  
  const cacheKey = `timings_${province.plate}_${yearStr}-${monthStr}-${dayStr}`;

  if (!forceRefresh) {
    const cached = await chrome.storage.local.get([cacheKey]);
    if (cached[cacheKey] && cached[cacheKey].timings) {
      return cached[cacheKey];
    }
  }

  // Aladhan API (DD-MM-YYYY formatı zorunludur)
  const apiDate = `${dayStr}-${monthStr}-${yearStr}`;
  const url = `https://api.aladhan.com/v1/timings/${apiDate}?latitude=${province.lat}&longitude=${province.lng}&method=13`;

  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(`API hatası: ${resp.status}`);
  }
  const json = await resp.json();

  if (json.code !== 200 || !json.data) {
    throw new Error("Geçersiz API verisi");
  }

  const raw = json.data.timings;
  const cleanTime = (t) => (t ? t.split(" ")[0].trim() : "00:00");

  const timings = {
    imsak: cleanTime(raw.Fajr),
    gunes: cleanTime(raw.Sunrise),
    ogle: cleanTime(raw.Dhuhr),
    ikindi: cleanTime(raw.Asr),
    aksam: cleanTime(raw.Maghrib),
    yatsi: cleanTime(raw.Isha)
  };

  // Hicri ve Miladi tarihler
  const hijriRaw = json.data.date?.hijri || {};
  const hijriMonthNum = hijriRaw.month?.number || 1;
  const hijriMonthName = HIJRI_MONTH_MAP[hijriMonthNum] || "Ramazan";
  const hijriFormatted = `${hijriRaw.day || ""} ${hijriMonthName} ${hijriRaw.year || ""}`.trim();

  const miladiFormatted = `${now.getDate()} ${TURKISH_MONTHS[now.getMonth() + 1]} ${now.getFullYear()} ${TURKISH_DAYS[now.getDay()]}`;

  const result = {
    province,
    date: `${yearStr}-${monthStr}-${dayStr}`,
    miladiDate: miladiFormatted,
    hijriDate: hijriFormatted,
    timings,
    fetchedAt: Date.now()
  };

  await chrome.storage.local.set({ [cacheKey]: result });
  return result;
}

/**
 * Şu anki zamana göre kalan süreyi ve aktif vakti hesaplar.
 */
export function calculateRemaining(data, now = new Date()) {
  const timings = data.timings;
  const year = now.getFullYear();
  const month = now.getMonth();
  const date = now.getDate();

  const prayerDates = PRAYER_NAMES.map((item) => {
    const [h, m] = timings[item.key].split(":").map(Number);
    const d = new Date(year, month, date, h, m, 0);
    return {
      key: item.key,
      name: item.name,
      desc: item.desc,
      icon: item.icon,
      timeStr: timings[item.key],
      dt: d
    };
  });

  const imsakDt = prayerDates[0].dt;
  const yatsiDt = prayerDates[5].dt;

  let prevPrayer, nextPrayer, prevDt, nextDt;

  if (now < imsakDt) {
    // Gece yarısı ile imsak arası
    prevPrayer = prayerDates[5]; // Dünkü Yatsı
    nextPrayer = prayerDates[0]; // Bugünkü İmsak
    prevDt = new Date(year, month, date - 1, ...timings.yatsi.split(":").map(Number));
    nextDt = imsakDt;
  } else if (now >= yatsiDt) {
    // Yatsıdan sonra gece yarısına kadar
    prevPrayer = prayerDates[5];
    nextPrayer = {
      key: "imsak",
      name: "İmsak",
      desc: "Sahur Sonu / Sabah Başlangıcı",
      icon: "🌅",
      timeStr: timings.imsak,
      dt: new Date(year, month, date + 1, ...timings.imsak.split(":").map(Number))
    };
    prevDt = yatsiDt;
    nextDt = nextPrayer.dt;
  } else {
    // Gün içindeki vakitler
    for (let i = 0; i < prayerDates.length - 1; i++) {
      if (now >= prayerDates[i].dt && now < prayerDates[i + 1].dt) {
        prevPrayer = prayerDates[i];
        nextPrayer = prayerDates[i + 1];
        break;
      }
    }
    prevDt = prevPrayer.dt;
    nextDt = nextPrayer.dt;
  }

  const diffMs = Math.max(0, nextDt - now);
  const totalSeconds = Math.floor(diffMs / 1000);

  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const pad = (n) => String(n).padStart(2, "0");
  const remainingStr = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;

  // İlerleme yüzdesi
  const totalSpan = Math.max(1, (nextDt - prevDt) / 1000);
  const elapsed = Math.max(0, (now - prevDt) / 1000);
  const progress = Math.min(1.0, Math.max(0.0, elapsed / totalSpan));

  let subTitle = `${nextPrayer.name} Vaktine Kalan Süre`;
  if (nextPrayer.key === "aksam") {
    subTitle = "Akşam (İftar) Vaktine Kalan Süre";
  } else if (nextPrayer.key === "imsak") {
    subTitle = "İmsak (Sahur Sonu) Vaktine Kalan Süre";
  }

  return {
    currentKey: prevPrayer.key,
    currentName: prevPrayer.name,
    nextKey: nextPrayer.key,
    nextName: nextPrayer.name,
    nextTime: nextPrayer.timeStr,
    subTitle,
    totalSeconds,
    remainingStr,
    progress,
    hours,
    minutes,
    seconds
  };
}

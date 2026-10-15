"""
Namaz Vakitleri API İstemcisi ve Hesaplama Motoru.
Aladhan Diyanet Metodu (Method 13) kullanarak vakitleri çeker ve yerel önbellekler.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta
from typing import Dict, Any, Tuple, Optional

# Namaz vakitleri sırası ve Türkçe etiketleri
PRAYER_NAMES = [
    ("imsak", "İmsak", "Fajr", "Sahur Sonu / Sabah Başlangıcı"),
    ("gunes", "Güneş", "Sunrise", "Güneş Doğuşu"),
    ("ogle", "Öğle", "Dhuhr", "Öğle Namazı"),
    ("ikindi", "İkindi", "Asr", "İkindi Namazı"),
    ("aksam", "Akşam", "Maghrib", "Akşam Namazı / İftar"),
    ("yatsi", "Yatsı", "Isha", "Yatsı Namazı")
]

TURKISH_MONTHS = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]

TURKISH_DAYS = [
    "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
]

import unicodedata

HIJRI_MONTH_MAP = {
    1: "Muharrem",
    2: "Safer",
    3: "Rebîülevvel",
    4: "Rebîülâhir",
    5: "Cemâziyelevvel",
    6: "Cemâziyelâhir",
    7: "Recep",
    8: "Şaban",
    9: "Ramazan",
    10: "Şevval",
    11: "Zilkade",
    12: "Zilhicce"
}

def normalize_text(text: str) -> str:
    """ASCII/Türkçe uyumlu metin temizleme (özel transliterasyon işaretlerini sadeleştirir)"""
    replacements = {
        '\u1e25': 'h', '\u1e24': 'H',
        '\u0101': 'a', '\u0100': 'A',
        '\u012b': 'i', '\u012a': 'I',
        '\u016b': 'u', '\u016a': 'U',
        '\u1e63': 's', '\u1e62': 'S',
        '\u1e0d': 'd', '\u1e0c': 'D',
        '\u1e6d': 't', '\u1e6c': 'T',
        '\u1e93': 'z', '\u1e92': 'Z',
        '\u02bf': '', '\u02be': '',
        '‘': '', '’': ''
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    return text


class NamazAPI:
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_file = os.path.join(cache_dir, "cache.json")
        self._ensure_cache()

    def _ensure_cache(self):
        if not os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    json.dump({}, f)
            except Exception:
                pass

    def _read_cache(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _write_cache(self, data: Dict[str, Any]):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def fetch_timings(self, province: Dict[str, Any], target_date: Optional[date] = None, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Belirtilen il ve tarih için namaz vakitlerini çeker.
        Önce önbelleği kontrol eder, yoksa Aladhan API'den temin eder.
        """
        if target_date is None:
            target_date = datetime.now().date()

        date_str = target_date.strftime("%Y-%m-%d")
        api_date_str = target_date.strftime("%d-%m-%Y")
        cache_key = f"{province['plate']}_{date_str}"
        cache = self._read_cache()

        if not force_refresh and cache_key in cache:
            cached_data = cache[cache_key]
            # Basit doğrulama
            if "timings" in cached_data and "imsak" in cached_data["timings"]:
                return cached_data

        # API'den çek (Method 13 = Diyanet İşleri Başkanlığı, tarih formatı DD-MM-YYYY)
        lat = province["lat"]
        lng = province["lng"]
        url = f"https://api.aladhan.com/v1/timings/{api_date_str}?latitude={lat}&longitude={lng}&method=13"

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NamazVaktiApp/1.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw_json = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            # İnternet bağlantısı yoksa ve önbellekte varsa önbellekten dön
            if cache_key in cache:
                return cache[cache_key]
            raise RuntimeError(f"Vakitler alınamadı ve önbellek bulunamadı: {e}")

        if raw_json.get("code") != 200 or "data" not in raw_json:
            if cache_key in cache:
                return cache[cache_key]
            raise RuntimeError("API yanıt vermedi veya geçersiz veri döndü.")

        api_data = raw_json["data"]
        raw_timings = api_data["timings"]

        # Türkiye Diyanet vakitlerini haritalandır
        # Aladhan method 13'te Fajr Diyanet İmsak saatine karşılık gelir.
        def clean_time(t: str) -> str:
            return t.split(" ")[0].strip()

        timings = {
            "imsak": clean_time(raw_timings.get("Fajr", "05:00")),
            "gunes": clean_time(raw_timings.get("Sunrise", "06:30")),
            "ogle": clean_time(raw_timings.get("Dhuhr", "13:00")),
            "ikindi": clean_time(raw_timings.get("Asr", "16:00")),
            "aksam": clean_time(raw_timings.get("Maghrib", "18:30")),
            "yatsi": clean_time(raw_timings.get("Isha", "20:00"))
        }

        # Tarih bilgileri
        hijri_raw = api_data.get("date", {}).get("hijri", {})
        hijri_day = hijri_raw.get("day", "")
        month_num = hijri_raw.get("month", {}).get("number", 1)
        hijri_month = HIJRI_MONTH_MAP.get(month_num, "Ramazan")
        hijri_year = hijri_raw.get("year", "")
        hijri_formatted = normalize_text(f"{hijri_day} {hijri_month} {hijri_year}".strip())

        # Miladi format
        miladi_day = target_date.day
        miladi_month = TURKISH_MONTHS[target_date.month]
        miladi_year = target_date.year
        miladi_weekday = TURKISH_DAYS[target_date.weekday()]
        miladi_formatted = f"{miladi_day} {miladi_month} {miladi_year} {miladi_weekday}"

        result = {
            "province": province,
            "date": date_str,
            "miladi_date": miladi_formatted,
            "hijri_date": hijri_formatted,
            "timings": timings,
            "meta": {
                "source": "Diyanet İşleri Başkanlığı (Aladhan API Method 13)",
                "timezone": api_data.get("meta", {}).get("timezone", "Europe/Istanbul")
            }
        }

        # Önbelleğe kaydet
        cache[cache_key] = result
        self._write_cache(cache)
        return result

    def calculate_remaining(self, today_data: Dict[str, Any], current_dt: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Şu anki zamana göre:
        - Aktif vakit
        - Bir sonraki vakit
        - Kalan süre (saat, dakika, saniye)
        - Geçen süre yüzdesi (progress bar: 0.0 - 1.0)
        hesaplar.
        """
        if current_dt is None:
            current_dt = datetime.now()

        current_date = current_dt.date()
        timings = today_data["timings"]

        # Günün namaz vakitlerini datetime nesnelerine dönüştür
        prayer_datetimes = []
        for key, name_tr, _, desc in PRAYER_NAMES:
            h, m = map(int, timings[key].split(":"))
            dt = datetime.combine(current_date, datetime.min.time()).replace(hour=h, minute=m, second=0)
            prayer_datetimes.append({
                "key": key,
                "name": name_tr,
                "desc": desc,
                "time_str": timings[key],
                "dt": dt
            })

        # Vakit tespiti
        # 1. Günün ilk vaktinden (İmsak) önce miyiz?
        imsak_dt = prayer_datetimes[0]["dt"]
        yatsi_dt = prayer_datetimes[5]["dt"]

        if current_dt < imsak_dt:
            # Gece yarısından sonra, İmsak'tan önce -> Aktif vakit dünkü Yatsı, Sonraki vakit bugünkü İmsak
            prev_prayer_name = "Yatsı"
            prev_prayer_key = "yatsi"
            next_prayer = prayer_datetimes[0]
            # Dünkü yatsı yaklaşık 24 saat önce
            prev_dt = yatsi_dt - timedelta(days=1)
            next_dt = imsak_dt
        elif current_dt >= yatsi_dt:
            # Yatsıdan sonra, gece yarısına kadar -> Aktif: Yatsı, Sonraki: Yarınki İmsak
            prev_prayer_name = "Yatsı"
            prev_prayer_key = "yatsi"
            next_prayer_name = "İmsak"
            next_prayer_key = "imsak"
            # Yarınki imsak yaklaşık bugünkü imsak + 1 gün
            next_dt = imsak_dt + timedelta(days=1)
            prev_dt = yatsi_dt
            next_prayer = {
                "key": "imsak",
                "name": "İmsak",
                "desc": "Sahur Sonu / Sabah Başlangıcı",
                "time_str": timings["imsak"],
                "dt": next_dt
            }
        else:
            # İmsak ile Yatsı arasında bir vakitteyiz
            prev_prayer = prayer_datetimes[0]
            next_prayer = prayer_datetimes[1]
            for i in range(len(prayer_datetimes) - 1):
                if prayer_datetimes[i]["dt"] <= current_dt < prayer_datetimes[i + 1]["dt"]:
                    prev_prayer = prayer_datetimes[i]
                    next_prayer = prayer_datetimes[i + 1]
                    break
            prev_prayer_name = prev_prayer["name"]
            prev_prayer_key = prev_prayer["key"]
            prev_dt = prev_prayer["dt"]
            next_dt = next_prayer["dt"]

        # Kalan süre
        diff = next_dt - current_dt
        total_seconds = max(0, int(diff.total_seconds()))

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        remaining_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # İlerleme yüzdesi (İki vakit arasındaki geçen süre)
        span_seconds = max(1, int((next_dt - prev_dt).total_seconds()))
        elapsed_seconds = max(0, int((current_dt - prev_dt).total_seconds()))
        progress = min(1.0, max(0.0, elapsed_seconds / span_seconds))

        # Özel iftar/sahur etiketleri
        sub_title = f"{next_prayer['name']} Vaktine Kalan Süre"
        if next_prayer["key"] == "aksam":
            sub_title = "Akşam (İftar) Vaktine Kalan Süre"
        elif next_prayer["key"] == "imsak":
            sub_title = "İmsak (Sahur Sonu) Vaktine Kalan Süre"

        return {
            "current_prayer_key": prev_prayer_key,
            "current_prayer_name": prev_prayer_name,
            "next_prayer_key": next_prayer["key"],
            "next_prayer_name": next_prayer["name"],
            "next_prayer_desc": next_prayer["desc"],
            "next_prayer_time": next_prayer["time_str"],
            "sub_title": sub_title,
            "remaining_seconds": total_seconds,
            "remaining_str": remaining_str,
            "progress": progress,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

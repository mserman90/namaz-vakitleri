package com.example.namazvakti.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

class NamazRepository(private val context: Context) {

    private val prefs = context.getSharedPreferences("namaz_vakti_prefs", Context.MODE_PRIVATE)

    private val turkishMonths = arrayOf(
        "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    )

    private val turkishDays = arrayOf(
        "", "Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"
    )

    private val hijriMonthMap = mapOf(
        1 to "Muharrem", 2 to "Safer", 3 to "Rebîülevvel", 4 to "Rebîülâhir",
        5 to "Cemâziyelevvel", 6 to "Cemâziyelâhir", 7 to "Recep", 8 to "Şaban",
        9 to "Ramazan", 10 to "Şevval", 11 to "Zilkade", 12 to "Zilhicce"
    )

    fun getSavedProvince(): Province {
        val plate = prefs.getString("selected_province_plate", "34") ?: "34"
        return TURKEY_PROVINCES.firstOrNull { it.plate == plate } ?: TURKEY_PROVINCES[33]
    }

    fun saveSelectedProvince(province: Province) {
        prefs.edit().putString("selected_province_plate", province.plate).apply()
    }

    suspend fun getPrayerTimes(province: Province, forceRefresh: Boolean = false): PrayerData = withContext(Dispatchers.IO) {
        val now = Calendar.getInstance()
        val dayStr = String.format(Locale.ROOT, "%02d", now.get(Calendar.DAY_OF_MONTH))
        val monthStr = String.format(Locale.ROOT, "%02d", now.get(Calendar.MONTH) + 1)
        val yearStr = now.get(Calendar.YEAR).toString()
        val dateKey = "$yearStr-$monthStr-$dayStr"
        val cacheKey = "cache_${province.plate}_$dateKey"

        if (!forceRefresh) {
            val cachedJson = prefs.getString(cacheKey, null)
            if (cachedJson != null) {
                try {
                    return@withContext parsePrayerData(JSONObject(cachedJson), province, dateKey)
                } catch (e: Exception) {
                    // cache parse error, fetch fresh
                }
            }
        }

        // Aladhan API (DD-MM-YYYY formatı)
        val apiDate = "$dayStr-$monthStr-$yearStr"
        val urlString = "https://api.aladhan.com/v1/timings/$apiDate?latitude=${province.lat}&longitude=${province.lng}&method=13"

        val url = URL(urlString)
        val conn = url.openConnection() as HttpURLConnection
        conn.requestMethod = "GET"
        conn.setRequestProperty("User-Agent", "NamazVaktiAndroid/1.0")
        conn.connectTimeout = 8000
        conn.readTimeout = 8000

        try {
            val code = conn.responseCode
            if (code != 200) {
                throw RuntimeException("API yanıt kodu: $code")
            }

            val reader = BufferedReader(InputStreamReader(conn.inputStream))
            val sb = StringBuilder()
            var line: String?
            while (reader.readLine().also { line = it } != null) {
                sb.append(line)
            }
            reader.close()

            val rawJson = JSONObject(sb.toString())
            if (rawJson.getInt("code") != 200) {
                throw RuntimeException("API başarısız yanıt döndü")
            }

            // Önbelleğe kaydet
            prefs.edit().putString(cacheKey, sb.toString()).apply()

            return@withContext parsePrayerData(rawJson, province, dateKey)
        } finally {
            conn.disconnect()
        }
    }

    private fun parsePrayerData(json: JSONObject, province: Province, dateKey: String): PrayerData {
        val dataObj = json.getJSONObject("data")
        val timingsObj = dataObj.getJSONObject("timings")

        fun clean(t: String): String = t.split(" ")[0].trim()

        val timings = PrayerTimes(
            imsak = clean(timingsObj.getString("Fajr")),
            gunes = clean(timingsObj.getString("Sunrise")),
            ogle = clean(timingsObj.getString("Dhuhr")),
            ikindi = clean(timingsObj.getString("Asr")),
            aksam = clean(timingsObj.getString("Maghrib")),
            yatsi = clean(timingsObj.getString("Isha"))
        )

        val now = Calendar.getInstance()
        val miladi = "${now.get(Calendar.DAY_OF_MONTH)} ${turkishMonths[now.get(Calendar.MONTH) + 1]} ${now.get(Calendar.YEAR)} ${turkishDays[now.get(Calendar.DAY_OF_WEEK)]}"

        val hijriObj = dataObj.optJSONObject("date")?.optJSONObject("hijri")
        val hijriDay = hijriObj?.optString("day", "") ?: ""
        val hijriMonthNum = hijriObj?.optJSONObject("month")?.optInt("number", 1) ?: 1
        val hijriMonth = hijriMonthMap[hijriMonthNum] ?: "Ramazan"
        val hijriYear = hijriObj?.optString("year", "") ?: ""
        val hijri = "$hijriDay $hijriMonth $hijriYear".trim()

        return PrayerData(
            province = province,
            dateStr = dateKey,
            miladiDate = miladi,
            hijriDate = hijri,
            timings = timings
        )
    }

    fun calculateRemaining(data: PrayerData, now: Calendar = Calendar.getInstance()): RemainingTimeInfo {
        val timings = data.timings

        fun toCalendar(timeStr: String, dayOffset: Int = 0): Calendar {
            val parts = timeStr.split(":").map { it.toInt() }
            val c = now.clone() as Calendar
            c.add(Calendar.DAY_OF_MONTH, dayOffset)
            c.set(Calendar.HOUR_OF_DAY, parts[0])
            c.set(Calendar.MINUTE, parts[1])
            c.set(Calendar.SECOND, 0)
            c.set(Calendar.MILLISECOND, 0)
            return c
        }

        val prayerTimesList = listOf(
            Triple("imsak", "İmsak", toCalendar(timings.imsak)),
            Triple("gunes", "Güneş", toCalendar(timings.gunes)),
            Triple("ogle", "Öğle", toCalendar(timings.ogle)),
            Triple("ikindi", "İkindi", toCalendar(timings.ikindi)),
            Triple("aksam", "Akşam", toCalendar(timings.aksam)),
            Triple("yatsi", "Yatsı", toCalendar(timings.yatsi))
        )

        val imsakCal = prayerTimesList[0].third
        val yatsiCal = prayerTimesList[5].third

        val prevPrayer: Triple<String, String, Calendar>
        val nextPrayer: Triple<String, String, Calendar>
        val nextTimeStr: String

        if (now.before(imsakCal)) {
            // Gece yarısı ile imsak arası
            prevPrayer = Triple("yatsi", "Yatsı", toCalendar(timings.yatsi, -1))
            nextPrayer = prayerTimesList[0]
            nextTimeStr = timings.imsak
        } else if (now.after(yatsiCal) || now == yatsiCal) {
            // Yatsıdan sonra gece yarısına kadar
            prevPrayer = prayerTimesList[5]
            nextPrayer = Triple("imsak", "İmsak", toCalendar(timings.imsak, 1))
            nextTimeStr = timings.imsak
        } else {
            // İki vakit arasında
            var p = prayerTimesList[0]
            var n = prayerTimesList[1]
            for (i in 0 until prayerTimesList.size - 1) {
                if ((now.after(prayerTimesList[i].third) || now == prayerTimesList[i].third) && now.before(prayerTimesList[i + 1].third)) {
                    p = prayerTimesList[i]
                    n = prayerTimesList[i + 1]
                    break
                }
            }
            prevPrayer = p
            nextPrayer = n
            nextTimeStr = when (nextPrayer.first) {
                "imsak" -> timings.imsak
                "gunes" -> timings.gunes
                "ogle" -> timings.ogle
                "ikindi" -> timings.ikindi
                "aksam" -> timings.aksam
                else -> timings.yatsi
            }
        }

        val diffMs = Math.max(0L, nextPrayer.third.timeInMillis - now.timeInMillis)
        val totalSeconds = diffMs / 1000

        val hours = totalSeconds / 3600
        val minutes = (totalSeconds % 3600) / 60
        val seconds = totalSeconds % 60
        val remainingStr = String.format(Locale.ROOT, "%02d:%02d:%02d", hours, minutes, seconds)

        val totalSpan = Math.max(1L, (nextPrayer.third.timeInMillis - prevPrayer.third.timeInMillis) / 1000)
        val elapsed = Math.max(0L, (now.timeInMillis - prevPrayer.third.timeInMillis) / 1000)
        val progress = Math.min(1.0f, Math.max(0.0f, elapsed.toFloat() / totalSpan.toFloat()))

        val subTitle = when (nextPrayer.first) {
            "aksam" -> "Akşam (İftar) Vaktine Kalan Süre"
            "imsak" -> "İmsak (Sahur Sonu) Vaktine Kalan Süre"
            else -> "${nextPrayer.second} Vaktine Kalan Süre"
        }

        return RemainingTimeInfo(
            currentKey = prevPrayer.first,
            currentName = prevPrayer.second,
            nextKey = nextPrayer.first,
            nextName = nextPrayer.second,
            nextTime = nextTimeStr,
            subTitle = subTitle,
            remainingSeconds = totalSeconds,
            remainingStr = remainingStr,
            progress = progress
        )
    }
}

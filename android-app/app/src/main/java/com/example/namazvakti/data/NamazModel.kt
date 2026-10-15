package com.example.namazvakti.data

import java.util.Calendar

data class PrayerTimes(
    val imsak: String,
    val gunes: String,
    val ogle: String,
    val ikindi: String,
    val aksam: String,
    val yatsi: String
)

data class PrayerData(
    val province: Province,
    val dateStr: String,
    val miladiDate: String,
    val hijriDate: String,
    val timings: PrayerTimes
)

data class RemainingTimeInfo(
    val currentKey: String,
    val currentName: String,
    val nextKey: String,
    val nextName: String,
    val nextTime: String,
    val subTitle: String,
    val remainingSeconds: Long,
    val remainingStr: String,
    val progress: Float
)

data class PrayerDefinition(
    val key: String,
    val name: String,
    val desc: String,
    val icon: String
)

val PRAYER_DEFINITIONS = listOf(
    PrayerDefinition("imsak", "İmsak", "Sahur Sonu / Sabah", "🌅"),
    PrayerDefinition("gunes", "Güneş", "Güneş Doğuşu", "☀️"),
    PrayerDefinition("ogle", "Öğle", "Öğle Namazı", "🌤️"),
    PrayerDefinition("ikindi", "İkindi", "İkindi Namazı", "🌇"),
    PrayerDefinition("aksam", "Akşam", "Akşam / İftar", "🌆"),
    PrayerDefinition("yatsi", "Yatsı", "Yatsı Namazı", "🌙")
)

data class DailyQuote(
    val type: String,
    val text: String,
    val source: String
)

val DAILY_QUOTES = listOf(
    DailyQuote(
        "Ayet-i Kerîme",
        "Şüphesiz namaz, müminlere belirli vakitlerde farz kılınmıştır.",
        "Nisâ Sûresi, 103"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Dua müminin silahı, dinin direği, göklerin ve yerin nurudur.",
        "Hâkim, Müstedrek"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Bilesiniz ki, kalpler ancak Allah'ı anmakla huzur bulur.",
        "Ra'd Sûresi, 28"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Cennetin anahtarı namaz, namazın anahtarı ise abdesttir.",
        "Tirmizî, Tahâret, 1"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Bana dua edin, size cevap vereyim (duanızı kabul edeyim).",
        "Mü'min Sûresi, 60"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Amellerin Allah'a en sevimli olanı, vaktinde kılınan namazdır.",
        "Buhârî, Mevâkît, 5"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Sabır ve namaz ile Allah'tan yardım isteyin. Şüphesiz bu, saygılı olanlardan başkasına ağır gelir.",
        "Bakara Sûresi, 45"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Kolaylaştırınız, güçleştirmeyiniz; müjdeleyiniz, nefret ettirmeyiniz.",
        "Buhârî, İlim, 11"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Rabbiniz şöyle buyurdu: Bana şükrederseniz, elbette size nimetimi artırırım.",
        "İbrâhîm Sûresi, 7"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.",
        "Buhârî, Îmân, 4"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Allah sabredenlerle beraberdir.",
        "Bakara Sûresi, 153"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "Birbirinize hediye veriniz ki birbirinize olan sevginiz artsın.",
        "Buhârî, el-Edebü'l-Müfred"
    ),
    DailyQuote(
        "Ayet-i Kerîme",
        "Muhakkak ki zorlukla beraber bir kolaylık vardır.",
        "İnşirâh Sûresi, 6"
    ),
    DailyQuote(
        "Hadis-i Şerif",
        "İki nimet vardır ki insanların çoğu bunların kıymetini bilmekte aldanmıştır: Sağlık ve boş vakit.",
        "Buhârî, Rikâk, 1"
    )
)

fun getDailyQuote(calendar: Calendar = Calendar.getInstance()): DailyQuote {
    val dayIndex = (calendar.get(Calendar.YEAR) * 365 + (calendar.get(Calendar.MONTH) + 1) * 31 + calendar.get(Calendar.DAY_OF_MONTH)) % DAILY_QUOTES.size
    return DAILY_QUOTES[dayIndex]
}

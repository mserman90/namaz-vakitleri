package com.example.namazvakti.data

data class Province(
    val plate: String,
    val name: String,
    val lat: Double,
    val lng: Double
) {
    val displayName: String
        get() = "$plate - $name"
}

val TURKEY_PROVINCES = listOf(
    Province("01", "Adana", 37.0000, 35.3213),
    Province("02", "Adıyaman", 37.7648, 38.2786),
    Province("03", "Afyonkarahisar", 38.7507, 30.5567),
    Province("04", "Ağrı", 39.7191, 43.0503),
    Province("05", "Amasya", 40.6534, 35.8331),
    Province("06", "Ankara", 39.9334, 32.8597),
    Province("07", "Antalya", 36.8969, 30.7133),
    Province("08", "Artvin", 41.1828, 41.8183),
    Province("09", "Aydın", 37.8560, 27.8416),
    Province("10", "Balıkesir", 39.6484, 27.8826),
    Province("11", "Bilecik", 40.1451, 29.9799),
    Province("12", "Bingöl", 38.8854, 40.4983),
    Province("13", "Bitlis", 38.4006, 42.1095),
    Province("14", "Bolu", 40.7358, 31.6061),
    Province("15", "Burdur", 37.7206, 30.2908),
    Province("16", "Bursa", 40.1885, 29.0610),
    Province("17", "Çanakkale", 40.1553, 26.4142),
    Province("18", "Çankırı", 40.6013, 33.6134),
    Province("19", "Çorum", 40.5506, 34.9556),
    Province("20", "Denizli", 37.7765, 29.0864),
    Province("21", "Diyarbakır", 37.9144, 40.2306),
    Province("22", "Edirne", 41.6818, 26.5623),
    Province("23", "Elazığ", 38.6810, 39.2264),
    Province("24", "Erzincan", 39.7500, 39.5000),
    Province("25", "Erzurum", 39.9043, 41.2679),
    Province("26", "Eskişehir", 39.7767, 30.5206),
    Province("27", "Gaziantep", 37.0662, 37.3833),
    Province("28", "Giresun", 40.9128, 38.3895),
    Province("29", "Gümüşhane", 40.4600, 39.4718),
    Province("30", "Hakkâri", 37.5833, 43.7333),
    Province("31", "Hatay", 36.4018, 36.3498),
    Province("32", "Isparta", 37.7648, 30.5566),
    Province("33", "Mersin", 36.8121, 34.6415),
    Province("34", "İstanbul", 41.0082, 28.9784),
    Province("35", "İzmir", 38.4237, 27.1428),
    Province("36", "Kars", 40.6167, 43.1000),
    Province("37", "Kastamonu", 41.3887, 33.7827),
    Province("38", "Kayseri", 38.7312, 35.4787),
    Province("39", "Kırklareli", 41.7333, 27.2167),
    Province("40", "Kırşehir", 39.1425, 34.1709),
    Province("41", "Kocaeli", 40.8533, 29.8815),
    Province("42", "Konya", 37.8667, 32.4833),
    Province("43", "Kütahya", 39.4167, 29.9833),
    Province("44", "Malatya", 38.3552, 38.3095),
    Province("45", "Manisa", 38.6191, 27.4289),
    Province("46", "Kahramanmaraş", 37.5858, 36.9371),
    Province("47", "Mardin", 37.3212, 40.7245),
    Province("48", "Muğla", 37.2153, 28.3636),
    Province("49", "Muş", 38.7432, 41.5064),
    Province("50", "Nevşehir", 38.6244, 34.7144),
    Province("51", "Niğde", 37.9667, 34.6833),
    Province("52", "Ordu", 40.9839, 37.8764),
    Province("53", "Rize", 41.0201, 40.5234),
    Province("54", "Sakarya", 40.7569, 30.3783),
    Province("55", "Samsun", 41.2928, 36.3313),
    Province("56", "Siirt", 37.9333, 41.9500),
    Province("57", "Sinop", 42.0231, 35.1531),
    Province("58", "Sivas", 39.7477, 37.0179),
    Province("59", "Tekirdağ", 40.9833, 27.5167),
    Province("60", "Tokat", 40.3167, 36.5500),
    Province("61", "Trabzon", 41.0027, 39.7168),
    Province("62", "Tunceli", 39.1079, 39.5401),
    Province("63", "Şanlıurfa", 37.1674, 38.7955),
    Province("64", "Uşak", 38.6823, 29.4082),
    Province("65", "Van", 38.4891, 43.4089),
    Province("66", "Yozgat", 39.8181, 34.8147),
    Province("67", "Zonguldak", 41.4564, 31.7987),
    Province("68", "Aksaray", 38.3687, 34.0370),
    Province("69", "Bayburt", 40.2552, 40.2249),
    Province("70", "Karaman", 37.1759, 33.2287),
    Province("71", "Kırıkkale", 39.8468, 33.5153),
    Province("72", "Batman", 37.8812, 41.1294),
    Province("73", "Şırnak", 37.5164, 42.4611),
    Province("74", "Bartın", 41.6344, 32.3375),
    Province("75", "Ardahan", 41.1105, 42.7022),
    Province("76", "Iğdır", 39.9196, 44.0450),
    Province("77", "Yalova", 40.6500, 29.2667),
    Province("78", "Karabük", 41.2061, 32.6204),
    Province("79", "Kilis", 36.7184, 37.1212),
    Province("80", "Osmaniye", 37.0742, 36.2472),
    Province("81", "Düzce", 40.8438, 31.1565)
)

fun findProvince(query: String): Province {
    val q = query.trim().lowercase()
    return TURKEY_PROVINCES.firstOrNull {
        it.displayName.lowercase() == q ||
        it.name.lowercase() == q ||
        it.plate == q
    } ?: TURKEY_PROVINCES[33] // 34 - İstanbul
}

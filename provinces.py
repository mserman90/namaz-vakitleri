"""
Türkiye'nin 81 İli ve Resmi Koordinatları.
"""

from typing import List, Dict, Optional

PROVINCES: List[Dict[str, any]] = [
    {"plate": "01", "name": "Adana", "lat": 37.0000, "lng": 35.3213},
    {"plate": "02", "name": "Adıyaman", "lat": 37.7648, "lng": 38.2786},
    {"plate": "03", "name": "Afyonkarahisar", "lat": 38.7507, "lng": 30.5567},
    {"plate": "04", "name": "Ağrı", "lat": 39.7191, "lng": 43.0503},
    {"plate": "05", "name": "Amasya", "lat": 40.6534, "lng": 35.8331},
    {"plate": "06", "name": "Ankara", "lat": 39.9334, "lng": 32.8597},
    {"plate": "07", "name": "Antalya", "lat": 36.8969, "lng": 30.7133},
    {"plate": "08", "name": "Artvin", "lat": 41.1828, "lng": 41.8183},
    {"plate": "09", "name": "Aydın", "lat": 37.8560, "lng": 27.8416},
    {"plate": "10", "name": "Balıkesir", "lat": 39.6484, "lng": 27.8826},
    {"plate": "11", "name": "Bilecik", "lat": 40.1451, "lng": 29.9799},
    {"plate": "12", "name": "Bingöl", "lat": 38.8854, "lng": 40.4983},
    {"plate": "13", "name": "Bitlis", "lat": 38.4006, "lng": 42.1095},
    {"plate": "14", "name": "Bolu", "lat": 40.7358, "lng": 31.6061},
    {"plate": "15", "name": "Burdur", "lat": 37.7206, "lng": 30.2908},
    {"plate": "16", "name": "Bursa", "lat": 40.1885, "lng": 29.0610},
    {"plate": "17", "name": "Çanakkale", "lat": 40.1553, "lng": 26.4142},
    {"plate": "18", "name": "Çankırı", "lat": 40.6013, "lng": 33.6134},
    {"plate": "19", "name": "Çorum", "lat": 40.5506, "lng": 34.9556},
    {"plate": "20", "name": "Denizli", "lat": 37.7765, "lng": 29.0864},
    {"plate": "21", "name": "Diyarbakır", "lat": 37.9144, "lng": 40.2306},
    {"plate": "22", "name": "Edirne", "lat": 41.6818, "lng": 26.5623},
    {"plate": "23", "name": "Elazığ", "lat": 38.6810, "lng": 39.2264},
    {"plate": "24", "name": "Erzincan", "lat": 39.7500, "lng": 39.5000},
    {"plate": "25", "name": "Erzurum", "lat": 39.9043, "lng": 41.2679},
    {"plate": "26", "name": "Eskişehir", "lat": 39.7767, "lng": 30.5206},
    {"plate": "27", "name": "Gaziantep", "lat": 37.0662, "lng": 37.3833},
    {"plate": "28", "name": "Giresun", "lat": 40.9128, "lng": 38.3895},
    {"plate": "29", "name": "Gümüşhane", "lat": 40.4600, "lng": 39.4718},
    {"plate": "30", "name": "Hakkâri", "lat": 37.5833, "lng": 43.7333},
    {"plate": "31", "name": "Hatay", "lat": 36.4018, "lng": 36.3498},
    {"plate": "32", "name": "Isparta", "lat": 37.7648, "lng": 30.5566},
    {"plate": "33", "name": "Mersin", "lat": 36.8121, "lng": 34.6415},
    {"plate": "34", "name": "İstanbul", "lat": 41.0082, "lng": 28.9784},
    {"plate": "35", "name": "İzmir", "lat": 38.4237, "lng": 27.1428},
    {"plate": "36", "name": "Kars", "lat": 40.6167, "lng": 43.1000},
    {"plate": "37", "name": "Kastamonu", "lat": 41.3887, "lng": 33.7827},
    {"plate": "38", "name": "Kayseri", "lat": 38.7312, "lng": 35.4787},
    {"plate": "39", "name": "Kırklareli", "lat": 41.7333, "lng": 27.2167},
    {"plate": "40", "name": "Kırşehir", "lat": 39.1425, "lng": 34.1709},
    {"plate": "41", "name": "Kocaeli", "lat": 40.8533, "lng": 29.8815},
    {"plate": "42", "name": "Konya", "lat": 37.8667, "lng": 32.4833},
    {"plate": "43", "name": "Kütahya", "lat": 39.4167, "lng": 29.9833},
    {"plate": "44", "name": "Malatya", "lat": 38.3552, "lng": 38.3095},
    {"plate": "45", "name": "Manisa", "lat": 38.6191, "lng": 27.4289},
    {"plate": "46", "name": "Kahramanmaraş", "lat": 37.5858, "lng": 36.9371},
    {"plate": "47", "name": "Mardin", "lat": 37.3212, "lng": 40.7245},
    {"plate": "48", "name": "Muğla", "lat": 37.2153, "lng": 28.3636},
    {"plate": "49", "name": "Muş", "lat": 38.7432, "lng": 41.5064},
    {"plate": "50", "name": "Nevşehir", "lat": 38.6244, "lng": 34.7144},
    {"plate": "51", "name": "Niğde", "lat": 37.9667, "lng": 34.6833},
    {"plate": "52", "name": "Ordu", "lat": 40.9839, "lng": 37.8764},
    {"plate": "53", "name": "Rize", "lat": 41.0201, "lng": 40.5234},
    {"plate": "54", "name": "Sakarya", "lat": 40.7569, "lng": 30.3783},
    {"plate": "55", "name": "Samsun", "lat": 41.2928, "lng": 36.3313},
    {"plate": "56", "name": "Siirt", "lat": 37.9333, "lng": 41.9500},
    {"plate": "57", "name": "Sinop", "lat": 42.0231, "lng": 35.1531},
    {"plate": "58", "name": "Sivas", "lat": 39.7477, "lng": 37.0179},
    {"plate": "59", "name": "Tekirdağ", "lat": 40.9833, "lng": 27.5167},
    {"plate": "60", "name": "Tokat", "lat": 40.3167, "lng": 36.5500},
    {"plate": "61", "name": "Trabzon", "lat": 41.0027, "lng": 39.7168},
    {"plate": "62", "name": "Tunceli", "lat": 39.1079, "lng": 39.5401},
    {"plate": "63", "name": "Şanlıurfa", "lat": 37.1674, "lng": 38.7955},
    {"plate": "64", "name": "Uşak", "lat": 38.6823, "lng": 29.4082},
    {"plate": "65", "name": "Van", "lat": 38.4891, "lng": 43.4089},
    {"plate": "66", "name": "Yozgat", "lat": 39.8181, "lng": 34.8147},
    {"plate": "67", "name": "Zonguldak", "lat": 41.4564, "lng": 31.7987},
    {"plate": "68", "name": "Aksaray", "lat": 38.3687, "lng": 34.0370},
    {"plate": "69", "name": "Bayburt", "lat": 40.2552, "lng": 40.2249},
    {"plate": "70", "name": "Karaman", "lat": 37.1759, "lng": 33.2287},
    {"plate": "71", "name": "Kırıkkale", "lat": 39.8468, "lng": 33.5153},
    {"plate": "72", "name": "Batman", "lat": 37.8812, "lng": 41.1294},
    {"plate": "73", "name": "Şırnak", "lat": 37.5164, "lng": 42.4611},
    {"plate": "74", "name": "Bartın", "lat": 41.6344, "lng": 32.3375},
    {"plate": "75", "name": "Ardahan", "lat": 41.1105, "lng": 42.7022},
    {"plate": "76", "name": "Iğdır", "lat": 39.9196, "lng": 44.0450},
    {"plate": "77", "name": "Yalova", "lat": 40.6500, "lng": 29.2667},
    {"plate": "78", "name": "Karabük", "lat": 41.2061, "lng": 32.6204},
    {"plate": "79", "name": "Kilis", "lat": 36.7184, "lng": 37.1212},
    {"plate": "80", "name": "Osmaniye", "lat": 37.0742, "lng": 36.2472},
    {"plate": "81", "name": "Düzce", "lat": 40.8438, "lng": 31.1565}
]


def get_display_list() -> List[str]:
    """İlleri plaka numarası ve adı ile birlikte döndürür: Örn: '34 - İstanbul'"""
    return [f"{p['plate']} - {p['name']}" for p in PROVINCES]


def find_province(query: str) -> Optional[Dict[str, any]]:
    """
    Plaka numarası, tam adı veya '34 - İstanbul' formatındaki dizgiden ili bulur.
    """
    q = query.strip().lower()
    for p in PROVINCES:
        full_display = f"{p['plate']} - {p['name']}".lower()
        if q == full_display or q == p["name"].lower() or q == p["plate"]:
            return p
        if p["name"].lower() in q:
            return p
    return PROVINCES[33]  # Varsayılan: 34 - İstanbul

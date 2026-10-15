"""
Günün Ayeti ve Hadis-i Şerifleri Havuzu (Türkçe Mealleriyle).
Her gün için ilham verici, huzur veren ayet ve hadisler.
"""

from typing import Dict, List
import random
from datetime import date

DAILY_QUOTES: List[Dict[str, str]] = [
    {
        "type": "Ayet-i Kerîme",
        "text": "Şüphesiz namaz, müminlere belirli vakitlerde farz kılınmıştır.",
        "source": "Nisâ Sûresi, 103"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Dua müminin silahı, dinin direği, göklerin ve yerin nurudur.",
        "source": "Hâkim, Müstedrek"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Bilesiniz ki, kalpler ancak Allah'ı anmakla huzur bulur.",
        "source": "Ra'd Sûresi, 28"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Cennetin anahtarı namaz, namazın anahtarı ise abdesttir.",
        "source": "Tirmizî, Tahâret, 1"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Bana dua edin, size cevap vereyim (duanızı kabul edeyim).",
        "source": "Mü'min Sûresi, 60"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Amellerin Allah'a en sevimli olanı, vaktinde kılınan namazdır.",
        "source": "Buhârî, Mevâkît, 5"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Sabır ve namaz ile Allah'tan yardım isteyin. Şüphesiz bu, saygılı olanlardan başkasına ağır gelir.",
        "source": "Bakara Sûresi, 45"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Kolaylaştırınız, güçleştirmeyiniz; müjdeleyiniz, nefret ettirmeyiniz.",
        "source": "Buhârî, İlim, 11"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Rabbiniz şöyle buyurdu: Bana şükrederseniz, elbette size nimetimi artırırım.",
        "source": "İbrâhîm Sûresi, 7"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.",
        "source": "Buhârî, Îmân, 4"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Allah sabredenlerle beraberdir.",
        "source": "Bakara Sûresi, 153"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "Birbirinize hediye veriniz ki birbirinize olan sevginiz artsın.",
        "source": "Buhârî, el-Edebü'l-Müfred"
    },
    {
        "type": "Ayet-i Kerîme",
        "text": "Muhakkak ki zorlukla beraber bir kolaylık vardır.",
        "source": "İnşirâh Sûresi, 6"
    },
    {
        "type": "Hadis-i Şerif",
        "text": "İki nimet vardır ki insanların çoğu bunların kıymetini bilmekte aldanmıştır: Sağlık ve boş vakit.",
        "source": "Buhârî, Rikâk, 1"
    }
]


def get_quote_for_today(current_date: date = None) -> Dict[str, str]:
    """Günün tarihine göre kararlı (tüm gün boyunca aynı kalan) bir ayet/hadis seçer."""
    if current_date is None:
        current_date = date.today()
    day_index = (current_date.year * 365 + current_date.month * 31 + current_date.day) % len(DAILY_QUOTES)
    return DAILY_QUOTES[day_index]

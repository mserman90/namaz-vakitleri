/**
 * Günün Ayeti ve Hadis-i Şerifleri Havuzu (Türkçe Mealleriyle).
 */
export const DAILY_QUOTES = [
  {
    type: "Ayet-i Kerîme",
    text: "Şüphesiz namaz, müminlere belirli vakitlerde farz kılınmıştır.",
    source: "Nisâ Sûresi, 103"
  },
  {
    type: "Hadis-i Şerif",
    text: "Dua müminin silahı, dinin direği, göklerin ve yerin nurudur.",
    source: "Hâkim, Müstedrek"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Bilesiniz ki, kalpler ancak Allah'ı anmakla huzur bulur.",
    source: "Ra'd Sûresi, 28"
  },
  {
    type: "Hadis-i Şerif",
    text: "Cennetin anahtarı namaz, namazın anahtarı ise abdesttir.",
    source: "Tirmizî, Tahâret, 1"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Bana dua edin, size cevap vereyim (duanızı kabul edeyim).",
    source: "Mü'min Sûresi, 60"
  },
  {
    type: "Hadis-i Şerif",
    text: "Amellerin Allah'a en sevimli olanı, vaktinde kılınan namazdır.",
    source: "Buhârî, Mevâkît, 5"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Sabır ve namaz ile Allah'tan yardım isteyin. Şüphesiz bu, saygılı olanlardan başkasına ağır gelir.",
    source: "Bakara Sûresi, 45"
  },
  {
    type: "Hadis-i Şerif",
    text: "Kolaylaştırınız, güçleştirmeyiniz; müjdeleyiniz, nefret ettirmeyiniz.",
    source: "Buhârî, İlim, 11"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Rabbiniz şöyle buyurdu: Bana şükrederseniz, elbette size nimetimi artırırım.",
    source: "İbrâhîm Sûresi, 7"
  },
  {
    type: "Hadis-i Şerif",
    text: "Müslüman, elinden ve dilinden diğer Müslümanların güvende olduğu kimsedir.",
    source: "Buhârî, Îmân, 4"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Allah sabredenlerle beraberdir.",
    source: "Bakara Sûresi, 153"
  },
  {
    type: "Hadis-i Şerif",
    text: "Birbirinize hediye veriniz ki birbirinize olan sevginiz artsın.",
    source: "Buhârî, el-Edebü'l-Müfred"
  },
  {
    type: "Ayet-i Kerîme",
    text: "Muhakkak ki zorlukla beraber bir kolaylık vardır.",
    source: "İnşirâh Sûresi, 6"
  },
  {
    type: "Hadis-i Şerif",
    text: "İki nimet vardır ki insanların çoğu bunların kıymetini bilmekte aldanmıştır: Sağlık ve boş vakit.",
    source: "Buhârî, Rikâk, 1"
  }
];

export function getQuoteForToday(d = new Date()) {
  const dayIndex = (d.getFullYear() * 365 + (d.getMonth() + 1) * 31 + d.getDate()) % DAILY_QUOTES.length;
  return DAILY_QUOTES[dayIndex];
}

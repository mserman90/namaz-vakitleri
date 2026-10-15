/**
 * Ezan & Namaz Vakitleri - Arka Plan Servis İşçisi (Service Worker)
 * Manifest V3 Uyumlu: Alarms, Notifications, Action Badge
 */

import { findProvince } from "./provinces.js";
import { fetchPrayerTimings, calculateRemaining } from "./api.js";

const ALARM_NAME = "namaz_timer_alarm";

// Kurulum ve güncelleme
chrome.runtime.onInstalled.addListener(async () => {
  const current = await chrome.storage.local.get([
    "selected_province",
    "notify_on_prayer",
    "notify_minutes_before",
    "badge_mode"
  ]);

  if (!current.selected_province) {
    await chrome.storage.local.set({
      selected_province: "34 - İstanbul",
      notify_on_prayer: true,
      notify_minutes_before: 15,
      badge_mode: "countdown", // 'countdown', 'prayer_name', 'off'
      sent_notifications: []
    });
  }

  // Her 1 dakikada bir çalışacak alarm kur
  await chrome.alarms.create(ALARM_NAME, { periodInMinutes: 1 });

  // İlk güncelleme
  await updateBadgeAndCheckNotifications();
});

// Alarm tetiklendiğinde
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === ALARM_NAME) {
    await updateBadgeAndCheckNotifications();
  }
});

// Ayarlar veya il değiştiğinde
chrome.storage.onChanged.addListener(async (changes, area) => {
  if (area === "local" && (changes.selected_province || changes.badge_mode)) {
    await updateBadgeAndCheckNotifications();
  }
});

/**
 * Rozet metnini günceller ve vakit bildirimlerini denetler
 */
async function updateBadgeAndCheckNotifications() {
  try {
    const config = await chrome.storage.local.get([
      "selected_province",
      "notify_on_prayer",
      "notify_minutes_before",
      "badge_mode",
      "sent_notifications"
    ]);

    const provinceChoice = config.selected_province || "34 - İstanbul";
    const province = findProvince(provinceChoice);
    const timingsData = await fetchPrayerTimings(province);
    const rem = calculateRemaining(timingsData);

    // 1. Action Badge ve Tooltip Güncellemesi
    const badgeMode = config.badge_mode ?? "countdown";
    if (badgeMode === "countdown") {
      let badgeText = "";
      if (rem.hours > 0) {
        badgeText = `${rem.hours}s${rem.minutes}d`;
      } else {
        badgeText = `${rem.minutes}d`;
      }
      await chrome.action.setBadgeText({ text: badgeText });
      await chrome.action.setBadgeBackgroundColor({ color: "#10b981" });
    } else if (badgeMode === "prayer_name") {
      const shortNames = {
        imsak: "İMSK",
        gunes: "GÜNŞ",
        ogle: "ÖĞLE",
        ikindi: "İKND",
        aksam: "AKŞM",
        yatsi: "YATS"
      };
      await chrome.action.setBadgeText({ text: shortNames[rem.nextKey] || "" });
      await chrome.action.setBadgeBackgroundColor({ color: "#f59e0b" });
    } else {
      await chrome.action.setBadgeText({ text: "" });
    }

    // Tooltip
    const tooltip = `Namaz Vakitleri (${province.name})\nSonraki: ${rem.nextName} (${rem.nextTime})\nKalan Süre: ${rem.remainingStr}`;
    await chrome.action.setTitle({ title: tooltip });

    // 2. Bildirim Kontrolü
    const notifyOnPrayer = config.notify_on_prayer ?? true;
    const minutesBefore = config.notify_minutes_before ?? 15;
    const sentList = config.sent_notifications || [];
    const todayStr = new Date().toISOString().split("T")[0];

    // Temizlik: Dünden kalan bildirim tokenlerini sil
    const validSent = sentList.filter((token) => token.startsWith(todayStr));

    // Vakit Girdi Bildirimi (1 dakika aralığında)
    const enterToken = `${todayStr}_${rem.nextKey}_entered`;
    if (notifyOnPrayer && rem.totalSeconds <= 70 && !validSent.includes(enterToken)) {
      validSent.push(enterToken);
      await chrome.storage.local.set({ sent_notifications: validSent });

      await chrome.notifications.create(`prayer_entered_${Date.now()}`, {
        type: "basic",
        iconUrl: "icons/icon-128.png",
        title: `🕋 Vakit Girdi: ${rem.nextName} (${rem.nextTime})`,
        message: `${province.name} için ${rem.nextName} namazı vakti girdi. Haydi namaza ve kurtuluşa!`,
        priority: 2
      });
    }

    // Hatırlatma Bildirimi
    if (minutesBefore > 0) {
      const targetSec = minutesBefore * 60;
      const reminderToken = `${todayStr}_${rem.nextKey}_${minutesBefore}m`;
      if (
        rem.totalSeconds >= targetSec - 60 &&
        rem.totalSeconds <= targetSec + 60 &&
        !validSent.includes(reminderToken)
      ) {
        validSent.push(reminderToken);
        await chrome.storage.local.set({ sent_notifications: validSent });

        await chrome.notifications.create(`prayer_reminder_${Date.now()}`, {
          type: "basic",
          iconUrl: "icons/icon-128.png",
          title: `⏳ ${rem.nextName} Vaktine ${minutesBefore} Dakika Kaldı`,
          message: `${province.name} için ${rem.nextName} vakti (${rem.nextTime}) yaklaşıyor.`,
          priority: 1
        });
      }
    }
  } catch (err) {
    console.error("Arka plan güncelleme hatası:", err);
  }
}

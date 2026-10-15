/**
 * Ezan & Namaz Vakitleri - Popup Etkileşim Scripti
 */

import { PROVINCES, findProvince } from "./provinces.js";
import { fetchPrayerTimings, calculateRemaining, PRAYER_NAMES } from "./api.js";
import { getQuoteForToday } from "./quotes.js";

// DOM Elemanları
const provinceSelect = document.getElementById("provinceSelect");
const btnRefresh = document.getElementById("btnRefresh");
const btnTheme = document.getElementById("btnTheme");
const btnSettings = document.getElementById("btnSettings");
const btnCloseSettings = document.getElementById("btnCloseSettings");
const settingsDrawer = document.getElementById("settingsDrawer");

const miladiDateEl = document.getElementById("miladiDate");
const hijriDateEl = document.getElementById("hijriDate");

const countdownTitleEl = document.getElementById("countdownTitle");
const timerDisplayEl = document.getElementById("timerDisplay");
const progressBarEl = document.getElementById("progressBar");
const currPrayerNameEl = document.getElementById("currPrayerName");
const nextPrayerNameEl = document.getElementById("nextPrayerName");
const nextPrayerTimeEl = document.getElementById("nextPrayerTime");

const prayersGridEl = document.getElementById("prayersGrid");

const quoteTypeEl = document.getElementById("quoteType");
const quoteTextEl = document.getElementById("quoteText");
const quoteSourceEl = document.getElementById("quoteSource");

const chkNotifyPrayer = document.getElementById("chkNotifyPrayer");
const selectRemindMinutes = document.getElementById("selectRemindMinutes");
const selectBadgeMode = document.getElementById("selectBadgeMode");

let currentTimingsData = null;
let timerInterval = null;

// Başlatıcı
document.addEventListener("DOMContentLoaded", async () => {
  initProvinceDropdown();
  await loadTheme();
  await loadSettings();
  renderQuote();
  renderPrayerGridSkeleton();

  await loadCurrentProvinceTimings();

  // Canlı sayaç döngüsü
  timerInterval = setInterval(updateLiveTimer, 1000);

  // Olay dinleyicileri
  provinceSelect.addEventListener("change", onProvinceChange);
  btnRefresh.addEventListener("click", () => loadCurrentProvinceTimings(true));
  btnTheme.addEventListener("click", toggleTheme);
  btnSettings.addEventListener("click", () => settingsDrawer.classList.add("open"));
  btnCloseSettings.addEventListener("click", () => settingsDrawer.classList.remove("open"));

  // Ayar değişiklikleri
  chkNotifyPrayer.addEventListener("change", saveSettings);
  selectRemindMinutes.addEventListener("change", saveSettings);
  selectBadgeMode.addEventListener("change", saveSettings);
});

function initProvinceDropdown() {
  provinceSelect.innerHTML = "";
  PROVINCES.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = `${p.plate} - ${p.name}`;
    opt.textContent = `${p.plate} - ${p.name}`;
    provinceSelect.appendChild(opt);
  });
}

async function loadTheme() {
  const data = await chrome.storage.local.get(["theme_mode"]);
  const theme = data.theme_mode || "dark";
  document.documentElement.setAttribute("data-theme", theme);
  btnTheme.textContent = theme === "dark" ? "🌙" : "☀️";
}

async function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  btnTheme.textContent = next === "dark" ? "🌙" : "☀️";
  await chrome.storage.local.set({ theme_mode: next });
}

async function loadSettings() {
  const data = await chrome.storage.local.get([
    "selected_province",
    "notify_on_prayer",
    "notify_minutes_before",
    "badge_mode"
  ]);

  if (data.selected_province) {
    provinceSelect.value = data.selected_province;
  } else {
    provinceSelect.value = "34 - İstanbul";
  }

  chkNotifyPrayer.checked = data.notify_on_prayer ?? true;
  selectRemindMinutes.value = String(data.notify_minutes_before ?? 15);
  selectBadgeMode.value = data.badge_mode ?? "countdown";
}

async function saveSettings() {
  await chrome.storage.local.set({
    notify_on_prayer: chkNotifyPrayer.checked,
    notify_minutes_before: parseInt(selectRemindMinutes.value, 10),
    badge_mode: selectBadgeMode.value
  });
}

async function onProvinceChange() {
  const choice = provinceSelect.value;
  await chrome.storage.local.set({ selected_province: choice });
  await loadCurrentProvinceTimings();
}

function renderPrayerGridSkeleton() {
  prayersGridEl.innerHTML = "";
  PRAYER_NAMES.forEach((p) => {
    const card = document.createElement("div");
    card.className = "prayer-card";
    card.id = `card_${p.key}`;
    card.innerHTML = `
      <div class="prayer-icon">${p.icon}</div>
      <div class="prayer-name">${p.name}</div>
      <div class="prayer-time" id="time_${p.key}">--:--</div>
      <span class="prayer-badge" id="badge_${p.key}"></span>
    `;
    prayersGridEl.appendChild(card);
  });
}

function renderQuote() {
  const quote = getQuoteForToday();
  quoteTypeEl.textContent = `Günün ${quote.type}`;
  quoteTextEl.textContent = `“${quote.text}”`;
  quoteSourceEl.textContent = `— ${quote.source}`;
}

async function loadCurrentProvinceTimings(force = false) {
  try {
    timerDisplayEl.textContent = "--:--:--";
    const choice = provinceSelect.value || "34 - İstanbul";
    const province = findProvince(choice);

    const data = await fetchPrayerTimings(province, force);
    currentTimingsData = data;

    miladiDateEl.textContent = `📅 ${data.miladiDate}`;
    hijriDateEl.textContent = `🌙 ${data.hijriDate}`;

    // Saatleri kartlara yaz
    PRAYER_NAMES.forEach((p) => {
      const el = document.getElementById(`time_${p.key}`);
      if (el) {
        el.textContent = data.timings[p.key] || "--:--";
      }
    });

    updateLiveTimer();
  } catch (err) {
    console.error("Vakitler yüklenemedi:", err);
    countdownTitleEl.textContent = "Vakitler yüklenirken hata oluştu";
  }
}

function updateLiveTimer() {
  if (!currentTimingsData) return;

  const rem = calculateRemaining(currentTimingsData);

  // Sayaç ve başlık
  timerDisplayEl.textContent = rem.remainingStr;
  countdownTitleEl.textContent = rem.subTitle;
  progressBarEl.style.width = `${Math.round(rem.progress * 100)}%`;

  currPrayerNameEl.textContent = rem.currentName;
  nextPrayerNameEl.textContent = rem.nextName;
  nextPrayerTimeEl.textContent = rem.nextTime;

  // Kart vurguları
  PRAYER_NAMES.forEach((p) => {
    const card = document.getElementById(`card_${p.key}`);
    const badge = document.getElementById(`badge_${p.key}`);
    if (!card || !badge) return;

    card.classList.remove("is-active", "is-next");

    if (p.key === rem.currentKey) {
      card.classList.add("is-active");
      badge.textContent = "Şu An";
    } else if (p.key === rem.nextKey) {
      card.classList.add("is-next");
      badge.textContent = "Sonraki";
    } else {
      badge.textContent = "";
    }
  });
}

"""
Namaz Vakitleri - Modern Windows Masaüstü Arayüzü (CustomTkinter).
81 İl Desteği, Canlı Geri Sayım, Vakit Kartları, Bildirim ve Ayarlar.
"""

import os
import sys
import threading
from datetime import datetime, date
from typing import Dict, Any, Optional

import customtkinter as ctk
from PIL import Image

from provinces import PROVINCES, get_display_list, find_province
from namaz_api import NamazAPI, PRAYER_NAMES
from quotes import get_quote_for_today
from config import ConfigManager
from notifications import NotificationManager
from tray import TrayIconManager

# Renk paletleri
ACCENT_GREEN = "#10b981"
ACCENT_GREEN_HOVER = "#059669"
ACCENT_GOLD = "#f59e0b"
CARD_BG_DARK = "#1e293b"
CARD_BG_LIGHT = "#f1f5f9"
ACTIVE_CARD_DARK = "#064e3b"
ACTIVE_CARD_LIGHT = "#d1fae5"
NEXT_CARD_DARK = "#451a03"
NEXT_CARD_LIGHT = "#fef3c7"


class SettingsWindow(ctk.CTkToplevel):
    """Kullanıcı Tercihleri ve Ayarlar Penceresi"""
    def __init__(self, parent, config_manager: ConfigManager, on_save: Optional[callable] = None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.on_save = on_save

        self.title("Uygulama Ayarları")
        self.geometry("450x420")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()

        self._init_ui()

    def _init_ui(self):
        pad_x, pad_y = 24, 14

        # Başlık
        title_lbl = ctk.CTkLabel(
            self,
            text="⚙️ Tercihler & Bildirim Ayarları",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_lbl.pack(pady=(20, 15), padx=pad_x, anchor="w")

        # 1. Vakit Girdiğinde Bildirim
        self.notify_on_prayer_var = ctk.BooleanVar(value=self.config_manager.get("notify_on_prayer", True))
        chk1 = ctk.CTkCheckBox(
            self,
            text="Namaz vakti girdiğinde Windows bildirimi göster",
            variable=self.notify_on_prayer_var,
            font=ctk.CTkFont(size=13),
            checkbox_height=20,
            checkbox_width=20
        )
        chk1.pack(pady=pad_y, padx=pad_x, anchor="w")

        # 2. Önceden Hatırlatma
        frame_rem = ctk.CTkFrame(self, fg_color="transparent")
        frame_rem.pack(pady=pad_y, padx=pad_x, fill="x")

        lbl_rem = ctk.CTkLabel(frame_rem, text="Vakitten önce hatırlatıcı:", font=ctk.CTkFont(size=13))
        lbl_rem.pack(side="left")

        current_rem = str(self.config_manager.get("notify_minutes_before", 15))
        self.combo_rem = ctk.CTkComboBox(
            frame_rem,
            values=["Kapalı", "5 dakika önce", "10 dakika önce", "15 dakika önce", "30 dakika önce"],
            state="readonly",
            width=180
        )
        rem_map_rev = {"0": "Kapalı", "5": "5 dakika önce", "10": "10 dakika önce", "15": "15 dakika önce", "30": "30 dakika önce"}
        self.combo_rem.set(rem_map_rev.get(current_rem, "15 dakika önce"))
        self.combo_rem.pack(side="right")

        # 3. Sesli Uyarı
        self.sound_var = ctk.BooleanVar(value=self.config_manager.get("sound_enabled", True))
        chk2 = ctk.CTkCheckBox(
            self,
            text="Bildirimlerde zarif sesli uyarı çal",
            variable=self.sound_var,
            font=ctk.CTkFont(size=13),
            checkbox_height=20,
            checkbox_width=20
        )
        chk2.pack(pady=pad_y, padx=pad_x, anchor="w")

        # 4. Kapatıldığında Sistem Tepsisine Küçült
        self.tray_var = ctk.BooleanVar(value=self.config_manager.get("minimize_to_tray", True))
        chk3 = ctk.CTkCheckBox(
            self,
            text="Pencere kapatıldığında arka planda (tepside) çalışmaya devam et",
            variable=self.tray_var,
            font=ctk.CTkFont(size=13),
            checkbox_height=20,
            checkbox_width=20
        )
        chk3.pack(pady=pad_y, padx=pad_x, anchor="w")

        # Butonlar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(25, 10), padx=pad_x, fill="x")

        btn_save = ctk.CTkButton(
            btn_frame,
            text="Kaydet ve Kapat",
            fg_color=ACCENT_GREEN,
            hover_color=ACCENT_GREEN_HOVER,
            command=self._save_settings,
            height=36
        )
        btn_save.pack(side="right", padx=(10, 0))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="gray",
            hover_color="#555555",
            command=self.destroy,
            height=36,
            width=80
        )
        btn_cancel.pack(side="right")

    def _save_settings(self):
        rem_text = self.combo_rem.get()
        rem_min = 0
        if "5" in rem_text:
            rem_min = 5
        elif "10" in rem_text:
            rem_min = 10
        elif "15" in rem_text:
            rem_min = 15
        elif "30" in rem_text:
            rem_min = 30

        self.config_manager.set("notify_on_prayer", self.notify_on_prayer_var.get())
        self.config_manager.set("notify_minutes_before", rem_min)
        self.config_manager.set("sound_enabled", self.sound_var.get())
        self.config_manager.set("minimize_to_tray", self.tray_var.get())

        if self.on_save:
            self.on_save()
        self.destroy()


class NamazVaktiApp(ctk.CTk):
    def __init__(self, base_dir: str):
        super().__init__()
        self.base_dir = base_dir
        self.assets_dir = os.path.join(base_dir, "assets")

        # Bileşenler
        self.config_mgr = ConfigManager(base_dir)
        self.api = NamazAPI(base_dir)
        self.notifier = NotificationManager(self.assets_dir)

        # Tema modu
        theme_mode = self.config_mgr.get("theme_mode", "dark")
        ctk.set_appearance_mode(theme_mode)
        ctk.set_default_color_theme("green")

        # Pencere Boyut ve Konumu
        self.title("Ezan & Namaz Vakitleri (Türkiye)")
        self.geometry("920x760")
        self.minsize(860, 720)

        # İkon yükleme
        ico_path = os.path.join(self.assets_dir, "icon.ico")
        png_path = os.path.join(self.assets_dir, "icon.png")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # Sistem Tepsisi
        self.tray_mgr = TrayIconManager(
            png_path,
            on_show=self._show_window,
            on_exit=self._exit_app
        )
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Durum değişkenleri
        self.current_data: Optional[Dict[str, Any]] = None
        self.current_rem: Optional[Dict[str, Any]] = None
        self.last_fetch_date: Optional[date] = None
        self.is_fetching = False

        # Arayüzü oluştur
        self._build_ui()

        # Sistem tepsisini başlat
        self.tray_mgr.start("Namaz Vakitleri")

        # İlk veri yüklemesi
        self._load_province_timings(initial=True)

        # Canlı sayaç döngüsü
        self._tick()

    def _build_ui(self):
        # Ana Taşıyıcı
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. Üst Başlık & Kontrol Çubuğu
        self._build_header()

        # 2. Tarih Şeridi
        self._build_date_bar()

        # 3. Canlı Geri Sayım & Durum Alanı (Hero Card)
        self._build_hero_card()

        # 4. 6 Namaz Vakti Kartları
        self._build_prayer_grid()

        # 5. Günün Ayeti / Hadisi Kartı
        self._build_quote_card()

        # 6. Alt Bilgi Çubuğu
        self._build_footer()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        # Sol: Logo ve Başlık
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left", fill="y")

        lbl_icon = ctk.CTkLabel(title_box, text="🕌", font=ctk.CTkFont(size=28))
        lbl_icon.pack(side="left", padx=(0, 10))

        lbl_app_name = ctk.CTkLabel(
            title_box,
            text="Namaz Vakitleri",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_app_name.pack(side="left")

        # Sağ: İl Seçimi ve Hızlı Aksiyon Butonları
        actions_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_box.pack(side="right", fill="y")

        # 81 İl Dropdown
        saved_province = self.config_mgr.get("selected_province", "34 - İstanbul")
        self.province_combo = ctk.CTkComboBox(
            actions_box,
            values=get_display_list(),
            command=self._on_province_change,
            width=210,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.province_combo.set(saved_province)
        self.province_combo.pack(side="left", padx=(0, 8))

        # Yenile Butonu
        btn_refresh = ctk.CTkButton(
            actions_box,
            text="🔄",
            width=36,
            height=32,
            command=lambda: self._load_province_timings(force=True),
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35")
        )
        btn_refresh.pack(side="left", padx=(0, 6))

        # Ses Açık/Kapalı Butonu
        sound_on = self.config_mgr.get("sound_enabled", True)
        self.btn_sound = ctk.CTkButton(
            actions_box,
            text="🔊" if sound_on else "🔇",
            width=36,
            height=32,
            command=self._toggle_sound,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35")
        )
        self.btn_sound.pack(side="left", padx=(0, 6))

        # Koyu / Açık Tema Değiştirici
        self.btn_theme = ctk.CTkButton(
            actions_box,
            text="🌙" if ctk.get_appearance_mode() == "Dark" else "☀️",
            width=36,
            height=32,
            command=self._toggle_theme,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35")
        )
        self.btn_theme.pack(side="left", padx=(0, 6))

        # Ayarlar Butonu
        btn_settings = ctk.CTkButton(
            actions_box,
            text="⚙️",
            width=36,
            height=32,
            command=self._open_settings,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35")
        )
        btn_settings.pack(side="left")

    def _build_date_bar(self):
        date_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        date_bar.pack(fill="x", pady=(0, 15))

        # Miladi Tarih Rozeti
        self.lbl_miladi = ctk.CTkLabel(
            date_bar,
            text="📅 Yükleniyor...",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("gray85", "#1e293b"),
            corner_radius=8,
            padx=14,
            pady=6
        )
        self.lbl_miladi.pack(side="left", padx=(0, 10))

        # Hicri Tarih Rozeti
        self.lbl_hijri = ctk.CTkLabel(
            date_bar,
            text="🌙 Hicri Tarih",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ACCENT_GOLD,
            fg_color=("gray85", "#1e293b"),
            corner_radius=8,
            padx=14,
            pady=6
        )
        self.lbl_hijri.pack(side="left")

        # Şehir Başlığı Göstergesi
        self.lbl_location = ctk.CTkLabel(
            date_bar,
            text="📍 İstanbul",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ACCENT_GREEN,
            padx=10
        )
        self.lbl_location.pack(side="right")

    def _build_hero_card(self):
        self.hero_card = ctk.CTkFrame(
            self.main_container,
            corner_radius=16,
            fg_color=("#e2e8f0", CARD_BG_DARK),
            border_width=2,
            border_color=("#cbd5e1", "#334155")
        )
        self.hero_card.pack(fill="x", pady=(0, 20), padx=2)

        content = ctk.CTkFrame(self.hero_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)

        # Üst Etiket
        self.lbl_countdown_title = ctk.CTkLabel(
            content,
            text="Sonraki Vakte Kalan Süre",
            font=ctk.CTkFont(size=15, weight="normal"),
            text_color=("gray40", "gray70")
        )
        self.lbl_countdown_title.pack(anchor="center")

        # Büyük Dijital Sayaç
        self.lbl_timer = ctk.CTkLabel(
            content,
            text="00:00:00",
            font=ctk.CTkFont(family="Consolas", size=54, weight="bold"),
            text_color=(ACCENT_GREEN_HOVER, ACCENT_GREEN)
        )
        self.lbl_timer.pack(anchor="center", pady=(4, 10))

        # İlerleme Çubuğu (Progress bar)
        self.progress_bar = ctk.CTkProgressBar(
            content,
            height=10,
            corner_radius=5,
            progress_color=ACCENT_GREEN
        )
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x", padx=40, pady=(0, 10))

        # Alt Vakit Bilgisi Satırı
        self.lbl_current_next_info = ctk.CTkLabel(
            content,
            text="Şu Anki Vakit: ... • Sonraki Vakit: ...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "gray85")
        )
        self.lbl_current_next_info.pack(anchor="center")

    def _build_prayer_grid(self):
        # 6 Namaz Vakti Kutuları
        grid_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 20))

        grid_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="prayer_col")

        self.prayer_cards = {}
        prayer_icons = {
            "imsak": "🌅",
            "gunes": "☀️",
            "ogle": "🌤️",
            "ikindi": "🌇",
            "aksam": "🌆",
            "yatsi": "🌙"
        }

        for idx, (key, name_tr, _, desc) in enumerate(PRAYER_NAMES):
            card = ctk.CTkFrame(
                grid_frame,
                corner_radius=12,
                fg_color=("#f1f5f9", CARD_BG_DARK),
                border_width=2,
                border_color=("#e2e8f0", "#334155")
            )
            card.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")

            # İkon ve İsim
            lbl_icon = ctk.CTkLabel(
                card,
                text=prayer_icons.get(key, "⏰"),
                font=ctk.CTkFont(size=22)
            )
            lbl_icon.pack(pady=(12, 2))

            lbl_name = ctk.CTkLabel(
                card,
                text=name_tr,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl_name.pack()

            # Saat
            lbl_time = ctk.CTkLabel(
                card,
                text="--:--",
                font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
                text_color=("gray10", "white")
            )
            lbl_time.pack(pady=(4, 6))

            # Açıklama / Alt Başlık (Örn: Sahur Sonu / İftar)
            lbl_desc = ctk.CTkLabel(
                card,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color=("gray50", "gray60")
            )
            lbl_desc.pack(pady=(0, 6))

            # Durum Rozeti (Şu Anki / Sonraki)
            lbl_status = ctk.CTkLabel(
                card,
                text="",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=22,
                corner_radius=6,
                padx=6
            )
            lbl_status.pack(pady=(0, 12))

            self.prayer_cards[key] = {
                "card": card,
                "lbl_time": lbl_time,
                "lbl_status": lbl_status,
                "name": name_tr
            }

    def _build_quote_card(self):
        self.quote_card = ctk.CTkFrame(
            self.main_container,
            corner_radius=12,
            fg_color=("#e2e8f0", CARD_BG_DARK),
            border_width=1,
            border_color=("#cbd5e1", "#334155")
        )
        self.quote_card.pack(fill="x", pady=(0, 15), padx=2)

        content = ctk.CTkFrame(self.quote_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=16)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 6))

        self.lbl_quote_type = ctk.CTkLabel(
            header,
            text="✨ Günün Ayet-i Kerîmesi",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ACCENT_GOLD
        )
        self.lbl_quote_type.pack(side="left")

        self.lbl_quote_text = ctk.CTkLabel(
            content,
            text="“Şüphesiz namaz, müminlere belirli vakitlerde farz kılınmıştır.”",
            font=ctk.CTkFont(size=14, slant="italic"),
            wraplength=800,
            justify="left"
        )
        self.lbl_quote_text.pack(anchor="w", pady=(0, 6))

        self.lbl_quote_source = ctk.CTkLabel(
            content,
            text="— Nisâ Sûresi, 103",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray60")
        )
        self.lbl_quote_source.pack(anchor="e")

        # Günün sözünü yükle
        self._update_quote()

    def _build_footer(self):
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x", pady=(5, 5))

        lbl_credit = ctk.CTkLabel(
            footer,
            text="Kaynak: T.C. Diyanet İşleri Başkanlığı • Çevrimdışı Önbellek Desteği Mevcuttur",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50")
        )
        lbl_credit.pack(side="left")

        # Sistem tepsisine küçült butonu
        btn_tray = ctk.CTkButton(
            footer,
            text="📥 Simge Durumuna Küçült",
            font=ctk.CTkFont(size=12),
            height=28,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35"),
            text_color=("gray20", "gray85"),
            command=self._minimize_to_tray
        )
        btn_tray.pack(side="right")

    def _update_quote(self):
        quote = get_quote_for_today()
        self.lbl_quote_type.configure(text=f"✨ Günün {quote['type']}")
        self.lbl_quote_text.configure(text=f"“{quote['text']}”")
        self.lbl_quote_source.configure(text=f"— {quote['source']}")

    def _on_province_change(self, choice: str):
        self.config_mgr.set("selected_province", choice)
        self._load_province_timings(force=False)

    def _toggle_sound(self):
        cur = self.config_mgr.get("sound_enabled", True)
        new_val = not cur
        self.config_mgr.set("sound_enabled", new_val)
        self.btn_sound.configure(text="🔊" if new_val else "🔇")

    def _toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.config_mgr.set("theme_mode", new_mode.lower())
        self.btn_theme.configure(text="🌙" if new_mode == "Dark" else "☀️")
        self._update_card_styles()

    def _open_settings(self):
        SettingsWindow(self, self.config_mgr, on_save=self._on_settings_saved)

    def _on_settings_saved(self):
        sound_on = self.config_mgr.get("sound_enabled", True)
        self.btn_sound.configure(text="🔊" if sound_on else "🔇")

    def _load_province_timings(self, force: bool = False, initial: bool = False):
        if self.is_fetching:
            return

        choice = self.province_combo.get()
        province = find_province(choice)
        self.lbl_location.configure(text=f"📍 {province['name']}")

        def _fetch_thread():
            self.is_fetching = True
            try:
                data = self.api.fetch_timings(province, force_refresh=force)
                self.after(0, lambda: self._apply_timings(data))
            except Exception as e:
                self.after(0, lambda: self._show_error_banner(str(e)))
            finally:
                self.is_fetching = False

        threading.Thread(target=_fetch_thread, daemon=True).start()

    def _apply_timings(self, data: Dict[str, Any]):
        self.current_data = data
        self.last_fetch_date = date.today()

        # Tarihler
        self.lbl_miladi.configure(text=f"📅 {data['miladi_date']}")
        self.lbl_hijri.configure(text=f"🌙 {data['hijri_date']}")

        # 6 Namaz Saati
        timings = data["timings"]
        for key in timings:
            if key in self.prayer_cards:
                self.prayer_cards[key]["lbl_time"].configure(text=timings[key])

        # Anlık hesapla
        self._update_countdown()

    def _show_error_banner(self, err_msg: str):
        self.lbl_countdown_title.configure(text=f"⚠️ Vakitler alınırken hata oluştu (Önbellek kullanılıyor olabilir): {err_msg[:40]}")

    def _tick(self):
        """Her 1 saniyede bir çağrılır"""
        # Gece yarısı kontrolü (gün değiştiğinde otomatik yenile)
        today = date.today()
        if self.last_fetch_date and today != self.last_fetch_date:
            self._load_province_timings(force=True)
            self._update_quote()

        if self.current_data:
            self._update_countdown()

        # 1 saniye sonra tekrar tetikle
        self.after(1000, self._tick)

    def _update_countdown(self):
        if not self.current_data:
            return

        rem = self.api.calculate_remaining(self.current_data)
        self.current_rem = rem

        # 1. Büyük Dijital Sayaç
        self.lbl_timer.configure(text=rem["remaining_str"])
        self.lbl_countdown_title.configure(text=rem["sub_title"])

        # 2. İlerleme Çubuğu
        self.progress_bar.set(rem["progress"])

        # 3. Özet Bilgi Satırı
        curr_name = rem["current_prayer_name"]
        next_name = rem["next_prayer_name"]
        next_time = rem["next_prayer_time"]
        self.lbl_current_next_info.configure(
            text=f"Şu Anki Vakit: {curr_name}  •  Sonraki Vakit: {next_name} ({next_time})"
        )

        # 4. Kart Stilleri ve Rozetleri Güncelle
        self._update_card_styles()

        # 5. Bildirimleri Denetle
        province_name = self.current_data["province"]["name"]
        self.notifier.check_and_notify(rem, province_name, self.config_mgr)

        # 6. Sistem Tepsisi Tooltip Güncellemesi
        tray_tooltip = f"Namaz Vakitleri ({province_name})\nSonraki: {next_name} ({next_time})\nKalan: {rem['remaining_str']}"
        self.tray_mgr.update_tooltip(tray_tooltip)

    def _update_card_styles(self):
        if not self.current_rem:
            return

        curr_key = self.current_rem["current_prayer_key"]
        next_key = self.current_rem["next_prayer_key"]
        is_dark = ctk.get_appearance_mode() == "Dark"

        for key, widgets in self.prayer_cards.items():
            card = widgets["card"]
            lbl_status = widgets["lbl_status"]

            if key == curr_key:
                # Aktif vakit (Zümrüt Yeşili Vurgu)
                card.configure(
                    fg_color=ACTIVE_CARD_DARK if is_dark else ACTIVE_CARD_LIGHT,
                    border_color=ACCENT_GREEN,
                    border_width=2
                )
                lbl_status.configure(
                    text="Şu Anki Vakit",
                    fg_color=ACCENT_GREEN,
                    text_color="white"
                )
            elif key == next_key:
                # Sonraki vakit (Altın Sarısı Vurgu)
                card.configure(
                    fg_color=NEXT_CARD_DARK if is_dark else NEXT_CARD_LIGHT,
                    border_color=ACCENT_GOLD,
                    border_width=2
                )
                lbl_status.configure(
                    text="Sonraki Vakit",
                    fg_color=ACCENT_GOLD,
                    text_color="black"
                )
            else:
                # Diğer vakitler (Standart kart)
                card.configure(
                    fg_color=CARD_BG_DARK if is_dark else CARD_BG_LIGHT,
                    border_color="#334155" if is_dark else "#e2e8f0",
                    border_width=1
                )
                lbl_status.configure(
                    text="",
                    fg_color="transparent"
                )

    def _minimize_to_tray(self):
        self.withdraw()

    def _show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def _on_window_close(self):
        if self.config_mgr.get("minimize_to_tray", True):
            self._minimize_to_tray()
        else:
            self._exit_app()

    def _exit_app(self):
        self.tray_mgr.stop()
        self.destroy()
        sys.exit(0)

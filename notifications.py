"""
Windows Bildirim ve Ses Yönetimi.
Windows 10/11 yerel toast bildirimleri (winotify) ve ses uyarıları.
"""

import os
import threading
from datetime import date
from typing import Dict, Any, Set
import winsound

try:
    from winotify import Notification, audio
    HAS_WINOTIFY = True
except ImportError:
    HAS_WINOTIFY = False


class NotificationManager:
    def __init__(self, assets_dir: str):
        self.assets_dir = assets_dir
        self.icon_path = os.path.join(assets_dir, "icon.png")
        if not os.path.exists(self.icon_path):
            self.icon_path = ""
        self._sent_notifications: Set[str] = set()
        self._current_date_str = date.today().strftime("%Y-%m-%d")

    def _play_sound(self):
        """Arka planda hoş ve yumuşak bir bildirim sesi çalar"""
        def _beep():
            try:
                # Windows hoş sistem sesi
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            except Exception:
                try:
                    # Alternatif üçlü zarif ton
                    winsound.Beep(523, 150)  # C5
                    winsound.Beep(659, 150)  # E5
                    winsound.Beep(784, 300)  # G5
                except Exception:
                    pass
        threading.Thread(target=_beep, daemon=True).start()

    def send_toast(self, title: str, message: str, sound: bool = True):
        """Windows yerel bildirim kutusu gösterir"""
        if sound:
            self._play_sound()

        if HAS_WINOTIFY:
            try:
                toast = Notification(
                    app_id="Ezan & Namaz Vakitleri",
                    title=title,
                    msg=message,
                    icon=self.icon_path if os.path.exists(self.icon_path) else None
                )
                toast.set_audio(audio.Default, loop=False)
                toast.show()
                return
            except Exception:
                pass

        # Fallback: winsound beep
        try:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception:
            pass

    def check_and_notify(self, rem_info: Dict[str, Any], province_name: str, config: Any):
        """
        Geri sayım saniyelerine göre vakit girdiğinde veya hatırlatma dakikasında bildirim gönderir.
        """
        today_str = date.today().strftime("%Y-%m-%d")
        if today_str != self._current_date_str:
            self._current_date_str = today_str
            self._sent_notifications.clear()

        remaining_sec = rem_info.get("remaining_seconds", 0)
        next_key = rem_info.get("next_prayer_key", "")
        next_name = rem_info.get("next_prayer_name", "")
        next_time = rem_info.get("next_prayer_time", "")

        sound_enabled = config.get("sound_enabled", True)
        notify_on_prayer = config.get("notify_on_prayer", True)
        notify_minutes_before = config.get("notify_minutes_before", 15)

        # 1. Vakit Girdi Bildirimi (0 - 5 saniye aralığında tetiklenir)
        enter_token = f"{today_str}_{next_key}_entered"
        if notify_on_prayer and remaining_sec <= 2 and enter_token not in self._sent_notifications:
            self._sent_notifications.add(enter_token)
            title = f"🕋 Vakit Girdi: {next_name} ({next_time})"
            msg = f"{province_name} için {next_name} namazı vakti girdi. Haydi namaza ve kurtuluşa!"
            self.send_toast(title, msg, sound=sound_enabled)

        # 2. Hatırlatma Bildirimi (Örn: 15 veya 30 dakika kala)
        if notify_minutes_before > 0:
            target_sec = notify_minutes_before * 60
            reminder_token = f"{today_str}_{next_key}_{notify_minutes_before}m"
            if target_sec - 2 <= remaining_sec <= target_sec + 2 and reminder_token not in self._sent_notifications:
                self._sent_notifications.add(reminder_token)
                title = f"⏳ {next_name} Vaktine {notify_minutes_before} Dakika Kaldı"
                msg = f"{province_name} için {next_name} vakti ({next_time}) yaklaşıyor."
                self.send_toast(title, msg, sound=sound_enabled)

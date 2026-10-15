"""
Windows Sistem Tepsisi (System Tray) Entegrasyonu.
pystray kütüphanesi kullanarak arka planda çalışmayı sağlar.
"""

import threading
from typing import Callable, Optional
from PIL import Image

try:
    import pystray
    from pystray import MenuItem as item
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False


class TrayIconManager:
    def __init__(self, icon_path: str, on_show: Callable[[], None], on_exit: Callable[[], None]):
        self.icon_path = icon_path
        self.on_show = on_show
        self.on_exit = on_exit
        self.tray_icon: Optional[pystray.Icon] = None
        self._is_running = False

    def start(self, initial_title: str = "Namaz Vakitleri"):
        if not HAS_PYSTRAY:
            return

        try:
            image = Image.open(self.icon_path)
        except Exception:
            # Fallback küçük görsel
            image = Image.new("RGBA", (64, 64), (16, 60, 46, 255))

        menu = pystray.Menu(
            item("Pencereyi Göster", self._handle_show, default=True),
            pystray.Menu.SEPARATOR,
            item("Çıkış", self._handle_exit)
        )

        self.tray_icon = pystray.Icon(
            "NamazVaktiApp",
            image,
            initial_title,
            menu=menu
        )

        def _run_loop():
            self._is_running = True
            try:
                self.tray_icon.run()
            except Exception:
                pass
            self._is_running = False

        threading.Thread(target=_run_loop, daemon=True).start()

    def update_tooltip(self, title: str):
        if self.tray_icon and self._is_running:
            try:
                self.tray_icon.title = title
            except Exception:
                pass

    def _handle_show(self, icon, item):
        if self.on_show:
            self.on_show()

    def _handle_exit(self, icon, item):
        self.stop()
        if self.on_exit:
            self.on_exit()

    def stop(self):
        if self.tray_icon and self._is_running:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
            self._is_running = False

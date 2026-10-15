"""
Ezan & Namaz Vakitleri - Ana Başlatıcı (Main Entry Point).
Windows işletim sistemli bilgisayarlar için Türkiye illerine göre namaz vakitleri uygulaması.
"""

import os
import sys
import ctypes

# Windows görev çubuğu ve bildirim entegrasyonu için App ID kaydı
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Diyanet.NamazVakitleri.App.1.0")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from generate_assets import create_app_icon
from app_ui import NamazVaktiApp


def main():
    # Varlıkların (ikonların) varlığını doğrula, yoksa otomatik üret
    assets_dir = os.path.join(BASE_DIR, "assets")
    ico_path = os.path.join(assets_dir, "icon.ico")
    if not os.path.exists(ico_path):
        create_app_icon(assets_dir)

    # Uygulamayı başlat
    app = NamazVaktiApp(BASE_DIR)
    app.mainloop()


if __name__ == "__main__":
    main()

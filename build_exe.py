"""
PyInstaller ile Windows Standalone (.exe) Derleyici.
Tüm bağımlılıkları ve ikon varlıklarını tek bir çalıştırılabilir dosyada paketler.
"""

import os
import subprocess
import sys

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(base_dir, "main.py")
    icon_ico = os.path.join(base_dir, "assets", "icon.ico")
    assets_dir = os.path.join(base_dir, "assets")

    # CustomTkinter veri dosyaları dizinini bul
    import customtkinter
    ctk_dir = os.path.dirname(customtkinter.__file__)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",  # fast startup & reliable asset bundling
        "--windowed",  # no console window
        f"--icon={icon_ico}",
        f"--name=NamazVakti",
        f"--add-data={assets_dir};assets",
        f"--add-data={ctk_dir};customtkinter",
        main_py
    ]

    print("PyInstaller derleme başlatılıyor...")
    print(" ".join(cmd))
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode == 0:
        print("\n[OK] Derleme basariyla tamamlandi! Cikti: dist/NamazVakti/NamazVakti.exe")
    else:
        print(f"\n[FAIL] Derleme hatasi: Kod {res.returncode}")

if __name__ == "__main__":
    build()

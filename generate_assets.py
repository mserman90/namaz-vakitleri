"""
Uygulama İkonu ve Görsel Varlıklarını Oluşturucu.
Pillow kullanarak yüksek çözünürlüklü .ico ve .png ikonları üretir.
"""

import os
import math
from PIL import Image, ImageDraw

def create_app_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Zümrüt Yeşili / Koyu Mavi Degrade Arka Plan (Yuvarlatılmış Kare / Squircle)
    margin = 24
    rect = [margin, margin, size[0] - margin, size[1] - margin]
    radius = 110
    
    # Arka plan yuvarlak kutu
    draw.rounded_rectangle(rect, radius=radius, fill=(10, 38, 29, 255), outline=(212, 175, 55, 230), width=10)

    # İç parlama halkası
    inner_rect = [margin + 16, margin + 16, size[0] - margin - 16, size[1] - margin - 16]
    draw.rounded_rectangle(inner_rect, radius=radius - 12, outline=(24, 75, 58, 180), width=4)

    # 2. Kubbe ve Cami Silueti
    # Kubbe: Merkez (256, 380), Yarıçap 100
    dome_center_x, dome_center_y = 256, 380
    dome_radius = 115
    draw.chord(
        [dome_center_x - dome_radius, dome_center_y - dome_radius, 
         dome_center_x + dome_radius, dome_center_y + dome_radius],
        start=180, end=360, fill=(16, 60, 46, 255), outline=(212, 175, 55, 220), width=4
    )
    # Kubbe tabanı
    draw.rectangle([dome_center_x - dome_radius, dome_center_y, dome_center_x + dome_radius, 430], fill=(16, 60, 46, 255))
    
    # Kubbe Alemi (Hilal ucu)
    alem_x, alem_y = 256, 260
    draw.line([(alem_x, alem_y), (alem_x, 268)], fill=(212, 175, 55, 255), width=6)
    draw.ellipse([alem_x - 6, 250, alem_x + 6, 262], fill=(212, 175, 55, 255))

    # Minareler (Sol ve Sağ)
    for minaret_x in [105, 407]:
        # Gövde
        draw.rectangle([minaret_x - 14, 210, minaret_x + 14, 430], fill=(14, 52, 40, 255), outline=(212, 175, 55, 180), width=3)
        # Şerefe
        draw.rectangle([minaret_x - 20, 260, minaret_x + 20, 275], fill=(212, 175, 55, 255))
        # Külah (Minare çatısı)
        draw.polygon([(minaret_x - 14, 210), (minaret_x + 14, 210), (minaret_x, 150)], fill=(212, 175, 55, 255))
        # Minare Alemi
        draw.line([(minaret_x, 140), (minaret_x, 150)], fill=(255, 220, 100, 255), width=3)

    # 3. Zarif Hilal (Altın Sarısı)
    # Hilal oluşturmak için dış çember ve kesişen iç çember
    moon_img = Image.new("RGBA", size, (0, 0, 0, 0))
    moon_draw = ImageDraw.Draw(moon_img)

    mc_x, mc_y = 256, 175
    m_r = 75
    # Dış çember
    moon_draw.ellipse([mc_x - m_r, mc_y - m_r, mc_x + m_r, mc_y + m_r], fill=(245, 197, 66, 255))
    # İç oyuk çember
    inner_offset_x = mc_x + 24
    inner_offset_y = mc_y - 12
    inner_r = 65
    moon_draw.ellipse([inner_offset_x - inner_r, inner_offset_y - inner_r, 
                       inner_offset_x + inner_r, inner_offset_y + inner_r], fill=(0, 0, 0, 0))

    # Hilali ana resme yapıştır
    img.alpha_composite(moon_img)

    # 4. Parlayan Yıldız
    star_center_x, star_center_y = 230, 160
    star_r_out = 20
    star_r_in = 8
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        r = star_r_out if i % 2 == 0 else star_r_in
        x = star_center_x + r * math.cos(angle)
        y = star_center_y + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=(255, 235, 130, 255))

    # PNG ve ICO olarak kaydet
    png_path = os.path.join(output_dir, "icon.png")
    ico_path = os.path.join(output_dir, "icon.ico")

    # 256x256 PNG
    img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_256.save(png_path, "PNG")

    # Multi-resolution ICO
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format="ICO", sizes=icon_sizes)
    print(f"İkonlar üretildi: {png_path}, {ico_path}")

if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    create_app_icon(target_dir)

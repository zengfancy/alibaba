# -*- coding: utf-8 -*-
"""Alibaba Cloud quarterly revenue + YoY dual-axis chart."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
out = root / "assets" / "alibaba-cloud-revenue-quarterly.png"

rows = [
    ("1Q23", 185.82, -2.0),
    ("2Q23", 251.23, 4.0),
    ("3Q23", 276.48, 2.0),
    ("4Q23", 280.66, 3.0),
    ("1Q24", 255.95, 3.0),
    ("2Q24", 265.49, 5.7),
    ("3Q24", 296.10, 7.1),
    ("4Q24", 317.42, 13.1),
    ("1Q25", 301.27, 17.7),
    ("2Q25", 334.18, 25.9),
    ("3Q25", 398.24, 34.5),
    ("4Q25", 432.84, 36.4),
    ("1Q26", 416.26, 38.2),
    ("2Q26", 484.37, 45.0),
]

W, H = 1100, 620
ML, MR, MT, MB = 70, 70, 80, 70
pw, ph = W - ML - MR, H - MT - MB
img = Image.new("RGB", (W, H), "#FFFFFF")
draw = ImageDraw.Draw(img)


def font(size):
    for name in ("msyh.ttc", "msyh.ttf", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


f_title, f_sub, f_axis, f_lab = font(22), font(13), font(12), font(11)
draw.text((W // 2, 18), "阿里云业务营收（季度）", fill="#1A1A1A", font=f_title, anchor="mt")
draw.text(
    (W // 2, 48),
    "单位：亿元｜日历季度｜收入取公司公告，同比由同季收入重算",
    fill="#666",
    font=f_sub,
    anchor="mt",
)

rev = [r[1] for r in rows]
yoy = [r[2] for r in rows]
ymax_r, ymin_r = 550, 0
ymax_y, ymin_y = 50, -10


def y_rev(v):
    return MT + ph * (1 - (v - ymin_r) / (ymax_r - ymin_r))


def y_yoy(v):
    return MT + ph * (1 - (v - ymin_y) / (ymax_y - ymin_y))


n = len(rows)
bw = pw / n
gap = 0.35
bar_w = bw * (1 - gap)

# grids left
for t in range(0, 551, 100):
    yy = y_rev(t)
    draw.line([(ML, yy), (ML + pw, yy)], fill="#EEEEEE", width=1)
    draw.text((ML - 8, yy), str(t), fill="#555", font=f_axis, anchor="rm")
# right axis labels
for t in range(-10, 51, 10):
    yy = y_yoy(t)
    draw.text((ML + pw + 8, yy), f"{t}%", fill="#5B9BD5", font=f_axis, anchor="lm")

draw.line([(ML, MT), (ML, MT + ph)], fill="#333", width=2)
draw.line([(ML + pw, MT), (ML + pw, MT + ph)], fill="#5B9BD5", width=2)
draw.line([(ML, MT + ph), (ML + pw, MT + ph)], fill="#333", width=2)

centers = []
for i, (lab, rv, _) in enumerate(rows):
    x0 = ML + bw * i + bw * gap / 2
    x1 = x0 + bar_w
    y0 = y_rev(rv)
    draw.rectangle([x0, y0, x1, MT + ph], fill="#2F5D8C")
    cx = (x0 + x1) / 2
    centers.append(cx)
    draw.text((cx, MT + ph + 10), lab, fill="#333", font=f_lab, anchor="mt")

pts = [(centers[i], y_yoy(yoy[i])) for i in range(n)]
draw.line(pts, fill="#5B9BD5", width=3)
for i, (cx, cy) in enumerate(pts):
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill="#5B9BD5")

# legend
draw.rectangle([320, H - 28, 336, H - 12], fill="#2F5D8C")
draw.text((344, H - 20), "营业收入（亿元）", fill="#333", font=f_sub, anchor="lm")
draw.line([(520, H - 20), (560, H - 20)], fill="#5B9BD5", width=3)
draw.ellipse([534, H - 25, 544, H - 15], fill="#5B9BD5")
draw.text((568, H - 20), "同比增速 yoy", fill="#333", font=f_sub, anchor="lm")

img.save(out, "PNG")
print("wrote", out)

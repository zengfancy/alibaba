# -*- coding: utf-8 -*-
"""Render Alibaba revenue + net income on one dual-axis PNG for Markdown preview."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
out = root / "assets" / "alibaba-revenue-net-income-fy2017-2026.png"

rows = [
    (2017, 158273, 41226),
    (2018, 250266, 61412),
    (2019, 376844, 80234),
    (2020, 509711, 140350),
    (2021, 717289, 143284),
    (2022, 853062, 47079),
    (2023, 868687, 65573),
    (2024, 941168, 71332),
    (2025, 996347, 125976),
    (2026, 1023670, 102127),
]
rev = [r[1] / 100 for r in rows]  # 亿元
ni = [r[2] / 100 for r in rows]

W, H = 1120, 660
ML, MR, MT, MB = 78, 78, 96, 96
pw, ph = W - ML - MR, H - MT - MB
ymax_l = max(rev) * 1.12
ymax_r = max(ni) * 1.18
ymin = 0

img = Image.new("RGB", (W, H), "#FFFFFF")
draw = ImageDraw.Draw(img)


def font(size):
    for name in ("msyh.ttc", "msyh.ttf", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


f_title = font(24)
f_sub = font(14)
f_axis = font(13)
f_lab = font(12)
f_leg = font(14)

draw.text((W // 2, 22), "阿里巴巴营业收入与净利润（FY2017–FY2026）", fill="#1A1A1A", font=f_title, anchor="mt")
draw.text(
    (W // 2, 54),
    "单位：亿元｜左轴=营业收入（柱）｜右轴=净利润（线）｜财年截至3月31日｜净利润=合并报表 Net income",
    fill="#666666",
    font=f_sub,
    anchor="mt",
)


def y_left(v):
    return MT + ph * (1 - (v - ymin) / (ymax_l - ymin))


def y_right(v):
    return MT + ph * (1 - (v - ymin) / (ymax_r - ymin))


n = len(rows)
gap = 0.32
bw = pw / n
bar_w = bw * (1 - gap)

# left grid / ticks
step_l = 2000
t = 0
while t <= ymax_l:
    yy = y_left(t)
    draw.line([(ML, yy), (ML + pw, yy)], fill="#EEEEEE", width=1)
    draw.text((ML - 10, yy), f"{int(t)}", fill="#FF6A00", font=f_axis, anchor="rm")
    t += step_l

# right ticks
step_r = 200
t = 0
while t <= ymax_r:
    yy = y_right(t)
    draw.text((ML + pw + 10, yy), f"{int(t)}", fill="#2F5D8C", font=f_axis, anchor="lm")
    t += step_r

draw.line([(ML, MT), (ML, MT + ph)], fill="#FF6A00", width=2)
draw.line([(ML + pw, MT), (ML + pw, MT + ph)], fill="#2F5D8C", width=2)
draw.line([(ML, MT + ph), (ML + pw, MT + ph)], fill="#333333", width=2)

# axis titles
draw.text((18, MT + ph / 2), "营业收入", fill="#FF6A00", font=f_axis, anchor="mm")
draw.text((W - 18, MT + ph / 2), "净利润", fill="#2F5D8C", font=f_axis, anchor="mm")

# bars
bar_centers = []
for i, v in enumerate(rev):
    x0 = ML + bw * i + bw * gap / 2
    x1 = x0 + bar_w
    y0 = y_left(v)
    y1 = y_left(0)
    draw.rectangle([x0, y0, x1, y1], fill="#FF6A00")
    cx = (x0 + x1) / 2
    bar_centers.append(cx)
    draw.text((cx, y0 - 6), f"{v:.0f}", fill="#C45500", font=f_lab, anchor="ms")
    draw.text((cx, MT + ph + 14), str(rows[i][0]), fill="#333333", font=f_axis, anchor="mt")

# NI line on right axis
pts = [(bar_centers[i], y_right(ni[i])) for i in range(n)]
draw.line(pts, fill="#2F5D8C", width=3)
for i, (cx, cy) in enumerate(pts):
    r = 5
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#2F5D8C")
    # offset label slightly so it doesn't collide with bar tops
    draw.text((cx, cy - 14), f"{ni[i]:.0f}", fill="#2F5D8C", font=f_lab, anchor="ms")

# legend
ly = H - 40
draw.rectangle([300, ly - 8, 316, ly + 8], fill="#FF6A00")
draw.text((324, ly), "营业收入（左轴·柱）", fill="#333333", font=f_leg, anchor="lm")
draw.line([(520, ly), (560, ly)], fill="#2F5D8C", width=3)
draw.ellipse([534, ly - 5, 544, ly + 5], fill="#2F5D8C")
draw.text((570, ly), "净利润（右轴·线）", fill="#333333", font=f_leg, anchor="lm")
draw.text((W // 2, H - 12), "来源：公司业绩公告 / 年报（港交所、SEC）", fill="#888888", font=f_sub, anchor="mb")

img.save(out, "PNG")
print("wrote", out)

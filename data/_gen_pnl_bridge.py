# -*- coding: utf-8 -*-
"""Waterfall: 营业收入 → −营业成本 −销售费用 −其他费用 → 营业利润 → +投资损益 → 净利润"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
out = root / "assets" / "alibaba-pnl-bridge-fy25-fy26.png"

# 亿元
years = [
    {
        "title": "FY2025",
        "rev": 9963,
        "cogs": 5983,
        "sell": 1440,
        "op": 1409,
        "inv": 208,
        "ni": 1260,
    },
    {
        "title": "FY2026",
        "rev": 10237,
        "cogs": 6161,
        "sell": 2450,
        "op": 502,
        "inv": 875,
        "ni": 1021,
    },
]

W, H = 1280, 740
img = Image.new("RGB", (W, H), "#FFFFFF")
draw = ImageDraw.Draw(img)


def font(size):
    for name in ("msyh.ttc", "msyh.ttf", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


f_title = font(22)
f_sub = font(12)
f_lab = font(11)
f_num = font(12)

draw.text((W // 2, 16), "净利润形成过程（利润桥）FY2025 vs FY2026", fill="#1A1A1A", font=f_title, anchor="mt")
draw.text(
    (W // 2, 44),
    "单位：亿元｜营业收入 → −营业成本 −销售费用 −其他费用 → 营业利润 → ＋投资损益 → −税息及其他 → 净利润",
    fill="#666666",
    font=f_sub,
    anchor="mt",
)

panel_w = 600
gap = 40
left0 = (W - 2 * panel_w - gap) // 2
top = 70
panel_h = 580


def draw_waterfall(x0, y0, pw, ph, data):
    costs_total = data["rev"] - data["op"]
    other_opex = costs_total - data["cogs"] - data["sell"]
    other = data["op"] + data["inv"] - data["ni"]

    steps = [
        ("营业收入", data["rev"], "total", "#FF6A00"),
        ("−营业成本", -data["cogs"], "float", "#8899AA"),
        ("−销售费用", -data["sell"], "float", "#E67E22"),
        ("−其他费用", -other_opex, "float", "#B0B0B0"),
        ("=营业利润", data["op"], "total", "#2F5D8C"),
        ("+投资损益", data["inv"], "float", "#2E8B57"),
        ("−税息及其他", -other, "float", "#B0B0B0"),
        ("=净利润", data["ni"], "total", "#C0392B"),
    ]

    levels = []
    run = 0
    for name, val, kind, color in steps:
        if kind == "total":
            levels.append((0, val))
            run = val
        else:
            start = run
            end = run + val
            levels.append((min(start, end), max(start, end)))
            run = end

    ymax = max(data["rev"], data["op"] + data["inv"]) * 1.12
    ymin = 0

    ML, MR, MT, MB = 44, 16, 36, 90
    plot_w = pw - ML - MR
    plot_h = ph - MT - MB

    def y_to(v):
        return y0 + MT + plot_h * (1 - (v - ymin) / (ymax - ymin))

    draw.text((x0 + pw // 2, y0 + 6), data["title"], fill="#1A1A1A", font=f_title, anchor="mt")
    draw.line([(x0 + ML, y0 + MT), (x0 + ML, y0 + MT + plot_h)], fill="#333", width=1)
    draw.line([(x0 + ML, y_to(0)), (x0 + ML + plot_w, y_to(0))], fill="#333", width=1)

    n = len(steps)
    bw = plot_w / n
    bar_w = bw * 0.58

    for i, ((name, val, kind, color), (lo, hi)) in enumerate(zip(steps, levels)):
        cx = x0 + ML + bw * i + bw / 2
        x1 = cx - bar_w / 2
        x2 = cx + bar_w / 2
        y1 = y_to(hi)
        y2 = y_to(lo)
        if y2 - y1 < 2:
            y2 = y1 + 2
        draw.rectangle([x1, y1, x2, y2], fill=color)

        if i < n - 1 and steps[i + 1][2] == "float":
            r = 0
            for j in range(i + 1):
                _, v, k, _ = steps[j]
                r = v if k == "total" else r + v
            yy = y_to(r)
            nx1 = x0 + ML + bw * (i + 1) + bw / 2 - bar_w / 2
            draw.line([(x2, yy), (nx1, yy)], fill="#999", width=1)

        label = f"{val:+.0f}" if kind == "float" else f"{val:.0f}"
        draw.text((cx, y1 - 5), label, fill=color, font=f_num, anchor="ms")
        draw.text((cx, y0 + MT + plot_h + 12), name, fill="#333", font=f_lab, anchor="mt")


draw_waterfall(left0, top, panel_w, panel_h, years[0])
draw_waterfall(left0 + panel_w + gap, top, panel_w, panel_h, years[1])

ly = H - 28
items = [
    ("#FF6A00", "营业收入"),
    ("#8899AA", "营业成本"),
    ("#E67E22", "销售费用"),
    ("#2F5D8C", "营业利润"),
    ("#2E8B57", "投资损益"),
    ("#C0392B", "净利润"),
]
x = 120
for c, t in items:
    draw.rectangle([x, ly - 6, x + 12, ly + 6], fill=c)
    draw.text((x + 16, ly), t, fill="#333", font=f_lab, anchor="lm")
    x += 170

img.save(out, "PNG")
print("wrote", out)
for d in years:
    costs = d["rev"] - d["op"]
    other_opex = costs - d["cogs"] - d["sell"]
    other = d["op"] + d["inv"] - d["ni"]
    print(d["title"], "cogs", d["cogs"], "sell", d["sell"], "other_opex", other_opex, "taxish", other)

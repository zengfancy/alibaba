# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
assets = root / "assets"
data_dir = root / "data"
assets.mkdir(exist_ok=True)
data_dir.mkdir(exist_ok=True)

rows = [
    {"fy": 2017, "year_label": "FY2017", "period_end": "2017-03-31", "revenue_rmb_mn": 158273, "net_income_rmb_mn": 41226},
    {"fy": 2018, "year_label": "FY2018", "period_end": "2018-03-31", "revenue_rmb_mn": 250266, "net_income_rmb_mn": 61412},
    {"fy": 2019, "year_label": "FY2019", "period_end": "2019-03-31", "revenue_rmb_mn": 376844, "net_income_rmb_mn": 80234},
    {"fy": 2020, "year_label": "FY2020", "period_end": "2020-03-31", "revenue_rmb_mn": 509711, "net_income_rmb_mn": 140350},
    {"fy": 2021, "year_label": "FY2021", "period_end": "2021-03-31", "revenue_rmb_mn": 717289, "net_income_rmb_mn": 143284},
    {"fy": 2022, "year_label": "FY2022", "period_end": "2022-03-31", "revenue_rmb_mn": 853062, "net_income_rmb_mn": 47079},
    {"fy": 2023, "year_label": "FY2023", "period_end": "2023-03-31", "revenue_rmb_mn": 868687, "net_income_rmb_mn": 65573},
    {"fy": 2024, "year_label": "FY2024", "period_end": "2024-03-31", "revenue_rmb_mn": 941168, "net_income_rmb_mn": 71332},
    {"fy": 2025, "year_label": "FY2025", "period_end": "2025-03-31", "revenue_rmb_mn": 996347, "net_income_rmb_mn": 125976},
    {"fy": 2026, "year_label": "FY2026", "period_end": "2026-03-31", "revenue_rmb_mn": 1023670, "net_income_rmb_mn": 102127},
]

meta = {
    "company": "Alibaba Group Holding Limited",
    "ticker": ["9988.HK", "BABA"],
    "currency": "RMB million",
    "metric_note": "净利润为合并报表 Net income（非归母）；财年截至3月31日",
    "source": [
        "Alibaba FY2017–FY2026 results announcements / annual reports (SEC / HKEX)",
        "FY2026 ARA: https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0513/2026051300653.pdf",
    ],
    "as_of": "2026-09-12",
    "rows": rows,
}
json_path = data_dir / "alibaba_revenue_net_income_fy2017_2026.json"
json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

W, H = 960, 540
ML, MR, MT, MB = 70, 70, 70, 70
pw, ph = W - ML - MR, H - MT - MB
n = len(rows)
gap = 0.28
bw = pw / n
bar_w = bw * (1 - gap)
rev = [r["revenue_rmb_mn"] / 100 for r in rows]  # 亿元
ni = [r["net_income_rmb_mn"] / 100 for r in rows]
ymax = max(rev) * 1.12
ymin = min(0, min(ni) * 1.05)


def y_to(v):
    return MT + ph * (1 - (v - ymin) / (ymax - ymin))


def x_center(i):
    return ML + bw * i + bw / 2


ticks = []
step = 2000 if ymax > 8000 else 1000
t = 0
while t <= ymax:
    ticks.append(t)
    t += step

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
parts.append('<rect width="100%" height="100%" fill="#ffffff"/>')
parts.append(
    '<text x="480" y="36" text-anchor="middle" font-family="Microsoft YaHei, SimHei, sans-serif" '
    'font-size="20" font-weight="700" fill="#1a1a1a">阿里巴巴营业收入与净利润（FY2017–FY2026）</text>'
)
parts.append(
    '<text x="480" y="58" text-anchor="middle" font-family="Microsoft YaHei, SimHei, sans-serif" '
    'font-size="12" fill="#666">单位：亿元人民币｜财年截至3月31日｜净利润=合并报表Net income</text>'
)
parts.append(f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+ph}" stroke="#333" stroke-width="1.2"/>')
parts.append(f'<line x1="{ML}" y1="{MT+ph}" x2="{ML+pw}" y2="{MT+ph}" stroke="#333" stroke-width="1.2"/>')
for tv in ticks:
    yy = y_to(tv)
    parts.append(f'<line x1="{ML}" y1="{yy}" x2="{ML+pw}" y2="{yy}" stroke="#e6e6e6" stroke-width="1"/>')
    parts.append(
        f'<text x="{ML-10}" y="{yy+4}" text-anchor="end" font-family="Segoe UI, sans-serif" '
        f'font-size="11" fill="#555">{int(tv)}</text>'
    )

for i, v in enumerate(rev):
    x = ML + bw * i + bw * gap / 2
    y = y_to(v)
    h = y_to(0) - y
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="#FF6A00" opacity="0.9"/>'
    )
    parts.append(
        f'<text x="{x_center(i):.1f}" y="{y-6:.1f}" text-anchor="middle" '
        f'font-family="Segoe UI, sans-serif" font-size="10" fill="#FF6A00">{v:.0f}</text>'
    )
    parts.append(
        f'<text x="{x_center(i):.1f}" y="{MT+ph+18}" text-anchor="middle" '
        f'font-family="Segoe UI, sans-serif" font-size="11" fill="#333">{rows[i]["year_label"].replace("FY", "")}</text>'
    )

pts = " ".join(f"{x_center(i):.1f},{y_to(v):.1f}" for i, v in enumerate(ni))
parts.append(f'<polyline points="{pts}" fill="none" stroke="#2F5D8C" stroke-width="2.5"/>')
for i, v in enumerate(ni):
    cx, cy = x_center(i), y_to(v)
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#2F5D8C"/>')
    parts.append(
        f'<text x="{cx:.1f}" y="{cy-10:.1f}" text-anchor="middle" '
        f'font-family="Segoe UI, sans-serif" font-size="10" fill="#2F5D8C">{v:.0f}</text>'
    )

parts.append('<rect x="300" y="500" width="14" height="14" fill="#FF6A00"/>')
parts.append(
    '<text x="320" y="512" font-family="Microsoft YaHei, SimHei, sans-serif" font-size="13" fill="#333">营业收入（柱）</text>'
)
parts.append('<line x1="450" y1="507" x2="480" y2="507" stroke="#2F5D8C" stroke-width="2.5"/>')
parts.append('<circle cx="465" cy="507" r="4" fill="#2F5D8C"/>')
parts.append(
    '<text x="490" y="512" font-family="Microsoft YaHei, SimHei, sans-serif" font-size="13" fill="#333">净利润（线）</text>'
)
parts.append(
    '<text x="480" y="532" text-anchor="middle" font-family="Microsoft YaHei, SimHei, sans-serif" '
    'font-size="11" fill="#888">来源：公司业绩公告 / 年报（港交所、SEC）</text>'
)
parts.append("</svg>")

svg_path = assets / "alibaba-revenue-net-income-fy2017-2026.svg"
svg_path.write_text("\n".join(parts), encoding="utf-8")
print("wrote", svg_path)
print("wrote", json_path)

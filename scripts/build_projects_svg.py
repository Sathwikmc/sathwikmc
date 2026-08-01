import json
from xml.sax.saxutils import escape

with open("projects.json") as f:
    projects = json.load(f)

W = 1180
TITLE_H = 36
PAD = 22
COLS = 2
GAP = 20
CARD_W = (W - PAD * 2 - GAP * (COLS - 1)) // COLS
CARD_H = 132
ROWS = (len(projects) + COLS - 1) // COLS
H = TITLE_H + PAD * 2 + ROWS * CARD_H + (ROWS - 1) * GAP

TECH_COLORS = ["#A78BFA", "#22D3EE", "#10B981", "#F59E0B"]

def build_svg(mode):
    is_dark = mode == "dark"
    C = {
        "bg": "#0A101F" if is_dark else "#F5F7FA",
        "panel": "#0D1424" if is_dark else "#FFFFFF",
        "border": "#22D3EE" if is_dark else "#0891B2",
        "chrome": "#22D3EE" if is_dark else "#0891B2",
        "name": "#A78BFA" if is_dark else "#7C3AED",
        "text": "#CBD5E1" if is_dark else "#334155",
        "dim": "#64748B" if is_dark else "#94A3B8",
        "star": "#F59E0B",
    }

    parts = [f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono','Fira Code',monospace">
<rect width="{W}" height="{H}" fill="{C['bg']}"/>
<rect x="0" y="0" width="{W}" height="{TITLE_H}" fill="{C['panel']}"/>
<circle cx="20" cy="{TITLE_H/2}" r="6" fill="#ef4444"/>
<circle cx="42" cy="{TITLE_H/2}" r="6" fill="#f59e0b"/>
<circle cx="64" cy="{TITLE_H/2}" r="6" fill="#10B981"/>
<text x="{W/2}" y="{TITLE_H/2+5}" text-anchor="middle" fill="{C['chrome']}" font-size="13">projects.sh --list</text>
''']

    for i, p in enumerate(projects):
        col = i % COLS
        row = i // COLS
        x = PAD + col * (CARD_W + GAP)
        y = TITLE_H + PAD + row * (CARD_H + GAP)

        parts.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="8" '
            f'fill="{C["panel"]}" stroke="{C["border"]}" stroke-opacity="0.3"/>'
        )
        parts.append(
            f'<text x="{x+18}" y="{y+30}" fill="{C["name"]}" font-size="16" font-weight="bold">{escape(p["name"])}</text>'
        )
        stars = p.get("stars", 0)
        if stars:
            parts.append(
                f'<text x="{x+CARD_W-18}" y="{y+30}" text-anchor="end" fill="{C["star"]}" font-size="13">&#9733; {stars}</text>'
            )
        desc = p["desc"]
        if len(desc) > 58:
            desc = desc[:55] + "..."
        parts.append(
            f'<text x="{x+18}" y="{y+54}" fill="{C["text"]}" font-size="12.5">{escape(desc)}</text>'
        )
        tx = x + 18
        ty = y + CARD_H - 20
        for j, tech in enumerate(p["tech"]):
            tw = len(tech) * 7 + 20
            color = TECH_COLORS[j % len(TECH_COLORS)]
            parts.append(
                f'<rect x="{tx}" y="{ty-16}" width="{tw}" height="22" rx="11" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-opacity="0.5"/>'
            )
            parts.append(
                f'<text x="{tx+tw/2}" y="{ty}" text-anchor="middle" fill="{color}" font-size="11">{escape(tech)}</text>'
            )
            tx += tw + 8

    parts.append("</svg>")
    return "".join(parts)

for mode in ["dark", "light"]:
    svg = build_svg(mode)
    fname = f"projects-{mode}.svg"
    with open(fname, "w") as f:
        f.write(svg)
    print(mode, len(svg.encode()), "bytes, height", H)

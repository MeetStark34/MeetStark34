#!/usr/bin/env python3
"""Moonlight Arcade: static README graphics (header, project cards, footer).

Edit the PROJECTS list below, then run:  python scripts/static_assets.py
Writes assets/header.svg, assets/footer.svg and assets/projects/*.svg. Standard library only.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import (  # noqa: E402
    BLUE, BORDER, CYAN, FONT, GREEN, MONO, MOON, MUTED, ORANGE, PANEL_2, PIECE_COLORS, PINK,
    SUBTEXT, TEXT, VIOLET, YELLOW, block, esc, panel, panel_defs, pixel_art, svg,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

NAME = "MEET STARK"
SUBTITLE = "AI & Data Science Student  ·  Front-End Developer  ·  Founder of The Moonlight Mic"
PHRASES = [
    "turning raw data into decisions",
    "next.js · typescript · python · postgresql",
    "now shipping: GameHub, 8 daily puzzles",
    "open to internships in AI & data engineering",
]

# 5x7 block font, only the letters we need
FONT_5x7 = {
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "K": ["X...X", "X..X.", "X.X..", "XX...", "X.X..", "X..X.", "X...X"],
}

ICONS = {
    "gamepad": ["..XXXXXXXX..", ".XXXXXXXXXX.", "XX.XXXXXX.XX", "X...XXXX.X.X",
                "XX.XXXXXX.XX", "XXXXXXXXXXXX", "XXXX....XXXX", ".XX......XX."],
    "coin": ["..XXXXX..", ".X.....X.", "X..XXX..X", "X..X..X.X", "X..XXX..X",
             "X..X..X.X", "X..XXX..X", ".X.....X.", "..XXXXX.."],
    "play": [".XXXXXXXX.", "XXXXXXXXXX", "XXX.XXXXXX", "XXX..XXXXX", "XXX...XXXX",
             "XXX..XXXXX", "XXX.XXXXXX", "XXXXXXXXXX", ".XXXXXXXX."],
    "chart": [".......XX", ".......XX", "....XX.XX", "....XX.XX", ".XX.XX.XX",
              ".XX.XX.XX", ".XX.XX.XX", ".........", "XXXXXXXXX"],
    "bubble": ["XXXXXXXXX", "X.......X", "X.XXXXX.X", "X.......X", "X.XXX...X",
               "X.......X", "XXXXXXXXX", ".XX......", ".X......."],
    "pin": ["..XXXXX..", ".XXXXXXX.", "XXX...XXX", "XXX...XXX", "XXX...XXX",
            ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X...."],
    "hourglass": ["XXXXXXXXX", ".X.....X.", ".XX...XX.", "..XX.XX..", "...XXX...",
                  "..X...X..", ".X..X..X.", ".X.XXX.X.", "XXXXXXXXX"],
}

PROJECTS = [
    {
        "slug": "crypto", "title": "Crypto Portfolio", "kicker": "FINTECH DASHBOARD",
        "icon": "coin", "accent": YELLOW, "status": "LIVE",
        "lines": ["Apple-inspired portfolio tracker for holdings,",
                  "purchases, fees and profit/loss. Live market data,",
                  "EUR/USD/INR conversion and price alerts."],
        "tags": ["Next.js", "TypeScript", "Supabase"],
        "link": "stark-crypto-portfolio.vercel.app",
    },
    {
        "slug": "youtube", "title": "YouTube Network", "kicker": "ANALYTICS DASHBOARD",
        "icon": "play", "accent": PINK, "status": "LIVE",
        "lines": ["Tracks 11 channels in one place: subscribers,",
                  "views, uploads and engagement, with custom",
                  "rankings, channel families and Shorts filters."],
        "tags": ["Next.js", "TypeScript", "YouTube API"],
        "link": "youtube-network-dashboard.vercel.app",
    },
    {
        "slug": "gamescope", "title": "GameScope", "kicker": "DATA PIPELINE + DASHBOARD",
        "icon": "chart", "accent": CYAN, "status": "LIVE",
        "lines": ["Video game sales intelligence: a reproducible",
                  "Python pipeline (cleaning, validation, audit log)",
                  "feeding a source-aware Next.js dashboard."],
        "tags": ["Python", "pandas", "Next.js"],
        "link": "gamescope-video-game-analytics.vercel.app",
    },
    {
        "slug": "wellpack", "title": "Wellpack", "kicker": "PREDICTIVE MARKETING",
        "icon": "bubble", "accent": GREEN, "status": "LIVE",
        "lines": ["Event-aware campaign prediction platform that",
                  "blends real-world events with data analysis to",
                  "time SMS & RCS marketing campaigns."],
        "tags": ["Python", "Jupyter", "Next.js"],
        "link": "wellpack-project.vercel.app",
    },
    {
        "slug": "geolocation", "title": "AI Geolocation", "kicker": "ML · ANOMALY DETECTION",
        "icon": "pin", "accent": VIOLET, "status": "PYTHON",
        "lines": ["GPS mission tracking for advertising bikes:",
                  "Flask API, route simulation, Random Forest",
                  "anomaly detection and automated PDF reports."],
        "tags": ["Python", "Flask", "scikit-learn", "Folium"],
        "link": "github.com/MeetStark34/AI-Based-Geolocation",
    },
    {
        "slug": "timeviz", "title": "Time-Viz", "kicker": "CREATIVE FRONT-END",
        "icon": "hourglass", "accent": ORANGE, "status": "LIVE",
        "lines": ["Time, reimagined: a sleek, distraction-free",
                  "interface that turns the passing of time into",
                  "a calm, animated visualization."],
        "tags": ["Next.js", "Tailwind CSS"],
        "link": "time-viz.vercel.app",
    },
]

GAMES = [
    ("Patches", "Shape logic"), ("Mini Sudoku", "Number logic"), ("Zip", "Path logic"),
    ("Werd", "Word game"), ("Pinpoint", "Word association"), ("Crossclimb", "Word ladder"),
    ("Tango", "Binary logic"), ("Queens", "Placement logic"),
]

MOON_PIXELS = ["..XXXX..", ".XXX....", "XXX.....", "XXX.....", "XXX.....", "XXX.....",
               ".XXX....", "..XXXX.."]


def chips(tags, x, y, size=13, h=30):
    out = []
    for tag in tags:
        w = int(len(tag) * size * 0.62) + 26
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{PANEL_2}" stroke="{BORDER}"/>'
            f'<text class="m" x="{x + w / 2}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" '
            f'font-size="{size}" fill="{SUBTEXT}">{esc(tag)}</text>'
        )
        x += w + 8
    return "".join(out)


def icon_tile(name, x, y, size, accent):
    rows = ICONS[name]
    cols = max(len(r) for r in rows)
    px = (size - 20) // max(cols, len(rows))
    ix = x + (size - px * cols) / 2
    iy = y + (size - px * len(rows)) / 2
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="16" fill="{accent}" fill-opacity=".12" '
        f'stroke="{accent}" stroke-opacity=".45"/>' + pixel_art(rows, ix, iy, px, accent)
    )


def status_pill(text, x_right, y, accent):
    live = text == "LIVE"
    label = "LIVE" if live else text
    w = len(label) * 9 + (42 if live else 28)
    x = x_right - w
    color = GREEN if live else accent
    dot = (f'<circle class="pulse" cx="{x + 16}" cy="{y + 14}" r="4.5" fill="{GREEN}"/>' if live else "")
    tx = x + (28 if live else 14)
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{color}" fill-opacity=".12" '
        f'stroke="{color}" stroke-opacity=".5"/>{dot}'
        f'<text class="m" x="{tx}" y="{y + 18.5}" font-size="12" font-weight="700" letter-spacing="1.5" '
        f'fill="{color}">{esc(label)}</text>'
    )


BASE_CSS = (f"text{{font-family:{FONT}}}.m{{font-family:{MONO}}}"
            "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}.pulse{animation:pulse 2s ease-in-out infinite}")


def accent_glow(uid, accent):
    return (f'<radialGradient id="{uid}a" cx="1" cy="0" r="0.75"><stop offset="0" stop-color="{accent}" '
            f'stop-opacity=".16"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>')


def project_card(p):
    W, H = 600, 300
    uid = p["slug"][:3]
    out = [f"<defs>{panel_defs(uid)}{accent_glow(uid, p['accent'])}</defs>", panel(W, H, uid),
           f'<rect width="{W}" height="{H}" rx="20" fill="url(#{uid}a)"/>']
    out.append(icon_tile(p["icon"], 32, 32, 68, p["accent"]))
    out.append(f'<text x="120" y="64" font-size="28" font-weight="700" fill="{TEXT}">{esc(p["title"])}</text>')
    out.append(f'<text class="m" x="121" y="90" font-size="12.5" letter-spacing="1.6" fill="{p["accent"]}">'
               f'{esc(p["kicker"])}</text>')
    out.append(status_pill(p["status"], W - 32, 34, p["accent"]))
    for i, line in enumerate(p["lines"]):
        out.append(f'<text x="32" y="{142 + i * 27}" font-size="17.5" fill="{SUBTEXT}">{esc(line)}</text>')
    out.append(chips(p["tags"], 32, 214))
    out.append(f'<text class="m" x="32" y="{H - 30}" font-size="13" fill="{p["accent"]}">↗ {esc(p["link"])}</text>')
    # a tiny stack of blocks in the corner, the arcade signature
    for i, (bx, by) in enumerate([(0, 1), (1, 1), (2, 1), (2, 0)]):
        out.append(block(W - 74 + bx * 14, H - 52 + by * 14, 12, p["accent"], extra=' opacity=".55"'))
    alt = f'{p["title"]}: {" ".join(p["lines"])}'
    return svg(W, H, "".join(out), alt, BASE_CSS)


def featured_card():
    W, H = 1200, 420
    out = [f"<defs>{panel_defs('fe')}{accent_glow('fe', VIOLET)}</defs>", panel(W, H, "fe", r=24),
           f'<rect width="{W}" height="{H}" rx="24" fill="url(#fea)"/>']
    # left: the pitch
    out.append(f'<rect x="40" y="38" width="196" height="30" rx="15" fill="{VIOLET}" fill-opacity=".14" '
               f'stroke="{VIOLET}" stroke-opacity=".5"/><text class="m" x="138" y="58" text-anchor="middle" '
               f'font-size="12" font-weight="700" letter-spacing="2" fill="{VIOLET}">★ FEATURED PROJECT</text>')
    out.append(status_pill("LIVE", 330, 39, GREEN))
    out.append(icon_tile("gamepad", 40, 92, 80, CYAN))
    out.append(f'<text x="140" y="138" font-size="50" font-weight="800" fill="{TEXT}">GameHub</text>')
    out.append(f'<text class="m" x="142" y="166" font-size="13" letter-spacing="2" fill="{CYAN}">'
               f'PUZZLE PLATFORM · FULL-STACK</text>')
    out.append(f'<text x="40" y="218" font-size="23" font-weight="600" fill="{TEXT}">'
               f'Daily brain training, without the daily limit.</text>')
    for i, line in enumerate(["Eight original puzzles, one shared Daily Set and an Unlimited",
                              "mode, with XP, ranks, streaks, achievements, leaderboards",
                              "and 11 themes. Everything that matters is server-validated."]):
        out.append(f'<text x="40" y="{256 + i * 27}" font-size="17.5" fill="{SUBTEXT}">{line}</text>')
    out.append(chips(["Next.js 16", "React 19", "TypeScript", "PostgreSQL", "Supabase"], 40, 338))
    out.append(f'<text class="m" x="40" y="{H - 24}" font-size="13" fill="{CYAN}">↗ stark-game-hub.vercel.app</text>')

    # right: level select
    gx, gy, tw, th = 676, 66, 236, 64
    out.append(f'<text class="m" x="{gx}" y="{gy - 14}" font-size="12" letter-spacing="2.5" fill="{MUTED}">'
               f'SELECT A GAME</text>')
    colors = list(PIECE_COLORS.values()) + [PINK]
    for i, (name, sub) in enumerate(GAMES):
        x = gx + (i % 2) * (tw + 16)
        y = gy + (i // 2) * (th + 16)
        c = colors[i]
        out.append(
            f'<g class="tile" style="animation-delay:{0.15 + i * 0.09:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{PANEL_2}" stroke="{BORDER}"/>'
            + block(x + 16, y + 17, 13, c) + block(x + 31, y + 17, 13, c) + block(x + 16, y + 32, 13, c)
            + block(x + 31, y + 32, 13, c, extra=' opacity=".35"')
            + f'<text x="{x + 60}" y="{y + 29}" font-size="17" font-weight="700" fill="{TEXT}">{esc(name)}</text>'
            f'<text class="m" x="{x + 60}" y="{y + 49}" font-size="12" fill="{MUTED}">{esc(sub)}</text>'
            f'<text class="m" x="{x + tw - 16}" y="{y + 29}" text-anchor="end" font-size="12" fill="{c}">'
            f'{i + 1:02d}</text></g>'
        )
    css = BASE_CSS + ("@keyframes pop{from{opacity:0;transform:translateY(-14px)}to{opacity:1;transform:none}}"
                      ".tile{animation:pop .45s steps(4,end) both}")
    alt = ("GameHub, featured project: daily brain training without the daily limit. Eight original puzzles "
           "(Patches, Mini Sudoku, Zip, Werd, Pinpoint, Crossclimb, Tango, Queens), XP, ranks, streaks "
           "and 11 themes. Built with Next.js, React, TypeScript, PostgreSQL and Supabase.")
    return svg(W, H, "".join(out), alt, css)


def header():
    W, H = 1200, 380
    rng = random.Random(34)
    css = [BASE_CSS,
           "@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}.st{animation:tw ease-in-out infinite}",
           "@keyframes drop{from{transform:translateY(-300px)}to{transform:none}}"
           ".lt{animation:drop .6s steps(10,end) both}",
           "@keyframes glow{0%,100%{opacity:.35}50%{opacity:.6}}.mg{animation:glow 5s ease-in-out infinite}",
           "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.bl{animation:blink 1s step-end infinite}",
           "@keyframes fade{from{opacity:0}to{opacity:1}}.fd{animation:fade .8s ease-out 1.4s both}"]
    defs = [panel_defs("hd"),
            f'<linearGradient id="name" gradientUnits="userSpaceOnUse" x1="200" y1="0" x2="1000" y2="0">'
            f'<stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{CYAN}"/>'
            f'<stop offset="1" stop-color="{PINK}"/></linearGradient>',
            '<filter id="blur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="18"/></filter>']
    out = [panel(W, H, "hd", r=24)]

    # stars
    for _ in range(70):
        x, y = rng.uniform(16, W - 16), rng.uniform(14, H - 90)
        if 180 < x < 1020 and 70 < y < 330:
            continue  # keep the centre clear for the name
        r = rng.choice([0.8, 1.1, 1.5])
        out.append(f'<circle class="st" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" '
                   f'style="animation-duration:{rng.uniform(2.5, 6):.1f}s;animation-delay:-{rng.uniform(0, 6):.1f}s"/>')

    # pixel moon with a soft glow
    mx, my, ms = 1070, 46, 9
    out.append(f'<circle class="mg" cx="{mx + 30}" cy="{my + 36}" r="46" fill="{MOON}" filter="url(#blur)"/>')
    out.append(pixel_art(MOON_PIXELS, mx, my, ms, MOON))

    # name in falling blocks
    s, p = 13, 15
    letter_w = 5 * p
    space_w = 3 * p
    total_w = sum(letter_w + p if ch != " " else space_w for ch in NAME) - p
    x = (W - total_w) / 2
    y0 = 92
    li = 0
    for ch in NAME:
        if ch == " ":
            x += space_w
            continue
        cells = []
        for j, row in enumerate(FONT_5x7[ch]):
            for i, c in enumerate(row):
                if c == "X":
                    cells.append(block(x + i * p, y0 + j * p, s, "url(#name)"))
        out.append(f'<g class="lt" style="animation-delay:{0.1 + li * 0.11:.2f}s">{"".join(cells)}</g>')
        x += letter_w + p
        li += 1

    out.append(f'<text class="fd" x="{W / 2}" y="242" text-anchor="middle" font-size="21" fill="{SUBTEXT}">'
               f'{esc(SUBTITLE)}</text>')

    # terminal line that types, holds and erases each phrase
    cw = 10.8
    longest = max(len(t) for t in PHRASES)
    pw = longest * cw + 84
    px0 = (W - pw) / 2
    ty = 270
    out.append(f'<g class="fd"><rect x="{px0:.1f}" y="{ty}" width="{pw:.1f}" height="42" rx="21" fill="#0A0D21" '
               f'stroke="{BORDER}"/><text class="m" x="{px0 + 22:.1f}" y="{ty + 27}" font-size="18" '
               f'font-weight="700" fill="{CYAN}">&gt;</text>')
    tx = px0 + 46
    slots, t = [], 0.0
    for phrase in PHRASES:
        typing = len(phrase) * 0.055
        slots.append((t, typing, len(phrase)))
        t += typing + 2.0 + 0.45 + 0.35
    total = t

    def pc(v):
        return f"{v / total * 100:.3f}%"

    cursor_frames = ["0%{transform:translateX(0)}"]
    for k, (phrase, (start, typing, n)) in enumerate(zip(PHRASES, slots)):
        width = n * cw
        hold_end = start + typing + 2.0
        erase_end = hold_end + 0.45
        css.append(
            f"@keyframes c{k}{{0%,{pc(start)}{{transform:scaleX(1);animation-timing-function:steps({n},end)}}"
            f"{pc(start + typing)},{pc(hold_end)}{{transform:scaleX(0);animation-timing-function:steps({n},end)}}"
            f"{pc(erase_end)},100%{{transform:scaleX(1)}}}}"
            f".c{k}{{transform-box:fill-box;transform-origin:100% 50%;animation:c{k} {total:.2f}s infinite}}"
            f"@keyframes v{k}{{0%,{pc(start)}{{opacity:0}}{pc(start + 0.001)},{pc(erase_end)}{{opacity:1}}"
            f"{pc(erase_end + 0.001)},100%{{opacity:0}}}}.v{k}{{animation:v{k} {total:.2f}s step-end infinite}}"
        )
        cursor_frames.append(f"{pc(start)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}")
        cursor_frames.append(f"{pc(start + typing)}{{transform:translateX({width:.1f}px)}}")
        cursor_frames.append(f"{pc(hold_end)}{{transform:translateX({width:.1f}px);"
                             f"animation-timing-function:steps({n},end)}}")
        cursor_frames.append(f"{pc(erase_end)}{{transform:translateX(0)}}")
        out.append(
            f'<g class="v{k}" opacity="0"><text class="m" x="{tx:.1f}" y="{ty + 27}" font-size="18" fill="{TEXT}" '
            f'textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs">{esc(phrase)}</text>'
            f'<rect class="c{k}" x="{tx - 1:.1f}" y="{ty + 8}" width="{width + 2:.1f}" height="26" fill="#0A0D21"/></g>'
        )
    cursor_frames.append("100%{transform:translateX(0)}")
    css.append(f"@keyframes cur{{{''.join(cursor_frames)}}}.cur{{animation:cur {total:.2f}s infinite}}")
    out.append(f'<g class="cur"><rect class="bl" x="{tx + 2:.1f}" y="{ty + 11}" width="10" height="21" '
               f'fill="{VIOLET}"/></g></g>')

    # a dim block stack along the bottom edge
    colors = [VIOLET, CYAN, BLUE, PINK]
    x, bs = 14.0, 15
    while x < W - 28:
        hgt = rng.choice([0, 1, 1, 2, 2, 3])
        col = rng.choice(colors)
        for j in range(hgt):
            out.append(block(x, H - 18 - (j + 1) * (bs + 2), bs, col, extra=' opacity=".16"'))
        x += bs + 2
    alt = f"Meet Stark: {SUBTITLE.replace('  ', ' ')}"
    return svg(W, H, f"<defs>{''.join(defs)}</defs>" + "".join(out), alt, "".join(css))


def footer():
    W, H = 1200, 170
    css = BASE_CSS + "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.15}}.bl{animation:blink 1.2s step-end infinite}"
    out = [f"<defs>{panel_defs('ft')}</defs>", panel(W, H, "ft", r=24)]
    out.append(pixel_art(MOON_PIXELS, 70, 52, 8, MOON))
    out.append(f'<text class="m" x="{W / 2}" y="78" text-anchor="middle" font-size="30" font-weight="800" '
               f'letter-spacing="8" fill="{TEXT}">THANKS FOR PLAYING</text>')
    out.append(f'<text class="m bl" x="{W / 2}" y="118" text-anchor="middle" font-size="16" letter-spacing="4" '
               f'fill="{VIOLET}">★ STAR A REPO TO CONTINUE ★</text>')
    # two interlocking pieces filling a 2x4 well, rows counted from the bottom
    for color, cells in ((ORANGE, [(0, 0), (1, 0), (1, 1), (1, 2)]), (BLUE, [(0, 1), (0, 2), (0, 3), (1, 3)])):
        for bx, by in cells:
            out.append(block(1094 + bx * 18, 116 - by * 18, 16, color, extra=' opacity=".85"'))
    return svg(W, H, "".join(out), "Thanks for playing. Star a repo to continue.", css)


def main():
    (ASSETS / "projects").mkdir(parents=True, exist_ok=True)
    (ASSETS / "header.svg").write_text(header(), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(footer(), encoding="utf-8")
    (ASSETS / "projects" / "gamehub.svg").write_text(featured_card(), encoding="utf-8")
    for p in PROJECTS:
        (ASSETS / "projects" / f"{p['slug']}.svg").write_text(project_card(p), encoding="utf-8")
    print(f"wrote header, footer and {len(PROJECTS) + 1} project cards to {ASSETS}")


if __name__ == "__main__":
    main()

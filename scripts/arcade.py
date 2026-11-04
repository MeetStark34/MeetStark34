#!/usr/bin/env python3
"""Moonlight Arcade: live graphics for the GitHub profile README.

  commit-stack.svg   falling blocks build the last 12 months of contributions, the real
                     contribution graph is revealed, then every line clears and it loops
  player-stats.svg   contributions, streaks, repositories, stars and top languages

Usage:  python scripts/arcade.py --user MeetStark34 --out dist

With GITHUB_TOKEN set (GitHub Actions provides one) the GraphQL API is used. Without it the
public contribution calendar page is read instead, so the script also runs locally.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import (  # noqa: E402
    BORDER, CYAN, FONT, GREEN, GRID, LEVELS, MONO, MUTED, ORANGE, PANEL_2, PIECE_COLORS,
    PINK, BLUE, SUBTEXT, TEXT, VIOLET, block, esc, panel, panel_defs, svg,
)

API = "https://api.github.com"
UA = "moonlight-arcade-readme"


# --------------------------------------------------------------------------- data

def http(url, payload=None, token=None):
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8")


LEVEL_ENUM = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
              "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch_calendar(user, token):
    """List of (date, count, level 0-4) for the last year, oldest first."""
    if token:
        query = """query($login: String!) { user(login: $login) { contributionsCollection {
          contributionCalendar { weeks { contributionDays {
            date contributionCount contributionLevel } } } } } }"""
        res = json.loads(http(f"{API}/graphql", {"query": query, "variables": {"login": user}}, token))
        if res.get("errors"):
            raise RuntimeError(res["errors"])
        weeks = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        return [(dt.date.fromisoformat(d["date"]), d["contributionCount"],
                 LEVEL_ENUM.get(d["contributionLevel"], 0))
                for w in weeks for d in w["contributionDays"]]

    page = http(f"https://github.com/users/{user}/contributions")
    counts = {}
    for m in re.finditer(r'<tool-tip\b[^>]*\sfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        n = re.match(r"\s*([\d,]+) contributions?", m.group(2))
        counts[m.group(1)] = int(n.group(1).replace(",", "")) if n else 0
    days = []
    for m in re.finditer(r"<td\b[^>]*>", page):
        tag = m.group(0)
        date = re.search(r'data-date="([\d-]+)"', tag)
        level = re.search(r'data-level="(\d)"', tag)
        ident = re.search(r'\sid="([^"]+)"', tag)
        if date and level:
            days.append((dt.date.fromisoformat(date.group(1)),
                         counts.get(ident.group(1) if ident else "", 0), int(level.group(1))))
    if not days:
        raise RuntimeError("could not read the contribution calendar")
    return sorted(days)


def fetch_profile(user, token):
    info = json.loads(http(f"{API}/users/{user}", token=token))
    repos = json.loads(http(f"{API}/users/{user}/repos?per_page=100&type=owner", token=token))
    own = [r for r in repos if not r["fork"]]
    weights = {}
    skip = {"CSS", "SCSS", "HTML", "Shell", "PowerShell", "Batchfile", "Dockerfile", "Makefile"}
    for r in own:
        try:
            langs = json.loads(http(r["languages_url"], token=token))
        except Exception:  # noqa: BLE001 - fall back to the primary language
            langs = {r["language"]: 1} if r["language"] else {}
        langs = {("SQL" if k == "PLpgSQL" else k): v for k, v in langs.items() if k not in skip}
        total = sum(langs.values())
        for k, v in langs.items():  # every project counts equally, split by its byte share
            weights[k] = weights.get(k, 0) + v / total
    live = sum(1 for r in own if r.get("homepage") and "github.com" not in r["homepage"])
    return {
        "name": info.get("name") or user,
        "public_repos": info.get("public_repos", len(repos)),
        "followers": info.get("followers", 0),
        "stars": sum(r["stargazers_count"] for r in own),
        "live": live,
        "languages": sorted(weights.items(), key=lambda kv: -kv[1]),
    }


def streaks(days):
    active = [n > 0 or lv > 0 for _, n, lv in days]
    longest = run = 0
    for a in active:
        run = run + 1 if a else 0
        longest = max(longest, run)
    i = len(active) - 1
    if i >= 0 and not active[i]:  # a quiet "today" doesn't break the streak yet
        i -= 1
    current = 0
    while i >= 0 and active[i]:
        current += 1
        i -= 1
    return current, longest, sum(active)


# ------------------------------------------------------------------ board + tiling

BASE = {
    "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "T": [(0, 1), (1, 1), (2, 1), (1, 0)],
    "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "Z": [(0, 1), (1, 1), (1, 0), (2, 0)],
    "J": [(0, 1), (0, 0), (1, 0), (2, 0)],
    "L": [(2, 1), (0, 0), (1, 0), (2, 0)],
}


def rotations(cells):
    out, cur = [], list(cells)
    for _ in range(4):
        mx, my = min(x for x, _ in cur), min(y for _, y in cur)
        norm = tuple(sorted((x - mx, y - my) for x, y in cur))
        if norm not in out:
            out.append(norm)
        cur = [(y, -x) for x, y in cur]
    return out


TETROMINOES = {k: rotations(v) for k, v in BASE.items()}
# Smaller fallbacks guarantee the board can always be completed; they are rarely needed.
FALLBACKS = [
    [("I", s) for s in rotations([(0, 0), (1, 0), (2, 0)])]
    + [("L", s) for s in rotations([(0, 0), (1, 0), (0, 1)])],
    [("I", s) for s in rotations([(0, 0), (1, 0)])],
    [("T", ((0, 0),))],
]


def fits(shape, ox, oy, h, hi, width):
    low = {}
    for x, y in shape:
        cx, cy = ox + x, oy + y
        if cx < 0 or cx >= width or cy >= hi[cx]:
            return False
        low[cx] = min(low.get(cx, cy), cy)
    # Every column the piece touches must rest exactly on that column's stack: no holes,
    # and nothing above, so each piece can fall straight down into place.
    return all(low[cx] == h[cx] for cx in low)


def options(col, row, shapes, h, hi, width):
    found = []
    for kind, shape in shapes:
        for ax, ay in shape:
            ox, oy = col - ax, row - ay
            if fits(shape, ox, oy, h, hi, width):
                found.append((kind, shape, ox, oy))
    return found


def tile_once(width, lo, hi, rng):
    h, pieces, small = list(lo), [], 0
    while True:
        open_cols = [c for c in range(width) if h[c] < hi[c]]
        if not open_cols:
            return pieces, small
        low = min(h[c] for c in open_cols)
        col = rng.choice([c for c in open_cols if h[c] == low])
        tetro = {k: options(col, low, [(k, s) for s in shapes], h, hi, width)
                 for k, shapes in TETROMINOES.items()}
        tetro = {k: v for k, v in tetro.items() if v}
        if tetro:
            kind, shape, ox, oy = rng.choice(tetro[rng.choice(sorted(tetro))])
        else:
            for group in FALLBACKS:
                found = options(col, low, group, h, hi, width)
                if found:
                    kind, shape, ox, oy = rng.choice(found)
                    small += 1
                    break
        cells = [(ox + x, oy + y) for x, y in shape]
        for x, y in cells:
            h[x] = max(h[x], y + 1)
        pieces.append((kind, cells))


def tile(width, lo, hi, seed, tries=160):
    rng = random.Random(seed)
    best = None
    for _ in range(tries):
        pieces, small = tile_once(width, lo, hi, rng)
        if best is None or small < best[1]:
            best = (pieces, small)
        if small == 0:
            break
    return best[0]


def build_board(days):
    def sunday_index(d):
        return (d.weekday() + 1) % 7  # Sunday = 0 ... Saturday = 6

    start = days[0][0] - dt.timedelta(days=sunday_index(days[0][0]))
    cells = {}
    for d, n, lv in days:
        cells[((d - start).days // 7, 6 - sunday_index(d))] = (d, n, lv)  # row 0 = Saturday
    width = max(c for c, _ in cells) + 1
    lo, hi = [], []
    for c in range(width):
        rows = [r for (cc, r) in cells if cc == c]
        lo.append(min(rows))
        hi.append(max(rows) + 1)
    return cells, width, lo, hi


# ---------------------------------------------------------------- commit stack svg

def pct(t, total):
    return f"{max(0.0, min(100.0, t / total * 100)):.3f}%"


def commit_stack(user, days, stats):
    cells, width, lo, hi = build_board(days)
    seed = f"{user}-{days[-1][0]}"
    pieces = tile(width, lo, hi, seed)
    current, longest, active_days = stats
    total = sum(n for _, n, _ in days)

    S, P = 15, 18                 # block size, pitch
    HEAD = 6                      # empty rows above the stack
    ROWS = 7 + HEAD
    WX, WY = 64, 92               # well origin (top-left of visible area)
    WW, WH = width * P - (P - S), ROWS * P - (P - S)
    HX = WX + WW + 36             # HUD x
    W = 1200
    H = WY + WH + 82

    def cx(c):
        return WX + c * P

    def cy(r):
        return WY + (ROWS - 1 - r) * P

    # ---- timeline (seconds)
    n = len(pieces)
    speed = 28.0                         # rows per second
    gap = min(0.13, 10.5 / max(n, 1))    # time between landings
    land, spawn, dist = [], [], []
    for i, (_, pc) in enumerate(pieces):
        rows_to_fall = ROWS - min(y for _, y in pc)
        fall = rows_to_fall / speed
        t_land = 1.0 + i * gap
        land.append(t_land)
        spawn.append(t_land - fall)
        dist.append(rows_to_fall)
    reveal = land[-1] + 0.5
    sweep = 0.8
    clear = reveal + sweep + 0.3 + 5.8
    T = clear + 1.6
    level_end = T - 0.9

    css = [
        f"text{{font-family:{FONT}}}.m{{font-family:{MONO}}}",
    ]
    # fall + fade, one keyframe set per piece
    body_pieces = []
    for i, (kind, pc) in enumerate(pieces):
        D = dist[i] * P
        css.append(
            f"@keyframes d{i}{{0%,{pct(spawn[i], T)}{{transform:translateY(-{D}px);"
            f"animation-timing-function:steps({dist[i]},end)}}"
            f"{pct(land[i], T)},{pct(clear + 0.3, T)}{{transform:translateY(0);opacity:1}}"
            f"{pct(clear + 0.55, T)},100%{{transform:translateY(0);opacity:0}}}}"
            f".q{i}{{animation:d{i} {T:.2f}s infinite}}"
        )
        blocks = []
        for c, r in pc:
            lv = cells.get((c, r), (None, 0, 0))[2]
            blocks.append(block(cx(c), cy(r), S, PIECE_COLORS[kind], cls=f"f{kind}{lv} k{c}"))
        body_pieces.append(f'<g class="q{i}">{"".join(blocks)}</g>')

    # colour reveal: piece colour -> contribution level, swept left to right
    for kind, color in PIECE_COLORS.items():
        for lv, lcolor in enumerate(LEVELS):
            css.append(
                f"@keyframes f{kind}{lv}{{0%,{pct(reveal, T)}{{fill:{color}}}"
                f"{pct(reveal + 0.3, T)},{pct(level_end, T)}{{fill:{lcolor}}}"
                f"{pct(level_end + 0.05, T)},100%{{fill:{color}}}}}"
                f".f{kind}{lv}{{animation:f{kind}{lv} {T:.2f}s infinite}}"
            )
    for c in range(width):
        css.append(f".k{c}{{animation-delay:{c / width * sweep:.3f}s}}")

    # row flashes + banner on line clear
    flashes = []
    for r in range(7):
        a = clear + (6 - r) * 0.035
        css.append(
            f"@keyframes x{r}{{0%,{pct(a, T)}{{opacity:0}}{pct(a + 0.1, T)}{{opacity:.9}}"
            f"{pct(a + 0.45, T)},100%{{opacity:0}}}}.x{r}{{animation:x{r} {T:.2f}s infinite}}"
        )
        flashes.append(f'<rect class="x{r}" x="{WX - 4}" y="{cy(r) - 1.5}" width="{WW + 8}" '
                       f'height="{S + 3}" rx="3" fill="#fff" opacity="0"/>')
    css.append(
        f"@keyframes lc{{0%,{pct(clear, T)}{{opacity:0}}{pct(clear + 0.1, T)},"
        f"{pct(clear + 0.85, T)}{{opacity:1}}{pct(clear + 1.05, T)},100%{{opacity:0}}}}"
        f".lc{{animation:lc {T:.2f}s infinite}}"
    )
    mid_y = cy(3) + S / 2
    banner = (
        f'<g class="lc" opacity="0"><rect x="{WX + WW / 2 - 170}" y="{mid_y - 26}" width="340" height="52" '
        f'rx="12" fill="#0B0E22" stroke="{VIOLET}" stroke-width="2"/>'
        f'<text class="m" x="{WX + WW / 2}" y="{mid_y + 9}" text-anchor="middle" font-size="24" '
        f'font-weight="700" letter-spacing="5" fill="{TEXT}">7 LINES CLEAR!</text></g>'
    )

    # ---- static layers
    slots = []
    for (c, r) in cells:
        slots.append(f'<rect x="{cx(c)}" y="{cy(r)}" width="{S}" height="{S}" rx="3" fill="{GRID}"/>')
    for c in range(width):
        for r in range(0, lo[c]):  # days still to come this week
            slots.append(f'<rect x="{cx(c) + 0.75}" y="{cy(r) + 0.75}" width="{S - 1.5}" height="{S - 1.5}" '
                         f'rx="3" fill="none" stroke="{BORDER}" stroke-dasharray="3 2"/>')

    labels = []
    for r_top, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        labels.append(f'<text class="m" x="{WX - 12}" y="{cy(6 - r_top) + 11.5}" text-anchor="end" '
                      f'font-size="11" fill="{MUTED}">{name}</text>')
    last_month, last_x = None, -99
    for c in range(width):
        col_days = sorted(v[0] for (cc, _), v in cells.items() if cc == c)
        month = col_days[0].month
        if month != last_month:
            if c - last_x >= 3 and c < width - 1:
                labels.append(f'<text class="m" x="{cx(c)}" y="{WY + WH + 22}" font-size="11" '
                              f'fill="{MUTED}">{col_days[0].strftime("%b")}</text>')
                last_x = c
            last_month = month
    ly = WY + WH + 50
    legend_x = WX + WW - 5 * 17 - 34
    legend = [f'<text class="m" x="{legend_x - 10}" y="{ly}" text-anchor="end" font-size="11" '
              f'fill="{MUTED}">Less</text>']
    for i, col in enumerate(LEVELS):
        legend.append(f'<rect x="{legend_x + i * 17}" y="{ly - 11}" width="13" height="13" rx="3" fill="{col}"/>')
    legend.append(f'<text class="m" x="{legend_x + 5 * 17 + 4}" y="{ly}" font-size="11" '
                  f'fill="{MUTED}">More</text>')
    legend.append(f'<text class="m" x="{WX - 10}" y="{ly}" font-size="11" fill="{MUTED}">'
                  f'Blocks fall, the real graph is revealed, then every line clears · '
                  f'updated {days[-1][0].isoformat()}</text>')

    # ---- HUD
    def hud_box(y, label, value, unit, color):
        return (
            f'<rect x="{HX}" y="{y}" width="{W - HX - 28}" height="52" rx="10" fill="{PANEL_2}" stroke="{BORDER}"/>'
            f'<rect x="{HX}" y="{y + 12}" width="3" height="28" rx="1.5" fill="{color}"/>'
            f'<text class="m" x="{HX + 14}" y="{y + 19}" font-size="10" letter-spacing="1.5" fill="{MUTED}">{label}</text>'
            f'<text x="{HX + 14}" y="{y + 42}" font-size="21" font-weight="700" fill="{TEXT}">{value}'
            f'<tspan font-size="12" font-weight="400" fill="{MUTED}"> {unit}</tspan></text>'
        )

    hud = [
        hud_box(WY - 6, "SCORE", f"{total:,}", "contribs", VIOLET),
        hud_box(WY + 54, "ACTIVE DAYS", active_days, "/ year", CYAN),
        hud_box(WY + 114, "BEST STREAK", longest, "days", PINK),
    ]
    ny = WY + 174
    hud.append(f'<rect x="{HX}" y="{ny}" width="{W - HX - 28}" height="{WY + WH - ny}" rx="10" fill="{PANEL_2}" stroke="{BORDER}"/>'
               f'<text class="m" x="{HX + 14}" y="{ny + 19}" font-size="10" letter-spacing="1.5" fill="{MUTED}">NEXT</text>')
    order = sorted(range(n), key=lambda i: spawn[i])
    events = [(0.0, pieces[order[0]][0])]
    events += [(spawn[a], pieces[b][0]) for a, b in zip(order, order[1:])]
    events.append((spawn[order[-1]], pieces[order[0]][0]))
    box_w = W - HX - 28
    for kind, shapes in TETROMINOES.items():
        shape = shapes[0]
        sw = max(x for x, _ in shape) + 1
        sh = max(y for _, y in shape) + 1
        s2 = 13
        px = HX + 14 + (box_w - 28 - sw * (s2 + 2)) / 2 + 10
        py = ny + 26 + (WY + WH - ny - 34 - sh * (s2 + 2)) / 2
        mini = "".join(block(px + x * (s2 + 2), py + (sh - 1 - y) * (s2 + 2), s2, PIECE_COLORS[kind]) for x, y in shape)
        stops = {}
        for t, k in events:
            stops[pct(t, T)] = 1 if k == kind else 0
        frames = "".join(f"{p}{{opacity:{v}}}" for p, v in stops.items())
        last = list(stops.values())[-1]
        css.append(f"@keyframes n{kind}{{{frames}100%{{opacity:{last}}}}}"
                   f".n{kind}{{animation:n{kind} {T:.2f}s step-end infinite}}")
        hud.append(f'<g class="n{kind}" opacity="0">{mini}</g>')

    # ---- title bar
    logo = "".join(block(32 + i * 13, 34 + (0 if i == 1 else 0), 11, col) for i, col in
                   enumerate([CYAN, VIOLET, PINK]))
    logo += block(45, 47, 11, VIOLET)
    title = (
        f'{logo}<text class="m" x="86" y="52" font-size="20" font-weight="700" letter-spacing="4" '
        f'fill="{TEXT}">COMMIT STACK</text>'
        f'<text class="m" x="{W - 28}" y="52" text-anchor="end" font-size="13" fill="{MUTED}">'
        f'@{esc(user)} · contributions · last 12 months</text>'
    )

    defs = (f"<defs>{panel_defs('cs')}<clipPath id=\"well\"><rect x=\"{WX - 6}\" y=\"{WY - 2}\" "
            f"width=\"{WW + 12}\" height=\"{WH + 4}\"/></clipPath></defs>")
    well = (f'<rect x="{WX - 10}" y="{WY - 10}" width="{WW + 20}" height="{WH + 20}" rx="12" '
            f'fill="#090C1F" stroke="{BORDER}"/>')
    body = (defs + panel(W, H, "cs") + title + well + "".join(slots) + "".join(labels) + "".join(legend)
            + f'<g clip-path="url(#well)">{"".join(body_pieces)}</g>' + "".join(flashes) + banner
            + "".join(hud))
    alt = (f"Commit Stack: falling blocks assemble {user}'s contribution graph. {total} contributions, "
           f"{active_days} active days and a best streak of {longest} days in the last 12 months.")
    return svg(W, H, body, alt, "".join(css))


# ---------------------------------------------------------------- player stats svg

def player_stats(user, profile, days, stats):
    current, longest, active_days = stats
    total = sum(n for _, n, _ in days)
    W, H = 1200, 282
    tiles = [
        ("CONTRIBUTIONS", f"{total:,}", "past year", VIOLET),
        ("CURRENT STREAK", current, "days", CYAN),
        ("LONGEST STREAK", longest, "days", PINK),
        ("PUBLIC REPOS", profile["public_repos"], "", GREEN),
        ("LIVE APPS", profile["live"], "deployed", ORANGE),
        ("STARS EARNED", profile["stars"], "", BLUE),
    ]
    out = []
    logo = "".join(block(32 + i * 13, 34, 11, col) for i, col in enumerate([GREEN, ORANGE, BLUE]))
    logo += block(32, 47, 11, GREEN)
    out.append(
        f'{logo}<text class="m" x="86" y="52" font-size="20" font-weight="700" letter-spacing="4" '
        f'fill="{TEXT}">PLAYER STATS</text>'
        f'<text class="m" x="{W - 28}" y="52" text-anchor="end" font-size="13" fill="{MUTED}">'
        f'P1 · {esc(profile["name"])} · @{esc(user)}</text>'
    )
    tw, gap, x0, y0 = 176, 16, 32, 78
    for i, (label, value, unit, color) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        out.append(
            f'<g class="t" style="animation-delay:{i * 0.08:.2f}s">'
            f'<rect x="{x}" y="{y0}" width="{tw}" height="98" rx="14" fill="{PANEL_2}" stroke="{BORDER}"/>'
            + block(x + 16, y0 + 16, 11, color)
            + f'<text class="m" x="{x + 35}" y="{y0 + 26}" font-size="11" letter-spacing="1.2" fill="{MUTED}">{label}</text>'
            f'<text x="{x + 16}" y="{y0 + 74}" font-size="34" font-weight="700" fill="{TEXT}">{value}'
            f'<tspan font-size="14" font-weight="400" fill="{MUTED}"> {unit}</tspan></text></g>'
        )

    langs = profile["languages"][:6]
    other = sum(v for _, v in profile["languages"][6:])
    if other > 0:
        langs.append(("Other", other))
    total_w = sum(v for _, v in langs) or 1
    palette = [VIOLET, CYAN, PINK, GREEN, ORANGE, BLUE, MUTED]
    by = 210
    out.append(f'<text class="m" x="32" y="{by}" font-size="11" letter-spacing="1.5" fill="{MUTED}">'
               f'TOP LANGUAGES · WEIGHTED BY PROJECT</text>')
    bar_w = W - 64
    out.append(f'<clipPath id="bar"><rect x="32" y="{by + 12}" width="{bar_w}" height="12" rx="6"/></clipPath>')
    x = 32.0
    segs, legend = [], []
    lx = 32
    for i, (name, v) in enumerate(langs):
        w = v / total_w * bar_w
        segs.append(f'<rect x="{x:.1f}" y="{by + 12}" width="{w + 0.5:.1f}" height="12" fill="{palette[i]}"/>')
        x += w
        label = f"{name} {v / total_w * 100:.0f}%"
        legend.append(block(lx, by + 40, 11, palette[i])
                      + f'<text x="{lx + 18}" y="{by + 50}" font-size="14" fill="{SUBTEXT}">{esc(name)}'
                      f'<tspan fill="{MUTED}"> {v / total_w * 100:.0f}%</tspan></text>')
        lx += 34 + int(len(label) * 7.6)
    out.append(f'<g clip-path="url(#bar)">{"".join(segs)}</g>' + "".join(legend))

    css = (f"text{{font-family:{FONT}}}.m{{font-family:{MONO}}}"
           "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
           ".t{animation:up .6s ease-out both}")
    alt = (f"Player stats for {user}: {total} contributions this year, current streak {current} days, "
           f"longest streak {longest} days, {profile['public_repos']} public repos, "
           f"{profile['live']} live apps, {profile['stars']} stars.")
    return svg(W, H, f"<defs>{panel_defs('ps')}</defs>" + panel(W, H, "ps") + "".join(out), alt, css)


# ------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or None

    days = fetch_calendar(args.user, token)
    profile = fetch_profile(args.user, token)
    stats = streaks(days)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "commit-stack.svg").write_text(commit_stack(args.user, days, stats), encoding="utf-8")
    (out / "player-stats.svg").write_text(player_stats(args.user, profile, days, stats), encoding="utf-8")
    print(f"wrote {out}/commit-stack.svg and {out}/player-stats.svg "
          f"({sum(n for _, n, _ in days)} contributions, streaks {stats[0]}/{stats[1]})")


if __name__ == "__main__":
    main()

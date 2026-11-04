"""Moonlight Arcade theme: shared palette and SVG helpers for every profile graphic."""
from html import escape

# Night-sky surfaces
BG_TOP = "#0E1130"
BG_BOTTOM = "#070916"
PANEL = "#11152E"
PANEL_2 = "#161B3A"
BORDER = "#272D57"
GRID = "#1A1F3F"

# Text
TEXT = "#ECEEFF"
SUBTEXT = "#C3C7EA"
MUTED = "#8A8FBA"

# Accents
VIOLET = "#A78BFA"
VIOLET_DEEP = "#7C3AED"
CYAN = "#22D3EE"
PINK = "#F472B6"
MOON = "#FDE68A"
GREEN = "#34D399"
ORANGE = "#FB923C"
BLUE = "#60A5FA"
YELLOW = "#FACC15"

# One colour per falling-block shape
PIECE_COLORS = {
    "I": CYAN,
    "O": YELLOW,
    "T": VIOLET,
    "S": GREEN,
    "Z": PINK,
    "J": BLUE,
    "L": ORANGE,
}

# Contribution intensity, empty day -> busiest day
LEVELS = ["#1C2144", "#3E318A", "#6246C9", "#9277F5", "#D4C8FF"]

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'DejaVu Sans Mono', Menlo, monospace"


def esc(text):
    return escape(str(text), quote=True)


def panel_defs(uid="p"):
    """Gradient + soft glow shared by the dark panels."""
    return (
        f'<linearGradient id="{uid}bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>'
        f"</linearGradient>"
        f'<radialGradient id="{uid}glow" cx="0.15" cy="0" r="0.9">'
        f'<stop offset="0" stop-color="{VIOLET_DEEP}" stop-opacity="0.22"/>'
        f'<stop offset="1" stop-color="{VIOLET_DEEP}" stop-opacity="0"/>'
        f"</radialGradient>"
    )


def panel(w, h, uid="p", r=20):
    return (
        f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#{uid}bg)"/>'
        f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#{uid}glow)"/>'
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="none" '
        f'stroke="{BORDER}" stroke-width="1.5"/>'
    )


def svg(w, h, body, title, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        + (f"<style>{style}</style>" if style else "")
        + body
        + "</svg>\n"
    )


def block(x, y, s, fill, cls="", extra=""):
    """A single bevelled block: base square plus a soft top highlight."""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{s}" height="{s}" rx="{max(2, s // 5)}" fill="{fill}"{c}{extra}/>'
        f'<rect x="{x + 2:g}" y="{y + 2:g}" width="{s - 4}" height="{max(2, s // 6)}" rx="1" '
        f'fill="#fff" opacity=".22"/>'
    )


def pixel_art(rows, x, y, s, fill, gap=0):
    """Render a list of strings ('X' = filled) as crisp squares."""
    out = []
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "X":
                out.append(
                    f'<rect x="{x + i * (s + gap):g}" y="{y + j * (s + gap):g}" '
                    f'width="{s}" height="{s}" fill="{fill}"/>'
                )
    return "".join(out)

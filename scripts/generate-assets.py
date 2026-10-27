"""Generates the profile README assets (hero, project cards, avatar) in the duthris-dpi palette.

Every image ships in a dark and a light variant; the README swaps them with <picture>.
SVGs use only system fonts and inline CSS, because GitHub serves them as plain images.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "Inter, 'Segoe UI Variable Display', 'Segoe UI', system-ui, -apple-system, sans-serif"
MONO = "'Cascadia Code', 'JetBrains Mono', Consolas, 'SFMono-Regular', monospace"

THEMES = {
    "dark": dict(
        bg0="#140c26", bg1="#0b0911", bg2="#1a0f33",
        grid="#ffffff", grid_op="0.035",
        glow1_op="0.55", glow2_op="0.35",
        t0="#d4c8ff", t1="#9c81f9", t2="#6b6cf0",
        text="#c9c2e6", muted="#8f86ad",
        card="#110c1d", card_border="#2a2140", panel="#1a1330", panel2="#231a40", line="#352a57",
        chip_text="#d4c8ff", green_text="#a7f3d0", amber_text="#fde68a",
        flow_op="0.28",
    ),
    "light": dict(
        bg0="#f3eeff", bg1="#ffffff", bg2="#ebe4ff",
        grid="#2a1d5c", grid_op="0.045",
        glow1_op="0.22", glow2_op="0.16",
        t0="#3a1f7a", t1="#6833e6", t2="#4f46e5",
        text="#2b2347", muted="#6b6385",
        card="#ffffff", card_border="#e2d9fb", panel="#f5f1ff", panel2="#ece5ff", line="#d9cff7",
        chip_text="#4b28b8", green_text="#047857", amber_text="#92400e",
        flow_op="0.35",
    ),
}

ICON_GRADIENT = """
    <linearGradient id="icon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#9C81F9"/>
      <stop offset="0.5" stop-color="#6833E6"/>
      <stop offset="1" stop-color="#3A1F7A"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0.22"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>"""


def text_width(s: str, size: float, k: float = 0.56) -> float:
    return len(s) * size * k


def chips(items, x, y, size=17, h=34, gap=12, theme=None):
    """items: list of (label, tone) where tone is violet | green | amber."""
    tones = {
        "violet": ("#7c4dff", "#9c81f9", theme["chip_text"]),
        "green": ("#10b981", "#34d399", theme["green_text"]),
        "amber": ("#f59e0b", "#fbbf24", theme["amber_text"]),
    }
    out, cx = [], x
    for label, tone in items:
        fill, stroke, color = tones[tone]
        w = text_width(label, size) + 36
        out.append(
            f'<rect x="{cx:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{fill}" '
            f'fill-opacity="0.16" stroke="{stroke}" stroke-opacity="0.5"/>'
            f'<text x="{cx + w/2:.0f}" y="{y + h/2 + size*0.35:.0f}" text-anchor="middle" '
            f'font-size="{size}" font-weight="600" fill="{color}">{escape(label)}</text>'
        )
        cx += w + gap
    return "\n    ".join(out)


def mark(size: int, glow: bool = True) -> str:
    """The personal mark: the old `>_` prompt redrawn in the duthris-dpi icon style (240-unit box)."""
    s = size / 240
    glow_rect = (
        '<rect x="14" y="26" width="212" height="212" rx="56" fill="#7c4dff" opacity="0.55" filter="url(#soft)"/>'
        if glow else ""
    )
    return f"""<g transform="scale({s:.4f})">
      {glow_rect}
      <rect width="240" height="240" rx="60" fill="url(#icon)"/>
      <rect width="240" height="240" rx="60" fill="url(#shine)"/>
      <path d="M62 78 L112 120 L62 162" fill="none" stroke="#fff" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
      <rect class="cursor" x="128" y="150" width="58" height="22" rx="11" fill="#fff"/>
    </g>"""


def hero(t, name):
    th = THEMES[t]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 420" width="1280" height="420" role="img" aria-label="Anıl Yalımdemir — full-stack developer, open source at heart">
  <style>
    .cursor {{ animation: blink 1.1s steps(1) infinite; }}
    .flow {{ stroke-dasharray: 6 18; animation: flow 2.4s linear infinite; }}
    .flow.slow {{ animation-duration: 3.6s; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes flow {{ to {{ stroke-dashoffset: -96; }} }}
    @media (prefers-reduced-motion: reduce) {{ .cursor, .flow {{ animation: none; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{th['bg0']}"/>
      <stop offset="0.55" stop-color="{th['bg1']}"/>
      <stop offset="1" stop-color="{th['bg2']}"/>
    </linearGradient>
    <radialGradient id="glow1" cx="0.2" cy="0.5" r="0.45">
      <stop offset="0" stop-color="#7c4dff" stop-opacity="{th['glow1_op']}"/>
      <stop offset="1" stop-color="#7c4dff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="0.88" cy="0.1" r="0.5">
      <stop offset="0" stop-color="#4f46e5" stop-opacity="{th['glow2_op']}"/>
      <stop offset="1" stop-color="#4f46e5" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{th['t0']}"/>
      <stop offset="0.55" stop-color="{th['t1']}"/>
      <stop offset="1" stop-color="{th['t2']}"/>
    </linearGradient>{ICON_GRADIENT}
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{th['grid']}" stroke-opacity="{th['grid_op']}" stroke-width="1"/>
    </pattern>
    <clipPath id="frame"><rect width="1280" height="420" rx="28"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1280" height="420" fill="url(#bg)"/>
    <rect width="1280" height="420" fill="url(#grid)"/>
    <rect width="1280" height="420" fill="url(#glow1)"/>
    <rect width="1280" height="420" fill="url(#glow2)"/>

    <!-- Data flowing out to the right edge. -->
    <g fill="none" stroke-linecap="round" stroke-width="2.5">
      <path class="flow" d="M880 352 C 1000 352, 1080 312, 1290 312" stroke="#9c81f9" stroke-opacity="{th['flow_op']}"/>
      <path class="flow slow" d="M900 378 C 1030 378, 1110 360, 1290 360" stroke="#6b6cf0" stroke-opacity="{th['flow_op']}"/>
      <path class="flow" d="M1080 322 C 1140 322, 1180 270, 1290 270" stroke="#b9a6ff" stroke-opacity="{th['flow_op']}"/>
      <path class="flow slow" d="M960 70 C 1060 70, 1120 110, 1290 110" stroke="#6b6cf0" stroke-opacity="{th['flow_op']}"/>
    </g>
  </g>

  <g transform="translate(100 90)">{mark(240)}</g>

  <g font-family="{FONT}">
    <text x="410" y="168" font-size="80" font-weight="800" letter-spacing="-2.5" fill="url(#title)">{name}</text>
    <text x="414" y="222" font-size="30" font-weight="500" fill="{th['text']}">Full-stack developer. Open source at heart.</text>
    <text x="414" y="262" font-size="22" font-weight="400" fill="{th['muted']}" font-family="{MONO}">web · local-first apps · discord bots</text>
    {chips([("Antalya, TR", "violet"), ("DT Cloud", "violet"), ("Open source", "green")], 414, 296, theme=th)}
  </g>
</svg>
"""
    (OUT / f"hero-{t}.svg").write_text(svg, encoding="utf-8")


def dpi_scene(th):
    """Mini app window: one big button, live status, service toggles."""
    toggles = ""
    for i, (label, on) in enumerate([("Discord", True), ("YouTube", True), ("Roblox", False)]):
        y = 58 + i * 34
        knob_x = 252 if on else 236
        toggles += f"""
      <text x="150" y="{y + 14}" font-size="13" font-weight="500" fill="{th['text']}">{label}</text>
      <rect x="230" y="{y}" width="40" height="22" rx="11" fill="{'#7c4dff' if on else th['line']}"/>
      <circle cx="{knob_x + 7}" cy="{y + 11}" r="8" fill="#fff"/>"""
    return f"""
    <g transform="translate(150 26)">
      <rect width="300" height="170" rx="14" fill="{th['panel']}" stroke="{th['line']}"/>
      <circle cx="18" cy="16" r="4" fill="{th['line']}"/><circle cx="32" cy="16" r="4" fill="{th['line']}"/><circle cx="46" cy="16" r="4" fill="{th['line']}"/>
      <circle cx="70" cy="96" r="44" fill="#7c4dff" opacity="0.35" filter="url(#soft)"/>
      <circle cx="70" cy="96" r="38" fill="url(#icon)"/>
      <path d="M70 76 V96 M56 84 A 20 20 0 1 0 84 84" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
      <circle cx="40" cy="152" r="4" fill="#34d399"/>
      <text x="50" y="156" font-size="12" font-weight="600" fill="{th['green_text']}">Connected</text>{toggles}
    </g>"""


def iptv_scene(th):
    """Mini app window: channel list on the left, poster grid on the right."""
    rows = ""
    for i in range(5):
        y = 34 + i * 26
        active = i == 1
        rows += (
            f'<rect x="10" y="{y}" width="78" height="20" rx="6" fill="{"#7c4dff" if active else th["panel2"]}" '
            f'fill-opacity="{"0.85" if active else "1"}"/>'
            f'<rect x="18" y="{y + 8}" width="{40 - (i * 5) % 18}" height="4" rx="2" fill="{"#fff" if active else th["line"]}"/>'
        )
    posters = ""
    shades = ["#3A1F7A", "#6833E6", "#4f46e5", "#9C81F9", "#2b1a5c", "#6b6cf0"]
    for i in range(6):
        x = 102 + (i % 3) * 64
        y = 34 + (i // 3) * 66
        posters += f'<rect x="{x}" y="{y}" width="56" height="58" rx="7" fill="{shades[i]}" fill-opacity="0.85"/>'
    return f"""
    <g transform="translate(150 26)">
      <rect width="300" height="170" rx="14" fill="{th['panel']}" stroke="{th['line']}"/>
      <circle cx="18" cy="16" r="4" fill="{th['line']}"/><circle cx="32" cy="16" r="4" fill="{th['line']}"/><circle cx="46" cy="16" r="4" fill="{th['line']}"/>
      {rows}
      {posters}
      <circle cx="166" cy="96" r="20" fill="#000" fill-opacity="0.35"/>
      <path d="M160 86 L176 96 L160 106 Z" fill="#fff"/>
      <rect x="102" y="152" width="184" height="4" rx="2" fill="{th['line']}"/>
      <rect x="102" y="152" width="112" height="4" rx="2" fill="#9c81f9"/>
    </g>"""


def card(t, slug, title, tagline, chip_items, scene):
    th = THEMES[t]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="600" height="380" role="img" aria-label="{title}: {tagline}">
  <defs>{ICON_GRADIENT}
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
    <radialGradient id="g" cx="0.5" cy="0" r="0.8">
      <stop offset="0" stop-color="#7c4dff" stop-opacity="{'0.28' if t == 'dark' else '0.14'}"/>
      <stop offset="1" stop-color="#7c4dff" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{th['grid']}" stroke-opacity="{th['grid_op']}"/>
    </pattern>
  </defs>
  <rect x="0.5" y="0.5" width="599" height="379" rx="22" fill="{th['card']}" stroke="{th['card_border']}"/>
  <path d="M1 222 V22 A21 21 0 0 1 22 1 H578 A21 21 0 0 1 599 22 V222 Z" fill="url(#grid)"/>
  <path d="M1 222 V22 A21 21 0 0 1 22 1 H578 A21 21 0 0 1 599 22 V222 Z" fill="url(#g)"/>
  <line x1="1" y1="222" x2="599" y2="222" stroke="{th['card_border']}"/>
  <g font-family="{FONT}">{scene(th)}
    <text x="32" y="270" font-size="28" font-weight="800" letter-spacing="-0.6" fill="{th['text']}">{title}</text>
    <text x="32" y="302" font-size="16" fill="{th['muted']}">{tagline}</text>
    {chips(chip_items, 32, 326, size=13, h=28, gap=8, theme=th)}
    <text x="568" y="270" text-anchor="end" font-size="22" fill="{th['t1']}">→</text>
  </g>
</svg>
"""
    (OUT / f"card-{slug}-{t}.svg").write_text(svg, encoding="utf-8")


def avatar():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>{ICON_GRADIENT}
    <radialGradient id="bg" cx="0.5" cy="0.42" r="0.7">
      <stop offset="0" stop-color="#2a1660"/>
      <stop offset="0.6" stop-color="#140c26"/>
      <stop offset="1" stop-color="#0b0911"/>
    </radialGradient>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
  </defs>
  <rect width="512" height="512" fill="url(#bg)"/>
  <g transform="translate(136 130)">{mark(240)}</g>
</svg>
"""
    (OUT / "avatar.svg").write_text(svg, encoding="utf-8")


for t in THEMES:
    hero(t, "Anıl Yalımdemir")
    card(t, "dpi", "Duthris DPI", "One-click DPI bypass that finds what works.",
         [("One click", "violet"), ("Open source", "violet"), ("331 downloads", "green")], dpi_scene)
    card(t, "iptv", "Duthris IPTV", "Local-first IPTV player. Bring your own playlist.",
         [("Local-first", "violet"), ("Plays MKV & AC-3", "violet"), ("No account", "amber")], iptv_scene)
avatar()
print("ok:", sorted(p.name for p in OUT.iterdir()))

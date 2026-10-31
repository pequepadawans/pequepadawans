#!/usr/bin/env python3
"""Genera assets/hero.svg: terminal animada para el perfil de GitHub.

Sin dependencias, sin fuentes externas, sin JS. Todo el movimiento es CSS/SVG
para que funcione dentro de un <img> en GitHub.
"""
import pathlib

W, H = 880, 300
BG = "#0b0f12"
BAR = "#11171c"
LINE = "#21262d"
TXT = "#c9d1d9"
DIM = "#7d8590"
LIME = "#9fef00"
MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', monospace")

ADV = 0.6 * 15.5  # avance aproximado de la monoespaciada

X = 30
BASE = 80
LH = 32


def tw(s: str, spacing: float = 0.0) -> float:
    return len(s) * (ADV + spacing)


# ------------------------------------------------------------------ líneas
lines = []

y = BASE
cmd1 = "$ whoami"
lines.append(f'  <text x="{X}" y="{y}" font-size="15.5" fill="{LIME}" mask="url(#m1)">$ whoami</text>')

y += LH
lines.append(
    f'  <text x="{X}" y="{y}" font-size="15.5" fill="{TXT}" class="fade" style="animation-delay:.60s">'
    f'daniel calvo<tspan fill="{DIM}"> · offensive security</tspan></text>'
)

y += LH + 8
cmd2 = "$ cat focus.txt"
lines.append(f'  <text x="{X}" y="{y}" font-size="15.5" fill="{LIME}" mask="url(#m2)">$ cat focus.txt</text>')

y += LH
lines.append(
    f'  <text x="{X}" y="{y}" font-size="15.5" fill="{TXT}" class="fade" style="animation-delay:1.55s">'
    f'active directory <tspan fill="{DIM}">·</tspan> windows internals '
    f'<tspan fill="{DIM}">·</tspan> c2 <tspan fill="{DIM}">·</tspan> evasion</text>'
)

y += LH + 8
cmd3 = "$ ls ~/certs"
lines.append(f'  <text x="{X}" y="{y}" font-size="15.5" fill="{LIME}" mask="url(#m3)">$ ls ~/certs</text>')

y += LH
certs = ["CRTO", "CPTS", "CWI-RTO", "CPIA", "CRT-ID", "AZRTS"]
SP, SPACING = 24, 0.5
cursor_x = X
spans = []
for i, c in enumerate(certs):
    spans.append(f'<tspan x="{cursor_x:.1f}">{c}</tspan>')
    cursor_x += tw(c, SPACING) + SP
lines.append(
    f'  <g class="fade" style="animation-delay:2.35s">\n'
    f'    <text y="{y}" font-size="15.5" fill="{LIME}" letter-spacing="{SPACING}">'
    f'{"".join(spans)}</text>\n  </g>'
)

# cursor parpadeante al final de la última salida
lines.append(
    f'  <g class="appear" style="animation-delay:2.55s">\n'
    f'    <rect x="{X}" y="{y + 6}" width="9" height="17" fill="{LIME}" class="blink"/>\n  </g>'
)

# ------------------------------------------------------------ máscaras typing
def mask(mid: str, text: str, line_y: int, dur: str, delay: str, steps: int) -> str:
    w = tw(text) + 14
    return (
        f'  <mask id="{mid}" maskUnits="userSpaceOnUse">\n'
        f'    <rect class="type" x="{X}" y="{line_y - 16}" width="{w:.1f}" height="24" fill="#fff"\n'
        f'          style="transform-origin:{X}px 0px; animation:type {dur}s steps({steps}) {delay}s both"/>\n'
        f'  </mask>'
    )


masks = "\n".join([
    mask("m1", cmd1, BASE, ".40", ".10", 9),
    mask("m2", cmd2, BASE + 2 * LH + 8, ".45", "1.00", 15),
    mask("m3", cmd3, BASE + 4 * LH + 16, ".35", "1.90", 13),
])

# ------------------------------------------------------------ panel derecho
PX = 620
panel = f"""  <line x1="588" y1="66" x2="588" y2="252" stroke="{LINE}" stroke-width="1"/>
  <text x="{PX}" y="84" font-size="10" fill="{DIM}" letter-spacing="2.4">STATUS</text>
  <circle cx="{PX + 4}" cy="106" r="4" fill="{LIME}">
    <animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="{PX + 16}" y="111" font-size="13" fill="{TXT}">open to work</text>

  <text x="{PX}" y="148" font-size="10" fill="{DIM}" letter-spacing="2.4">LOCATION</text>
  <text x="{PX}" y="172" font-size="13" fill="{TXT}">Madrid, ES</text>

  <text x="{PX}" y="208" font-size="10" fill="{DIM}" letter-spacing="2.4">HACK THE BOX</text>
  <text x="{PX}" y="232" font-size="13" fill="{TXT}">Top 100 <tspan fill="{DIM}">·</tspan> Spain</text>"""

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="pequepadawans — offensive security">
  <title>pequepadawans — offensive security</title>
  <style>
    text {{ font-family: {MONO}; }}
    /* Sin opacity:0 en la clase: si el navegador no ejecuta animaciones,
       el texto queda visible en vez de desaparecer. */
    .fade   {{ animation: fade .45s ease-out both; }}
    .appear {{ animation: fade .01s linear both; }}
    .blink  {{ animation: blink 1.1s steps(1) infinite; }}
    .type   {{ transform-box: view-box; }}
    @keyframes fade  {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes blink {{ 0%, 49%   {{ opacity: 1; }}
                        50%, 100% {{ opacity: 0; }} }}
    @keyframes type  {{ from {{ transform: scaleX(0); }}
                        to   {{ transform: scaleX(1); }} }}
    @keyframes scan  {{ from {{ transform: translateY(0); }}
                        to   {{ transform: translateY(220px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .fade, .appear {{ animation: none; }}
      .blink, .scan  {{ animation: none; }}
      .type          {{ animation: none; transform: none; }}
    }}
  </style>

  <defs>
    <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{LIME}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#161d23" stroke-width="1"/>
    </pattern>
    <clipPath id="body">
      <rect x="1" y="37" width="{W - 2}" height="{H - 38}" rx="13"/>
    </clipPath>
{masks}
  </defs>

  <!-- ventana -->
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14"
        fill="{BG}" stroke="{LINE}" stroke-width="1"/>
  <path d="M0.5 14.5A14 14 0 0 1 14.5 0.5h{W - 29}a14 14 0 0 1 14 14V37H0.5Z" fill="{BAR}"/>
  <line x1="1" y1="37.5" x2="{W - 1}" y2="37.5" stroke="{LINE}" stroke-width="1"/>

  <!-- chrome -->
  <circle cx="22" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="41" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="60" cy="19" r="5.5" fill="#27c93f"/>
  <text x="{W / 2}" y="23" font-size="11.5" fill="{DIM}" text-anchor="middle">pequepadawans@github: ~</text>

  <g clip-path="url(#body)">
    <rect x="1" y="38" width="{W - 2}" height="{H - 39}" fill="url(#grid)" opacity="0.55"/>
    <rect x="1" y="38" width="420" height="200" fill="url(#glow)"/>
    <rect class="scan" x="1" y="38" width="{W - 2}" height="34" fill="url(#scan)" opacity="0.13"/>
{chr(10).join(lines)}
{panel}
  </g>
</svg>
"""

out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"escrito {out} ({len(svg)} bytes)")

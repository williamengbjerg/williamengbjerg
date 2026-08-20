"""
Regenerates dark_mode.svg and light_mode.svg from the content below.

Edit PANEL / SECTIONS / the ASCII art in art.txt, then run:

    python3 build_svg.py

The numbers in the GitHub Stats block are placeholders here; today.py
overwrites them (and the dot leaders) on every scheduled run.
"""

ART_FILE = 'art.txt'

# ---------------------------------------------------------------- content ---

TITLE = 'william@engbjerg'

# (label, value, element_id) -- label parts split on '.' are coloured as keys.
# element_id is set for the fields today.py rewrites; None for static text.
PANEL = [
    ('OS', 'macOS 26, iOS, Linux', None),
    ('Experience', '0 years (since 2006)', 'age_data'),
    ('Host', 'Self-employed', None),
    ('Kernel', 'Indie SaaS builder', None),
    ('IDE', 'PhpStorm, PyCharm, Rider, Xcode', None),
    None,
    ('Languages.Programming', 'PHP, Swift, Python, JavaScript', None),
    ('Languages.Computer', 'HTML, CSS, Blade, YAML, SQL', None),
    ('Languages.Real', 'English', None),
    None,
    ('Hobbies.Software', 'SaaS, web apps, iOS apps', None),
    ('Hobbies.Hardware', 'Self-hosting, Incus fleet', None),
]

# Extra titled sections between the panel and the GitHub Stats block.
# Add or remove rows freely -- the vertical spacing rebalances itself.
SECTIONS = [
    ('- Stack', [
        ('Stack.Backend', 'Laravel, Filament, Livewire, FastAPI', None),
        ('Stack.Frontend', 'Tailwind, Alpine, Astro, React', None),
        ('Stack.Infra', 'Incus, Hetzner, Caddy, n8n', None),
        ('Stack.Services', 'Stripe, Cloudflare, S3', None),
    ]),
]

# ------------------------------------------------------------------ layout ---

COLS = 58          # panel width, in characters
ART_COLS = 70      # art.txt width, in characters

# Monospace advance is 0.602em on the widest common fallbacks (DejaVu Sans Mono,
# Menlo). Consolas is narrower, so sizing for 0.602 leaves slack, never clips.
ADVANCE = 0.602
FONT = 16          # panel font size
ART_FONT = 11      # the art is set smaller so a denser grid fits the same width
CHAR = FONT * ADVANCE
ART_CHAR = ART_FONT * ADVANCE
ART_X = 15
GUTTER = 26
PANEL_X = int(ART_X + ART_COLS * ART_CHAR + GUTTER)
LINE = 20          # panel line height
ART_LINE = 13      # art line height (keeps cells near 1:2 so the face isn't squashed)
TOP = 30
SECTION_GAP = 40   # blank space above '- Contact' and '- GitHub Stats'
WIDTH = int(PANEL_X + COLS * CHAR + ART_X)
HEIGHT = 530

THEMES = {
    'dark_mode.svg': dict(bg='#161b22', fg='#c9d1d9', key='#ffa657', value='#a5d6ff',
                          add='#3fb950', dele='#f85149', cc='#616e7f'),
    'light_mode.svg': dict(bg='#ffffff', fg='#24292f', key='#953800', value='#0550ae',
                           add='#1a7f37', dele='#cf222e', cc='#57606a'),
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def dots(label, value):
    """Dot leader that right-aligns value at COLS. Mirrors justify_format()."""
    n = COLS - 2 - len(label) - 1 - 2 - len(value)
    return ' ' + '.' * max(0, n) + ' '


def field_length(label, value):
    """The `length` argument today.py needs to reproduce this row's alignment."""
    return COLS - 2 - len(label) - 1 - 2


def keyed(label):
    """Colour 'Languages.Programming' as two keys separated by a literal dot."""
    return '.'.join(f'<tspan class="key">{esc(p)}</tspan>' for p in label.split('.'))


def row(y, label, value, elem_id):
    d = dots(label, value)
    did = f' id="{elem_id}_dots"' if elem_id else ''
    vid = f' id="{elem_id}"' if elem_id else ''
    return (f'<tspan x="{PANEL_X}" y="{y}" class="cc">. </tspan>{keyed(label)}:'
            f'<tspan class="cc"{did}>{d}</tspan>'
            f'<tspan class="value"{vid}>{esc(value)}</tspan>')


def rule(y, text):
    pad = COLS - len(text) - 2
    return (f'<tspan x="{PANEL_X}" y="{y}">{esc(text)}</tspan> '
            + '—' * max(0, pad))


def build(path, t):
    art = [l.rstrip('\n') for l in open(ART_FILE, encoding='utf-8')]
    out = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" '
        f'width="{WIDTH}px" height="{HEIGHT}px" font-size="16px">',
        '<style>',
        '@font-face {',
        "src: local('Consolas'), local('Consolas Bold');",
        "font-family: 'ConsolasFallback';",
        'font-display: swap;',
        '-webkit-size-adjust: 109%;',
        'size-adjust: 109%;',
        '}',
        f'.key {{fill: {t["key"]};}}',
        f'.value {{fill: {t["value"]};}}',
        f'.addColor {{fill: {t["add"]};}}',
        f'.delColor {{fill: {t["dele"]};}}',
        f'.cc {{fill: {t["cc"]};}}',
        'text, tspan {white-space: pre;}',
        '</style>',
        f'<rect width="{WIDTH}px" height="{HEIGHT}px" fill="{t["bg"]}" rx="15"/>',
        f'<text x="{ART_X}" y="{TOP}" fill="{t["fg"]}" class="ascii" '
        f'font-size="{ART_FONT}px" xml:space="preserve">',
    ]
    art_top = TOP + max(0, (HEIGHT - TOP - len(art) * ART_LINE)) // 2
    for i, line in enumerate(art):
        out.append(f'<tspan x="{ART_X}" y="{art_top + i * ART_LINE}">{esc(line)}</tspan>')
    out.append('</text>')

    out.append(f'<text x="{PANEL_X}" y="{TOP}" fill="{t["fg"]}" xml:space="preserve">')
    out.append(rule(TOP, TITLE))
    y = TOP
    for item in PANEL:
        y += LINE
        if item is None:
            out.append(f'<tspan x="{PANEL_X}" y="{y}" class="cc">. </tspan>')
        else:
            out.append(row(y, *item))

    # Sections are spaced by SECTION_GAP, then whatever vertical slack is left
    # over (the art is taller than the panel) is shared evenly between the two
    # gaps, so the panel stays balanced when rows are added or removed.
    n_gaps = len(SECTIONS) + 1
    body = sum((1 + len(rows)) * LINE for _, rows in SECTIONS) + 4 * LINE
    natural_end = y + n_gaps * SECTION_GAP + body
    gap = SECTION_GAP + max(0, (HEIGHT - TOP) - natural_end) // n_gaps

    for title, rows in SECTIONS:
        y += gap
        out.append(rule(y, title))
        for item in rows:
            y += LINE
            out.append(row(y, *item))

    y += gap
    out.append(rule(y, '- GitHub Stats'))
    # Repos / Stars
    out.append(
        f'<tspan x="{PANEL_X}" y="{y + 20}" class="cc">. </tspan><tspan class="key">Repos</tspan>:'
        f'<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan>'
        f' {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>}}'
        f' | <tspan class="key">Stars</tspan>:'
        f'<tspan class="cc" id="star_data_dots"> ....... </tspan><tspan class="value" id="star_data">0</tspan>')
    # Commits / Followers
    out.append(
        f'<tspan x="{PANEL_X}" y="{y + 40}" class="cc">. </tspan><tspan class="key">Commits</tspan>:'
        f'<tspan class="cc" id="commit_data_dots"> ............. </tspan><tspan class="value" id="commit_data">0</tspan>'
        f' | <tspan class="key">Followers</tspan>:'
        f'<tspan class="cc" id="follower_data_dots"> ... </tspan><tspan class="value" id="follower_data">0</tspan>')
    # Lines of code
    out.append(
        f'<tspan x="{PANEL_X}" y="{y + 60}" class="cc">. </tspan>'
        f'<tspan class="key">Lines of Code</tspan>:'
        f'<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan>'
        f' ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>,'
        f' <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
        f'<tspan class="delColor">--</tspan> )')
    out.append('</text>')
    out.append('</svg>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'wrote {path}')


if __name__ == '__main__':
    for path, theme in THEMES.items():
        build(path, theme)
    print('\njustify_format lengths for today.py:')
    for item in [i for i in PANEL + [r for _, rows in SECTIONS for r in rows] if i]:
        label, value, elem_id = item
        if elem_id:
            print(f'  {elem_id}: {field_length(label, value)}')

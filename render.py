#!/usr/bin/env python3
"""Draw the news-image-20261118 front page (@kanbara12) with Pillow.

One newspaper front page for Wednesday 18 November 2026: 26 stories from
six continents, 12 with illustrations, a world map pinning the 12, and the
other 14 as a numbered list. Run it, then main.py copies entry.png to the
output directory. Deterministic: same inputs, same bytes.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
PANELS = ROOT / "assets"

W = H = 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996

# --- newsprint palette ---
PAPER = (247, 241, 227)
INK = (32, 34, 38)
SLATE = (36, 50, 66)
RED = (178, 44, 32)
BLUE = (58, 106, 143)
SKY = (198, 220, 230)
LAND = (233, 220, 192)
LAND_LINE = (190, 175, 140)
GREEN = (74, 128, 84)
OCHRE = (216, 162, 74)
PURPLE = (128, 74, 140)
TEAL = (46, 130, 126)
GREY = (120, 122, 118)
LIGHT_GREY = (226, 224, 216)
WHITE = (252, 250, 244)

REGION_COLORS = {
    "Europe": BLUE,
    "Middle East": OCHRE,
    "Asia": PURPLE,
    "Africa": GREEN,
    "Americas": TEAL,
    "World": GREY,
}

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/LiberationSerif-Regular.ttf"
SANS_B = f"{FONT_DIR}/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel_image(path, w, h):
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, (w, h), Image.LANCZOS)


def caption_bar(draw, x, y, w, text, bar_h=20, size=11):
    draw.rectangle([x, y, x + w, y + bar_h], fill=SLATE)
    size = size
    while size > 8 and draw.textlength(text, font=font(SANS_B, size)) > w - 12:
        size -= 1
    draw.text((x + 6, y + (bar_h - size) // 2 - 1), text,
              font=font(SANS_B, size), fill=WHITE)
    return y + bar_h


def story_block(img, draw, x, y, w, img_h, story, sizes):
    """One illustrated story: image, caption bar, kicker, headline, deck."""
    img.paste(panel_image(PANELS / story["panel"], w, img_h), (x, y))
    y += img_h
    y = caption_bar(draw, x, y, w, story["caption"])
    y += 5
    col = REGION_COLORS[story["region"]]
    draw.text((x, y), f"{story['num']} · {story['region'].upper()} · {story['beat']}",
              font=font(SANS_B, sizes["kicker"]), fill=col)
    y += sizes["kicker"] + 5
    y = draw_text_block(draw, x, y, story["headline"], font(SERIF_B, sizes["head"]),
                        INK, w, sizes["head"] + 4, max_lines=sizes["head_lines"])
    y += 3
    y = draw_text_block(draw, x, y, story["deck"], font(SANS, sizes["deck"]),
                        INK, w, sizes["deck"] + 4, max_lines=sizes["deck_lines"])
    return y


# --- the 12 illustrated stories ---
HEROES = [
    {"num": 1, "panel": "panel-01.png", "region": "Asia", "beat": "DIPLOMACY",
     "caption": "SHENZHEN — APEC OPENS",
     "headline": "Xi and Putin meet in Shenzhen as Trump flies in",
     "deck": "First trilateral of the three sitting presidents due Thursday, on the APEC sidelines; no agenda published."},
    {"num": 2, "panel": "panel-02.png", "region": "Middle East", "beat": "GULF WAR",
     "caption": "GULF — INTERCEPTORS UP",
     "headline": "Iran fires on US bases in Kuwait and Bahrain",
     "deck": "Tehran says it hit US drone and missile sites; Bahrain and Kuwait say the attacks were intercepted."},
    {"num": 3, "panel": "panel-03.png", "region": "Europe", "beat": "UKRAINE WAR",
     "caption": "KERCH STRAIT — SECOND DAY",
     "headline": "Kerch Bridge hit again; road span falls",
     "deck": "Ukraine strikes the Crimea link for a second day; part of the road deck collapses into the strait."},
]

ROW1 = [
    {"num": 4, "panel": "panel-04.png", "region": "Americas", "beat": "POLITICS",
     "caption": "ALASKA — 56–44",
     "headline": "Peltola wins Alaska; Democrats take the Senate",
     "deck": "Democrat beats Dan Sullivan; ninth flip gives a 56–44 majority."},
    {"num": 5, "panel": "panel-05.png", "region": "Americas", "beat": "BUSINESS",
     "caption": "SANTA CLARA — $115.8BN",
     "headline": "Nvidia rules out Huang return; sales double",
     "deck": "Record $115.8bn quarter; ousted founder will not return."},
    {"num": 6, "panel": "panel-06.png", "region": "Asia", "beat": "SECURITY",
     "caption": "MANILA — QUAD MEETS",
     "headline": "Quad unveils sea-watch plan in Manila",
     "deck": "US, India, Japan, Australia agree sea-watch, cables and AI."},
    {"num": 7, "panel": "panel-07.png", "region": "Asia", "beat": "WEATHER",
     "caption": "BAY OF BENGAL — LANDFALL",
     "headline": "Cyclone Akvan bears down on India's east coast",
     "deck": "Due to cross Andhra Pradesh Friday; winds 120–130 km/h."},
    {"num": 8, "panel": "panel-08.png", "region": "Asia", "beat": "SPORT",
     "caption": "CHENNAI — END OF AN ERA",
     "headline": "Dhoni retires from the IPL",
     "deck": "After 272 games and five titles, he becomes mentor for 2027."},
]

ROW2 = [
    {"num": 9, "panel": "panel-09.png", "region": "World", "beat": "SCIENCE",
     "caption": "DEEP SPACE — 16.1BN MILES",
     "headline": "Voyager 1 reaches one light-day from Earth",
     "deck": "NASA: probe crossed about 16.1bn miles at 5:16 a.m. Eastern."},
    {"num": 10, "panel": "panel-10.png", "region": "Africa", "beat": "HEALTH",
     "caption": "CONGO — 11,000 CASES",
     "headline": "Ebola outbreak passes 11,000 cases",
     "deck": "Already the second largest on record, across 67 health zones."},
    {"num": 11, "panel": "panel-11.png", "region": "Americas", "beat": "HEALTH",
     "caption": "WASHINGTON — 26 YEARS",
     "headline": "US loses measles-free status",
     "deck": "Virus spread for over a year; 5,412 cases in 2026, most since 1991."},
    {"num": 12, "panel": "panel-12.png", "region": "Asia", "beat": "POLITICS",
     "caption": "DHAKA — UNREST GROWS",
     "headline": "Bangladesh deploys paramilitary troops",
     "deck": "Clashes and arson as exiled ex-PM Hasina plans a December return."},
]

# --- the 14 also-on stories (number, one line) ---
ALSO_ON = [
    (13, "Anthropic prices its IPO at $83 a share, above its $70–$78 range."),
    (14, "GTA VI goes on sale tomorrow after a 13-year wait."),
    (15, "Turkish court gives jailed Istanbul mayor Imamoglu two more years and a new political ban."),
    (16, "EU proposes a €45bn loan for Ukraine in 2027: €25bn military, €20bn budget."),
    (17, "Russian An-12 transport plane crashes in Siberia; 13 reported killed."),
    (18, "Israel's parliament elects Matan Kahana speaker; Board of Peace faults Israel and Hamas over the Gaza truce."),
    (19, "Houthis close on Aden; Saudi-led coalition intercepts a missile aimed at Riyadh."),
    (20, "Uganda charges activist Sam Mugumya with treachery in a military court."),
    (21, "Mozambique opposition leader Mondlane goes on trial over 2024 election protests."),
    (22, "Police in Zamfara free 20 abducted women and children."),
    (23, "Australia sanctions Israelis over West Bank settlements."),
    (24, "EU approves signing of trade and investment deals with Indonesia."),
    (25, "Cyberattack hits Apple, Zoom, BBC and IKEA services."),
    (26, "Rare contact reported with isolated Indigenous people in the Brazilian Amazon."),
]

# --- simplified continent outlines (lon, lat), equirectangular ---
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
     (-75, 62), (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-90, 21), (-97, 26), (-105, 22), (-110, 23), (-115, 29), (-125, 40),
     (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 9), (-72, 11), (-62, 9), (-52, 5), (-50, -2), (-40, -5), (-35, -9),
     (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -54), (-73, -37),
     (-70, -20), (-75, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -29), (20, -35),
     (15, -27), (12, -18), (9, -2), (9, 4), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56), (21, 55),
     (28, 59), (30, 60), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50),
     (140, 40), (135, 35), (127, 35), (122, 30), (120, 22), (110, 20), (105, 10),
     (100, 8), (98, 15), (92, 21), (88, 22), (80, 15), (76, 10), (72, 20), (66, 25),
     (60, 25), (56, 27), (52, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36),
     (26, 38), (22, 37), (18, 40), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (146, -19), (142, -11), (136, -12),
     (132, -12), (126, -14), (122, -17), (118, -20)],
    [(-5, 54), (-3, 58), (0, 53), (1, 51), (-4, 50)],  # Britain & Ireland
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44)],  # Japan
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9),
     (130, -5), (135, -4), (140, -8)],  # Indonesia
    [(131, -1), (136, -3), (141, -4), (146, -7), (150, -10), (146, -8), (141, -8),
     (136, -6), (131, -3)],  # New Guinea
]

# story num -> (lon, lat, region, badge offset dx, dy)
PINS = {
    1: (114.1, 22.5, "Asia", 0, 0),
    2: (50.6, 26.2, "Middle East", 0, 0),
    3: (35.0, 45.3, "Europe", 0, 0),
    4: (-152.0, 64.5, "Americas", 0, 0),
    5: (-122.0, 37.4, "Americas", 0, 0),
    6: (121.0, 14.6, "Asia", 15, 7),
    7: (82.3, 16.3, "Asia", 0, 0),
    8: (80.3, 13.1, "Asia", -17, 9),
    9: (-118.1, 34.2, "Americas", 16, 10),
    10: (23.6, -2.9, "Africa", 0, 0),
    11: (-77.0, 38.9, "Americas", 0, 0),
    12: (90.4, 23.8, "Asia", 14, -7),
}


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    draw.text((MARGIN, 8), "THE WORLD'S NEWS IN ONE PICTURE",
              font=font(SANS_B, 13), fill=RED)
    right = "26 STORIES · 6 CONTINENTS · ALL FROM WEDNESDAY"
    draw.text((W - MARGIN - draw.textlength(right, font=font(SANS_B, 13)), 8),
              right, font=font(SANS_B, 13), fill=INK)
    draw.text((MARGIN, 26), "Wednesday 18 November 2026",
              font=font(SERIF_B, 44), fill=INK)
    draw.line([MARGIN, 82, W - MARGIN, 82], fill=INK, width=3)

    # --- stat strip ---
    stats = [
        ("56–44", "Peltola Senate win"),
        ("$115.8bn", "Nvidia quarterly sales"),
        ("11,000+", "Ebola cases in Congo"),
        ("16.1bn", "Voyager 1 miles from Earth"),
        ("120–130", "Akvan landfall winds km/h"),
        ("$83", "Anthropic IPO price"),
    ]
    col_w = CW // 6
    y = 88
    for i, (num, label) in enumerate(stats):
        x = MARGIN + i * col_w
        draw.text((x, y), num, font=font(SERIF_B, 20), fill=INK)
        draw.text((x, y + 22), label, font=font(SANS, 10), fill=GREY)
    draw.line([MARGIN, 124, W - MARGIN, 124], fill=INK, width=1)

    # --- region counts ---
    counts = "EUROPE 4 · MIDDLE EAST 3 · ASIA 6 · AFRICA 4 · AMERICAS 5 · WORLD 4"
    draw.text(((W - draw.textlength(counts, font=font(SANS_B, 11))) / 2, 130),
              counts, font=font(SANS_B, 11), fill=INK)

    # --- heroes: 3 across ---
    y0 = 148
    hero_w = 324
    gap = (CW - 3 * hero_w) // 2
    for i, s in enumerate(HEROES):
        x = MARGIN + i * (hero_w + gap)
        story_block(img, draw, x, y0, hero_w, 120, s,
                    {"kicker": 11, "head": 17, "head_lines": 2,
                     "deck": 11, "deck_lines": 2})

    # --- row 1: 5 across ---
    y1 = 392
    w1 = 190
    g1 = (CW - 5 * w1) // 4
    for i, s in enumerate(ROW1):
        x = MARGIN + i * (w1 + g1)
        story_block(img, draw, x, y1, w1, 80, s,
                    {"kicker": 10, "head": 13, "head_lines": 2,
                     "deck": 10, "deck_lines": 2})

    # --- row 2: 4 across ---
    y2 = 579
    w2 = 241
    g2 = (CW - 4 * w2) // 3
    for i, s in enumerate(ROW2):
        x = MARGIN + i * (w2 + g2)
        story_block(img, draw, x, y2, w2, 92, s,
                    {"kicker": 10, "head": 14, "head_lines": 2,
                     "deck": 10, "deck_lines": 2})

    # --- also-on section ---
    y3 = 780
    draw.line([MARGIN, y3, W - MARGIN, y3], fill=INK, width=2)
    draw.text((MARGIN, y3 + 6), "ALSO ON WEDNESDAY 18 NOVEMBER",
              font=font(SANS_B, 12), fill=RED)

    map_x, map_y, map_w, map_h = MARGIN, y3 + 26, 330, 140

    def project(lon, lat):
        px = map_x + (lon + 170) / 360 * map_w
        py = map_y + (75 - lat) / 130 * map_h
        return px, py

    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SKY)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, (lon, lat, region, dx, dy) in PINS.items():
        px, py = project(lon, lat)
        bx, by = px + dx, py + dy
        if dx or dy:
            draw.line([px, py, bx, by], fill=INK, width=1)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
        col = REGION_COLORS[region]
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col, outline=WHITE, width=1)
        t = str(num)
        tw = draw.textlength(t, font=font(SANS_B, 10))
        draw.text((bx - tw / 2, by - 7), t, font=font(SANS_B, 10), fill=WHITE)
    draw.text((map_x, map_y + map_h + 4), "Pins: stories 1–12. Pins approximate.",
              font=font(SANS, 9), fill=GREY)

    # also-on list, two columns
    lx = map_x + map_w + 16
    col2_w = (W - MARGIN - lx - 14) // 2
    fnum = font(SANS_B, 11)
    ftext = font(SANS, 11)
    for col_i in range(2):
        x = lx + col_i * (col2_w + 14)
        yy = y3 + 26
        for num, text in ALSO_ON[col_i * 7:(col_i + 1) * 7]:
            draw.text((x, yy), str(num), font=fnum, fill=RED)
            yy = draw_text_block(draw, x + 20, yy, text, ftext, INK,
                                 col2_w - 20, 13, max_lines=2)
            yy += 1

    # --- footer ---
    fy = 988
    draw.line([MARGIN, fy, W - MARGIN, fy], fill=INK, width=1)
    draw.text((MARGIN, fy + 5),
              "DATE CHECK — Due, not yet held: the Trump–Xi–Putin trilateral is set for Thursday 19 November.",
              font=font(SANS_B, 10), fill=INK)
    draw.text((MARGIN, fy + 19),
              "Every story here happened or was first reported on Wednesday 18 November 2026. Contested claims are marked as claims. "
              "Sources: Reuters, AP, AFP, BBC, NASA, IMD. Original drawings.",
              font=font(SANS, 9), fill=GREY)

    out = ROOT / "entry.png"
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    print(render())

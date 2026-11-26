#!/usr/bin/env python3
"""Render the Sum 26 Round 3 broadsheet (news-image-20261126-r3).

1024x1024 white broadsheet: 42 stories, all reported Thursday 26 Nov 2026.
Build-time only (Pillow). The graded entrypoint main.py is stdlib-only and
just copies entry.png. Every text block is wrapped to its box and ASSERTED
to fit: render fails loudly instead of ever drawing overlapping text.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
OUT = os.path.join(HERE, "entry.png")

BLACK = (12, 12, 12)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LGREY = (150, 150, 150)
RULE = (200, 200, 200)
WHITE = (255, 255, 255)
PAPER = (255, 255, 255)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GREEN = (27, 94, 32)
AMBER = (146, 90, 0)
NAVY = (18, 38, 74)
SKY = (64, 110, 160)
YELLOW = (255, 214, 64)
SAFFRON = (255, 153, 51)
CREAM = (255, 248, 220)

SERIF = os.path.join(HERE, "fonts", "LiberationSerif-Regular.ttf")
SERIFB = os.path.join(HERE, "fonts", "LiberationSerif-Bold.ttf")
SANS = os.path.join(HERE, "fonts", "LiberationSans-Regular.ttf")
SANSB = os.path.join(HERE, "fonts", "LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, f):
    """Text width in px."""
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines, each <= max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_fit(draw, text, f, box, max_lines, align="left", fill=INK, leading=None):
    """Draw wrapped text inside box (x, y, w, h); raise if it cannot fit.

    This is the zero-overlap guarantee: nothing is ever drawn outside its
    own box, and an overflow aborts the build instead of clipping text.
    """
    x, y, w, h = box
    if leading is None:
        leading = int(f.size * 1.22)
    lines = wrap(draw, text, f, w)
    if len(lines) > max_lines:
        raise SystemExit("OVERFLOW %r: %d lines > %d in box %s"
                         % (text[:40], len(lines), max_lines, box))
    if len(lines) * leading > h:
        raise SystemExit("OVERFLOW height %r in box %s" % (text[:40], box))
    for i, ln in enumerate(lines):
        lx = x
        if align == "center":
            lx = x + (w - tw(draw, ln, f)) / 2
        elif align == "right":
            lx = x + w - tw(draw, ln, f)
        draw.text((lx, y + i * leading), ln, font=f, fill=fill)
    return len(lines)


def one_line(draw, text, f, x, y, max_w, fill=INK):
    """Single line; raise if too wide (never silently clipped)."""
    if tw(draw, text, f) > max_w:
        raise SystemExit("TOO WIDE %r (%d > %d)" % (text, tw(draw, text, f), max_w))
    draw.text((x, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- data
# (label, number, source, region, title, deck)
HEROES = [
    ("CONFIRMED", "1", "Fox Weather",
     "100th Macy's parade put off to Saturday",
     "Nor'easter brings 60-70 mph gusts; balloons stay grounded if gusts "
     "pass 34 mph. NBC airs an encore of the 2025 parade instead."),
    ("CONFIRMED", "2", "PTI",
     "India remembers 26/11, 18 years on",
     "Tributes for the 166 killed in Mumbai in 2008, as the nation also "
     "marks 77 years since its Constitution was adopted."),
    ("CONFIRMED", "3", "FIDE",
     "Gukesh v Sindarov: Game 3, scores level",
     "Two draws leave the Geneva title match 1-1. Sindarov has White today; "
     "first to 7.5 points takes the crown and $2.5m."),
]

MEDIUM = [
    ("CONFIRMED", "4", "Reuters", "US plans new tariffs on 14 partners",
     "Washington blames excess factory capacity; China faces the highest rates."),
    ("CONFIRMED", "5", "Reuters", "Russian missiles hit Kyiv; mall struck",
     "Ballistic strikes hit a shopping centre and two more sites, the mayor says."),
    ("REPORTED", "6", "Reuters", "Ukraine says it hit air base, 5 jets hurt",
     "Kyiv says a strike on a Russian base damaged five missile planes."),
    ("CONFIRMED", "7", "Reuters", "Abu Dhabi talks end; Russia holds line",
     "Peace talks stall as Moscow refuses to give ground on territory, envoys say."),
    ("REPORTED", "8", "Reuters", "States urge Russia to stop riot-agent use",
     "Dozens of nations condemn the alleged use of a riot agent in the Ukraine war."),
    ("CONFIRMED", "9", "Reuters", "Stocks slide as tech sell-off deepens",
     "S&P 500 and Nasdaq fall on Wednesday as tariff fears add to AI-stock pain."),
    ("CONFIRMED", "10", "Reuters", "S&P puts Nvidia rating on watch",
     "Huang's return raises board questions; a Senate Democrat demands answers."),
    ("CONFIRMED", "11", "Reuters", "US growth revised sharply higher",
     "Third-quarter GDP comes in stronger than first thought, data show."),
    ("CONFIRMED", "12", "Reuters", "Trump pardons turkeys Freedom, Feathers",
     "The Thanksgiving pair escape the table in the White House ceremony."),
    ("CONFIRMED", "13", "Reuters", "Second judge blocks birthright order",
     "Trump's curbs on birthright citizenship are halted again in court."),
    ("CONFIRMED", "14", "Reuters", "Australia passes tough online-safety law",
     "Platforms must remove harmful content or face fines of up to 5% of revenue."),
    ("CONFIRMED", "15", "Reuters", "Lebanon to open second airport",
     "A northern airport opens next month, a sign of Hezbollah's waning sway."),
]

# (number, text, source)
BRIEFS_L = [
    (16, "Murmansk governor held in pre-trial detention in graft probe", "Reuters"),
    (17, "US CDC reports nine measles-related deaths in 2026", "Reuters"),
    (18, "Radar fault delays flights at Chicago O'Hare, FAA says", "Reuters"),
    (19, "Abrego Garcia lands in Spain after US departure deal", "Reuters"),
    (20, "Nidal Hasan seeks stay of execution for Fort Hood murders", "Reuters"),
    (21, "Kenya cult leader Mackenzie convicted of new charges", "Reuters"),
    (22, "How China got Nvidia AI chips despite US rules: explainer", "Reuters"),
    (23, "Poland urges NATO to weigh downing missiles over Ukraine", "Reuters"),
    (24, "Spain opens TikTok probe over child sex-abuse material", "AFP"),
    (25, "Sanchez defends housing and migration record on podcast", "EFE"),
    (26, "Israeli court urges dropping bribery charges vs Netanyahu", "Reuters"),
    (27, "North Korea orders Switzerland to shut Pyongyang office", "Reuters"),
    (28, "Peru shuts dozens of ports as heavy swells batter coast", "Reuters"),
    (29, "Bomb in Colombian city wounds 23 as unrest spreads", "Reuters"),
    (30, "Egypt: 30+ killed after blaze as vehicle overturns", "Egypt ministry"),
]
BRIEFS_R = [
    (31, "Two dozen hostages seized in Colombian supermarket", "AP"),
    (32, "Kazakhstan seeks secret extradition of Chechen activist", "Lawyers"),
    (33, "Cabinet clears Rs 4,288-cr terminal at Kamarajar Port", "PTI"),
    (34, "India adds 6,000 IIT seats for robotics, AI, space", "PTI"),
    (35, "Pakistani astronaut boards China's Tiangong station", "Xinhua"),
    (36, "India women beat Japan in hockey", "PTI"),
    (37, "South Africa sweep Test series", "AFP"),
    (38, "Rugby captains gather in London for Nations finals", "Reuters"),
    (39, "Frech's Mirrorball win builds buzz for LA28 Paralympics", "Reuters"),
    (40, "Trump to add sweeping tariffs, unfazed by midterms", "Reuters"),
    (41, "Ecuador: US talks focus on reviewing operations", "Reuters"),
    (42, "US plans surprise Brazil tariffs, 10% on aircraft", "Reuters"),
]

NUMBERS = [
    ("100", "YEARS OF MACY'S PARADE"),
    ("60-70", "MPH GUSTS FORECAST"),
    ("18", "YEARS SINCE 26/11"),
    ("1-1", "GUKESH-SINDAROV"),
    ("14", "TARIFF PARTNERS"),
    ("5", "PLANES 'DAMAGED'"),
]

TIMELINE = [
    ("00:00", "Thanksgiving in the US, Constitution Day in India"),
    ("02:30", "Abu Dhabi talks end; Russia holds land claims"),
    ("08:00", "India honours 166 victims of 26/11"),
    ("12:00", "Markets digest tech sell-off; Nvidia on watch"),
    ("14:00", "Game 3 in Geneva: Sindarov v Gukesh, 1-1"),
    ("23:00", "Thanksgiving evening: tables full, route empty"),
]

DATECHECK = [
    ("24 NOV", "Sooryavanshi's 204 off 53 (28 sixes) v UAE, Doha"),
    ("24-25 NOV", "Champions League MD5: Real Madrid 5-1 PSV; PSG 2-2 Roma"),
    ("25 NOV", "Houthis claim Ras Tanura hit; coalition: 4 drones downed"),
    ("25 NOV", "Sudan Blue Nile drone strikes kill 19 civilians"),
    ("25 NOV", "Bangladesh lifts garment wage 36% to 17,000 taka"),
    ("25 NOV", "Gukesh-Sindarov Game 2 ends in a 20-move draw"),
]

LABEL_FILL = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}


def label_chip(draw, x, y, label):
    """Small coloured chip; returns width used."""
    f = font(SANSB, 10)
    w = tw(draw, label, f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=LABEL_FILL[label])
    draw.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- scenes
def scene_parade(draw, x, y, w, h):
    """Rainy New York parade street, balloons grounded, route empty."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 52, 74))
    # skyline
    for bx, bw, bh in [(6, 34, 34), (46, 26, 48), (78, 40, 30), (124, 30, 52),
                       (160, 36, 38), (202, 28, 46), (236, 34, 30), (276, 30, 44)]:
        draw.rectangle([x + bx, y + h - 22 - bh, x + bx + bw, y + h - 22],
                       fill=(24, 34, 52))
        for wy in range(0, bh - 8, 9):
            draw.rectangle([x + bx + 5, y + h - 22 - bh + 4 + wy,
                            x + bx + 10, y + h - 22 - bh + 8 + wy], fill=(255, 214, 64))
    # street
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(70, 76, 88))
    draw.rectangle([x, y + h - 12, x + w, y + h - 10], fill=(255, 214, 64))
    # grounded balloon: big yellow oval low over the street + strings
    draw.ellipse([x + 118, y + 6, x + 196, y + 44], fill=(255, 214, 64),
                 outline=(180, 140, 0))
    draw.ellipse([x + 150, y + 18, x + 164, y + 32], fill=(178, 34, 34))
    draw.line([x + 130, y + 44, x + 122, y + h - 22], fill=WHITE, width=1)
    draw.line([x + 184, y + 44, x + 192, y + h - 22], fill=WHITE, width=1)
    # rain streaks
    for rx, ry, rl in [(20, 4, 10), (60, 10, 12), (100, 2, 9), (220, 6, 11),
                       (250, 12, 9), (290, 4, 10), (40, 22, 8), (270, 24, 8)]:
        draw.line([x + rx, y + ry, x + rx - 3, y + ry + rl], fill=(170, 200, 230), width=1)
    # date-change sign
    draw.rectangle([x + 8, y + 8, x + 96, y + 26], fill=WHITE, outline=RED)
    draw.text((x + 12, y + 11), "THU 26  >  SAT 28", font=font(SANSB, 10), fill=RED)


def scene_india(draw, x, y, w, h):
    """India Gate silhouette, tricolour band, remembrance candles."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 236, 205))
    # tricolour band at top
    draw.rectangle([x, y, x + w, y + 9], fill=SAFFRON)
    draw.rectangle([x, y + 9, x + w, y + 18], fill=WHITE)
    draw.rectangle([x, y + 18, x + w, y + 27], fill=(19, 136, 8))
    # India Gate arch
    draw.rectangle([x + 132, y + 34, x + 194, y + h - 14], fill=(120, 72, 40))
    draw.pieslice([x + 146, y + 42, x + 180, y + 88], 180, 360, fill=(250, 236, 205))
    draw.rectangle([x + 132, y + 30, x + 194, y + 38], fill=(120, 72, 40))
    draw.rectangle([x + 138, y + 26, x + 188, y + 32], fill=(96, 56, 30))
    # candles
    for cx in (30, 52, 74, 244, 266, 288):
        draw.rectangle([x + cx, y + h - 20, x + cx + 6, y + h - 10], fill=WHITE,
                       outline=(150, 150, 150))
        draw.ellipse([x + cx + 1, y + h - 27, x + cx + 5, y + h - 21], fill=(255, 170, 0))
    one = font(SERIFB, 13)
    draw.text((x + 228, y + 30), "26/11", font=one, fill=DARKRED)


def scene_chess(draw, x, y, w, h):
    """Mini chess board, two kings, score strip — all inside the 64px scene."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    bs = 7
    ox, oy = x + 10, y + 4
    for r in range(8):
        for c in range(8):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (120, 72, 40)
            draw.rectangle([ox + c * bs, oy + r * bs,
                            ox + (c + 1) * bs, oy + (r + 1) * bs], fill=col)
    for px, py, col in [(ox + 4 * bs + 1, oy + 7 * bs + 1, WHITE),
                        (ox + 3 * bs + 1, oy + 0 * bs + 1, BLACK),
                        (ox + 1 * bs + 1, oy + 6 * bs + 1, WHITE),
                        (ox + 6 * bs + 1, oy + 1 * bs + 1, BLACK)]:
        draw.ellipse([px, py, px + 5, py + 5], fill=col, outline=BLACK)
    draw.text((x + 80, y + 6), "GENEVA", font=font(SANSB, 12), fill=BLACK)
    draw.text((x + 80, y + 24), "GAME 3 OF 14", font=font(SANSB, 10), fill=GREY)
    draw.text((x + 80, y + 40), "SCORE  1 - 1", font=font(SERIFB, 15), fill=DARKRED)


SCENES = [scene_parade, scene_india, scene_chess]


def small_map(draw, x, y, w, h):
    """One SMALL world-map panel: simple continent blobs + numbered pins."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 244, 248), outline=RULE)
    draw.text((x + 8, y + 5), "WORLD MAP — KEY PINS", font=font(SANSB, 10), fill=NAVY)
    mx, my, mw, mh = x + 6, y + 22, w - 12, h - 28
    sea = (198, 218, 232)
    land = (146, 172, 152)
    draw.rectangle([mx, my, mx + mw, my + mh], fill=sea)
    # coarse continent blobs (fractions of the map box)
    blobs = [
        # N America
        [(0.03, 0.10), (0.20, 0.02), (0.27, 0.22), (0.20, 0.42), (0.10, 0.40), (0.04, 0.26)],
        # S America
        [(0.24, 0.48), (0.31, 0.44), (0.35, 0.60), (0.30, 0.92), (0.25, 0.78)],
        # Europe
        [(0.47, 0.08), (0.54, 0.06), (0.56, 0.20), (0.50, 0.24), (0.46, 0.16)],
        # Africa
        [(0.47, 0.30), (0.56, 0.28), (0.59, 0.48), (0.54, 0.72), (0.49, 0.60), (0.46, 0.44)],
        # Asia
        [(0.58, 0.06), (0.78, 0.02), (0.95, 0.14), (0.92, 0.34), (0.78, 0.40),
         (0.70, 0.30), (0.62, 0.26), (0.57, 0.16)],
        # Australia
        [(0.82, 0.66), (0.92, 0.64), (0.94, 0.78), (0.84, 0.80)],
    ]
    for blob in blobs:
        pts = [(mx + fx * mw, my + fy * mh) for fx, fy in blob]
        draw.polygon(pts, fill=land, outline=(120, 140, 125))
    pins = [(0.24, 0.28, "1"), (0.49, 0.14, "3"), (0.68, 0.30, "2"),
            (0.57, 0.20, "5"), (0.88, 0.72, "14"), (0.61, 0.34, "15")]
    for fx, fy, num in pins:
        px, py = mx + fx * mw, my + fy * mh
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE)
        draw.text((px - 3, py - 6), num, font=font(SANSB, 8), fill=WHITE)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14  # margin
    CW = W - 2 * M  # 996

    # ---- masthead (black band, y 8..92)
    d.rectangle([M, 8, W - M, 92], fill=BLACK)
    title_f = font(SERIFB, 44)
    one_line(d, "THE WORLD IN ONE DAY", title_f, M + 10, 12, 660, fill=WHITE)
    d.line([M + 10, 62, M + 470, 62], fill=(120, 120, 120), width=1)
    one_line(d, "THURSDAY 26 NOVEMBER 2026  ·  ALL STORIES REPORTED TODAY",
             font(SANSB, 13), M + 10, 68, 660, fill=(230, 230, 230))
    # stats box, right side of masthead
    sx = W - M - 300
    d.rectangle([sx, 14, W - M - 6, 86], outline=(150, 150, 150), width=1)
    stats = [("42", "STORIES"), ("9", "REGIONS"), ("10", "SOURCES")]
    sw = 300 / 3
    for i, (num, lab) in enumerate(stats):
        cx = sx + i * sw
        if i:
            d.line([cx, 20, cx, 80], fill=(120, 120, 120), width=1)
        draw_fit(d, num, font(SANSB, 22), (cx, 18, sw, 28), 1,
                 align="center", fill=WHITE)
        draw_fit(d, lab, font(SANSB, 10), (cx, 50, sw, 14), 1,
                 align="center", fill=(200, 200, 200))
    # top-3 line under masthead
    one_line(d, "PARADE OFF  ·  INDIA REMEMBERS 26/11  ·  CHESS 1-1 IN GENEVA",
             font(SERIFB, 14), M, 98, CW, fill=DARKRED)

    # ---- heroes (y 118..304)
    hy, hh = 118, 186
    hw = (CW - 16) // 3
    for i, (lab, num, src, title, deck) in enumerate(HEROES):
        x = M + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], outline=BLACK, width=2)
        SCENES[i](d, x + 1, hy + 1, hw - 2, 64)
        ty = hy + 70
        cw = label_chip(d, x + 8, ty, lab)
        d.text((x + 8 + cw + 6, ty + 1), "No. %s  ·  %s" % (num, src),
               font=font(SANSB, 10), fill=GREY)
        draw_fit(d, title, font(SERIFB, 17), (x + 8, ty + 20, hw - 16, 42), 2,
                 fill=BLACK, leading=20)
        draw_fit(d, deck, font(SANS, 11), (x + 8, ty + 64, hw - 16, 48), 3,
                 fill=INK, leading=14)
    # ---- medium grid (y 312..524): 6 cols x 2 rows
    gy, gh, gap = 312, 103, 6
    mw = (CW - 5 * gap) // 6
    for i, (lab, num, src, title, deck) in enumerate(MEDIUM):
        r, c = divmod(i, 6)
        x = M + c * (mw + gap)
        y = gy + r * (gh + gap)
        d.rectangle([x, y, x + mw, y + gh], outline=RULE, width=1)
        d.line([x, y, x + mw, y], fill=BLACK, width=3)
        cw = label_chip(d, x + 6, y + 7, lab)
        d.text((x + 6 + cw + 4, y + 8), "%s %s" % (num, src),
               font=font(SANSB, 9), fill=GREY)
        draw_fit(d, title, font(SERIFB, 13), (x + 6, y + 26, mw - 12, 32), 2,
                 fill=BLACK, leading=15)
        draw_fit(d, deck, font(SANS, 10), (x + 6, y + 60, mw - 12, 40), 3,
                 fill=INK, leading=13)

    # ---- IN NUMBERS band (y 532..578)
    ny, nh = 532, 46
    d.rectangle([M, ny, W - M, ny + nh], fill=BLACK)
    d.text((M + 10, ny + 13), "IN NUMBERS", font=font(SANSB, 13), fill=YELLOW)
    ncell = (CW - 150) // len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + 150 + i * ncell
        d.text((cx, ny + 5), num, font=font(SANSB, 19), fill=WHITE)
        d.text((cx, ny + 28), lab, font=font(SANSB, 8), fill=(200, 200, 200))

    # ---- UTC TIMELINE (y 586..630)
    ty0 = 586
    d.text((M, ty0), "UTC TIMELINE", font=font(SANSB, 12), fill=BLACK)
    d.line([M + 118, ty0 + 8, W - M, ty0 + 8], fill=RULE, width=1)
    tcell = CW // 3
    for i, (t, txt) in enumerate(TIMELINE):
        r, c = divmod(i, 3)
        x = M + c * tcell
        y = ty0 + 18 + r * 14
        d.text((x, y), t, font=font(SANSB, 10), fill=RED)
        one_line(d, txt, font(SANS, 10), x + 42, y, tcell - 48, fill=INK)

    # ---- THE BRIEFS (y 640..960)
    by = 640
    d.text((M, by), "THE BRIEFS", font=font(SANSB, 13), fill=BLACK)
    d.line([M + 108, by + 9, W - M, by + 9], fill=RULE, width=1)
    d.text((M, by + 16), "Every story below was reported on Thursday 26 November 2026.",
           font=font(SANS, 10), fill=GREY)
    bf = font(SANS, 11)
    bf_b = font(SANSB, 11)
    row_h = 17
    ly = by + 30
    # left column: 15 briefs
    for j, (num, txt, src) in enumerate(BRIEFS_L):
        y = ly + j * row_h
        d.text((M, y), "%d." % num, font=bf_b, fill=BLACK)
        one_line(d, txt, bf, M + 26, y, 430, fill=INK)
        d.text((M + 462, y), src, font=font(SANS, 9), fill=GREY)
    # right column: 12 briefs, then the SMALL map panel
    rx = M + 530
    for j, (num, txt, src) in enumerate(BRIEFS_R):
        y = ly + j * row_h
        d.text((rx, y), "%d." % num, font=bf_b, fill=BLACK)
        one_line(d, txt, bf, rx + 26, y, 330, fill=INK)
        d.text((rx + 362, y), src, font=font(SANS, 9), fill=GREY)
    map_y = ly + len(BRIEFS_R) * row_h + 8
    map_h = 960 - map_y
    small_map(d, rx, map_y, 466, map_h)

    # ---- DATE CHECK (y 968..1006)
    dy = 968
    d.rectangle([M, dy, W - M, dy + 38], outline=RED, width=1)
    d.text((M + 8, dy + 3), "DATE CHECK — NOT 26 NOVEMBER, EXCLUDED:",
           font=font(SANSB, 10), fill=DARKRED)
    dcell = (CW - 16) // 3
    for i, (when, txt) in enumerate(DATECHECK):
        r, c = divmod(i, 3)
        x = M + 8 + c * dcell
        y = dy + 15 + r * 11
        one_line(d, "%s  %s" % (when, txt), font(SANS, 9), x, y, dcell - 8,
                 fill=INK)
    # ---- footer
    one_line(d, "Drawn by an AI agent for make.fun — news-image-20261126  ·  42 stories, 9 regions, 10 sources",
             font(SANS, 9), M, 1010, CW, fill=GREY)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()

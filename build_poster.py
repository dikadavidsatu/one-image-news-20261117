#!/usr/bin/env python3
"""Build the news poster for 17 November 2026 (dev-time generator).

Renders entry.png with Pillow + DejaVu fonts (dev machine only). The submitted
program is main.py, which simply copies the committed entry.png to
/output/entry.png, exactly like the kit starter. Deterministic: this script
has no randomness, no clock, no network; re-running it reproduces the same
bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
PAPER = (245, 239, 227)
INK = (20, 20, 20)
NAVY = (14, 42, 71)
NAVY_LT = (30, 62, 96)
RED = (178, 44, 34)
TEAL = (14, 110, 110)
BLUE = (28, 84, 150)
GREEN = (46, 125, 70)
GREY = (90, 88, 80)
BORDER = (206, 198, 180)
CARD_BG = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_spaced(draw, xy, text, fnt, fill, tracking=0):
    """Draw text with extra tracking (pixels between glyphs)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w, _ = text_size(draw, ch, fnt)
        x += w + tracking
    return x


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        w, _ = text_size(draw, trial, fnt)
        if w <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


# ---------------------------------------------------------------- hero art
def draw_hero(draw):
    """Stylised dusk scene: the Kerch Bridge, road arch collapsed."""
    x0, y0, x1, y1 = 0, 124, W, 470
    vgrad(draw, (x0, y0, x1, 330), (43, 72, 110), (232, 176, 106))
    # low sun
    draw.ellipse([820, 168, 900, 248], fill=(244, 214, 140))
    draw.ellipse([838, 186, 882, 230], fill=(252, 232, 176))
    # distant shore silhouette
    draw.polygon([(0, 300), (140, 282), (260, 298), (430, 284), (620, 300),
                  (790, 286), (1024, 302), (1024, 330), (0, 330)],
                 fill=(52, 74, 96))
    # sea
    draw.rectangle([x0, 330, x1, y1], fill=(28, 56, 80))
    for yy, alpha in ((352, (62, 100, 132)), (392, (52, 88, 118)),
                      (430, (44, 76, 104))):
        for xx in range(0, W, 96):
            draw.arc([xx, yy, xx + 52, yy + 16], 200, 340, fill=alpha, width=3)
    # bridge deck: two surviving spans with a gap in the middle
    deck_y = 316
    steel = (138, 151, 165)
    steel_dk = (96, 108, 122)
    draw.rectangle([0, deck_y, 428, deck_y + 14], fill=steel)
    draw.rectangle([604, deck_y, W, deck_y + 14], fill=steel_dk)
    draw.rectangle([0, deck_y + 14, 428, deck_y + 18], fill=(70, 80, 92))
    draw.rectangle([604, deck_y + 14, W, deck_y + 18], fill=(70, 80, 92))
    # deck posts
    for xx in range(24, 420, 48):
        draw.rectangle([xx, deck_y + 18, xx + 5, 356], fill=(70, 80, 92))
    for xx in range(628, 1010, 48):
        draw.rectangle([xx, deck_y + 18, xx + 5, 356], fill=(70, 80, 92))
    # standing arch over the right span
    draw.arc([640, 196, 960, 330], 180, 360, fill=steel, width=10)
    draw.arc([660, 214, 940, 330], 180, 360, fill=steel_dk, width=5)
    for xx in (700, 760, 820, 880):
        draw.line([(xx, 252), (xx, deck_y)], fill=steel_dk, width=4)
    # collapsed span: one steel arch sagging between the two deck ends,
    # dipping into the water where the road arch fell
    import math
    pts = []
    for i in range(17):
        t = i / 16.0
        px = 428 + 176 * t
        py = deck_y + 84 * math.sin(math.pi * t)
        pts.append((px, py))
    draw.line(pts, fill=steel_dk, width=10, joint="curve")
    # broken stub hanging off the right deck end
    draw.line([(604, deck_y), (576, 356)], fill=steel, width=9)
    # debris in the water
    for (dx, dy, dw) in ((470, 424, 26), (540, 442, 34), (500, 454, 20)):
        draw.rectangle([dx, dy, dx + dw, dy + 7], fill=(120, 130, 140))
    # smoke column rising from the gap (slimmer than before)
    smoke = [(508, 296, 18), (520, 264, 24), (534, 230, 30), (548, 200, 20),
             (494, 320, 20), (560, 276, 16)]
    for (sx, sy, sr) in smoke:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 116, 124))
    smoke_lt = [(526, 246, 15), (540, 216, 19), (510, 282, 12)]
    for (sx, sy, sr) in smoke_lt:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 156, 164))
    # missile streak, upper left, thin and short
    draw.line([(150, 158), (206, 190)], fill=(255, 240, 200), width=3)
    draw.line([(150, 158), (176, 172)], fill=(255, 180, 90), width=5)
    # caption on the water
    fnt = font(SANS_B, 17)
    draw_spaced(draw, (36, 446), "KERCH STRAIT", fnt, (210, 222, 232), tracking=4)


# ---------------------------------------------------------------- icons
def icon_tanker(draw, cx, cy, s):
    """Oil tanker on waves, inside a teal roundel."""
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=TEAL)
    u = s / 50.0
    # hull
    draw.polygon([(cx - 34 * u, cy - 2 * u), (cx + 36 * u, cy - 2 * u),
                  (cx + 26 * u, cy + 12 * u), (cx - 26 * u, cy + 12 * u)],
                 fill=(255, 255, 255))
    draw.rectangle([cx - 8 * u, cy - 18 * u, cx + 8 * u, cy - 2 * u],
                   fill=(255, 255, 255))
    draw.rectangle([cx + 14 * u, cy - 12 * u, cx + 22 * u, cy - 2 * u],
                   fill=(255, 255, 255))
    draw.rectangle([cx + 24 * u, cy - 20 * u, cx + 28 * u, cy - 2 * u],
                   fill=(244, 190, 80))
    for xx in (-30, -14, 2, 18):
        draw.line([(cx + xx * u, cy + 20 * u), (cx + (xx + 10) * u, cy + 20 * u)],
                  fill=(255, 255, 255), width=3)


def icon_plane(draw, cx, cy, s):
    """Airliner silhouette inside a blue roundel."""
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=BLUE)
    u = s / 50.0
    draw.polygon([(cx - 34 * u, cy + 2 * u), (cx + 30 * u, cy - 2 * u),
                  (cx + 38 * u, cy + 2 * u), (cx + 30 * u, cy + 6 * u),
                  (cx - 34 * u, cy + 8 * u)], fill=(255, 255, 255))
    draw.polygon([(cx - 6 * u, cy - 2 * u), (cx + 8 * u, cy - 26 * u),
                  (cx + 14 * u, cy - 26 * u), (cx + 12 * u, cy + 2 * u)],
                 fill=(255, 255, 255))
    draw.polygon([(cx - 2 * u, cy + 6 * u), (cx + 6 * u, cy + 24 * u),
                  (cx + 12 * u, cy + 24 * u), (cx + 12 * u, cy + 4 * u)],
                 fill=(255, 255, 255))
    draw.polygon([(cx - 34 * u, cy + 2 * u), (cx - 26 * u, cy - 12 * u),
                  (cx - 20 * u, cy - 12 * u), (cx - 24 * u, cy + 4 * u)],
                 fill=(255, 255, 255))


def icon_jet(draw, cx, cy, s):
    """Fighter jet seen from above: delta wings, inside a red roundel."""
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=RED)
    u = s / 50.0
    # fuselage: long pointed diamond, nose up
    draw.polygon([(cx, cy - 34 * u), (cx + 6 * u, cy - 8 * u),
                  (cx + 5 * u, cy + 22 * u), (cx, cy + 30 * u),
                  (cx - 5 * u, cy + 22 * u), (cx - 6 * u, cy - 8 * u)],
                 fill=(255, 255, 255))
    # swept delta wings
    draw.polygon([(cx - 4 * u, cy - 2 * u), (cx - 34 * u, cy + 18 * u),
                  (cx - 30 * u, cy + 24 * u), (cx - 4 * u, cy + 12 * u)],
                 fill=(255, 255, 255))
    draw.polygon([(cx + 4 * u, cy - 2 * u), (cx + 34 * u, cy + 18 * u),
                  (cx + 30 * u, cy + 24 * u), (cx + 4 * u, cy + 12 * u)],
                 fill=(255, 255, 255))
    # tail fins
    draw.polygon([(cx - 4 * u, cy + 20 * u), (cx - 14 * u, cy + 30 * u),
                  (cx - 8 * u, cy + 30 * u), (cx - 3 * u, cy + 24 * u)],
                 fill=(255, 255, 255))
    draw.polygon([(cx + 4 * u, cy + 20 * u), (cx + 14 * u, cy + 30 * u),
                  (cx + 8 * u, cy + 30 * u), (cx + 3 * u, cy + 24 * u)],
                 fill=(255, 255, 255))


def icon_trade(draw, cx, cy, s):
    """Stacked shipping containers with an upward arrow, green roundel."""
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=GREEN)
    u = s / 50.0
    draw.rectangle([cx - 30 * u, cy + 2 * u, cx + 2 * u, cy + 18 * u],
                   fill=(255, 255, 255))
    draw.rectangle([cx - 14 * u, cy - 16 * u, cx + 18 * u, cy - 0 * u],
                   fill=(255, 255, 255))
    for xx in (-26, -18, -10):
        draw.line([(cx + xx * u, cy + 4 * u), (cx + xx * u, cy + 16 * u)],
                  fill=GREEN, width=2)
    for xx in (-10, -2, 6):
        draw.line([(cx + xx * u, cy - 14 * u), (cx + xx * u, cy - 2 * u)],
                  fill=GREEN, width=2)
    draw.polygon([(cx + 22 * u, cy - 24 * u), (cx + 30 * u, cy - 12 * u),
                  (cx + 26 * u, cy - 12 * u), (cx + 26 * u, cy + 6 * u),
                  (cx + 18 * u, cy + 6 * u), (cx + 18 * u, cy - 12 * u),
                  (cx + 14 * u, cy - 12 * u)], fill=(244, 190, 80))


# ---------------------------------------------------------------- layout
def card(draw, x, y, w, h, accent, kicker, headline, body, icon_fn):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=accent)
    cx, cy, s = x + 62, y + 62, 46
    icon_fn(draw, cx, cy, s)
    tx = x + 128
    tw = w - 128 - 18
    f_kick = font(SANS_B, 15)
    draw_spaced(draw, (tx, y + 18), kicker, f_kick, accent, tracking=2)
    f_head = font(SANS_B, 23)
    lines = wrap(draw, headline, f_head, tw)
    hy = y + 42
    for ln in lines[:2]:
        draw.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 28
    f_body = font(SANS, 15)
    blines = wrap(draw, body, f_body, tw)
    by = hy + 4
    for ln in blines[:2]:
        draw.text((tx, by), ln, font=f_body, fill=(60, 58, 52))
        by += 20


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # masthead
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    f_over = font(SANS_B, 19)
    over = "THE WORLD IN ONE IMAGE"
    ow, _ = text_size(draw, over, f_over)
    draw_spaced(draw, ((W - ow - 19 * 4) / 2, 14), over, f_over,
                (196, 206, 220), tracking=4)
    f_date = font(SERIF_B, 50)
    date = "TUESDAY 17 NOVEMBER 2026"
    dw, _ = text_size(draw, date, f_date)
    draw.text(((W - dw) / 2, 44), date, font=f_date, fill=(255, 255, 255))
    draw.rectangle([0, 118, W, 124], fill=RED)

    # hero illustration
    draw_hero(draw)

    # hero headline block
    y = 482
    f_kick = font(SANS_B, 17)
    draw_spaced(draw, (32, y), "UKRAINE — RUSSIA", f_kick, RED, tracking=3)
    f_head = font(SERIF_B, 47)
    draw.text((32, y + 26), "THE BRIDGE TO CRIMEA FALLS", font=f_head, fill=INK)
    f_deck = font(SANS, 21)
    deck = ("Ukraine's second strike in two days drops the Kerch road arch "
            "into the strait. Russia answers with missiles on two bridges in Kyiv.")
    dy = y + 88
    for ln in wrap(draw, deck, f_deck, W - 64):
        draw.text((32, dy), ln, font=f_deck, fill=(52, 50, 44))
        dy += 28
    draw.line([(32, 630), (W - 32, 630)], fill=BORDER, width=2)

    # secondary stories, 2 x 2
    gx, gy, gw, gh, gap = 32, 644, 472, 142, 12
    card(draw, gx, gy, gw, gh, TEAL, "THE GULF — HORMUZ & BAHRAIN",
         "TANKERS HIT, DRONES DOWNED IN THE GULF",
         "Iran fires drones at a US radar base in Bahrain; tankers are hit "
         "near Hormuz.",
         icon_tanker)
    card(draw, gx + gw + gap, gy, gw, gh, BLUE, "MANILA — DIPLOMACY",
         "TRUMP LANDS IN MANILA",
         "Quad summit first, then Shenzhen on Thursday for the first "
         "Xi–Trump–Putin talks.",
         icon_plane)
    card(draw, gx, gy + gh + gap, gw, gh, RED, "EAST ASIA — JAPAN",
         "RUSSIAN JETS BREACH JAPAN'S SKIES",
         "Two suspected Russian jets enter airspace off Fukuoka; Tokyo "
         "protests.",
         icon_jet)
    card(draw, gx + gw + gap, gy + gh + gap, gw, gh, GREEN, "SHENZHEN — TRADE",
         "CHINA CUTS TARIFFS FOR CANADA",
         "Xi and Carney agree C$400m of relief on pork and seafood at APEC.",
         icon_trade)

    # also-today strip
    sy = 948
    draw.rectangle([0, sy, W, sy + 48], fill=NAVY)
    f_tick = font(SANS_B, 16)
    tick = ("ALSO TODAY   •   Estonia to shut all Russia border crossings on 1 Dec   •   "
            "Pentagon fails its 9th audit in a row   •   UK sanctions Israeli "
            "settlement firms   •   COP31 draft urges faster fossil-fuel phase-out")
    tlines = wrap(draw, tick, f_tick, W - 48)
    ty = sy + 6
    for ln in tlines[:2]:
        draw.text((24, ty), ln, font=f_tick, fill=(235, 238, 242))
        ty += 19
    # footer
    f_foot = font(SANS, 14)
    foot = "Compiled from wire reports  •  All events of Tuesday 17 November 2026"
    fw, _ = text_size(draw, foot, f_foot)
    draw.text(((W - fw) / 2, 1004), foot, font=f_foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

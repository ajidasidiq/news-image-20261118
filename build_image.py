#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page (1024x1024 PNG).

Draws a newspaper front page with PIL: masthead + date, one lead story
with a drawn bridge illustration, four story cards, and an "also today"
strip. All text is drawn from the strings below; no external assets.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 32, 44)
BLUE = (29, 78, 137)
GREY = (90, 86, 78)
RULE = (180, 172, 156)
CARD = (255, 252, 245)
SKY = (214, 230, 240)
SEA = (64, 110, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, wdt=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def kicker(draw, x, y, text, fill=RED, size=21):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=fill)
    return y + size + 8


def headline(draw, x, y, max_w, text, size=40, fill=INK):
    f = font(SERIF, size)
    y2 = para(draw, x, y, max_w, text, f, fill=fill, leading=int(size * 1.08))
    return y2


def draw_bridge(draw, x, y, w, h):
    """Broken road bridge over strait water, with smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    draw.ellipse([x + w - 78, y + 14, x + w - 34, y + 58], fill=(240, 200, 90))
    # far shore
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(96, 140, 170))
    # water
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=SEA)
    for i, wy in enumerate((y + h - 40, y + h - 26, y + h - 12)):
        for sx in range(0, w, 46):
            draw.arc([x + sx, wy, x + sx + 34, wy + 12], 0, 180,
                     fill=(200, 225, 240), width=3)
    # deck: left span, gap, right span
    deck_y = y + h - 56
    draw.rectangle([x + 8, deck_y, x + w * 0.42, deck_y + 10], fill=(60, 60, 60))
    draw.rectangle([x + w * 0.62, deck_y, x + w - 8, deck_y + 10], fill=(60, 60, 60))
    # tilted fallen section in the gap
    draw.polygon([(x + w * 0.44, deck_y + 2), (x + w * 0.60, deck_y + 2),
                  (x + w * 0.57, deck_y + 26), (x + w * 0.46, deck_y + 26)],
                 fill=(90, 90, 90))
    # arch (broken): left arc and right arc
    draw.arc([x + w * 0.10, deck_y - 48, x + w * 0.44, deck_y + 8], 180, 360,
             fill=RED, width=7)
    draw.arc([x + w * 0.58, deck_y - 48, x + w * 0.92, deck_y + 8], 180, 360,
             fill=RED, width=7)
    # support pillars
    for px in (x + w * 0.16, x + w * 0.34, x + w * 0.68, x + w * 0.86):
        draw.rectangle([px, deck_y + 10, px + 8, y + h - 8], fill=(70, 70, 70))
    # smoke puffs over the gap
    for cx, cy, r in ((x + w * 0.50, deck_y - 34, 16), (x + w * 0.54, deck_y - 52, 20),
                      (x + w * 0.47, deck_y - 58, 13)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_radar(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 226))
    cx, cy = x + w // 2, y + h - 18
    for r in (34, 24, 14):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=BLUE, width=3)
    draw.line([(cx, cy), (cx + 24, cy - 24)], fill=BLUE, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # drones as small crosses
    for dx, dy in ((x + 14, y + 16), (x + w - 16, y + 24), (x + w - 34, y + 10)):
        draw.line([(dx - 6, dy), (dx + 6, dy)], fill=INK, width=2)
        draw.line([(dx, dy - 6), (dx, dy + 6)], fill=INK, width=2)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    # four flags / four leaders as four coloured dots on a table line
    cols = [RED, BLUE, (34, 120, 70), (200, 130, 30)]
    for i, c in enumerate(cols):
        fx = x + 12 + i * ((w - 24) // 3)
        draw.rectangle([fx - 2, y + 16, fx + 2, y + 58], fill=INK)
        draw.polygon([(fx + 2, y + 16), (fx + 18, y + 25), (fx + 2, y + 34)],
                     fill=c)
    draw.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 16], fill=(120, 100, 70))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 28, 40))
    cx, cy = x + w // 2, y + h // 2
    for i in range(5):
        px = x + 18 + i * 16
        draw.line([(px, y + 8), (px, y + 34)], fill=(120, 200, 255), width=3)
        draw.line([(px, y + h - 34), (px, y + h - 8)], fill=(120, 200, 255), width=3)
    for j in range(5):
        py = y + 18 + j * 16
        draw.line([(x + 8, py), (x + 34, py)], fill=(120, 200, 255), width=3)
        draw.line([(x + w - 34, py), (x + w - 8, py)], fill=(120, 200, 255), width=3)
    draw.rectangle([cx - 42, cy - 42, cx + 42, cy + 42], fill=(40, 90, 140),
                   outline=(160, 220, 255), width=3)
    draw.text((cx, cy), "AI", font=font(SANS_B, 34), fill=(255, 255, 255),
              anchor="mm")
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 232, 238))
    cx, cy = x + w // 2, y + h // 2
    for r, col in ((34, (90, 130, 170)), (24, (60, 100, 150)), (14, (30, 70, 120))):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=6)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def card(draw, x, y, w, h, tag, title, body, art):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    ax, ay, aw, ah = x + 12, y + 12, 96, 80
    art(draw, ax, ay, aw, ah)
    tx = x + 120
    tw = w - 120 - 12
    ty = kicker(draw, tx, y + 12, tag, size=17)
    ty = headline(draw, tx, ty, tw, title, size=22)
    para(draw, tx, ty + 4, tw, body, font(SANS, 16), leading=21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin

    # ---- top strip ----
    d.text((M, 22), "THE WORLD IN ONE PAGE  •  EST. 2026",
           font=font(SANS_B, 17), fill=GREY)
    d.text((W - M, 22), "ONE DAY • ONE IMAGE", font=font(SANS_B, 17),
           fill=GREY, anchor="ra")
    rule(d, M, 52, W - M, 2)

    # ---- masthead ----
    d.text((W // 2, 60), "THE WORLD TODAY", font=font(SERIF, 58), fill=INK,
           anchor="ma")
    d.text((W // 2, 124), "WEDNESDAY, 18 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=RED, anchor="ma")
    d.text((W // 2, 164),
           "The day's most consequential stories — from every region, every field.",
           font=font(SERIF_R, 19), fill=GREY, anchor="ma")
    rule(d, M, 196, W - M, 3, fill=INK)

    # ---- lead story ----
    ly = 208
    d.text((M, ly), "LEAD STORY  •  UKRAINE", font=font(SANS_B, 19), fill=RED)
    hy = headline(d, M, ly + 28, W - 2 * M,
                  "UKRAINE CRIPPLES THE CRIMEA BRIDGE", size=38)
    draw_bridge(d, M, hy + 8, 560, 140)
    tx = M + 584
    by = para(d, tx, hy + 10, W - M - tx,
              "Kyiv says its drones and missiles brought down the road arch "
              "of the 19-km bridge linking Russia to occupied Crimea.",
              font(SANS, 19), leading=25)
    by = para(d, tx, by + 8, W - M - tx,
              "Biggest drone attack of the war — 1,441 drones, Russia says. "
              "Two killed; traffic halted. Russia hit two Kyiv bridges in reply.",
              font(SANS_B, 18), leading=24)
    lead_bottom = max(hy + 148, by)
    rule(d, M, lead_bottom + 10, W - M, 2)

    # ---- second row: two cards ----
    ry = lead_bottom + 22
    cw = (W - 2 * M - 24) // 2
    ch = 192
    card(d, M, ry, cw, ch, "The Gulf",
         "IRAN DRONES AT U.S. BASE — U.S. HITS BACK",
         "Iranian drones aimed at a U.S. radar at Sheikh Isa air base in "
         "Bahrain were intercepted, CENTCOM says, with no damage. The U.S. "
         "then hit a missile site on Qeshm Island.",
         draw_radar)
    card(d, M + cw + 24, ry, cw, ch, "Asia",
         "TRUMP MEETS QUAD LEADERS IN MANILA",
         "Donald Trump opened a three-day Asia trip with the first Quad "
         "summit in two years — the U.S., Japan, India and Australia — "
         "before heading to Shenzhen for APEC and talks with Xi and Putin.",
         draw_summit)

    # ---- third row: two cards ----
    ry2 = ry + ch + 14
    card(d, M, ry2, cw, ch, "Business • Technology",
         "NVIDIA DOUBLES SALES TO $115.8BN",
         "The AI chipmaker reported record quarterly revenue, up 103% on a "
         "year ago, and forecast $130bn next quarter. Interim chief Colette "
         "Kress led the call after Jensen Huang's exit.",
         draw_chip)
    card(d, M + cw + 24, ry2, cw, ch, "Weather • Asia",
         "CYCLONE AKVAN BEARS DOWN ON INDIA",
         "The severe cyclonic storm in the Bay of Bengal packed winds of "
         "85–95 km/h, gusting to 105, and was heading for the Andhra "
         "Pradesh coast, with landfall expected around 20 November.",
         draw_cyclone)

    # ---- also-today strip: four items in one row ----
    ay = ry2 + ch + 14
    rule(d, M, ay, W - M, 3, fill=INK)
    d.text((M, ay + 8), "ALSO ON 18 NOVEMBER", font=font(SANS_B, 19), fill=RED)
    items = [
        ("LATVIA", "Parliament backs a new government led by Kulbergs."),
        ("U.S.", "Asif Merchant jailed 27\u00bd years over a plot."),
        ("UKRAINE", "U.N.: 372 civilians killed in Ukraine in October."),
        ("TECH", "Google flags the first autonomous AI cyberattack."),
    ]
    iy = ay + 36
    col_w = (W - 2 * M) // 4
    for i, (tag, txt) in enumerate(items):
        cx = M + i * col_w
        d.text((cx, iy), tag, font=font(SANS_B, 15), fill=RED)
        para(d, cx, iy + 20, col_w - 12, txt, font(SANS, 14), leading=18)

    # ---- footer note on the strip title line ----
    d.text((W - M, ay + 8), "All stories first reported on 18 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ra")

    print("layout: lead_bottom", lead_bottom, "cards end", ry2 + ch,
          "strip items y", iy)

    img.save("/home/hatch/workspace/makefun/news-image-20261118/entry.png",
             optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

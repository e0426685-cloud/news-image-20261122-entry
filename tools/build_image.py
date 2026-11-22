#!/usr/bin/env python3
"""Build the front page for THE WORLD TODAY - Sunday, 22 November 2026.

Draws a 1024x1024 broadsheet front page with PIL: masthead, a lead story
on the widening Gulf war, and the day's other top stories, each with a
small programmatically drawn illustration. Run: python3 tools/build_image.py
Writes entry.png in the repository root.
"""
import math
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
SEA = (158, 196, 222)
SAND = (226, 205, 160)
GREY = (110, 110, 108)
LIGHT = (238, 233, 220)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest font size at or below `size` that fits `text` in `max_w`."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
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


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r, fill, spikes=12):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def gulf_scene(draw, box):
    """Stylised Gulf: sea, coastline, tanker, explosion bursts."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + 22), (x0 + 190, y0 + 28),
                  (x0 + 150, y0 + 58), (x0, y0 + 48)], fill=SAND)
    draw.polygon([(x0, y1), (x0 + 210, y1), (x0 + 235, y1 - 64),
                  (x0 + 130, y1 - 80), (x0 + 60, y1 - 44)], fill=SAND)
    draw.polygon([(x1, y1), (x1 - 120, y1), (x1 - 150, y1 - 50),
                  (x1 - 60, y1 - 36)], fill=SAND)
    draw.line([(x0 + 235, y1 - 64), (x1 - 150, y1 - 50)], fill=NAVY, width=3)
    # Tanker in the strait
    tx, ty = x0 + 380, y0 + 102
    draw.rectangle([tx, ty, tx + 120, ty + 20], fill=(60, 60, 62))
    draw.rectangle([tx + 96, ty - 14, tx + 112, ty], fill=(60, 60, 62))
    draw.rectangle([tx + 8, ty + 20, tx + 112, ty + 26], fill=RED)
    draw.arc([tx - 4, ty + 24, tx + 24, ty + 40], 0, 180, fill=INK, width=2)
    draw.arc([tx + 98, ty + 24, tx + 126, ty + 40], 0, 180, fill=INK, width=2)
    # Explosion bursts over Kuwait (left) and Bahrain (right)
    burst(draw, x0 + 70, y0 + 44, 24, (255, 176, 32))
    burst(draw, x0 + 70, y0 + 44, 13, RED)
    burst(draw, x1 - 78, y1 - 44, 20, (255, 176, 32))
    burst(draw, x1 - 78, y1 - 44, 10, RED)
    small = font(SANS_B, 13)
    draw.text((x0 + 8, y0 + 6), "IRAN", font=small, fill=NAVY)
    draw.text((x0 + 8, y1 - 20), "SAUDI ARABIA", font=small, fill=NAVY)
    draw.text((x1 - 92, y1 - 20), "OMAN", font=small, fill=NAVY)
    draw.text((x0 + 380, y0 + 80), "STRAIT OF HORMUZ", font=small, fill=NAVY)
    draw.text((x0 + 30, y0 + 76), "KUWAIT", font=small, fill=RED)
    draw.text((x1 - 118, y1 - 66), "BAHRAIN", font=small, fill=RED)


def globe_scene(draw, box):
    """A warming globe: blue sphere, green land, red thermometer band."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=LIGHT)
    cx, cy, r = (x0 + x1) // 2 - 34, (y0 + y1) // 2, 44
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 160, 210),
                 outline=NAVY, width=3)
    draw.ellipse([cx - 30, cy - 26, cx + 4, cy + 4], fill=(96, 178, 110))
    draw.ellipse([cx - 4, cy + 10, cx + 32, cy + 34], fill=(96, 178, 110))
    draw.ellipse([cx + 10, cy - 36, cx + 32, cy - 10], fill=(96, 178, 110))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=3)
    tx = x1 - 40
    draw.rounded_rectangle([tx, y0 + 16, tx + 18, y1 - 30], 9, fill=(255, 255, 255),
                           outline=RED, width=3)
    draw.ellipse([tx - 7, y1 - 44, tx + 25, y1 - 12], fill=RED)
    draw.rectangle([tx + 4, y0 + 38, tx + 14, y1 - 28], fill=RED)
    draw.text((tx - 4, y0 + 2), "1.5C", font=font(SANS_B, 12), fill=RED)


def sky_scene(draw, box):
    """Night sky over a city skyline, missile trails arcing down."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(22, 30, 52))
    rnd = random.Random(11)
    for _ in range(22):
        sx = rnd.randint(x0 + 4, x1 - 4)
        sy = rnd.randint(y0 + 4, y0 + 44)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    for sx, sy, ex, ey in [(x0 + 30, y0 + 12, x0 + 70, y1 - 42),
                           (x0 + 120, y0 + 6, x0 + 150, y1 - 48),
                           (x0 + 210, y0 + 16, x0 + 240, y1 - 40)]:
        draw.line([(sx, sy), (ex, ey)], fill=(255, 200, 80), width=3)
        burst(draw, ex, ey, 10, (255, 176, 32))
        burst(draw, ex, ey, 5, RED)
    base = y1
    heights = [34, 56, 42, 66, 46, 60, 38, 50]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 3, base - hh, bx + bw - 3, base], fill=(10, 14, 28))
        for wy in range(base - hh + 7, base - 5, 12):
            for wx in range(bx + 7, bx + bw - 7, 11):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))


def quake_scene(draw, box):
    """Seismograph trace over cracked mountain peaks."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=LIGHT)
    draw.polygon([(x0, y1), (x0 + 50, y0 + 34), (x0 + 110, y1)], fill=(150, 140, 125))
    draw.polygon([(x0 + 95, y1), (x0 + 170, y0 + 18), (x0 + 250, y1)], fill=(120, 110, 96))
    draw.polygon([(x0 + 158, y0 + 28), (x0 + 170, y0 + 18), (x0 + 182, y0 + 28),
                  (x0 + 176, y0 + 25), (x0 + 164, y0 + 25)], fill=(255, 255, 255))
    pts = [(x0 + 6, (y0 + y1) // 2 + 8)]
    for i in range(1, 36):
        px = x0 + 6 + i * (x1 - x0 - 12) / 36
        amp = 3 if i < 12 or i > 25 else 15
        py = (y0 + y1) // 2 + 8 + amp * math.sin(i * 1.7) * (1 if i % 2 else -1)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=2)
    draw.text((x0 + 6, y0 + 4), "M 6.9", font=font(SANS_B, 16), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)
    mx = 36

    # ---- top dateline bar ----
    d.text((mx, 12), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 16), fill=INK)
    d.text((W - mx - 290, 12), "VOL. I  ·  No. 327  ·  ONE DAY'S NEWS",
           font=font(SANS, 14), fill=GREY)
    rule(d, mx, 36, W - mx, 2)
    # ---- masthead (auto-fit) ----
    mast = fit(d, "THE WORLD TODAY", SERIF_B, 84, W - 2 * mx)
    d.text((mx, 42), "THE WORLD TODAY", font=mast, fill=INK)
    rule(d, mx, 134, W - mx, 5)
    d.text((mx, 140), "SUMMING UP THE WORLD'S NEWS IN ONE IMAGE",
           font=font(SANS_B, 17), fill=RED)
    d.text((W - mx - 250, 140), "LONDON  ·  NEW YORK  ·  THE WORLD",
           font=font(SANS, 13), fill=GREY)
    rule(d, mx, 164, W - mx, 2)

    # ---- lead story ----
    y = 172
    d.text((mx, y), "GULF WAR WIDENS", font=font(SERIF_B, 48), fill=RED)
    y += 56
    deck = fit(d, "Iran hits U.S. air base in Kuwait as attacks spread to Bahrain",
               SERIF_B, 25, W - 2 * mx)
    d.text((mx, y), "Iran hits U.S. air base in Kuwait as attacks spread to Bahrain",
           font=deck, fill=INK)
    y += 34
    gulf_scene(d, (mx, y, W - mx, y + 168))
    y += 176
    y = para(d, (mx, y),
             "Iran widened its attacks on its Gulf neighbours, firing on the U.S. "
             "air base at Ali Al Salem in Kuwait and striking several times at "
             "Bahrain, in apparent retaliation for American strikes the day before. "
             "Kuwait said its air defences met a wave of incoming drones; no damage "
             "was reported. Tankers in the Strait of Hormuz came under attack again: "
             "an ADNOC vessel was hit, leaving one crew member missing and 11 injured. "
             "Brent crude traded near $91 a barrel.",
             font(SERIF, 16), W - 2 * mx, leading=20)
    rule(d, mx, y + 6, W - mx, 2)

    # ---- middle row: two stories ----
    y += 16
    col_w = (W - 2 * mx - 24) // 2
    left_x, right_x = mx, mx + col_w + 24
    top = y
    d.text((left_x, top), "CLIMATE TALKS IN DEADLOCK",
           font=fit(d, "CLIMATE TALKS IN DEADLOCK", SERIF_B, 19, col_w), fill=INK)
    d.text((right_x, top), "400 DRONES, 110 MISSILES HIT UKRAINE",
           font=fit(d, "400 DRONES, 110 MISSILES HIT UKRAINE", SERIF_B, 19, col_w),
           fill=INK)
    y2 = top + 27
    d.text((left_x, y2), "COP31 stalls over fossil fuels", font=font(SERIF, 15), fill=GREY)
    d.text((right_x, y2), "Missile crashes in Poland; Kyiv under fire",
           font=font(SERIF, 15), fill=GREY)
    y2 += 22
    globe_scene(d, (left_x, y2, left_x + col_w, y2 + 96))
    sky_scene(d, (right_x, y2, right_x + col_w, y2 + 96))
    y2 += 104
    y2 = max(
        para(d, (left_x, y2),
             "Negotiators at the COP31 climate talks were deadlocked over fossil "
             "fuels and climate finance, with no agreement in sight as the summit "
             "entered its final stretch.",
             font(SERIF, 14), col_w, leading=18),
        para(d, (right_x, y2),
             "Russia struck Ukraine with 400 drones and 110 missiles in one of the "
             "war's largest attacks. A missile crashed in Poland near the border; "
             "Warsaw called it a provocation.",
             font(SERIF, 14), col_w, leading=18),
    )
    rule(d, mx, y2 + 6, W - mx, 2)

    # ---- lower row: three briefs ----
    y = y2 + 16
    bw3 = (W - 2 * mx - 48) // 3
    xs = [mx, mx + bw3 + 24, mx + 2 * (bw3 + 24)]
    stories = [
        ("QUAKE SHAKES PERU'S ANDES",
         "A magnitude 6.9 earthquake shook central Peru, its epicentre 34 km "
         "north of Junin at a depth of 108 km. Tremors were felt in Lima; no "
         "damage or casualties were immediately reported."),
        ("CARTEL BOSS 'EL CHAPO ISIDRO' SEIZED",
         "Mexican special forces arrested alleged drug cartel boss 'El Chapo "
         "Isidro' in a raid. The arrest set off deadly violence in Sinaloa, "
         "where 11 people were killed."),
        ("TRUMP, XI AND PUTIN MEET IN SHENZHEN",
         "President Trump called his trilateral summit with Xi Jinping and "
         "Vladimir Putin 'momentous' at the APEC meeting. Vice-President Vance "
         "refused to back Trump's Iran strikes."),
    ]
    head_end = y
    for x, (head, _body) in zip(xs, stories):
        end = para(d, (x, y), head, font(SERIF_B, 15), bw3, leading=19)
        head_end = max(head_end, end)
    y3 = head_end + 6
    quake_scene(d, (xs[0], y3, xs[0] + bw3, y3 + 62))
    d.rectangle([xs[1], y3, xs[1] + bw3, y3 + 62], fill=LIGHT)
    d.text((xs[1] + 10, y3 + 10), "HANDCUFFS", font=font(SANS_B, 18), fill=NAVY)
    d.text((xs[1] + 10, y3 + 36), "SINALOA  ·  11 DEAD", font=font(SANS_B, 12), fill=RED)
    d.rectangle([xs[2], y3, xs[2] + bw3, y3 + 62], fill=LIGHT)
    d.text((xs[2] + 10, y3 + 6), "SHENZHEN", font=font(SANS_B, 18), fill=NAVY)
    d.text((xs[2] + 10, y3 + 30), "APEC SUMMIT", font=font(SANS_B, 14), fill=INK)
    d.text((xs[2] + 10, y3 + 48), "TRUMP  ·  XI  ·  PUTIN", font=font(SANS_B, 12), fill=GREY)
    y3 += 70
    y3 = max(para(d, (x, y3), body, font(SERIF, 13), bw3, leading=17)
             for x, (_, body) in zip(xs, stories))
    rule(d, mx, y3 + 6, W - mx, 2)

    # ---- bottom ticker + footer ----
    y = y3 + 14
    ticker = ("ALSO TODAY:  Bolsonaro, Brazil's imprisoned ex-president, in intensive "
              "care  ·  Drones hit a Russian cargo ship in the Baltic  ·  India v New "
              "Zealand, 1st Test at Wellington  ·  Cummins keeps the captaincy")
    tfont = fit(d, ticker, SERIF, 13, W - 2 * mx)
    d.text((mx, y), ticker, font=tfont, fill=INK)
    rule(d, mx, H - 34, W - mx, 2)
    d.text((mx, H - 26), "THE WORLD TODAY — 22 NOVEMBER 2026",
           font=font(SANS_B, 14), fill=INK)
    d.text((W - mx - 250, H - 26), "All the news that fits on one page.",
           font=font(SERIF, 13), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

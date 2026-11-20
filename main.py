#!/usr/bin/env python3
"""A one-day newspaper picture for Thursday 19 November 2026.

This file paints a 1024x1024 PNG with nothing but the Python
standard library: a built-in 5x7 dot font, a small scene builder,
and a hand-rolled PNG writer. It reads no files, uses no network,
and prints the same bytes on every run.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

PARCH = (247, 243, 232)
INK = (22, 24, 30)
MID = (20, 33, 61)
MID2 = (30, 48, 84)
RUBY = (176, 32, 32)
HONEY = (201, 149, 44)
SMOKE = (112, 116, 122)
MIST = (214, 209, 196)
FROST = (250, 250, 246)
SKY2 = (166, 199, 224)
TIDE = (46, 94, 124)
JADE = (36, 122, 110)
BEACH = (226, 205, 158)
ABYSS = (16, 24, 48)
FERN = (46, 125, 72)
COBALT = (43, 88, 168)
FLAG = (28, 58, 140)
FLAME = (214, 110, 44)
PLUM = (92, 58, 140)

# ----------------------------------------------------------------- font --
# 5x7 dot glyphs, drawn for this picture. One glyph is a single
# 35-bit string, row by row, 1 for a filled dot and 0 for an empty
# one. Text is drawn in capitals; lowercase is upper-cased first.

GLYPH = {
    "A": "01110100011000111111100011000110001",
    "B": "11110100011000111110100011000111110",
    "C": "01111100001000010000100001000001111",
    "D": "11100100101000110001100011001011100",
    "E": "11111100001000011110100001000011111",
    "F": "11111100001000011110100001000010000",
    "G": "01111100001000010111100011000101110",
    "H": "10001100011000111111100011000110001",
    "I": "01110001000010000100001000010001110",
    "J": "00111000100001000010000101001001100",
    "K": "10001100101010011000101001001010001",
    "L": "10000100001000010000100001000011111",
    "M": "10001110111010110101100011000110001",
    "N": "10001110011100110101100111001110001",
    "O": "01110100011000110001100011000101110",
    "P": "11110100011000111110100001000010000",
    "Q": "01110100011000110001101011001001101",
    "R": "11110100011000111110101001001010001",
    "S": "01111100001000001110000010000111110",
    "T": "11111001000010000100001000010000100",
    "U": "10001100011000110001100011000101110",
    "V": "10001100011000110001100010101000100",
    "W": "10001100011000110101101011101110001",
    "X": "10001010100010000100001000101010001",
    "Y": "10001100010101000100001000010000100",
    "Z": "11111000010001000100010001000011111",
    "0": "01110100011001110101110011000101110",
    "1": "00100011000010000100001000010001110",
    "2": "01110100010000100110010001000011111",
    "3": "11110000010000101110000010000111110",
    "4": "00010001100101010010111110001000010",
    "5": "11111100001111000001000011000101110",
    "6": "01110100001000011110100011000101110",
    "7": "11111000010001000100001000010000100",
    "8": "01110100011000101110100011000101110",
    "9": "01110100011000101111000010000101110",
    " ": "00000000000000000000000000000000000",
    ".": "00000000000000000000000000110001100",
    ",": "00000000000000000000011000010001000",
    ":": "00000011000110000000011000110000000",
    ";": "00000011000110000000011000010001000",
    "'": "00100001000100000000000000000000000",
    "-": "00000000000000011111000000000000000",
    "!": "00100001000010000100001000000000100",
    "?": "01110100010000100010001000000000100",
    "/": "00001000010001000100010001000010000",
    "(": "00010001000100001000010000010000010",
    ")": "01000001000001000010000100010001000",
    "%": "11001110100001000100010001010110011",
    "+": "00000001000010011111001000010000000",
    "$": "00100011111010001110001011111000100",
    "&": "01100100101001001000101011001001101",
    "=": "00000000001111100000111110000000000",
    '"': "01010010100101000000000000000000000",
    "_": "00000000000000000000000000000011111",
    "|": "00100001000010000100001000010000100",
    "<": "00001000100010001000001000001000001",
    ">": "10000010000010000010001000100010000",
}


def text_w(s, sc):
    """Pixel width of text drawn at the given scale."""
    return len(s) * 6 * sc - sc if s else 0


def wrap(t, sc, maxw):
    """Greedy word wrap. Returns a list of lines, all upper-cased."""
    words = t.upper().split()
    out = []
    cur = []
    wsum = 0
    for wd in words:
        add = len(wd) * 6 * sc
        if cur:
            add += 6 * sc
        if cur and wsum + add - sc > maxw:
            out.append(" ".join(cur))
            cur = [wd]
            wsum = len(wd) * 6 * sc
        else:
            cur.append(wd)
            wsum += add
    if cur:
        out.append(" ".join(cur))
    return out


# ------------------------------------------------------------ drawing ----

def put(b, x, y, rgb):
    """Set one pixel, silently skipping anything off the sheet."""
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        b[i:i + 3] = bytes(rgb)


def box(b, x, y, bw, bh, rgb):
    """Fill a rectangle, clipped to the sheet."""
    x0 = x if x > 0 else 0
    y0 = y if y > 0 else 0
    x1 = x + bw if x + bw < W else W
    y1 = y + bh if y + bh < H else H
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(rgb) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        b[i:i + len(row)] = row


def hbar(b, x, y, ln, rgb, th=1):
    box(b, x, y, ln, th, rgb)


def vbar(b, x, y, ln, rgb, th=1):
    box(b, x, y, th, ln, rgb)


def frame(b, x, y, bw, bh, rgb, th=1):
    box(b, x, y, bw, th, rgb)
    box(b, x, y + bh - th, bw, th, rgb)
    box(b, x, y, th, bh, rgb)
    box(b, x + bw - th, y, th, bh, rgb)


def trace(b, x0, y0, x1, y1, rgb, th=1):
    """A straight segment, Bresenham's walk, with a square nib."""
    dx = x1 - x0
    dy = y1 - y0
    ax = dx if dx >= 0 else -dx
    ay = dy if dy >= 0 else -dy
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    err = ax - ay
    half = th // 2
    offs = [(a, c) for a in range(-half, half + 1)
            for c in range(-half, half + 1)]
    for _ in range(max(ax, ay) + 1):
        for (ox, oy) in offs:
            put(b, x0 + ox, y0 + oy, rgb)
        e2 = err + err
        if e2 > -ay:
            err = err - ay
            x0 = x0 + sx
        if e2 < ax:
            err = err + ax
            y0 = y0 + sy


def disc(b, cx, cy, r, rgb):
    """A filled disc, one horizontal run per row."""
    for dy in range(-r, r + 1):
        dx = math.isqrt(r * r - dy * dy)
        hbar(b, cx - dx, cy + dy, 2 * dx + 1, rgb)


def hoop(b, cx, cy, r, rgb, th=2):
    """A ring, plotted degree by degree."""
    for deg in range(360):
        th_rad = deg * (math.pi / 180)
        for t in range(th):
            put(b, cx + int((r + t) * math.cos(th_rad)),
                cy + int((r + t) * math.sin(th_rad)), rgb)


def bend(b, cx, cy, r, a0, a1, rgb, th=2):
    """An arc between two angles, plotted degree by degree."""
    for deg in range(a0, a1 + 1):
        th_rad = deg * (math.pi / 180)
        for t in range(th):
            put(b, cx + int((r + t) * math.cos(th_rad)),
                cy + int((r + t) * math.sin(th_rad)), rgb)


def poly(b, pts, rgb):
    """Fill a polygon with the even-odd scanline rule."""
    if len(pts) < 3:
        return
    top = min(p[1] for p in pts)
    bot = max(p[1] for p in pts)
    n = len(pts)
    for y in range(top, bot + 1):
        xs = []
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append((x1 - x0) * (y - y0) / (y1 - y0) + x0)
        xs.sort()
        for xa, xb in zip(xs[::2], xs[1::2]):
            hbar(b, int(xa), y, max(1, int(xb) - int(xa)), rgb)


def star(b, cx, cy, r, rgb):
    """A four-point sparkle: two diagonals and two axes."""
    for (ax, ay, bx, by, th) in ((-r, 0, r, 0, 2), (0, -r, 0, r, 2),
                                (-(r // 2), -(r // 2), r // 2, r // 2, 1),
                                (-(r // 2), r // 2, r // 2, -(r // 2), 1)):
        trace(b, cx + ax, cy + ay, cx + bx, cy + by, rgb, th)


def paint_text(b, x, y, s, sc, rgb):
    """Draw text with the dot font; returns the width drawn."""
    cx = x
    for ch in s.upper():
        bits = GLYPH.get(ch, GLYPH[" "])
        for k in range(35):
            if bits[k] == "1":
                row, col = divmod(k, 5)
                box(b, cx + col * sc, y + row * sc, sc, sc, rgb)
        cx += 6 * sc
    return cx - x


def center_text(b, cx, y, s, sc, rgb):
    paint_text(b, cx - text_w(s.upper(), sc) // 2, y, s, sc, rgb)


# ------------------------------------------------------------ pictures ----

def summit(b, x, y, w, h):
    """Shenzhen skyline with three flags: US, China, Russia."""
    box(b, x, y, w, h, SKY2)
    box(b, x, y + h - 30, w, 30, MID2)
    bxs = [8, 60, 100, 280, 326]
    bws = [46, 34, 52, 40, 52]
    bhs = [52, 68, 44, 58, 40]
    for bx, bw, bh in zip(bxs, bws, bhs):
        box(b, x + bx, y + h - 30 - bh, bw, bh, MID)
    trace(b, x + 77, y + h - 98, x + 77, y + h - 116, MID, 3)
    disc(b, x + 77, y + h - 118, 3, RUBY)

    def mast(px):
        vbar(b, x + px, y + 8, h - 38, FROST, 3)

    def us_flag(fx, fy):
        for i in range(7):
            box(b, x + fx, y + fy + i * 5, 58, 5,
                RUBY if i % 2 == 0 else FROST)
        box(b, x + fx, y + fy, 26, 20, MID)
        for dy in range(3):
            for dx in range(3):
                put(b, x + fx + 4 + dx * 8, y + fy + 4 + dy * 6, FROST)

    def cn_flag(fx, fy):
        box(b, x + fx, y + fy, 58, 35, RUBY)
        star(b, x + fx + 12, y + fy + 12, 6, HONEY)
        sxs = [30, 38, 38, 30]
        sys = [6, 12, 20, 26]
        for sx, sy in zip(sxs, sys):
            star(b, x + fx + sx, y + fy + sy, 3, HONEY)

    def ru_flag(fx, fy):
        box(b, x + fx, y + fy, 58, 12, FROST)
        box(b, x + fx, y + fy + 12, 58, 11, COBALT)
        box(b, x + fx, y + fy + 23, 58, 12, RUBY)

    mast(150)
    us_flag(154, 10)
    mast(232)
    cn_flag(236, 10)
    mast(314)
    ru_flag(318, 10)
    paint_text(b, x + 12, y + h - 24, "SHENZHEN", 2, FROST)
    paint_text(b, x + 250, y + h - 24, "KYLIN VILLA", 2, HONEY)


def storm(b, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal with the Indian coast."""
    box(b, x, y, w, h, TIDE)
    cxs = [x, x + 74, x + 58, x + 84, x + 66, x]
    cys = [y, y, y + 30, y + 58, y + h, y + h]
    poly(b, list(zip(cxs, cys)), BEACH)
    paint_text(b, x + 4, y + 6, "INDIA", 2, INK)
    cx, cy = x + w // 2 + 30, y + h // 2
    pts = []
    for spoke in range(3):
        for step in range(300):
            an = math.radians(step + spoke * 120)
            rr = step * 0.22 + 8
            dx = int(rr * math.cos(an))
            dy = int(rr * math.sin(an) * 0.82)
            pts.append((cx + dx, cy + dy))
    for (px, py) in pts:
        disc(b, px, py, 3, FROST)
    disc(b, cx, cy, 11, HONEY)
    hoop(b, cx, cy, 14, FROST, 2)
    for rx in range(x + w - 90, x + w - 8, 18):
        trace(b, rx, y + 10, rx - 8, y + 26, SKY2, 2)
    paint_text(b, x + w - 118, y + h - 40, "GUSTS 90", 2, FROST)
    paint_text(b, x + w - 118, y + h - 22, "KM/H", 2, FROST)


def shares(b, x, y, w, h):
    """A rising share-price bar for the record IPO debut."""
    box(b, x, y, w, h, FROST)
    frame(b, x, y, w, h, MIST, 1)
    paint_text(b, x + 12, y + 6, "ANT  -  NASDAQ", 2, MID)
    paint_text(b, x + 12, y + 24, "CLOSE $97.17", 2, INK)
    ax0, ay0 = x + 34, y + h - 8
    trace(b, ax0, y + 44, ax0, ay0, SMOKE, 2)
    trace(b, ax0, ay0, x + w - 12, ay0, SMOKE, 2)
    heights = [12, 18, 24, 30, 38]
    for i, bh in enumerate(heights):
        bx = ax0 + 22 + i * 62
        box(b, bx, ay0 - bh, 34, bh, JADE if i < 4 else FERN)
    pxs = [ax0 + 30, ax0 + 92, ax0 + 154, ax0 + 216, ax0 + 286]
    pys = [ay0 - 16, ay0 - 22, ay0 - 28, ay0 - 34, ay0 - 42]
    for i in range(len(pxs) - 1):
        trace(b, pxs[i], pys[i], pxs[i + 1], pys[i + 1], FERN, 3)
    txs = [pxs[-1], pxs[-1] - 10, pxs[-1] + 10]
    tys = [pys[-1] - 12, pys[-1] + 2, pys[-1] + 2]
    poly(b, list(zip(txs, tys)), FERN)


def vice(b, x, y, w, h):
    """Vice City sunset: sun, palms, skyline and a car."""
    box(b, x, y, w, h, FLAME)
    disc(b, x + w // 2, y + 42, 26, HONEY)
    box(b, x, y + h - 34, w, 34, PLUM)
    bxs = [10, 56, 320, 372]
    bws = [40, 28, 44, 30]
    bhs = [30, 44, 34, 48]
    for bx, bw, bh in zip(bxs, bws, bhs):
        box(b, x + bx, y + h - 34 - bh, bw, bh, MID)
    # Palm trees.
    for tx, ty in ((150, h - 34), (260, h - 34)):
        trace(b, x + tx, y + ty, x + tx + 6, y + ty - 34, INK, 3)
        dxs = [-18, -10, 0, 12, 20]
        dys = [-8, -14, -16, -12, -6]
        for dx, dy in zip(dxs, dys):
            trace(b, x + tx + 6, y + ty - 34,
                  x + tx + 6 + dx, y + ty - 34 + dy, INK, 2)
    # A low car silhouette.
    box(b, x + 170, y + h - 22, 120, 10, INK)
    cxs = [x + 195, x + 210, x + 250, x + 265]
    cys = [y + h - 22, y + h - 34, y + h - 34, y + h - 22]
    poly(b, list(zip(cxs, cys)), INK)
    disc(b, x + 195, y + h - 10, 6, INK)
    disc(b, x + 265, y + h - 10, 6, INK)
    paint_text(b, x + 12, y + 8, "VICE CITY", 2, FROST)
    paint_text(b, x + w - 60, y + 8, "VI", 3, FROST)


def probe(b, x, y, w, h):
    """Voyager 1 in deep space: dish, golden record, one light-day."""
    box(b, x, y, w, h, ABYSS)
    sxs = [18, 52, 96, 150, 205, 260, 318, 360, 30, 235, 400, 430]
    sys = [12, 26, 8, 20, 10, 24, 14, 30, 44, 40, 12, 44]
    for sx, sy in zip(sxs, sys):
        put(b, x + sx, y + sy, FROST)
        put(b, x + sx + 1, y + sy, FROST)
    # Sun, far behind.
    disc(b, x + 40, y + h - 30, 16, HONEY)
    # Probe body, dish and golden record disc.
    qx, qy = x + w // 2 + 20, y + h // 2 - 6
    box(b, qx - 34, qy - 8, 68, 16, FROST)
    trace(b, qx - 34, qy, qx - 62, qy - 22, FROST, 3)
    trace(b, qx - 34, qy, qx - 62, qy + 22, FROST, 3)
    trace(b, qx - 62, qy - 22, qx - 62, qy + 22, FROST, 3)
    disc(b, qx + 48, qy, 14, HONEY)
    hoop(b, qx + 48, qy, 14, FROST, 1)
    trace(b, qx + 34, qy - 4, qx + 62, qy - 14, JADE, 2)
    trace(b, qx + 34, qy + 4, qx + 62, qy + 14, JADE, 2)
    # Signal path back to Earth, dotted.
    for i in range(0, 120, 8):
        put(b, x + 60 + i, y + h - 30 - i // 3, HONEY)
    paint_text(b, x + 12, y + 8, "1 LIGHT-DAY", 2, HONEY)
    paint_text(b, x + w - 150, y + h - 22, "26BN KM", 2, FROST)


# -------------------------------------------------------------- layout ----

def card(b, x, y, w, tag, heads, body, paint):
    """One story: picture on top, kicker, headlines, wrapped deck."""
    paint(b, x, y, w, 86)
    paint_text(b, x, y + 96, tag, 2, RUBY)
    yy = y + 118
    for line in heads:
        paint_text(b, x, yy, line, 3, INK)
        yy += 28
    for line in wrap(body, 2, w):
        paint_text(b, x, yy, line, 2, INK)
        yy += 18


def build():
    b = bytearray(bytes(PARCH) * (W * H))
    frame(b, 0, 0, W, H, INK, 4)

    # Masthead.
    box(b, 4, 4, W - 8, 124, MID)
    paint_text(b, 24, 22, "WORLD NEWS", 2, HONEY)
    paint_text(b, W - 24 - text_w("DRAWN IN CODE", 2), 22,
               "DRAWN IN CODE", 2, HONEY)
    center_text(b, W // 2, 20, "THE WORLD TODAY", 5, FROST)
    center_text(b, W // 2, 70, "THURSDAY, 19 NOVEMBER 2026", 3, FROST)
    hbar(b, 24, 106, W - 48, HONEY, 2)
    center_text(b, W // 2, 112, "ONE DAY  -  ONE IMAGE", 2, MIST)
    box(b, 4, 128, W - 8, 5, RUBY)

    # Lead story: Trump-Xi-Putin trilateral.
    gx, gy, gw = 24, 146, 560
    hx, hw = 608, 392
    paint_text(b, gx, gy, "DIPLOMACY  -  LEAD STORY", 2, RUBY)
    paint_text(b, gx, gy + 24, "THREE LEADERS", 4, INK)
    paint_text(b, gx, gy + 56, "4-POINT DECLARATION", 4, INK)
    lead = ("THE FIRST-EVER TRUMP-XI-PUTIN SUMMIT ENDED WITH A "
            "4-POINT DECLARATION: UN REFORM, MORE REFINED OIL, "
            "ICC LIMITS AND NUCLEAR-RISK TALKS. NO DEAL ON "
            "UKRAINE, IRAN OR ARMS LIMITS.")
    yy = gy + 96
    for line in wrap(lead, 2, gw):
        paint_text(b, gx, yy, line, 2, INK)
        yy += 18
    paint_text(b, gx, yy + 8, "TALKS RAN 4:16-6:01 PM, NEARLY 2 HRS LATE.",
               2, SMOKE)
    paint_text(b, gx, yy + 26, "REPORTS SAY TRUMP-XI EXTENDED TRADE TRUCE.",
               2, SMOKE)
    summit(b, hx, gy, hw, 270)
    frame(b, hx, gy, hw, 270, INK, 2)

    # Divider.
    hbar(b, 24, 430, W - 48, INK, 2)

    # Middle and bottom rows, driven by one story table.
    rows = [
        (24, 444, 472, "WEATHER  -  BAY OF BENGAL",
         ("CYCLONE AKVAN", "BEARS DOWN"),
         "SEVERE STORM OFF INDIA'S EAST COAST. RED WARNING, "
         "SCHOOLS SHUT, 299,000 EVACUATED IN ODISHA. "
         "LANDFALL DUE FRI NEAR GOPALPUR, GUSTS TO 90 KM/H.",
         storm),
        (528, 444, 472, "BUSINESS  -  AI",
         ("ANTHROPIC DEBUTS", "ON NASDAQ"),
         "THE AI MAKER PRICED ITS IPO AT $83, RAISING "
         "$81.3BN, THE BIGGEST EVER. OPENED $111.50, "
         "CLOSED $97.17, UP 17% ON DAY ONE.",
         shares),
        (24, 704, 472, "CULTURE  -  GAMES",
         ("GTA 6 HITS", "CONSOLES"),
         "LAUNCHED AT MIDNIGHT ON PS5 AND XBOX. REVIEWS: "
         "99/100. STREAMS PEAKED AT 7.9M VIEWERS.",
         vice),
        (528, 704, 472, "SCIENCE  -  SPACE",
         ("VOYAGER 1, ONE", "LIGHT-DAY OUT"),
         "NASA'S 1977 PROBE IS THE FIRST HUMAN-MADE OBJECT "
         "ONE LIGHT-DAY OUT. NASA CONFIRMED IT THU MORNING.",
         probe),
    ]
    for (sx, sy, sw, tag, heads, body, paint) in rows:
        card(b, sx, sy, sw, tag, heads, body, paint)

    # Divider.
    hbar(b, 24, 690, W - 48, INK, 2)

    # Footer ticker.
    box(b, 4, 948, W - 8, 72, INK)
    tape = ("JEFFRIES NOMINATED 251-11 TO BE FIRST BLACK US "
            "SPEAKER  |  GAZA TANK RAID ENDED THU  |  "
            "US STOCKS FELL THU, DOW -2.2%, S&P -2.0%, 6TH DAY DOWN")
    yy = 958
    for line in wrap(tape, 2, W - 48):
        paint_text(b, 24, yy, line, 2, FROST)
        yy += 18
    paint_text(b, 24, yy + 2, "ALL EVENTS OF THURSDAY 19 NOVEMBER 2026",
               2, HONEY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    size = save(b, path)
    print("wrote %s (%d bytes)" % (path, size))


def save(b, path):
    """Encode the sheet as a PNG file and return its byte size."""
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += b[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    parts = [(b"IHDR", ihdr),
             (b"IDAT", zlib.compress(bytes(raw), 9)),
             (b"IEND", b"")]
    blob = b"\x89PNG\r\n\x1a\n"
    for tag, data in parts:
        blob += _block(tag, data)
    with open(path, "wb") as f:
        f.write(blob)
    return len(blob)


def _block(tag, data):
    n = len(data)
    return (struct.pack(">I", n) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


if __name__ == "__main__":
    build()

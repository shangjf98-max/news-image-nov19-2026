#!/usr/bin/env python3
"""A one-day newspaper picture for Thursday 19 November 2026.

Everything is painted by this file alone: a built-in 5x7 dot font,
a hand-rolled PNG writer, and vector-style scene panels. It uses
only the Python standard library, touches no network and reads no
external files. Running it twice gives the same bytes every time.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

SHEET = (247, 243, 232)
SOOT = (22, 24, 30)
DEEP = (20, 33, 61)
DEEP2 = (30, 48, 84)
CRIMSON = (176, 32, 32)
AMBER = (201, 149, 44)
ASH = (112, 116, 122)
PALE = (214, 209, 196)
SNOW = (250, 250, 246)
PALE_BLUE = (166, 199, 224)
OCEAN = (46, 94, 124)
JADITE = (36, 122, 110)
DUNE = (226, 205, 158)
MIDNIGHT = (16, 24, 48)
LEAF = (46, 125, 72)
ROYAL = (43, 88, 168)
UNION = (28, 58, 140)
EMBER = (214, 110, 44)
GRAPE = (92, 58, 140)

# ----------------------------------------------------------------- font --
# 5x7 dot glyphs, drawn for this picture. Each row is five bits, 1 for
# a filled dot and 0 for an empty one. Text is drawn in capitals;
# lowercase input is upper-cased before it is painted.

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "00100", "00100", "00100"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "/": ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "10101", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "&": ("01100", "10010", "10010", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "<": ("00001", "00010", "00100", "01000", "00100", "00010", "00001"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
}


def measure(text, scale):
    """Pixel width of text drawn at the given scale (1px gap per char)."""
    if not text:
        return 0
    return len(text) * (5 * scale + scale) - scale


def fold(text, scale, max_w):
    """Greedy word wrap. Returns a list of lines, all upper-cased."""
    words = text.upper().split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if measure(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------- sheet ----

class Sheet:
    """A plain RGB pixel buffer with tiny vector drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def dot(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(rgb)

    def fill(self, x, y, w, h, rgb):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(rgb) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + len(row)] = row

    def hrow(self, x, y, length, rgb, thick=1):
        self.fill(x, y, length, thick, rgb)

    def vcol(self, x, y, length, rgb, thick=1):
        self.fill(x, y, thick, length, rgb)

    def frame(self, x, y, w, h, rgb, thick=1):
        self.fill(x, y, w, thick, rgb)
        self.fill(x, y + h - thick, w, thick, rgb)
        self.fill(x, y, thick, h, rgb)
        self.fill(x + w - thick, y, thick, h, rgb)

    def seg(self, x0, y0, x1, y1, rgb, thick=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        half = thick // 2
        while True:
            for ox in range(-half, half + 1):
                for oy in range(-half, half + 1):
                    self.dot(x0 + ox, y0 + oy, rgb)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, rgb):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.hrow(cx - dx, cy + dy, 2 * dx + 1, rgb)

    def hoop(self, cx, cy, r, rgb, thick=2):
        for a in range(0, 360):
            rad = math.radians(a)
            for t in range(thick):
                self.dot(cx + int((r + t) * math.cos(rad)),
                         cy + int((r + t) * math.sin(rad)), rgb)

    def bend(self, cx, cy, r, a0, a1, rgb, thick=2):
        for a in range(a0, a1 + 1):
            rad = math.radians(a)
            for t in range(thick):
                self.dot(cx + int((r + t) * math.cos(rad)),
                         cy + int((r + t) * math.sin(rad)), rgb)

    def shape(self, pts, rgb):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.hrow(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), rgb)

    def spark(self, cx, cy, r, rgb):
        self.seg(cx - r, cy, cx + r, cy, rgb, 2)
        self.seg(cx, cy - r, cx, cy + r, rgb, 2)
        self.seg(cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2, rgb, 1)
        self.seg(cx - r // 2, cy + r // 2, cx + r // 2, cy - r // 2, rgb, 1)

    def draw(self, x, y, s, scale, rgb):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = GLYPHS.get(ch, GLYPHS[" "])
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.fill(cx + col * scale, y + row * scale,
                                  scale, scale, rgb)
            cx += 6 * scale
        return cx - x

    def middle(self, cx, y, s, scale, rgb):
        self.draw(cx - measure(s.upper(), scale) // 2, y, s, scale, rgb)


# ------------------------------------------------------------------ png ----

def _block(kind, data):
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def save_png(path, sheet):
    raw = bytearray()
    row_bytes = sheet.w * 3
    for y in range(sheet.h):
        raw.append(0)
        raw += sheet.buf[y * row_bytes:(y + 1) * row_bytes]
    ihdr = struct.pack(">IIBBBBB", sheet.w, sheet.h, 8, 2, 0, 0, 0)
    blob = (b"\x89PNG\r\n\x1a\n" + _block(b"IHDR", ihdr) +
            _block(b"IDAT", zlib.compress(bytes(raw), 9)) + _block(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(blob)
    return len(blob)


# ------------------------------------------------------------ pictures ----

def paint_summit(s, x, y, w, h):
    """Shenzhen skyline with three flags: US, China, Russia."""
    s.fill(x, y, w, h, PALE_BLUE)
    s.fill(x, y + h - 30, w, 30, DEEP2)
    for bx, bw, bh in ((8, 46, 52), (60, 34, 68), (100, 52, 44),
                       (280, 40, 58), (326, 52, 40)):
        s.fill(x + bx, y + h - 30 - bh, bw, bh, DEEP)
    s.seg(x + 77, y + h - 98, x + 77, y + h - 116, DEEP, 3)
    s.disc(x + 77, y + h - 118, 3, CRIMSON)

    def mast(px):
        s.vcol(x + px, y + 8, h - 38, SNOW, 3)

    def us_flag(fx, fy):
        for i in range(7):
            s.fill(x + fx, y + fy + i * 5, 58, 5,
                   CRIMSON if i % 2 == 0 else SNOW)
        s.fill(x + fx, y + fy, 26, 20, DEEP)
        for dy in range(3):
            for dx in range(3):
                s.dot(x + fx + 4 + dx * 8, y + fy + 4 + dy * 6, SNOW)

    def cn_flag(fx, fy):
        s.fill(x + fx, y + fy, 58, 35, CRIMSON)
        s.spark(x + fx + 12, y + fy + 12, 6, AMBER)
        for sx, sy in ((30, 6), (38, 12), (38, 20), (30, 26)):
            s.spark(x + fx + sx, y + fy + sy, 3, AMBER)

    def ru_flag(fx, fy):
        s.fill(x + fx, y + fy, 58, 12, SNOW)
        s.fill(x + fx, y + fy + 12, 58, 11, ROYAL)
        s.fill(x + fx, y + fy + 23, 58, 12, CRIMSON)

    mast(150)
    us_flag(154, 10)
    mast(232)
    cn_flag(236, 10)
    mast(314)
    ru_flag(318, 10)
    s.draw(x + 12, y + h - 24, "SHENZHEN", 2, SNOW)
    s.draw(x + 250, y + h - 24, "KYLIN VILLA", 2, AMBER)


def paint_storm(s, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal with the Indian coast."""
    s.fill(x, y, w, h, OCEAN)
    s.shape([(x, y), (x + 74, y), (x + 58, y + 30), (x + 84, y + 58),
             (x + 66, y + h), (x, y + h)], DUNE)
    s.draw(x + 4, y + 6, "INDIA", 2, SOOT)
    cx, cy = x + w // 2 + 30, y + h // 2
    for spoke in range(3):
        shift = spoke * 120
        for step in range(0, 300):
            ang = math.radians(shift + step)
            r = 8 + step * 0.22
            px = cx + int(r * math.cos(ang))
            py = cy + int(r * math.sin(ang) * 0.82)
            s.disc(px, py, 3, SNOW)
    s.disc(cx, cy, 11, AMBER)
    s.hoop(cx, cy, 14, SNOW, 2)
    for rx in range(x + w - 90, x + w - 8, 18):
        s.seg(rx, y + 10, rx - 8, y + 26, PALE_BLUE, 2)
    s.draw(x + w - 118, y + h - 40, "GUSTS 90", 2, SNOW)
    s.draw(x + w - 118, y + h - 22, "KM/H", 2, SNOW)


def paint_shares(s, x, y, w, h):
    """A rising share-price bar for the record IPO debut."""
    s.fill(x, y, w, h, SNOW)
    s.frame(x, y, w, h, PALE, 1)
    s.draw(x + 12, y + 6, "ANT  -  NASDAQ", 2, DEEP)
    s.draw(x + 12, y + 24, "CLOSE $97.17", 2, SOOT)
    ax0, ay0 = x + 34, y + h - 8
    s.seg(ax0, y + 44, ax0, ay0, ASH, 2)
    s.seg(ax0, ay0, x + w - 12, ay0, ASH, 2)
    heights = [12, 18, 24, 30, 38]
    for i, bh in enumerate(heights):
        bx = ax0 + 22 + i * 62
        s.fill(bx, ay0 - bh, 34, bh, JADITE if i < 4 else LEAF)
    peaks = [(ax0 + 30, ay0 - 16), (ax0 + 92, ay0 - 22), (ax0 + 154, ay0 - 28),
             (ax0 + 216, ay0 - 34), (ax0 + 286, ay0 - 42)]
    for i in range(len(peaks) - 1):
        s.seg(peaks[i][0], peaks[i][1], peaks[i + 1][0], peaks[i + 1][1], LEAF, 3)
    s.shape([(peaks[-1][0], peaks[-1][1] - 12), (peaks[-1][0] - 10, peaks[-1][1] + 2),
             (peaks[-1][0] + 10, peaks[-1][1] + 2)], LEAF)


def paint_vice(s, x, y, w, h):
    """Vice City sunset: sun, palms, skyline and a car."""
    s.fill(x, y, w, h, EMBER)
    s.disc(x + w // 2, y + 42, 26, AMBER)
    s.fill(x, y + h - 34, w, 34, GRAPE)
    for bx, bw, bh in ((10, 40, 30), (56, 28, 44), (320, 44, 34),
                       (372, 30, 48)):
        s.fill(x + bx, y + h - 34 - bh, bw, bh, DEEP)
    # Palm trees.
    for tx, ty in ((150, h - 34), (260, h - 34)):
        s.seg(x + tx, y + ty, x + tx + 6, y + ty - 34, SOOT, 3)
        for dx, dy in ((-18, -8), (-10, -14), (0, -16), (12, -12), (20, -6)):
            s.seg(x + tx + 6, y + ty - 34, x + tx + 6 + dx, y + ty - 34 + dy, SOOT, 2)
    # A low car silhouette.
    s.fill(x + 170, y + h - 22, 120, 10, SOOT)
    s.shape([(x + 195, y + h - 22), (x + 210, y + h - 34),
             (x + 250, y + h - 34), (x + 265, y + h - 22)], SOOT)
    s.disc(x + 195, y + h - 10, 6, SOOT)
    s.disc(x + 265, y + h - 10, 6, SOOT)
    s.draw(x + 12, y + 8, "VICE CITY", 2, SNOW)
    s.draw(x + w - 60, y + 8, "VI", 3, SNOW)


def paint_probe(s, x, y, w, h):
    """Voyager 1 in deep space: dish, golden record, one light-day."""
    s.fill(x, y, w, h, MIDNIGHT)
    for sx, sy in ((18, 12), (52, 26), (96, 8), (150, 20), (205, 10),
                   (260, 24), (318, 14), (360, 30), (30, 44), (235, 40),
                   (400, 12), (430, 44)):
        s.dot(x + sx, y + sy, SNOW)
        s.dot(x + sx + 1, y + sy, SNOW)
    # Sun, far behind.
    s.disc(x + 40, y + h - 30, 16, AMBER)
    # Probe body, dish and golden record disc.
    qx, qy = x + w // 2 + 20, y + h // 2 - 6
    s.fill(qx - 34, qy - 8, 68, 16, SNOW)
    s.seg(qx - 34, qy, qx - 62, qy - 22, SNOW, 3)
    s.seg(qx - 34, qy, qx - 62, qy + 22, SNOW, 3)
    s.seg(qx - 62, qy - 22, qx - 62, qy + 22, SNOW, 3)
    s.disc(qx + 48, qy, 14, AMBER)
    s.hoop(qx + 48, qy, 14, SNOW, 1)
    s.seg(qx + 34, qy - 4, qx + 62, qy - 14, JADITE, 2)
    s.seg(qx + 34, qy + 4, qx + 62, qy + 14, JADITE, 2)
    # Signal path back to Earth, dotted.
    for i in range(0, 120, 8):
        s.dot(x + 60 + i, y + h - 30 - i // 3, AMBER)
    s.draw(x + 12, y + 8, "1 LIGHT-DAY", 2, AMBER)
    s.draw(x + w - 150, y + h - 22, "26BN KM", 2, SNOW)


# -------------------------------------------------------------- layout ----

def card(s, x, y, w, h, tag, heads, body, paint):
    paint(s, x, y, w, 86)
    s.draw(x, y + 96, tag, 2, CRIMSON)
    yy = y + 118
    for line in heads:
        s.draw(x, yy, line, 3, SOOT)
        yy += 28
    for line in fold(body, 2, w):
        s.draw(x, yy, line, 2, SOOT)
        yy += 18


def build():
    s = Sheet(W, H, SHEET)
    s.frame(0, 0, W, H, SOOT, 4)

    # Masthead.
    s.fill(4, 4, W - 8, 124, DEEP)
    s.draw(24, 22, "WORLD NEWS", 2, AMBER)
    s.draw(W - 24 - measure("DRAWN IN CODE", 2), 22, "DRAWN IN CODE", 2, AMBER)
    s.middle(W // 2, 20, "THE WORLD TODAY", 5, SNOW)
    s.middle(W // 2, 70, "THURSDAY, 19 NOVEMBER 2026", 3, SNOW)
    s.hrow(24, 106, W - 48, AMBER, 2)
    s.middle(W // 2, 112, "ONE DAY  -  ONE IMAGE", 2, PALE)
    s.fill(4, 128, W - 8, 5, CRIMSON)

    # Lead story: Trump-Xi-Putin trilateral.
    gx, gy, gw = 24, 146, 560
    hx, hw = 608, 392
    s.draw(gx, gy, "DIPLOMACY  -  LEAD STORY", 2, CRIMSON)
    s.draw(gx, gy + 24, "THREE LEADERS", 4, SOOT)
    s.draw(gx, gy + 56, "4-POINT DECLARATION", 4, SOOT)
    lead = ("THE FIRST-EVER TRUMP-XI-PUTIN SUMMIT ENDED WITH A "
            "4-POINT DECLARATION: UN REFORM, MORE REFINED OIL, "
            "ICC LIMITS AND NUCLEAR-RISK TALKS. NO DEAL ON "
            "UKRAINE, IRAN OR ARMS LIMITS.")
    yy = gy + 96
    for line in fold(lead, 2, gw):
        s.draw(gx, yy, line, 2, SOOT)
        yy += 18
    s.draw(gx, yy + 8, "TALKS RAN 4:16-6:01 PM, NEARLY 2 HRS LATE.", 2, ASH)
    s.draw(gx, yy + 26, "REPORTS SAY TRUMP-XI EXTENDED TRADE TRUCE.", 2, ASH)
    paint_summit(s, hx, gy, hw, 270)
    s.frame(hx, gy, hw, 270, SOOT, 2)

    # Divider.
    s.hrow(24, 430, W - 48, SOOT, 2)

    # Middle row: cyclone + Anthropic IPO.
    card(s, 24, 444, 472, 232,
         "WEATHER  -  BAY OF BENGAL",
         ["CYCLONE AKVAN", "BEARS DOWN"],
         ("SEVERE STORM OFF INDIA'S EAST COAST. RED WARNING, "
          "SCHOOLS SHUT, 299,000 EVACUATED IN ODISHA. "
          "LANDFALL DUE FRI NEAR GOPALPUR, GUSTS TO 90 KM/H."),
         paint_storm)
    card(s, 528, 444, 472, 232,
         "BUSINESS  -  AI",
         ["ANTHROPIC DEBUTS", "ON NASDAQ"],
         ("THE AI MAKER PRICED ITS IPO AT $83, RAISING "
          "$81.3BN, THE BIGGEST EVER. OPENED $111.50, "
          "CLOSED $97.17, UP 17% ON DAY ONE."),
         paint_shares)

    # Divider.
    s.hrow(24, 690, W - 48, SOOT, 2)

    # Bottom row: GTA 6 + Voyager 1.
    card(s, 24, 704, 472, 232,
         "CULTURE  -  GAMES",
         ["GTA 6 HITS", "CONSOLES"],
         ("LAUNCHED AT MIDNIGHT ON PS5 AND XBOX. REVIEWS: "
          "99/100. STREAMS PEAKED AT 7.9M VIEWERS."),
         paint_vice)
    card(s, 528, 704, 472, 232,
         "SCIENCE  -  SPACE",
         ["VOYAGER 1, ONE", "LIGHT-DAY OUT"],
         ("NASA'S 1977 PROBE IS THE FIRST HUMAN-MADE OBJECT "
          "ONE LIGHT-DAY OUT. NASA CONFIRMED IT THU MORNING."),
         paint_probe)

    # Footer ticker.
    s.fill(4, 948, W - 8, 72, SOOT)
    tape = ("JEFFRIES NOMINATED 251-11 TO BE FIRST BLACK US "
            "SPEAKER  |  GAZA TANK RAID ENDED THU  |  "
            "US STOCKS FELL THU, DOW -2.2%, S&P -2.0%, 6TH DAY DOWN")
    yy = 958
    for line in fold(tape, 2, W - 48):
        s.draw(24, yy, line, 2, SNOW)
        yy += 18
    s.draw(24, yy + 2, "ALL EVENTS OF THURSDAY 19 NOVEMBER 2026",
           2, AMBER)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    size = save_png(path, s)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    build()

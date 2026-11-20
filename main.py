#!/usr/bin/env python3
"""One-day newspaper image for Thursday 19 November 2026.

Draws a 1024x1024 PNG entirely in code: a built-in 5x7 bitmap font,
a hand-written PNG encoder, and vector-style picture panels. Standard
library only, no network, no external files. Deterministic: the same
bytes on every run.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (22, 24, 30)
NAVY = (20, 33, 61)
NAVY2 = (30, 48, 84)
RED = (176, 32, 32)
GOLD = (201, 149, 44)
GREY = (112, 116, 122)
LGREY = (214, 209, 196)
WHITE = (250, 250, 246)
SKY = (166, 199, 224)
SEA = (46, 94, 124)
TEAL = (36, 122, 110)
SAND = (226, 205, 158)
NIGHT = (16, 24, 48)
GREEN = (46, 125, 72)
BLUE = (43, 88, 168)
EU_BLUE = (28, 58, 140)
ORANGE = (214, 110, 44)
PURPLE = (92, 58, 140)

# ---------------------------------------------------------------- font ----
# 5x7 bitmap glyphs, written for this program. Text is rendered in
# capitals; lowercase input is upper-cased before drawing.

FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", "..#..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.#.#", "#..##"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "<": ("....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"),
    ">": ("#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."),
}


def text_width(text, scale):
    """Pixel width of text drawn at the given scale (1px gap per char)."""
    if not text:
        return 0
    return len(text) * (5 * scale + scale) - scale


def wrap_text(text, scale, max_w):
    """Greedy word wrap. Returns a list of lines, all upper-cased."""
    words = text.upper().split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------- canvas ----

class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + len(row)] = row

    def hline(self, x, y, length, color, thick=1):
        self.rect(x, y, length, thick, color)

    def vline(self, x, y, length, color, thick=1):
        self.rect(x, y, thick, length, color)

    def border(self, x, y, w, h, color, thick=1):
        self.rect(x, y, w, thick, color)
        self.rect(x, y + h - thick, w, thick, color)
        self.rect(x, y, thick, h, color)
        self.rect(x + w - thick, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        half = thick // 2
        while True:
            for ox in range(-half, half + 1):
                for oy in range(-half, half + 1):
                    self.px(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.hline(cx - dx, cy + dy, 2 * dx + 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        for a in range(0, 360):
            rad = math.radians(a)
            for t in range(thick):
                self.px(cx + int((r + t) * math.cos(rad)),
                        cy + int((r + t) * math.sin(rad)), color)

    def arc(self, cx, cy, r, a0, a1, color, thick=2):
        for a in range(a0, a1 + 1):
            rad = math.radians(a)
            for t in range(thick):
                self.px(cx + int((r + t) * math.cos(rad)),
                        cy + int((r + t) * math.sin(rad)), color)

    def poly(self, pts, color):
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
                self.hline(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), color)

    def star(self, cx, cy, r, color):
        self.line(cx - r, cy, cx + r, cy, color, 2)
        self.line(cx, cy - r, cx, cy + r, color, 2)
        self.line(cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2, color, 1)
        self.line(cx - r // 2, cy + r // 2, cx + r // 2, cy - r // 2, color, 1)

    def text(self, x, y, s, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx - x

    def centered(self, cx, y, s, scale, color):
        self.text(cx - text_width(s.upper(), scale) // 2, y, s, scale, color)


# ----------------------------------------------------------------- PNG ----

def _chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def write_png(path, canvas):
    raw = bytearray()
    row_bytes = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.buf[y * row_bytes:(y + 1) * row_bytes]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    blob = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) +
            _chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(blob)
    return len(blob)


# ------------------------------------------------------------ pictures ----

def draw_trilateral(c, x, y, w, h):
    """Shenzhen skyline with three flags: US, China, Russia."""
    c.rect(x, y, w, h, SKY)
    c.rect(x, y + h - 30, w, 30, NAVY2)
    for bx, bw, bh in ((8, 46, 52), (60, 34, 68), (100, 52, 44),
                       (280, 40, 58), (326, 52, 40)):
        c.rect(x + bx, y + h - 30 - bh, bw, bh, NAVY)
    c.line(x + 77, y + h - 98, x + 77, y + h - 116, NAVY, 3)
    c.circle(x + 77, y + h - 118, 3, RED)

    def pole(px):
        c.vline(x + px, y + 8, h - 38, WHITE, 3)

    def flag_us(fx, fy):
        for i in range(7):
            c.rect(x + fx, y + fy + i * 5, 58, 5,
                   RED if i % 2 == 0 else WHITE)
        c.rect(x + fx, y + fy, 26, 20, NAVY)
        for dy in range(3):
            for dx in range(3):
                c.px(x + fx + 4 + dx * 8, y + fy + 4 + dy * 6, WHITE)

    def flag_cn(fx, fy):
        c.rect(x + fx, y + fy, 58, 35, RED)
        c.star(x + fx + 12, y + fy + 12, 6, GOLD)
        for sx, sy in ((30, 6), (38, 12), (38, 20), (30, 26)):
            c.star(x + fx + sx, y + fy + sy, 3, GOLD)

    def flag_ru(fx, fy):
        c.rect(x + fx, y + fy, 58, 12, WHITE)
        c.rect(x + fx, y + fy + 12, 58, 11, BLUE)
        c.rect(x + fx, y + fy + 23, 58, 12, RED)

    pole(150)
    flag_us(154, 10)
    pole(232)
    flag_cn(236, 10)
    pole(314)
    flag_ru(318, 10)
    c.text(x + 12, y + h - 24, "SHENZHEN", 2, WHITE)
    c.text(x + 250, y + h - 24, "KYLIN VILLA", 2, GOLD)


def draw_cyclone(c, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal with the Indian coast."""
    c.rect(x, y, w, h, SEA)
    c.poly([(x, y), (x + 74, y), (x + 58, y + 30), (x + 84, y + 58),
            (x + 66, y + h), (x, y + h)], SAND)
    c.text(x + 4, y + 6, "INDIA", 2, INK)
    cx, cy = x + w // 2 + 30, y + h // 2
    for arm in range(3):
        off = arm * 120
        for t in range(0, 300):
            ang = math.radians(off + t)
            r = 8 + t * 0.22
            px = cx + int(r * math.cos(ang))
            py = cy + int(r * math.sin(ang) * 0.82)
            c.circle(px, py, 3, WHITE)
    c.circle(cx, cy, 11, GOLD)
    c.ring(cx, cy, 14, WHITE, 2)
    for rx in range(x + w - 90, x + w - 8, 18):
        c.line(rx, y + 10, rx - 8, y + 26, SKY, 2)
    c.text(x + w - 118, y + h - 40, "GUSTS 90", 2, WHITE)
    c.text(x + w - 118, y + h - 22, "KM/H", 2, WHITE)


def draw_ipo(c, x, y, w, h):
    """A rising share-price bar for the record IPO debut."""
    c.rect(x, y, w, h, WHITE)
    c.border(x, y, w, h, LGREY, 1)
    c.text(x + 12, y + 6, "ANT  -  NASDAQ", 2, NAVY)
    c.text(x + 12, y + 24, "CLOSE $97.17", 2, INK)
    ox, oy = x + 34, y + h - 8
    c.line(ox, y + 44, ox, oy, GREY, 2)
    c.line(ox, oy, x + w - 12, oy, GREY, 2)
    bars = [12, 18, 24, 30, 38]
    for i, bh in enumerate(bars):
        bx = ox + 22 + i * 62
        c.rect(bx, oy - bh, 34, bh, TEAL if i < 4 else GREEN)
    pts = [(ox + 30, oy - 16), (ox + 92, oy - 22), (ox + 154, oy - 28),
           (ox + 216, oy - 34), (ox + 286, oy - 42)]
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], GREEN, 3)
    c.poly([(pts[-1][0], pts[-1][1] - 12), (pts[-1][0] - 10, pts[-1][1] + 2),
            (pts[-1][0] + 10, pts[-1][1] + 2)], GREEN)


def draw_gta(c, x, y, w, h):
    """Vice City sunset: sun, palms, skyline and a car."""
    c.rect(x, y, w, h, ORANGE)
    c.circle(x + w // 2, y + 42, 26, GOLD)
    c.rect(x, y + h - 34, w, 34, PURPLE)
    for bx, bw, bh in ((10, 40, 30), (56, 28, 44), (320, 44, 34),
                       (372, 30, 48)):
        c.rect(x + bx, y + h - 34 - bh, bw, bh, NAVY)
    # Palm trees.
    for px, py in ((150, h - 34), (260, h - 34)):
        c.line(x + px, y + py, x + px + 6, y + py - 34, INK, 3)
        for dx, dy in ((-18, -8), (-10, -14), (0, -16), (12, -12), (20, -6)):
            c.line(x + px + 6, y + py - 34, x + px + 6 + dx, y + py - 34 + dy, INK, 2)
    # A low car silhouette.
    c.rect(x + 170, y + h - 22, 120, 10, INK)
    c.poly([(x + 195, y + h - 22), (x + 210, y + h - 34),
            (x + 250, y + h - 34), (x + 265, y + h - 22)], INK)
    c.circle(x + 195, y + h - 10, 6, INK)
    c.circle(x + 265, y + h - 10, 6, INK)
    c.text(x + 12, y + 8, "VICE CITY", 2, WHITE)
    c.text(x + w - 60, y + 8, "VI", 3, WHITE)


def draw_voyager(c, x, y, w, h):
    """Voyager 1 in deep space: dish, golden record, one light-day."""
    c.rect(x, y, w, h, NIGHT)
    for sx, sy in ((18, 12), (52, 26), (96, 8), (150, 20), (205, 10),
                   (260, 24), (318, 14), (360, 30), (30, 44), (235, 40),
                   (400, 12), (430, 44)):
        c.px(x + sx, y + sy, WHITE)
        c.px(x + sx + 1, y + sy, WHITE)
    # Sun, far behind.
    c.circle(x + 40, y + h - 30, 16, GOLD)
    # Probe body, dish and golden record disc.
    cx, cy = x + w // 2 + 20, y + h // 2 - 6
    c.rect(cx - 34, cy - 8, 68, 16, WHITE)
    c.line(cx - 34, cy, cx - 62, cy - 22, WHITE, 3)
    c.line(cx - 34, cy, cx - 62, cy + 22, WHITE, 3)
    c.line(cx - 62, cy - 22, cx - 62, cy + 22, WHITE, 3)
    c.circle(cx + 48, cy, 14, GOLD)
    c.ring(cx + 48, cy, 14, WHITE, 1)
    c.line(cx + 34, cy - 4, cx + 62, cy - 14, TEAL, 2)
    c.line(cx + 34, cy + 4, cx + 62, cy + 14, TEAL, 2)
    # Signal path back to Earth, dotted.
    for i in range(0, 120, 8):
        c.px(x + 60 + i, y + h - 30 - i // 3, GOLD)
    c.text(x + 12, y + 8, "1 LIGHT-DAY", 2, GOLD)
    c.text(x + w - 150, y + h - 22, "26BN KM", 2, WHITE)


# -------------------------------------------------------------- layout ----

def story_block(c, x, y, w, h, kicker, headlines, deck, art):
    art(c, x, y, w, 86)
    c.text(x, y + 96, kicker, 2, RED)
    ty = y + 118
    for line in headlines:
        c.text(x, ty, line, 3, INK)
        ty += 28
    for line in wrap_text(deck, 2, w):
        c.text(x, ty, line, 2, INK)
        ty += 18


def main():
    c = Canvas(W, H, PAPER)
    c.border(0, 0, W, H, INK, 4)

    # Masthead.
    c.rect(4, 4, W - 8, 124, NAVY)
    c.text(24, 22, "WORLD NEWS", 2, GOLD)
    c.text(W - 24 - text_width("DRAWN IN CODE", 2), 22, "DRAWN IN CODE", 2, GOLD)
    c.centered(W // 2, 20, "THE WORLD TODAY", 5, WHITE)
    c.centered(W // 2, 70, "THURSDAY, 19 NOVEMBER 2026", 3, WHITE)
    c.hline(24, 106, W - 48, GOLD, 2)
    c.centered(W // 2, 112, "ONE DAY  -  ONE IMAGE", 2, LGREY)
    c.rect(4, 128, W - 8, 5, RED)

    # Lead story: Trump-Xi-Putin trilateral.
    lx, ly, lw = 24, 146, 560
    ax, aw = 608, 392
    c.text(lx, ly, "DIPLOMACY  -  LEAD STORY", 2, RED)
    c.text(lx, ly + 24, "THREE LEADERS", 4, INK)
    c.text(lx, ly + 56, "4-POINT DECLARATION", 4, INK)
    lead_deck = ("THE FIRST-EVER TRUMP-XI-PUTIN SUMMIT ENDED WITH A "
                 "4-POINT DECLARATION: UN REFORM, MORE REFINED OIL, "
                 "ICC LIMITS AND NUCLEAR-RISK TALKS. NO DEAL ON "
                 "UKRAINE, IRAN OR ARMS LIMITS.")
    ty = ly + 96
    for line in wrap_text(lead_deck, 2, lw):
        c.text(lx, ty, line, 2, INK)
        ty += 18
    c.text(lx, ty + 8, "TALKS RAN 4:16-6:01 PM, NEARLY 2 HRS LATE.", 2, GREY)
    c.text(lx, ty + 26, "REPORTS SAY TRUMP-XI EXTENDED TRADE TRUCE.", 2, GREY)
    draw_trilateral(c, ax, ly, aw, 270)
    c.border(ax, ly, aw, 270, INK, 2)

    # Divider.
    c.hline(24, 430, W - 48, INK, 2)

    # Middle row: cyclone + Anthropic IPO.
    story_block(c, 24, 444, 472, 232,
                "WEATHER  -  BAY OF BENGAL",
                ["CYCLONE AKVAN", "BEARS DOWN"],
                ("SEVERE STORM OFF INDIA'S EAST COAST. RED WARNING, "
                 "SCHOOLS SHUT, 299,000 EVACUATED IN ODISHA. "
                 "LANDFALL DUE FRI NEAR GOPALPUR, GUSTS TO 90 KM/H."),
                draw_cyclone)
    story_block(c, 528, 444, 472, 232,
                "BUSINESS  -  AI",
                ["ANTHROPIC DEBUTS", "ON NASDAQ"],
                ("THE AI MAKER PRICED ITS IPO AT $83, RAISING "
                 "$81.3BN, THE BIGGEST EVER. OPENED $111.50, "
                 "CLOSED $97.17, UP 17% ON DAY ONE."),
                draw_ipo)

    # Divider.
    c.hline(24, 690, W - 48, INK, 2)

    # Bottom row: GTA 6 + Voyager 1.
    story_block(c, 24, 704, 472, 232,
                "CULTURE  -  GAMES",
                ["GTA 6 HITS", "CONSOLES"],
                ("LAUNCHED AT MIDNIGHT ON PS5 AND XBOX. REVIEWS: "
                 "99/100. STREAMS PEAKED AT 7.9M VIEWERS."),
                draw_gta)
    story_block(c, 528, 704, 472, 232,
                "SCIENCE  -  SPACE",
                ["VOYAGER 1, ONE", "LIGHT-DAY OUT"],
                ("NASA'S 1977 PROBE IS THE FIRST HUMAN-MADE OBJECT "
                 "ONE LIGHT-DAY OUT. NASA CONFIRMED IT THU MORNING."),
                draw_voyager)

    # Footer ticker.
    c.rect(4, 948, W - 8, 72, INK)
    ticker = ("JEFFRIES NOMINATED 251-11 TO BE FIRST BLACK US "
              "SPEAKER  |  GAZA TANK RAID ENDED THU  |  "
              "US STOCKS FELL THU, DOW -2.2%, S&P -2.0%, 6TH DAY DOWN")
    ty = 958
    for line in wrap_text(ticker, 2, W - 48):
        c.text(24, ty, line, 2, WHITE)
        ty += 18
    c.text(24, ty + 2, "ALL EVENTS OF THURSDAY 19 NOVEMBER 2026",
           2, GOLD)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    size = write_png(path, c)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""THE WORLD IN ONE IMAGE -- Wednesday 18 November 2026.

Draws a 1024x1024 newspaper front-page infographic summarising the
day's top world news, using only the Python standard library.

No network, no external files, no randomness, no timestamps:
running the program twice produces byte-identical PNG output.

Usage:
    python3 main.py
    # writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output)
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
WHITE = (255, 255, 255)
NAVY = (20, 33, 61)
NAVY_LIGHT = (38, 55, 92)
RED = (178, 34, 34)
RED_DARK = (140, 22, 22)
INK = (24, 24, 24)
GREY = (96, 96, 96)
LIGHT_GREY = (228, 222, 208)
GOLD = (201, 162, 39)

# ------------------------------------------------------------------- font
# Hand-written 5x7 bitmap glyphs. '#' = ink, '.' = blank.
# Uppercase A-Z, digits 0-9 and punctuation . , ' : ; ! ? - / ( ) & % $ + =
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, length, t, color)

    def vline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, t, length, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        half = t // 2
        while True:
            self.fill_rect(x - half, y - half, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def fill_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def circle(self, cx, cy, r, color, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if abs(d - r) <= t / 2.0:
                    self.set(xx, yy, color)

    def fill_triangle(self, p0, p1, p2, color):
        xs = [p0[0], p1[0], p2[0]]
        ys = [p0[1], p1[1], p2[1]]
        for yy in range(min(ys), max(ys) + 1):
            row = []
            for (ax, ay), (bx, by) in ((p0, p1), (p1, p2), (p2, p0)):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by):
                    xx = ax + (yy - ay) * (bx - ax) / (by - ay)
                    row.append(xx)
            if len(row) >= 2:
                for xx in range(int(min(row)), int(max(row)) + 1):
                    self.set(xx, yy, color)


# -------------------------------------------------------------------- text
def text_width(text, scale):
    return len(text) * (5 * scale + scale)


def draw_text(c, x, y, text, scale, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    c.fill_rect(cx + col * scale, y + row * scale,
                                scale, scale, color)
        cx += 5 * scale + scale
    return cx


def draw_text_centered(c, y, text, scale, color, cx=W // 2):
    w = text_width(text, scale)
    draw_text(c, cx - w // 2, y, text, scale, color)


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    char_w = 5 * scale + scale
    max_chars = max(1, max_width // char_w)
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # hard-split a single over-long word
                while len(word) > max_chars:
                    lines.append(word[:max_chars])
                    word = word[max_chars:]
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ------------------------------------------------------------------- icons
def icon_plane(c, cx, cy, s):
    # s ~ half-width of the icon box. Navy plane, red tail stripe.
    c.fill_rect(cx - s, cy - 6, 2 * s, 12, NAVY)            # fuselage
    c.fill_triangle((cx + s, cy - 6), (cx + s, cy + 6),
                    (cx + s + 16, cy), NAVY)                 # nose
    c.fill_triangle((cx - s + 6, cy - 6), (cx - s + 22, cy - 6),
                    (cx - s + 6, cy - 26), NAVY)             # tail fin
    c.fill_triangle((cx - 6, cy + 6), (cx + 14, cy + 6),
                    (cx - 2, cy + 30), NAVY)                 # near wing
    c.fill_triangle((cx - 6, cy - 6), (cx + 14, cy - 6),
                    (cx - 2, cy - 30), NAVY_LIGHT)           # far wing
    c.fill_rect(cx - s, cy - 6, 10, 12, RED)                 # tail band
    c.fill_circle(cx + s - 8, cy, 3, WHITE)                  # window dot


def icon_bridge(c, cx, cy, s):
    # Two towers, a deck and suspension cables.
    c.fill_rect(cx - s, cy - 34, 10, 68, NAVY)
    c.fill_rect(cx + s - 10, cy - 34, 10, 68, NAVY)
    c.fill_rect(cx - s - 6, cy + 28, 2 * s + 12, 8, NAVY)    # deck
    c.line(cx - s + 5, cy - 34, cx, cy + 28, RED, 3)         # cable L
    c.line(cx + s - 5, cy - 34, cx, cy + 28, RED, 3)         # cable R
    c.line(cx - s + 5, cy - 34, cx - s + 5, cy + 28, NAVY, 2)
    c.line(cx + s - 5, cy - 34, cx + s - 5, cy + 28, NAVY, 2)
    c.fill_rect(cx - s - 2, cy - 40, 14, 6, RED)             # tower caps
    c.fill_rect(cx + s - 12, cy - 40, 14, 6, RED)
    # blast mark on the deck
    c.fill_circle(cx, cy + 10, 7, GOLD)
    c.fill_circle(cx, cy + 10, 3, RED)


def icon_radar(c, cx, cy, s):
    # Drone over a radar sweep: concentric rings + quad-rotor drone.
    # The drone sits just above the rings so it stays inside its row.
    c.circle(cx, cy, s, NAVY, 3)
    c.circle(cx, cy, s - 11, NAVY, 2)
    c.circle(cx, cy, s - 22, RED, 2)
    c.line(cx, cy, cx + s - 6, cy - s + 10, RED, 3)         # sweep arm
    c.fill_circle(cx, cy, 5, RED)
    # drone body above the rings
    c.fill_rect(cx - 16, cy - 46, 32, 9, NAVY)
    c.fill_circle(cx - 20, cy - 42, 6, NAVY_LIGHT)
    c.fill_circle(cx + 20, cy - 42, 6, NAVY_LIGHT)
    c.fill_rect(cx - 30, cy - 44, 20, 3, NAVY)
    c.fill_rect(cx + 10, cy - 44, 20, 3, NAVY)


def icon_document(c, cx, cy, s):
    # Sanction document with a red seal.
    c.fill_rect(cx - s, cy - 36, 2 * s - 12, 72, WHITE)
    c.rect(cx - s, cy - 36, 2 * s - 12, 72, NAVY, 3)
    c.fill_rect(cx - s + 8, cy - 26, 2 * s - 32, 6, NAVY)
    for i, yy in enumerate((cy - 12, cy, cy + 12)):
        c.fill_rect(cx - s + 8, yy, 2 * s - 32 - i * 8, 4, NAVY_LIGHT)
    c.fill_circle(cx + s - 8, cy + 22, 15, RED)
    c.circle(cx + s - 8, cy + 22, 10, WHITE, 2)
    draw_text(c, cx + s - 13, cy + 17, "X", 1, WHITE)


def icon_chip(c, cx, cy, s):
    # Microchip: square body, inner die, pins on all sides.
    for dx in (-1, 0, 1):
        c.fill_rect(cx + dx * 18 - 3, cy - s - 10, 6, 10, NAVY)
        c.fill_rect(cx + dx * 18 - 3, cy + s, 6, 10, NAVY)
        c.fill_rect(cx - s - 10, cy + dx * 18 - 3, 10, 6, NAVY)
        c.fill_rect(cx + s, cy + dx * 18 - 3, 10, 6, NAVY)
    c.fill_rect(cx - s, cy - s, 2 * s, 2 * s, NAVY)
    c.fill_rect(cx - s + 8, cy - s + 8, 2 * s - 16, 2 * s - 16, NAVY_LIGHT)
    c.fill_rect(cx - 14, cy - 14, 28, 28, RED)
    c.fill_rect(cx - 7, cy - 7, 14, 14, GOLD)
    c.fill_rect(cx - s + 4, cy - s + 4, 10, 4, GOLD)         # pin-1 mark


def icon_cyclone(c, cx, cy, s):
    # Cyclone spiral: expanding arcs around a calm eye.
    for r in range(8, s + 4, 8):
        for deg in range(0, 270, 6):
            import math
            a = math.radians(deg + r * 9)
            xx = int(cx + r * 0.95 * math.cos(a))
            yy = int(cy + r * 0.85 * math.sin(a))
            c.fill_circle(xx, yy, 3, NAVY if r % 16 else RED)
    c.fill_circle(cx, cy, 7, GOLD)
    c.fill_circle(cx, cy, 3, RED)


ICONS = [icon_plane, icon_bridge, icon_radar, icon_document, icon_chip,
         icon_cyclone]

# ------------------------------------------------------------------ stories
STORIES = [
    ("TRUMP LANDS IN MANILA",
     "US PRESIDENT DONALD TRUMP ARRIVES IN THE PHILIPPINES FOR QUAD TALKS "
     "WITH INDIA, JAPAN AND AUSTRALIA, AHEAD OF A CHINA VISIT AND THE APEC "
     "SUMMIT."),
    ("UKRAINE HITS CRIMEAN BRIDGE AGAIN",
     "UKRAINE STRIKES THE CRIMEAN BRIDGE FOR A SECOND STRAIGHT DAY, "
     "DAMAGING ITS ROAD SECTION, AS RUSSIAN STRIKES HIT BRIDGES IN KYIV."),
    ("IRAN DRONES TARGET US RADAR IN BAHRAIN",
     "IRAN FIRES DRONES AT A US MILITARY RADAR SITE IN BAHRAIN; GULF STATES "
     "REPORT INTERCEPTIONS AND AN ALL-CLEAR."),
    ("UK SANCTIONS ISRAELI SETTLEMENT FIRMS",
     "BRITAIN SANCTIONS EIGHT FIRMS OVER ILLEGAL WEST BANK SETTLEMENTS AND "
     "A GROUP BLOCKING AID TO GAZA."),
    ("NVIDIA'S RECORD $115.8BN QUARTER",
     "NVIDIA REPORTS RECORD QUARTERLY REVENUE, UP 103% ON A YEAR AGO, AS IT "
     "PROBES ITS CEO'S ALLEGED LINK TO A CHINESE SPY."),
    ("CYCLONE AKVAN BEARS DOWN ON INDIA",
     "CYCLONE AKVAN STRENGTHENS OVER THE BAY OF BENGAL, PUTTING ANDHRA "
     "PRADESH AND ODISHA ON HIGH ALERT."),
]

ALSO = ("CANADA AND CHINA EXTEND TRADE DEALS AS XI MEETS CARNEY "
        "AHEAD OF APEC  -  MS DHONI RETIRES FROM THE IPL")


# ------------------------------------------------------------------ drawing
def badge(c, cx, cy, r, number, scale=3):
    c.fill_circle(cx, cy, r, RED)
    c.circle(cx, cy, r, RED_DARK, 2)
    txt = str(number)
    w = text_width(txt, scale)
    draw_text(c, cx - w // 2, cy - (7 * scale) // 2, txt, scale, WHITE)


def draw():
    c = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    c.fill_rect(0, 0, W, 188, NAVY)
    c.fill_rect(0, 0, W, 8, RED)
    draw_text_centered(c, 26, "THE WORLD IN ONE IMAGE", 2, WHITE)
    draw_text_centered(c, 58, "WEDNESDAY 18 NOVEMBER 2026", 5, WHITE)
    c.fill_rect(92, 106, W - 184, 4, RED)
    draw_text_centered(c, 126,
                       "THE DAY'S TOP STORIES - FROM AROUND THE GLOBE",
                       2, (200, 210, 225))
    draw_text_centered(c, 154, "SIX STORIES  -  ONE PICTURE  -  ONE DAY",
                       1, GOLD)
    c.fill_rect(0, 188, W, 6, RED)

    # ---- lead story ----------------------------------------------------
    lead_x, lead_y, lead_w, lead_h = 16, 206, 992, 184
    c.fill_rect(lead_x, lead_y, lead_w, lead_h, WHITE)
    c.rect(lead_x, lead_y, lead_w, lead_h, NAVY, 3)
    c.fill_rect(lead_x, lead_y, lead_w, 6, RED)
    badge(c, 56, lead_y + 46, 24, 1, scale=3)
    draw_text(c, 32, lead_y + 84, "LEAD", 2, RED)
    ICONS[0](c, 158, lead_y + 92, 42)
    hx = 232
    draw_text(c, hx, lead_y + 26, STORIES[0][0], 4, NAVY)
    c.fill_rect(hx, lead_y + 68, 520, 4, RED)
    lines = wrap_text(STORIES[0][1], lead_w - (hx - lead_x) - 28, 2)
    for i, ln in enumerate(lines[:3]):
        draw_text(c, hx, lead_y + 88 + i * 22, ln, 2, INK)

    # ---- five more stories ---------------------------------------------
    # Rows are 100px tall so even the longest summary fits on 3 lines.
    row_y = 400
    row_h = 100
    gap = 5
    for idx in range(1, 6):
        y = row_y + (idx - 1) * (row_h + gap)
        c.fill_rect(16, y, 992, row_h, WHITE)
        c.rect(16, y, 992, row_h, LIGHT_GREY, 2)
        c.fill_rect(16, y, 6, row_h, RED if idx % 2 else NAVY)
        badge(c, 56, y + row_h // 2, 20, idx + 1, scale=3)
        ICONS[idx](c, 138, y + row_h // 2, 30)
        headline, summary = STORIES[idx]
        draw_text(c, 196, y + 12, headline, 3, NAVY)
        lines = wrap_text(summary, 992 - 196 - 24, 2)
        for i, ln in enumerate(lines[:3]):
            draw_text(c, 196, y + 44 + i * 20, ln, 2, INK)

    # ---- footer ---------------------------------------------------------
    fy = 932
    c.fill_rect(0, fy - 6, W, 4, RED)
    draw_text(c, 32, fy + 8, "ALSO:", 2, RED)
    also_lines = wrap_text(ALSO, W - 32 - 110, 2)
    for i, ln in enumerate(also_lines[:2]):
        draw_text(c, 32 + 96, fy + 8 + i * 21, ln, 2, NAVY)
    draw_text_centered(c, fy + 56,
                       "SUMMARISED FROM REPORTS PUBLISHED ON 18 NOVEMBER 2026",
                       2, GREY)
    c.fill_rect(0, H - 10, W, 10, NAVY)
    return c


# ---------------------------------------------------------------------- PNG
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def save_png(canvas, path):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * canvas.w * 3
        raw += canvas.px[start:start + canvas.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.w, canvas.h,
                                      8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = draw()
    path = os.path.join(out_dir, "entry.png")
    size = save_png(canvas, path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()

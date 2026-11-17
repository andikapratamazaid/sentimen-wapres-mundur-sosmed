#!/usr/bin/env python3
"""Bangun awan kata PNG dengan PIL.

Modul wordcloud tidak tersedia di lingkungan ini, jadi awan kata dibangun
manual: kata diurutkan menurut frekuensi, ukuran huruf sebanding akar
frekuensi, dan kata ditempatkan menyebar dari tengah kanvas dengan uji
tabrakan memakai kisi okupansi. Kata henti Bahasa Indonesia dan Inggris,
kata kunci pencarian, serta kata templat ringkasan layanan dikeluarkan
(lihat text_utils.SUMMARIZER_TEMPLATE_WORDS). Tabel frekuensi mentah di
data/word_frequencies.csv tetap menyertakan kata kunci pencarian.

Awan kata yang dibuat (7): keseluruhan, threads, instagram, facebook,
positif, negatif, netral. Awan kata TikTok tidak dibuat karena nol
postingan TikTok terkumpul; ketiadaannya dinyatakan eksplisit di
data/collection_notes.md dan README.

Jalankan setelah run_analysis.py: python3 analysis/build_wordclouds.py
"""

import csv
import math
import os
import random
import sys
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text_utils import (SUMMARIZER_TEMPLATE_WORDS, content_tokens,  # noqa: E402
                        load_stopwords)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "wordclouds")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
STOPWORDS = load_stopwords()
SEARCH_KEYWORDS = {"gibran", "rakabuming", "mundur", "mengundurkan",
                   "pengunduran", "wapres", "resign", "resigns", "resigned",
                   "resignation"}
WIDTH, HEIGHT = 1200, 800
CELL = 6

PALETTES = {
    "keseluruhan": ["#0d47a1", "#1565c0", "#37474f", "#00695c", "#4a148c"],
    "threads": ["#212121", "#00695c", "#00838f", "#37474f", "#4e342e"],
    "instagram": ["#880e4f", "#ad1457", "#6a1b9a", "#ef6c00", "#c62828"],
    "facebook": ["#0d47a1", "#1565c0", "#283593", "#00838f", "#37474f"],
    "positif": ["#1b5e20", "#2e7d32", "#00695c", "#33691e", "#00838f"],
    "negatif": ["#b71c1c", "#c62828", "#ad1457", "#e65100", "#4e342e"],
    "netral": ["#37474f", "#546e7a", "#616161", "#455a64", "#263238"],
}


def frequencies(rows):
    counts = Counter()
    for row in rows:
        tokens = content_tokens(row["analysis_text"], STOPWORDS)
        tokens = [t for t in tokens if t not in SEARCH_KEYWORDS
                  and t not in SUMMARIZER_TEMPLATE_WORDS]
        counts.update(tokens)
    return counts


def draw_cloud(counts, palette, path, top_n=90):
    words = counts.most_common(top_n)
    if not words:
        raise ValueError(f"tidak ada kata untuk {path}")
    max_freq = words[0][1]
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    grid = [[False] * (WIDTH // CELL) for _ in range(HEIGHT // CELL)]
    rng = random.Random(42)

    def fits(x, y, w, h):
        gx, gy = x // CELL, y // CELL
        gw, gh = max(1, w // CELL), max(1, h // CELL)
        if gx < 0 or gy < 0 or gx + gw >= WIDTH // CELL or gy + gh >= HEIGHT // CELL:
            return False
        return all(not grid[gy + dy][gx + dx]
                   for dy in range(gh) for dx in range(gw))

    def mark(x, y, w, h):
        gx, gy = x // CELL, y // CELL
        gw, gh = max(1, w // CELL), max(1, h // CELL)
        for dy in range(gh):
            for dx in range(gw):
                grid[gy + dy][gx + dx] = True

    placed = 0
    for word, freq in words:
        size = int(15 + 62 * math.sqrt(freq / max_freq))
        font = ImageFont.truetype(FONT, size)
        bbox = draw.textbbox((0, 0), word, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        done = False
        for attempt in range(300):
            if attempt == 0:
                angle = 0.0
                radius = 0.0
            else:
                angle = attempt * 0.35
                radius = 4.5 * angle
            cx = WIDTH // 2 + int(radius * math.cos(angle) * 1.6)
            cy = HEIGHT // 2 + int(radius * math.sin(angle))
            x, y = cx - w // 2, cy - h // 2
            if 4 <= x and 4 <= y and x + w <= WIDTH - 4 and y + h <= HEIGHT - 4 \
                    and fits(x, y, w + 4, h + 4):
                draw.text((x, y), word, font=font,
                          fill=palette[placed % len(palette)])
                mark(x, y, w + 4, h + 4)
                placed += 1
                done = True
                break
        if not done and size > 18:
            font = ImageFont.truetype(FONT, 16)
            bbox = draw.textbbox((0, 0), word, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            for attempt in range(300):
                x = rng.randint(4, WIDTH - w - 4)
                y = rng.randint(4, HEIGHT - h - 4)
                if fits(x, y, w + 4, h + 4):
                    draw.text((x, y), word, font=font,
                              fill=palette[placed % len(palette)])
                    mark(x, y, w + 4, h + 4)
                    placed += 1
                    break
    image.save(path)
    print("awan kata:", os.path.basename(path), f"({placed} kata)")


def main():
    with open(os.path.join(ROOT, "data", "posts_clean.csv"),
              encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    draw_cloud(frequencies(rows), PALETTES["keseluruhan"],
               os.path.join(OUT, "awan_kata_keseluruhan.png"))
    for platform in ("threads", "instagram", "facebook"):
        subset = [r for r in rows if r["platform"] == platform]
        draw_cloud(frequencies(subset), PALETTES[platform],
                   os.path.join(OUT, f"awan_kata_{platform}.png"))
    for label in ("positif", "negatif", "netral"):
        subset = [r for r in rows if r["sentiment_label"] == label]
        draw_cloud(frequencies(subset), PALETTES[label],
                   os.path.join(OUT, f"awan_kata_{label}.png"))


if __name__ == "__main__":
    main()

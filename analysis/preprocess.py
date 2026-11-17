#!/usr/bin/env python3
"""Praproses: deduplikasi postingan mentah.

Urutan deduplikasi:
1. Per URL ternormalisasi (huruf kecil, tanpa garis miring akhir). Untuk URL
   yang sama, disimpan rekaman dengan engagement tertinggi (likes + komentar)
   karena panggilan pencarian yang berbeda dapat mengembalikan angka yang
   sedikit berbeda untuk postingan yang sama.
2. Per teks ternormalisasi (summary yang ditokenisasi), untuk menangkap
   postingan silang (cross-post) yang sama di URL berbeda.

Kolom analysis_text adalah gabungan summary, comment_summary, dan focus:
persis representasi teks yang dikembalikan layanan pencarian untuk
postingan tersebut, dan itulah yang dianalisis mesin sentimen.

Jalankan: python3 analysis/preprocess.py
Masukan: data/posts_raw.csv
Keluaran: data/posts_dedup.csv dan ringkasan hitungan di stdout.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text_utils import normalize_text_key  # noqa: E402

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_CSV = os.path.join(PROJECT_ROOT, "data", "posts_raw.csv")
OUT_CSV = os.path.join(PROJECT_ROOT, "data", "posts_dedup.csv")


def engagement(row):
    total = 0
    for field in ("likes", "comments_count", "shares"):
        try:
            total += int(row.get(field) or 0)
        except (TypeError, ValueError):
            pass
    return total


def dedup_by(rows, keyfunc):
    best = {}
    order = []
    for row in rows:
        key = keyfunc(row)
        if not key:
            order.append(row)
            continue
        if key not in best:
            best[key] = row
            order.append(key)
        elif engagement(row) > engagement(best[key]):
            best[key] = row
    result = []
    for item in order:
        if isinstance(item, str):
            result.append(best[item])
        else:
            result.append(item)
    return result


def main():
    with open(IN_CSV, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    total_raw = len(rows)
    rows = dedup_by(rows, lambda r: r["url"].strip().lower())
    after_url = len(rows)
    rows = dedup_by(rows, lambda r: normalize_text_key(r["summary"])[:400])
    after_text = len(rows)
    for row in rows:
        row["analysis_text"] = " ".join(
            part for part in (row["summary"], row["comment_summary"], row["focus"])
            if part).strip()
    fieldnames = list(rows[0].keys()) if rows else []
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Mentah:", total_raw)
    print("Setelah dedup URL:", after_url)
    print("Setelah dedup teks:", after_text)


if __name__ == "__main__":
    main()

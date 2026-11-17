#!/usr/bin/env python3
"""Pengumpul postingan (tahap koleksi).

Project ini mengumpulkan postingan publik lewat layanan pencarian sosial
(social.search) pada 17 November 2026. Setiap panggilan pencarian menyimpan
keluaran mentahnya sebagai berkas teks di /tmp/zeitgeist-*.xml. Skrip ini
memparse semua berkas keluaran tersebut menjadi data/posts_raw.csv.

Keterbatasan penting yang didokumentasikan apa adanya:
- Connector Threads, Instagram, dan Facebook TIDAK terhubung ke akun mana pun
  pada saat pengumpulan (perintah accounts mengembalikan daftar kosong),
  sehingga CLI platform tidak dapat dipakai. Satu-satunya sumber adalah
  layanan pencarian sosial, yang mencakup Threads, Instagram, dan Facebook.
- Layanan pencarian mengembalikan representasi teks setiap postingan
  (ringkasan isi, ringkasan komentar yang memuat kutipan verbatim komentar
  publik dalam Bahasa Indonesia, dan garis fokus), bukan selalu teks caption
  verbatim. Kolom summary, comment_summary, dan focus menyimpan persis apa
  yang dikembalikan layanan.
- TikTok tidak dicakup layanan pencarian dan tidak memiliki connector,
  sehingga tidak ada postingan TikTok yang terkumpul (0 postingan).
- Tiga panggilan terakhir pada 17 November 2026 membentur batas laju
  (HTTP 429) dan dihentikan; tidak ada percobaan ulang untuk mengakalinya.

Jalankan: python3 analysis/collect_posts.py
Keluaran: data/posts_raw.csv dan output/collection_manifest.json
"""

import csv
import glob
import json
import os
import re
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_GLOB = "/tmp/zeitgeist-*.xml"
OUT_CSV = os.path.join(PROJECT_ROOT, "data", "posts_raw.csv")
OUT_MANIFEST = os.path.join(PROJECT_ROOT, "output", "collection_manifest.json")

ENGAGEMENT_RE = re.compile(r"^([\d.,]+)([KM]?) (Likes|Comments|Shares|Views)$")
FOLLOWERS_RE = re.compile(r"^([\d.,]+)([KM]?) Followers$")
BLOCK_START_RE = re.compile("^【[0-9a-f]+】$")
SENTIMENT_LABEL_RE = re.compile(r"^[A-Z][A-Za-z ]* Sentiment$")
HANDLE_RE = re.compile(r"handle=([^¦\]]+)")
ENTITY_RE = re.compile(r"entity-(.+?)¦")


def parse_number(text, suffix):
    value = float(text.replace(",", ""))
    if suffix == "K":
        value *= 1000
    elif suffix == "M":
        value *= 1000000
    return int(round(value))


def platform_from_url(url):
    if "threads." in url:
        return "threads"
    if "instagram." in url:
        return "instagram"
    if "facebook." in url or "fb." in url:
        return "facebook"
    if "tiktok." in url:
        return "tiktok"
    return "unknown"


def parse_block(lines):
    post = {
        "url": "", "post_type": "", "created_utc": "",
        "likes": "", "comments_count": "", "shares": "",
        "summary": "", "comment_summary": "", "focus": "",
        "provider_sentiment_label": "", "author_handle": "", "author_name": "",
        "author_url": "", "author_followers": "", "verified": "",
        "language": "",
    }
    current = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("URL "):
            post["url"] = stripped[4:].strip()
            current = None
        elif stripped.startswith("Type "):
            post["post_type"] = stripped[5:].strip()
            current = None
        elif stripped.startswith("Created "):
            post["created_utc"] = stripped[8:].strip()
            current = None
        elif ENGAGEMENT_RE.match(stripped):
            match = ENGAGEMENT_RE.match(stripped)
            value = parse_number(match.group(1), match.group(2))
            field = {"Likes": "likes", "Comments": "comments_count",
                     "Shares": "shares", "Views": "views"}[match.group(3)]
            if field != "views":
                post[field] = value
            current = None
        elif stripped.startswith("Summary:"):
            post["summary"] = stripped[len("Summary:"):].strip()
            current = "summary"
        elif stripped.startswith("CommentSummary:"):
            post["comment_summary"] = stripped[len("CommentSummary:"):].strip()
            current = "comment_summary"
        elif stripped.startswith("Temporal Data of event in content:"):
            current = None
        elif stripped.startswith("Focus "):
            post["focus"] = stripped[len("Focus "):].strip()
            current = "focus"
        elif stripped.startswith("Entities "):
            current = None
        elif re.match(r"^\d+ OnScreenTextLen$", stripped):
            current = None
        elif SENTIMENT_LABEL_RE.match(stripped):
            post["provider_sentiment_label"] = stripped
            current = None
        elif stripped.startswith("Author "):
            match = HANDLE_RE.search(stripped)
            if match:
                post["author_handle"] = match.group(1).strip()
            match_name = ENTITY_RE.search(stripped)
            if match_name:
                post["author_name"] = match_name.group(1).strip()
            current = None
        elif stripped.startswith("AuthorURL "):
            post["author_url"] = stripped[len("AuthorURL "):].strip()
            current = None
        elif stripped == "Verified":
            post["verified"] = "yes"
            current = None
        elif FOLLOWERS_RE.match(stripped):
            match = FOLLOWERS_RE.match(stripped)
            post["author_followers"] = parse_number(match.group(1), match.group(2))
            current = None
        elif stripped.startswith("Language "):
            post["language"] = stripped[len("Language "):].strip()
            current = None
        elif current in ("summary", "comment_summary", "focus") and stripped:
            post[current] = (post[current] + " " + stripped).strip()
    return post


def parse_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        lines = handle.read().splitlines()
    blocks = []
    current_lines = None
    for line in lines:
        if BLOCK_START_RE.match(line.strip()):
            if current_lines:
                blocks.append(current_lines)
            current_lines = []
        elif current_lines is not None:
            current_lines.append(line)
    if current_lines:
        blocks.append(current_lines)
    posts = []
    for block in blocks:
        post = parse_block(block)
        if post["url"]:
            post["source_file"] = os.path.basename(path)
            posts.append(post)
    return posts


def main():
    files = sorted(glob.glob(RAW_GLOB))
    all_posts = []
    manifest_files = []
    for path in files:
        posts = parse_file(path)
        if posts:
            manifest_files.append({
                "file": os.path.basename(path),
                "posts_parsed": len(posts),
            })
            all_posts.extend(posts)
    rows = []
    for post in all_posts:
        date_wib = ""
        created_wib = ""
        if post["created_utc"]:
            try:
                created_dt = datetime.strptime(
                    post["created_utc"].replace(" UTC", ""), "%Y-%m-%d %H:%M:%S")
                wib = created_dt + timedelta(hours=7)
                created_wib = wib.strftime("%Y-%m-%d %H:%M:%S")
                date_wib = wib.strftime("%Y-%m-%d")
            except ValueError:
                pass
        url = post["url"].rstrip("/")
        post_id = url.split("/")[-1]
        rows.append({
            "post_id": post_id,
            "platform": platform_from_url(url),
            "url": url,
            "author_handle": post["author_handle"],
            "author_name": post["author_name"],
            "author_followers": post["author_followers"],
            "verified": post["verified"],
            "post_type": post["post_type"],
            "created_utc": post["created_utc"],
            "created_wib": created_wib,
            "date_wib": date_wib,
            "likes": post["likes"],
            "comments_count": post["comments_count"],
            "shares": post["shares"],
            "language": post["language"],
            "summary": post["summary"],
            "comment_summary": post["comment_summary"],
            "focus": post["focus"],
            "provider_sentiment_label": post["provider_sentiment_label"],
            "source_file": post["source_file"],
        })
    fieldnames = list(rows[0].keys()) if rows else []
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    manifest = {
        "collection_date": "2026-11-17",
        "tool": "social.search (layanan pencarian sosial)",
        "source_files_used": manifest_files,
        "total_raw_posts": len(rows),
        "rate_limit_note": ("Tiga panggilan terakhir berhenti karena batas laju "
                            "HTTP 429 dan tidak dicoba ulang."),
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
    print("Berkas sumber terparse:", len(manifest_files))
    print("Total postingan mentah:", len(rows))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Utilitas teks bersama: tokenisasi dan pemuatan sumber daya bahasa."""

import os
import re

RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

URL_RE = re.compile(r"https?://\S+")
HANDLE_RE = re.compile(r"@\w+")
NONWORD_RE = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s]")


def load_lexicon(filename):
    """Muat berkas leksikon 'kata,bobot'. Baris diawali # adalah komentar."""
    lexicon = {}
    path = os.path.join(RESOURCES, filename)
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            word, _, weight = line.partition(",")
            weight = float(weight)
            if weight != 0:
                lexicon[word.strip().lower()] = weight
    return lexicon


def load_word_list(filename):
    words = set()
    path = os.path.join(RESOURCES, filename)
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                words.add(line.lower())
    return words


def load_stopwords():
    stopwords = load_word_list("stopwords_id.txt") | load_word_list("stopwords_en.txt")
    return stopwords


def tokenize(text):
    """Tokenisasi sederhana: huruf kecil, buang URL dan handle, pisah kata."""
    if not text:
        return []
    text = text.lower()
    text = text.replace("n't", " not")
    text = URL_RE.sub(" ", text)
    text = HANDLE_RE.sub(" ", text)
    text = text.replace("#", " ")
    text = NONWORD_RE.sub(" ", text)
    return [tok for tok in text.split() if len(tok) > 1 or tok.isdigit()]


def content_tokens(text, stopwords):
    """Token isi: tokenisasi lalu buang kata henti dan token satu huruf."""
    return [tok for tok in tokenize(text)
            if tok not in stopwords and len(tok) > 1 and not tok.isdigit()]


def normalize_text_key(text):
    """Kunci normalisasi untuk deduplikasi teks."""
    return " ".join(tokenize(text or ""))


# Kata templat ringkasan layanan pencarian: frasa baku yang dipakai layanan
# untuk mendeskripsikan gambar dan video (mis. "overall tone", "culture
# moment", "on-screen text"). Kata kata ini adalah artefak representasi
# teks, bukan isi postingan, jadi dikeluarkan dari awan kata dan dari
# frekuensi per kelompok. Tabel frekuensi mentah keseluruhan tetap
# menyertakannya agar transparan.
SUMMARIZER_TEMPLATE_WORDS = {
    "tone", "text", "post", "posts", "summary", "caption", "image", "video",
    "shows", "show", "showing", "depicts", "depicted", "features", "featuring",
    "reads", "overall", "culture", "moment", "significance", "origin",
    "details", "includes", "include", "included", "content", "visible",
    "appears", "appear", "wearing", "wears", "background", "foreground",
    "scene", "footage", "clip", "graphic", "photo", "photograph",
    "screenshot", "overlay", "overlaid", "slide", "slides", "branded",
    "watermark", "studio", "anchor", "anchors", "reporter", "reporters",
    "discusses", "discussing", "explains", "explained", "stating", "upper",
    "lower", "third", "left", "right", "front", "behind", "wore", "worn",
    "dressed", "standing", "seated", "sitting", "holding", "holds", "held",
    "looking", "looks", "toward", "towards", "camera", "cameras", "crowd",
    "him", "his", "her", "she", "they", "them", "their", "author", "account",
    "accounts", "user", "users", "page", "channel", "link", "article",
    "source", "media", "online", "social", "captioned", "titled",
    "several", "multiple", "various", "alongside", "onto", "upon",
}

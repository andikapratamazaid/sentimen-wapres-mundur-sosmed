#!/usr/bin/env python3
"""Mesin sentimen berbasis leksikon untuk Bahasa Indonesia.

Metode:
- Skor adalah jumlah bobot kata sentimen yang ditemukan dalam teks.
- Leksikon inti berbahasa Indonesia (resources/lexicon_*_id.txt), ditambah
  suplemen kata sentimen Bahasa Inggris (resources/lexicon_*_en.txt) karena
  layanan pencarian mengembalikan ringkasan isi berbahasa Inggris yang
  bercampur dengan kutipan verbatim komentar publik berbahasa Indonesia.
- Frasa dua kata tertentu dinilai lebih dulu (mis. "sakit hati",
  "tidak becus", "lapang dada", "luar biasa", "terima kasih", "air mata").
- Negasi: kata negasi (tidak, bukan, jangan, nggak, gak, ga, enggak, tak,
  belum, not, no, never) dalam jarak dua token sebelum kata sentimen
  membalik tanda bobot kata tersebut.
- Penguat: kata penguat (sangat, amat, banget, sekali, paling, terlalu,
  sungguh, very, really, extremely) dalam jarak satu token sebelum kata
  sentimen mengalikan bobot dengan 1,5. Pelemah (kurang, agak, slightly)
  mengalikan 0,5.
- Label: skor >= 1,0 positif; skor <= -1,0 negatif; selain itu netral.

Keterbatasan yang diakui: metode leksikon menilai valensi emosi teks, bukan
targetnya. Ia keliru pada sarkasme, teks campuran, dan pada postingan yang
mengekspresikan emosi negatif terhadap Gibran tetapi menyambut
pengunduran dirinya (atau sebaliknya). Akurasi terhadap label manusia
diukur dan dilaporkan apa adanya di output/analysis_results.json.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text_utils import load_lexicon, tokenize  # noqa: E402

POSITIVE = {}
POSITIVE.update(load_lexicon("lexicon_positive_id.txt"))
POSITIVE.update(load_lexicon("lexicon_positive_en.txt"))
NEGATIVE = {}
NEGATIVE.update(load_lexicon("lexicon_negative_id.txt"))
NEGATIVE.update(load_lexicon("lexicon_negative_en.txt"))

PHRASES = {
    "sakit hati": -2.0,
    "tidak becus": -2.0,
    "anak haram": -2.0,
    "air mata": -1.0,
    "lapang dada": 2.0,
    "luar biasa": 2.0,
    "terima kasih": 1.0,
    "besar hati": 1.0,
}

NEGATORS = {"tidak", "bukan", "jangan", "nggak", "gak", "ga", "enggak",
            "tak", "belum", "not", "no", "never", "tanpa"}
INTENSIFIERS = {"sangat", "amat", "banget", "sekali", "paling", "terlalu",
                "sungguh", "very", "really", "extremely", "so"}
DIMMERS = {"kurang", "agak", "slightly", "agaknya"}

POS_THRESHOLD = 1.0
NEG_THRESHOLD = -1.0


def score_text(text):
    """Kembalikan (skor, label, daftar kata positif, daftar kata negatif)."""
    if not text:
        return 0.0, "netral", [], []
    lowered = " " + text.lower() + " "
    score = 0.0
    pos_hits = []
    neg_hits = []
    for phrase, weight in PHRASES.items():
        if " " + phrase + " " in lowered or phrase in lowered:
            count = lowered.count(phrase)
            score += weight * count
            if weight > 0:
                pos_hits.extend([phrase] * count)
            else:
                neg_hits.extend([phrase] * count)
    tokens = tokenize(text)
    for index, token in enumerate(tokens):
        weight = None
        if token in POSITIVE:
            weight = POSITIVE[token]
        elif token in NEGATIVE:
            weight = -NEGATIVE[token]
        if weight is None:
            continue
        window = tokens[max(0, index - 2):index]
        if any(tok in NEGATORS for tok in window):
            weight = -weight
        if any(tok in INTENSIFIERS for tok in window):
            weight *= 1.5
        if any(tok in DIMMERS for tok in window):
            weight *= 0.5
        score += weight
        if weight > 0:
            pos_hits.append(token)
        else:
            neg_hits.append(token)
    if score >= POS_THRESHOLD:
        label = "positif"
    elif score <= NEG_THRESHOLD:
        label = "negatif"
    else:
        label = "netral"
    return round(score, 2), label, pos_hits, neg_hits


def classify(text):
    score, label, _, _ = score_text(text)
    return score, label


if __name__ == "__main__":
    examples = [
        "Saya sangat senang dan lega, keputusan yang bijak dan kesatria",
        "Sedih sekali, saya kecewa dan sakit hati melihatnya mundur",
        "Tidak bagus keputusan ini, sangat disayangkan",
        "Gibran menyerahkan surat pengunduran diri kepada MPR hari ini",
        "Dia tidak kecewa, justru bangga dan bersyukur",
    ]
    for example in examples:
        print(score_text(example), "<-", example)

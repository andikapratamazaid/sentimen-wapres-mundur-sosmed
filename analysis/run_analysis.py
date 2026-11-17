#!/usr/bin/env python3
"""Analisis utama project Sentimen Publik.

Langkah:
1. Klasifikasi sentimen semua postingan hasil dedup -> data/posts_clean.csv
2. Validasi mesin terhadap label manusia (analysis/human_labels.json,
   sampel acak seed 42, 120 postingan) -> data/labeled_sample.csv
3. Frekuensi kata dan bigram -> data/word_frequencies.csv,
   data/bigram_frequencies.csv
4. Statistik lengkap -> output/analysis_results.json
5. Kompetisi atensi dengan masalah nasional lain (kelompok kata kunci)
6. Indikator dampak -> data/impact_indicators.csv (baris pasar diambil dari
   project pendamping MarketShock ID, tidak diunduh ulang)
7. Proyeksi 14 hari metode Holt -> data/prediction_sentiment.csv

Jalankan: python3 analysis/run_analysis.py
"""

import csv
import json
import math
import os
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentiment_engine import score_text  # noqa: E402
from text_utils import (SUMMARIZER_TEMPLATE_WORDS, content_tokens,
                        load_stopwords, tokenize)  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUTPUT = os.path.join(ROOT, "output")
COMPANION_JSON = os.path.expanduser(
    "~/workspace/marketshock-id-event-study/output/analysis_results.json")
COMPANION_PANEL = os.path.expanduser(
    "~/workspace/marketshock-id-event-study/data/processed/market_daily.csv")

SEARCH_KEYWORDS = {"gibran", "rakabuming", "mundur", "mengundurkan",
                   "pengunduran", "wapres", "resign", "resigns", "resigned",
                   "resignation"}

ATTENTION_GROUPS = {
    "bencana": ["bencana", "banjir", "gempa", "longsor", "erupsi"],
    "harga": ["harga", "bbm", "sembako"],
    "ekonomi": ["ekonomi", "rupiah", "pengangguran"],
}

STOPWORDS = load_stopwords()


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def mean_median(values):
    if not values:
        return {"mean": 0.0, "median": 0.0, "n": 0}
    return {"mean": round(statistics.mean(values), 2),
            "median": float(statistics.median(values)),
            "n": len(values)}


def holt_forecast(series, steps=14, alpha=0.5, beta=0.3, phi=0.8):
    """Tren linear Holt teredam (damped trend, phi 0,8).

    Peredaman dipakai karena deretnya pendek dan berbentuk lonjakan
    peristiwa yang meluruh; tren linear murni mengekstrapolasi terlalu
    agresif. Kembalikan (proyeksi, sigma residual satu langkah).
    """
    if len(series) < 3:
        raise ValueError("deret terlalu pendek untuk Holt")
    level = series[0]
    trend = series[1] - series[0]
    errors = []
    for t in range(1, len(series)):
        errors.append(series[t] - (level + phi * trend))
        prev_level = level
        level = alpha * series[t] + (1 - alpha) * (level + phi * trend)
        trend = beta * (level - prev_level) + (1 - beta) * phi * trend
    sigma = statistics.pstdev(errors) if len(errors) > 1 else 0.0
    forecasts = []
    multiplier = 0.0
    for h in range(1, steps + 1):
        multiplier += phi ** h
        value = level + multiplier * trend
        band = 1.96 * sigma * math.sqrt(h)
        forecasts.append((value, value - band, value + band))
    return forecasts, sigma


def main():
    with open(os.path.join(DATA, "posts_dedup.csv"), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    # 1. Klasifikasi
    for row in rows:
        score, label, pos_hits, neg_hits = score_text(row["analysis_text"])
        row["sentiment_score"] = score
        row["sentiment_label"] = label
        row["pos_hit_count"] = len(pos_hits)
        row["neg_hit_count"] = len(neg_hits)
    clean_fields = list(rows[0].keys())
    with open(os.path.join(DATA, "posts_clean.csv"), "w", encoding="utf-8",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=clean_fields)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    per_platform = Counter(r["platform"] for r in rows)
    sentiment_overall = Counter(r["sentiment_label"] for r in rows)
    sentiment_per_platform = {}
    for platform in sorted(per_platform):
        subset = [r for r in rows if r["platform"] == platform]
        counts = Counter(r["sentiment_label"] for r in subset)
        sentiment_per_platform[platform] = {
            label: {"count": counts.get(label, 0),
                    "share_pct": round(100 * counts.get(label, 0) / len(subset), 2)}
            for label in ("positif", "negatif", "netral")}

    def user_key(r):
        ident = r["author_handle"] or r["author_name"]
        if not ident:
            parts = r["url"].split("/")
            ident = parts[3] if len(parts) > 3 else ""
        return (r["platform"], ident.lower())

    unique_users = len({user_key(r) for r in rows if user_key(r)[1]})

    # Volume dan sentimen harian
    daily = {}
    by_date = defaultdict(list)
    for r in rows:
        by_date[r["date_wib"]].append(r)
    for date in sorted(by_date):
        subset = by_date[date]
        counts = Counter(r["sentiment_label"] for r in subset)
        daily[date] = {
            "volume": len(subset),
            "positif": counts.get("positif", 0),
            "negatif": counts.get("negatif", 0),
            "netral": counts.get("netral", 0),
            "negatif_share_pct": round(100 * counts.get("negatif", 0) / len(subset), 2),
            "positif_share_pct": round(100 * counts.get("positif", 0) / len(subset), 2),
        }

    # Engagement per kelas sentimen
    engagement = {}
    for label in ("positif", "negatif", "netral"):
        subset = [r for r in rows if r["sentiment_label"] == label]
        engagement[label] = {
            "likes": mean_median([to_int(r["likes"]) for r in subset
                                  if r["likes"] != ""]),
            "comments": mean_median([to_int(r["comments_count"]) for r in subset
                                     if r["comments_count"] != ""]),
            "total_likes": sum(to_int(r["likes"]) for r in subset),
            "total_comments": sum(to_int(r["comments_count"]) for r in subset),
        }

    # Postingan teratas per platform
    top_posts = {}
    for platform in sorted(per_platform):
        subset = [r for r in rows if r["platform"] == platform]
        subset.sort(key=lambda r: to_int(r["likes"]) + to_int(r["comments_count"]),
                    reverse=True)
        top_posts[platform] = [
            {"url": r["url"], "date_wib": r["date_wib"],
             "likes": to_int(r["likes"]), "comments": to_int(r["comments_count"]),
             "sentiment_label": r["sentiment_label"],
             "summary_excerpt": r["summary"][:180]}
            for r in subset[:5]]

    # 2. Validasi terhadap label manusia
    with open(os.path.join(ROOT, "analysis", "human_labels.json"),
              encoding="utf-8") as fh:
        human_labels = json.load(fh)
    random.seed(42)
    sample = random.sample(rows, 120)
    labeled_rows = []
    correct = 0
    confusion = Counter()
    for r in sample:
        human = human_labels[r["post_id"]]
        engine = r["sentiment_label"]
        match = human == engine
        correct += match
        confusion[(human, engine)] += 1
        labeled_rows.append({
            "post_id": r["post_id"], "platform": r["platform"],
            "date_wib": r["date_wib"], "url": r["url"],
            "text_excerpt": r["analysis_text"][:400],
            "human_label": human, "engine_label": engine,
            "engine_score": r["sentiment_score"], "match": match})
    with open(os.path.join(DATA, "labeled_sample.csv"), "w", encoding="utf-8",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(labeled_rows[0].keys()))
        writer.writeheader()
        writer.writerows(labeled_rows)
    accuracy = round(100 * correct / len(sample), 2)
    per_class = {}
    for label in ("positif", "negatif", "netral"):
        n_class = sum(1 for lr in labeled_rows if lr["human_label"] == label)
        ok_class = sum(1 for lr in labeled_rows
                       if lr["human_label"] == label and lr["match"])
        per_class[label] = {"n": n_class, "correct": ok_class,
                            "accuracy_pct": round(100 * ok_class / n_class, 2)
                            if n_class else None}
    validation = {"sample_size": len(sample), "correct": correct,
                  "accuracy_pct": accuracy, "per_class": per_class,
                  "confusion": {f"{h}->{e}": n for (h, e), n in
                                sorted(confusion.items())}}

    # 3. Frekuensi kata dan bigram
    def frequencies(subset, filtered=False):
        words = Counter()
        bigrams = Counter()
        for r in subset:
            tokens = content_tokens(r["analysis_text"], STOPWORDS)
            if filtered:
                tokens = [t for t in tokens
                          if t not in SEARCH_KEYWORDS
                          and t not in SUMMARIZER_TEMPLATE_WORDS]
            words.update(tokens)
            bigrams.update(zip(tokens, tokens[1:]))
        return words, bigrams

    words_all, bigrams_all = frequencies(rows)
    with open(os.path.join(DATA, "word_frequencies.csv"), "w", encoding="utf-8",
              newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["word", "count"])
        writer.writerows(words_all.most_common(30))
    with open(os.path.join(DATA, "bigram_frequencies.csv"), "w", encoding="utf-8",
              newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["bigram", "count"])
        writer.writerows([(" ".join(bg), n) for bg, n in
                          bigrams_all.most_common(20)])

    top_by_sentiment = {}
    for label in ("positif", "negatif", "netral"):
        subset = [r for r in rows if r["sentiment_label"] == label]
        w, b = frequencies(subset, filtered=True)
        top_by_sentiment[label] = {
            "top_words": w.most_common(15),
            "top_bigrams": [(" ".join(bg), n) for bg, n in b.most_common(10)]}
    top_by_platform = {}
    for platform in sorted(per_platform):
        subset = [r for r in rows if r["platform"] == platform]
        w, _ = frequencies(subset, filtered=True)
        top_by_platform[platform] = w.most_common(15)

    # Polarisasi per platform
    polarization = {}
    for platform in sorted(per_platform):
        subset = [r for r in rows if r["platform"] == platform]
        counts = Counter(r["sentiment_label"] for r in subset)
        pos, neg = counts.get("positif", 0), counts.get("negatif", 0)
        polarization[platform] = {
            "non_neutral_share_pct": round(100 * (pos + neg) / len(subset), 2),
            "pos_neg_ratio": round(pos / neg, 2) if neg else None,
            "positif": pos, "negatif": neg, "netral": counts.get("netral", 0)}

    # 5. Kompetisi atensi
    def group_hits(text):
        tokens = tokenize(text)
        hits = set()
        for group, keywords in ATTENTION_GROUPS.items():
            for tok in tokens:
                if any(tok.startswith(kw) for kw in keywords):
                    hits.add(group)
                    break
        return hits

    attention = {"groups": {}, "per_platform": {}, "per_day": {}}
    group_counts = Counter()
    any_count = 0
    for r in rows:
        hits = group_hits(r["analysis_text"])
        r["_attention"] = hits
        for group in hits:
            group_counts[group] += 1
        if hits:
            any_count += 1
    for group in ATTENTION_GROUPS:
        attention["groups"][group] = {
            "count": group_counts.get(group, 0),
            "share_pct": round(100 * group_counts.get(group, 0) / total, 2),
            "keywords": ATTENTION_GROUPS[group]}
    attention["any_group"] = {"count": any_count,
                              "share_pct": round(100 * any_count / total, 2)}
    for platform in sorted(per_platform):
        subset = [r for r in rows if r["platform"] == platform]
        entry = {}
        for group in ATTENTION_GROUPS:
            n = sum(1 for r in subset if group in r["_attention"])
            entry[group] = {"count": n,
                            "share_pct": round(100 * n / len(subset), 2)}
        attention["per_platform"][platform] = entry
    for date in sorted(by_date):
        subset = by_date[date]
        entry = {}
        for group in ATTENTION_GROUPS:
            entry[group] = sum(1 for r in subset if group in r["_attention"])
        attention["per_day"][date] = entry

    # 6. Indikator dampak
    with open(COMPANION_JSON, encoding="utf-8") as fh:
        companion = json.load(fh)
    ev = companion["global_investor_decomposition"]["event_day_2026_11_12"]
    decomp = companion["global_investor_decomposition"]["bracket_11nov_to_16nov"]
    indicators = []

    def add(indicator, value, unit, type_, source):
        indicators.append({"indicator": indicator, "value": value,
                           "unit": unit, "type": type_, "source": source})

    src_comp = "Project pendamping MarketShock ID (data pasar Yahoo Finance)"
    add("Perubahan IHSG pada hari pengunduran diri (12 Nov 2026)",
        ev["ihsg_return_pct"], "%", "computed", src_comp)
    add("Level penutupan IHSG 12 Nov 2026",
        companion["levels"]["ihsg_close_2026_11_12"], "poin",
        "computed", src_comp)
    add("Perubahan EIDO (ETF Indonesia di AS) 12 Nov 2026",
        ev["eido_return_pct"], "%", "computed", src_comp)
    add("Perubahan USD/IDR 11 ke 16 Nov 2026 (data Yahoo valid)",
        decomp["usdidr_return_pct"], "%", "computed", src_comp)
    add("Perubahan indeks dolar DXY 11 ke 16 Nov 2026",
        decomp["dxy_return_pct"], "%", "computed", src_comp)
    add("Residu spesifik Indonesia USD/IDR vs DXY (11 ke 16 Nov 2026)",
        decomp["usdidr_residual_vs_dxy_pp"], "poin persen", "computed",
        src_comp)
    add("Perubahan IHSG jendela putusan MA (23 Okt ke 6 Nov 2026)",
        companion["events"]["ma_decision"]["series"]["ihsg"]
        ["window_cumulative_change_pct"], "%", "computed", src_comp)
    add("Perubahan IHSG year to date ke 12 Nov 2026",
        companion["context_ytd_to_2026_11_12_pct"]["ihsg"], "%",
        "computed", src_comp)
    add("Perubahan yield US Treasury 10 tahun 12 Nov 2026",
        ev["us10y_change_bps"], "basis poin", "computed", src_comp)
    add("Perubahan IHSG pada hari usulan HMP (11 Nov 2026)",
        companion["events"]["hmp_proposal"]["series"]["ihsg"]
        ["event_day_change_pct"], "%", "computed", src_comp)
    src_meas = "Dataset project ini (social.search, dikumpulkan 17 Nov 2026)"
    add("Total postingan terkumpul setelah dedup", total, "postingan",
        "measured", src_meas)
    for platform in sorted(per_platform):
        add(f"Postingan terkumpul platform {platform}",
            per_platform[platform], "postingan", "measured", src_meas)
    add("Postingan terkumpul platform tiktok", 0, "postingan", "measured",
        "Dataset project ini (social.search tidak mencakup TikTok)")
    add("Pengguna unik teridentifikasi", unique_users, "pengguna", "measured",
        src_meas)
    add("Porsi postingan non-netral (polarisasi keseluruhan)",
        round(100 * (sentiment_overall.get("positif", 0) +
                     sentiment_overall.get("negatif", 0)) / total, 2),
        "%", "measured", src_meas)
    add("Rasio postingan positif terhadap negatif",
        round(sentiment_overall.get("positif", 0) /
              sentiment_overall.get("negatif", 1), 2), "rasio", "measured",
        src_meas)
    add("Akurasi mesin sentimen terhadap label manusia (sampel 120)",
        accuracy, "%", "measured", src_meas)
    for group in ATTENTION_GROUPS:
        add(f"Postingan yang juga menyebut kelompok isu {group}",
            group_counts.get(group, 0), "postingan", "measured", src_meas)
        add(f"Porsi postingan yang juga menyebut kelompok isu {group}",
            attention["groups"][group]["share_pct"], "%", "measured", src_meas)
    add("Beli bersih investor asing 12 Nov 2026 (dilaporkan)", 443.53,
        "Rp miliar", "reported",
        "Kontan, dikutip project pendamping MarketShock ID")
    add("Jual bersih investor asing year to date ke 12 Nov 2026 (dilaporkan)",
        -127000, "Rp miliar", "reported",
        "Kontan, dikutip project pendamping MarketShock ID")
    add("Yield SBN 10 tahun sekitar 12 Nov 2026 (dilaporkan)", 7.63, "%",
        "reported", "Bareksa, dikutip project pendamping MarketShock ID")
    add("Kurs spot USD/IDR 12 Nov 2026 (dilaporkan)", 18216, "Rp per USD",
        "reported", "Suara.com, dikutip project pendamping MarketShock ID")
    add("Jiwa terdampak banjir dan longsor Aceh Tamiang (dilaporkan)", 18158,
        "jiwa", "reported", "BNPB per 15 Nov 2026, via bnpb.go.id dan Indowarta")
    add("Jiwa mengungsi banjir Aceh Tamiang (dilaporkan)", 5088, "jiwa",
        "reported", "BNPB per 15 Nov 2026, via Indowarta")
    add("Jiwa terdampak banjir Subulussalam (dilaporkan)", 7703, "jiwa",
        "reported", "BNPB, via Indowarta 17 Nov 2026")
    add("Jiwa terdampak banjir Langkat 12 Nov 2026 (dilaporkan)", 3155, "jiwa",
        "reported", "BNPB, via Indowarta dan Serayunusantara 13 Nov 2026")
    add("Magnitudo gempa Laut Banda 17 Nov 2026 setelah pemutakhiran "
        "(dilaporkan)", 6.8, "magnitudo", "reported",
        "BMKG, via Ringkasnow dan Politikindonesia 17 Nov 2026")
    add("Gunung api berstatus Siaga Level III (dilaporkan)", 3, "gunung",
        "reported", "PVMBG per 11 Nov 2026, via BNPB dan Jatimnet")
    with open(os.path.join(DATA, "impact_indicators.csv"), "w",
              encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["indicator", "value", "unit",
                                                "type", "source"])
        writer.writeheader()
        writer.writerows(indicators)

    # 7. Proyeksi Holt dari agregat harian 10 sampai 17 Nov 2026
    window_dates = [d for d in sorted(daily) if "2026-11-10" <= d <= "2026-11-17"]
    series = {
        "volume": [daily[d]["volume"] for d in window_dates],
        "negatif_share_pct": [daily[d]["negatif_share_pct"] for d in window_dates],
        "positif_share_pct": [daily[d]["positif_share_pct"] for d in window_dates],
    }
    from datetime import date, timedelta
    start = date(2026, 11, 18)
    pred_rows = []
    prediction_summary = {}
    for metric, values in series.items():
        forecasts, sigma = holt_forecast([float(v) for v in values])
        is_share = "share" in metric
        for h, (value, low, high) in enumerate(forecasts):
            if is_share:
                value = min(max(value, 0.0), 100.0)
                low = min(max(low, 0.0), 100.0)
                high = min(max(high, 0.0), 100.0)
            else:
                value = max(value, 0.0)
                low = max(low, 0.0)
                high = max(high, 0.0)
            pred_rows.append({
                "date": (start + timedelta(days=h)).isoformat(),
                "metric": metric,
                "projected_value": round(value, 2),
                "lower_band": round(low, 2),
                "upper_band": round(high, 2)})
        metric_rows = [r for r in pred_rows if r["metric"] == metric]
        prediction_summary[metric] = {
            "history_dates": window_dates,
            "history_values": values,
            "day1_projection": metric_rows[0]["projected_value"],
            "day7_projection": metric_rows[6]["projected_value"],
            "day14_projection": metric_rows[-1]["projected_value"],
            "residual_sigma": round(sigma, 2)}
    with open(os.path.join(DATA, "prediction_sentiment.csv"), "w",
              encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["date", "metric",
                                                "projected_value",
                                                "lower_band", "upper_band"])
        writer.writeheader()
        writer.writerows(pred_rows)

    results = {
        "project": "Sentimen Publik: Analisis Media Sosial Pengunduran Diri Wapres",
        "collection_date": "2026-11-17",
        "total_posts_raw": 1369,
        "total_posts_after_dedup": total,
        "posts_per_platform_raw": {"facebook": 484, "threads": 453,
                                   "instagram": 432, "tiktok": 0},
        "posts_per_platform": dict(per_platform),
        "posts_tiktok": 0,
        "unique_users": unique_users,
        "date_range_wib": [min(by_date), max(by_date)],
        "sentiment_overall": {
            label: {"count": sentiment_overall.get(label, 0),
                    "share_pct": round(100 * sentiment_overall.get(label, 0) / total, 2)}
            for label in ("positif", "negatif", "netral")},
        "sentiment_per_platform": sentiment_per_platform,
        "daily": daily,
        "engagement_by_sentiment": engagement,
        "top_posts_per_platform": top_posts,
        "validation": validation,
        "polarization_per_platform": polarization,
        "top_words_overall": words_all.most_common(30),
        "top_bigrams_overall": [(" ".join(bg), n) for bg, n in
                                bigrams_all.most_common(20)],
        "top_by_sentiment": top_by_sentiment,
        "top_by_platform": top_by_platform,
        "attention_competition": attention,
        "prediction": {
            "method": "Tren linear Holt teredam (alpha 0,5, beta 0,3, phi 0,8) "
                      "atas agregat harian 10 sampai 17 Nov 2026, pita "
                      "ketidakpastian 1,96 sigma residual dikali akar horizon, "
                      "porsi diklip ke rentang 0 sampai 100 dan volume ke "
                      "minimum 0",
            "window_dates": window_dates,
            "summary": prediction_summary,
        },
        "companion_market_reference": {
            "ihsg_return_event_day_pct": ev["ihsg_return_pct"],
            "ihsg_close_event_day": companion["levels"]["ihsg_close_2026_11_12"],
            "eido_return_event_day_pct": ev["eido_return_pct"],
            "residual_pp": decomp["usdidr_residual_vs_dxy_pp"],
            "ma_window_ihsg_pct": companion["events"]["ma_decision"]["series"]
            ["ihsg"]["window_cumulative_change_pct"],
            "ytd_ihsg_pct": companion["context_ytd_to_2026_11_12_pct"]["ihsg"],
        },
    }
    with open(os.path.join(OUTPUT, "analysis_results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("Total setelah dedup:", total)
    print("Per platform:", dict(per_platform))
    print("Pengguna unik:", unique_users)
    print("Sentimen:", dict(sentiment_overall))
    print("Akurasi validasi:", accuracy, "% dari", len(sample), "sampel")
    print("Kompetisi atensi:", dict(group_counts), "any:", any_count)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Pengujian project Sentimen Publik.

Mencakup: penanganan negasi dan klasifikasi kalimat contoh, penghapusan
kata henti, logika deduplikasi, integritas dataset terhadap
output/analysis_results.json, kesesuaian baris pasar
data/impact_indicators.csv dengan project pendamping MarketShock ID,
konsistensi baris kompetisi atensi, dan keberadaan berkas visual yang
dirujuk README.

Jalankan: python3 -m unittest discover -s tests
"""

import csv
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

from preprocess import dedup_by  # noqa: E402
from sentiment_engine import score_text  # noqa: E402
from text_utils import content_tokens, load_stopwords  # noqa: E402

COMPANION_JSON = os.path.expanduser(
    "~/workspace/marketshock-id-event-study/output/analysis_results.json")


def read_csv(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_results():
    with open(os.path.join(ROOT, "output", "analysis_results.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


class TestSentimentEngine(unittest.TestCase):
    def test_positive_sentence(self):
        _, label, _, _ = score_text(
            "Saya sangat senang dan lega, keputusan yang bijak dan kesatria")
        self.assertEqual(label, "positif")

    def test_negative_sentence(self):
        _, label, _, _ = score_text(
            "Sedih sekali, saya kecewa dan sakit hati melihatnya mundur")
        self.assertEqual(label, "negatif")

    def test_neutral_factual_sentence(self):
        _, label, _, _ = score_text(
            "Gibran menyerahkan surat pengunduran diri kepada MPR hari ini")
        self.assertEqual(label, "netral")

    def test_negation_flips_negative_word(self):
        score, label, pos_hits, _ = score_text(
            "Dia tidak kecewa, justru bangga dan bersyukur")
        self.assertEqual(label, "positif")
        self.assertIn("kecewa", pos_hits)
        self.assertGreater(score, 0)

    def test_negation_flips_positive_word(self):
        _, label, _, neg_hits = score_text(
            "Tidak bagus keputusan ini, sangat disayangkan")
        self.assertEqual(label, "negatif")
        self.assertIn("bagus", neg_hits)

    def test_intensifier_increases_magnitude(self):
        plain, _, _, _ = score_text("Saya senang")
        strong, _, _, _ = score_text("Saya sangat senang")
        self.assertGreater(strong, plain)


class TestTextUtils(unittest.TestCase):
    def test_stopwords_removed(self):
        tokens = content_tokens("yang dan di dalam negeri ini sangat besar",
                                load_stopwords())
        for word in ("yang", "dan", "di"):
            self.assertNotIn(word, tokens)

    def test_search_keywords_kept_in_raw_tokens(self):
        tokens = content_tokens("gibran mundur dari jabatan",
                                load_stopwords())
        self.assertIn("gibran", tokens)
        self.assertIn("mundur", tokens)


class TestDedup(unittest.TestCase):
    def test_dedup_keeps_highest_engagement(self):
        rows = [
            {"url": "https://x/1", "summary": "satu", "likes": "5",
             "comments_count": "1", "shares": ""},
            {"url": "https://x/1", "summary": "satu", "likes": "50",
             "comments_count": "2", "shares": ""},
            {"url": "https://x/2", "summary": "dua", "likes": "3",
             "comments_count": "0", "shares": ""},
        ]
        result = dedup_by(rows, lambda r: r["url"].strip().lower())
        self.assertEqual(len(result), 2)
        kept = [r for r in result if r["url"].endswith("/1")][0]
        self.assertEqual(kept["likes"], "50")


class TestDatasetIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean = read_csv("data/posts_clean.csv")
        cls.results = read_results()

    def test_required_columns(self):
        required = {"post_id", "platform", "url", "date_wib",
                    "sentiment_label", "sentiment_score", "analysis_text"}
        self.assertTrue(required.issubset(set(self.clean[0].keys())))

    def test_labels_within_allowed_set(self):
        labels = {r["sentiment_label"] for r in self.clean}
        self.assertTrue(labels.issubset({"positif", "negatif", "netral"}))

    def test_row_count_matches_results(self):
        self.assertEqual(len(self.clean),
                         self.results["total_posts_after_dedup"])

    def test_platform_counts_match_results(self):
        from collections import Counter
        counts = Counter(r["platform"] for r in self.clean)
        for platform, n in self.results["posts_per_platform"].items():
            self.assertEqual(counts[platform], n)

    def test_sentiment_counts_match_results(self):
        from collections import Counter
        counts = Counter(r["sentiment_label"] for r in self.clean)
        for label, entry in self.results["sentiment_overall"].items():
            self.assertEqual(counts[label], entry["count"])

    def test_labeled_sample_size_and_accuracy(self):
        sample = read_csv("data/labeled_sample.csv")
        self.assertGreaterEqual(len(sample), 100)
        correct = sum(1 for r in sample if r["match"] == "True")
        accuracy = round(100 * correct / len(sample), 2)
        self.assertEqual(accuracy, self.results["validation"]["accuracy_pct"])


class TestImpactIndicators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.indicators = {r["indicator"]: r
                          for r in read_csv("data/impact_indicators.csv")}
        with open(COMPANION_JSON, encoding="utf-8") as fh:
            cls.companion = json.load(fh)
        cls.results = read_results()

    def value(self, indicator):
        return float(self.indicators[indicator]["value"])

    def test_types_valid(self):
        for row in self.indicators.values():
            self.assertIn(row["type"], {"measured", "computed", "reported"})

    def test_ihsg_event_day_matches_companion(self):
        expected = self.companion["global_investor_decomposition"][
            "event_day_2026_11_12"]["ihsg_return_pct"]
        self.assertAlmostEqual(
            self.value("Perubahan IHSG pada hari pengunduran diri "
                       "(12 Nov 2026)"), expected, places=3)

    def test_ihsg_close_matches_companion(self):
        expected = self.companion["levels"]["ihsg_close_2026_11_12"]
        self.assertAlmostEqual(
            self.value("Level penutupan IHSG 12 Nov 2026"), expected,
            places=2)

    def test_eido_matches_companion(self):
        expected = self.companion["global_investor_decomposition"][
            "event_day_2026_11_12"]["eido_return_pct"]
        self.assertAlmostEqual(
            self.value("Perubahan EIDO (ETF Indonesia di AS) 12 Nov 2026"),
            expected, places=3)

    def test_residual_matches_companion(self):
        expected = self.companion["global_investor_decomposition"][
            "bracket_11nov_to_16nov"]["usdidr_residual_vs_dxy_pp"]
        self.assertAlmostEqual(
            self.value("Residu spesifik Indonesia USD/IDR vs DXY "
                       "(11 ke 16 Nov 2026)"), expected, places=3)

    def test_ma_window_matches_companion(self):
        expected = self.companion["events"]["ma_decision"]["series"][
            "ihsg"]["window_cumulative_change_pct"]
        self.assertAlmostEqual(
            self.value("Perubahan IHSG jendela putusan MA "
                       "(23 Okt ke 6 Nov 2026)"), expected, places=3)

    def test_ytd_matches_companion(self):
        expected = self.companion["context_ytd_to_2026_11_12_pct"]["ihsg"]
        self.assertAlmostEqual(
            self.value("Perubahan IHSG year to date ke 12 Nov 2026"),
            expected, places=3)

    def test_attention_rows_consistent_with_results(self):
        groups = self.results["attention_competition"]["groups"]
        for group in ("bencana", "harga", "ekonomi"):
            self.assertEqual(
                self.value(f"Postingan yang juga menyebut kelompok isu "
                           f"{group}"), groups[group]["count"])
            self.assertAlmostEqual(
                self.value(f"Porsi postingan yang juga menyebut kelompok "
                           f"isu {group}"), groups[group]["share_pct"],
                places=2)

    def test_measured_total_matches_results(self):
        self.assertEqual(
            self.value("Total postingan terkumpul setelah dedup"),
            self.results["total_posts_after_dedup"])


class TestPrediction(unittest.TestCase):
    def test_prediction_file_shape(self):
        rows = read_csv("data/prediction_sentiment.csv")
        self.assertEqual(len(rows), 42)
        dates = sorted({r["date"] for r in rows})
        self.assertEqual(dates[0], "2026-11-18")
        self.assertEqual(dates[-1], "2026-12-01")
        for row in rows:
            if "share" in row["metric"]:
                self.assertGreaterEqual(float(row["projected_value"]), 0)
                self.assertLessEqual(float(row["projected_value"]), 100)
            self.assertLessEqual(float(row["lower_band"]),
                                 float(row["projected_value"]) + 0.011)
            self.assertGreaterEqual(float(row["upper_band"]),
                                    float(row["projected_value"]) - 0.011)


class TestVisualFiles(unittest.TestCase):
    def test_charts_exist(self):
        for name in ("sentimen_per_platform.png", "volume_harian.png",
                     "engagement_per_sentimen.png",
                     "overlay_sentimen_pasar.png", "proyeksi_sentimen.png"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, "charts", name)),
                            name)

    def test_wordclouds_exist(self):
        for name in ("awan_kata_keseluruhan.png", "awan_kata_threads.png",
                     "awan_kata_instagram.png", "awan_kata_facebook.png",
                     "awan_kata_positif.png", "awan_kata_negatif.png",
                     "awan_kata_netral.png"):
            self.assertTrue(
                os.path.exists(os.path.join(ROOT, "wordclouds", name)), name)

    def test_readme_image_paths_exist(self):
        import re
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        refs = re.findall(r"\]\(([^)]+\.png)\)", readme)
        self.assertGreaterEqual(len(refs), 10)
        for ref in refs:
            self.assertTrue(os.path.exists(os.path.join(ROOT, ref)), ref)


if __name__ == "__main__":
    unittest.main()

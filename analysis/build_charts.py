#!/usr/bin/env python3
"""Bangun semua grafik project dari output/analysis_results.json.

Grafik:
- charts/sentimen_per_platform.png
- charts/volume_harian.png
- charts/engagement_per_sentimen.png
- charts/overlay_sentimen_pasar.png (memakai panel pasar project pendamping)
- charts/proyeksi_sentimen.png

Jalankan setelah run_analysis.py: python3 analysis/build_charts.py
"""

import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS = os.path.join(ROOT, "charts")
PANEL = os.path.expanduser(
    "~/workspace/marketshock-id-event-study/data/processed/market_daily.csv")

COLORS = {"positif": "#2e7d32", "negatif": "#c62828", "netral": "#757575"}
plt.rcParams.update({"font.size": 10, "axes.titlesize": 12,
                     "figure.dpi": 150})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, name))
    plt.close(fig)
    print("grafik:", name)


def main():
    with open(os.path.join(ROOT, "output", "analysis_results.json"),
              encoding="utf-8") as fh:
        res = json.load(fh)

    # 1. Sentimen per platform (batang bertumpuk)
    platforms = ["facebook", "instagram", "threads"]
    labels = ["positif", "negatif", "netral"]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    bottoms = [0, 0, 0]
    for label in labels:
        values = [res["sentiment_per_platform"][p][label]["count"]
                  for p in platforms]
        ax.bar(platforms, values, bottom=bottoms, color=COLORS[label],
               label=label.capitalize())
        bottoms = [b + v for b, v in zip(bottoms, values)]
    for i, p in enumerate(platforms):
        ax.text(i, bottoms[i] + 12, str(res["posts_per_platform"][p]),
                ha="center", fontweight="bold")
    ax.set_ylabel("Jumlah postingan")
    ax.set_title("Distribusi sentimen per platform (total tercantum di atas batang)")
    ax.legend()
    save(fig, "sentimen_per_platform.png")

    # 2. Volume harian
    dates = sorted(res["daily"])
    volumes = [res["daily"][d]["volume"] for d in dates]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.bar(range(len(dates)), volumes, color="#37474f", width=0.9)
    for event_date, text in (("2026-10-30", "Putusan MA\n30 Okt"),
                             ("2026-11-11", "Usulan HMP\n11 Nov"),
                             ("2026-11-12", "Pengunduran diri\n12 Nov")):
        if event_date in dates:
            ax.axvline(dates.index(event_date), color="#c62828", ls="--",
                       lw=1)
            ax.annotate(text, (dates.index(event_date),
                               max(volumes) * 0.92), fontsize=8,
                        color="#c62828", ha="center")
    ticks = list(range(0, len(dates), max(1, len(dates) // 14)))
    ax.set_xticks(ticks)
    ax.set_xticklabels([dates[i][5:] for i in ticks], rotation=45, ha="right",
                       fontsize=8)
    ax.set_ylabel("Postingan per hari")
    ax.set_title("Volume postingan per hari (tanggal WIB) pada sampel terkumpul")
    save(fig, "volume_harian.png")

    # 3. Engagement per kelas sentimen
    eng = res["engagement_by_sentiment"]
    classes = ["positif", "negatif", "netral"]
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    for ax, stat, title in ((axes[0], "mean", "Rata-rata"),
                            (axes[1], "median", "Median")):
        x = range(len(classes))
        likes = [eng[c]["likes"][stat] for c in classes]
        comments = [eng[c]["comments"][stat] for c in classes]
        ax.bar([i - 0.2 for i in x], likes, width=0.4, color="#1565c0",
               label="Likes")
        ax.bar([i + 0.2 for i in x], comments, width=0.4, color="#ef6c00",
               label="Komentar")
        ax.set_yscale("log")
        ax.set_xticks(list(x))
        ax.set_xticklabels([c.capitalize() for c in classes])
        ax.set_title(f"{title} likes dan komentar per kelas (skala log)")
        ax.legend()
    fig.suptitle("Engagement per kelas sentimen")
    save(fig, "engagement_per_sentimen.png")

    # 4. Overlay sentimen dan pasar, hari tumpang tindih November 2026
    market = {}
    with open(PANEL, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["date"].startswith("2026-11") and row["ihsg_close"]:
                market[row["date"]] = float(row["ihsg_close"])
    overlap = [d for d in sorted(market)
               if d in res["daily"] and d >= "2026-11-10"]
    fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), sharex=True)
    axes[0].plot(overlap, [market[d] for d in overlap], marker="o",
                 color="#1565c0")
    axes[0].set_ylabel("Penutupan IHSG")
    axes[0].set_title("Overlay sentimen publik dan IHSG, hari perdagangan "
                      "10 sampai 17 November 2026 yang tumpang tindih")
    axes[0].grid(alpha=0.3)
    axes[1].bar(overlap, [res["daily"][d]["volume"] for d in overlap],
                color="#90a4ae", label="Volume postingan")
    axes[1].plot(overlap,
                 [res["daily"][d]["negatif_share_pct"] for d in overlap],
                 marker="s", color="#c62828", label="Porsi negatif (%)")
    axes[1].set_ylabel("Volume dan porsi negatif (%)")
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    for label in axes[1].get_xticklabels():
        label.set_rotation(30)
        label.set_ha("right")
    save(fig, "overlay_sentimen_pasar.png")

    # 5. Proyeksi sentimen 14 hari
    pred = {}
    with open(os.path.join(ROOT, "data", "prediction_sentiment.csv"),
              encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            pred.setdefault(row["metric"], []).append(row)
    hist_dates = res["prediction"]["summary"]["volume"]["history_dates"]
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=False)
    hist_vol = res["prediction"]["summary"]["volume"]["history_values"]
    rows = pred["volume"]
    axes[0].plot(hist_dates, hist_vol, marker="o", color="#37474f",
                 label="Aktual sampel")
    axes[0].plot([r["date"] for r in rows],
                 [float(r["projected_value"]) for r in rows], marker="o",
                 color="#1565c0", label="Proyeksi Holt teredam")
    axes[0].fill_between([r["date"] for r in rows],
                         [float(r["lower_band"]) for r in rows],
                         [float(r["upper_band"]) for r in rows],
                         color="#1565c0", alpha=0.15,
                         label="Pita ketidakpastian")
    axes[0].set_ylabel("Postingan per hari")
    axes[0].set_title("Proyeksi volume postingan 14 hari (18 Nov sampai 1 Des 2026)")
    axes[0].legend(fontsize=8)
    axes[0].tick_params(axis="x", rotation=30, labelsize=8)
    for metric, color, label in (("negatif_share_pct", "#c62828", "Porsi negatif"),
                                 ("positif_share_pct", "#2e7d32", "Porsi positif")):
        hist = res["prediction"]["summary"][metric]["history_values"]
        rows = pred[metric]
        axes[1].plot(hist_dates, hist, marker="o", color=color,
                     label=f"{label} aktual")
        axes[1].plot([r["date"] for r in rows],
                     [float(r["projected_value"]) for r in rows], marker="o",
                     color=color, ls="--", label=f"{label} proyeksi")
        axes[1].fill_between([r["date"] for r in rows],
                             [float(r["lower_band"]) for r in rows],
                             [float(r["upper_band"]) for r in rows],
                             color=color, alpha=0.12)
    axes[1].set_ylabel("Porsi (%)")
    axes[1].set_title("Proyeksi porsi sentimen negatif dan positif")
    axes[1].legend(fontsize=8)
    axes[1].tick_params(axis="x", rotation=30, labelsize=8)
    save(fig, "proyeksi_sentimen.png")


if __name__ == "__main__":
    main()

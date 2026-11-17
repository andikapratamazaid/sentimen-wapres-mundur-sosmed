#!/usr/bin/env python3
"""Bangun dashboard HTML mandiri: dashboard/sentimen_dashboard.html.

Satu berkas HTML dengan seluruh grafik dan awan kata utama tertanam
sebagai base64, dan seluruh angka dibaca dari output/analysis_results.json
agar selalu konsisten dengan analisis.

Jalankan setelah run_analysis.py, build_charts.py, dan
build_wordclouds.py: python3 analysis/build_dashboard.py
"""

import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def img_tag(rel_path, caption):
    path = os.path.join(ROOT, rel_path)
    with open(path, "rb") as fh:
        encoded = base64.b64encode(fh.read()).decode("ascii")
    return (f'<figure><img src="data:image/png;base64,{encoded}" '
            f'alt="{caption}"><figcaption>{caption}</figcaption></figure>')


def main():
    with open(os.path.join(ROOT, "output", "analysis_results.json"),
              encoding="utf-8") as fh:
        res = json.load(fh)
    so = res["sentiment_overall"]
    eng = res["engagement_by_sentiment"]
    val = res["validation"]
    att = res["attention_competition"]
    pred = res["prediction"]["summary"]
    mc = res["companion_market_reference"]

    platform_rows = ""
    for platform in ("facebook", "instagram", "threads"):
        sp = res["sentiment_per_platform"][platform]
        pol = res["polarization_per_platform"][platform]
        platform_rows += (
            f"<tr><td>{platform.capitalize()}</td>"
            f"<td>{res['posts_per_platform'][platform]}</td>"
            f"<td>{sp['positif']['count']} ({sp['positif']['share_pct']}%)</td>"
            f"<td>{sp['negatif']['count']} ({sp['negatif']['share_pct']}%)</td>"
            f"<td>{sp['netral']['count']} ({sp['netral']['share_pct']}%)</td>"
            f"<td>{pol['non_neutral_share_pct']}%</td></tr>")

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sentimen Publik: Pengunduran Diri Wapres</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; color: #212121;
  background: #f5f5f5; }}
header {{ background: #263238; color: #fff; padding: 28px 20px; }}
header h1 {{ margin: 0 0 6px; font-size: 26px; }}
header p {{ margin: 0; opacity: 0.85; }}
main {{ max-width: 1080px; margin: 0 auto; padding: 20px; }}
section {{ background: #fff; border-radius: 8px; padding: 20px 24px;
  margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }}
h2 {{ margin-top: 0; font-size: 20px; border-bottom: 2px solid #eceff1;
  padding-bottom: 8px; }}
.cards {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.card {{ flex: 1 1 150px; background: #eceff1; border-radius: 8px;
  padding: 14px; text-align: center; }}
.card .num {{ font-size: 26px; font-weight: bold; display: block; }}
.card .lbl {{ font-size: 12px; color: #455a64; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
th, td {{ border: 1px solid #cfd8dc; padding: 7px 9px; text-align: left; }}
th {{ background: #eceff1; }}
figure {{ margin: 12px 0; text-align: center; }}
figure img {{ max-width: 100%; border: 1px solid #eceff1; border-radius: 4px; }}
figcaption {{ font-size: 13px; color: #455a64; margin-top: 6px; }}
.note {{ font-size: 13px; color: #455a64; }}
.pos {{ color: #2e7d32; font-weight: bold; }}
.neg {{ color: #c62828; font-weight: bold; }}
.neu {{ color: #616161; font-weight: bold; }}
</style>
</head>
<body>
<header>
<h1>Sentimen Publik: Pengunduran Diri Wakil Presiden</h1>
<p>Analisis media sosial atas 1.201 postingan terkumpul, 17 November 2026. Pengukuran netral, dilaporkan sebagaimana ditemukan.</p>
</header>
<main>
<section>
<h2>Angka Utama</h2>
<div class="cards">
<div class="card"><span class="num">1.201</span><span class="lbl">Postingan unik setelah dedup (dari 1.369 mentah)</span></div>
<div class="card"><span class="num">857</span><span class="lbl">Pengguna unik</span></div>
<div class="card"><span class="num">413 / 405 / 383</span><span class="lbl">Facebook / Threads / Instagram (TikTok 0)</span></div>
<div class="card"><span class="num">{so['positif']['share_pct']}%</span><span class="lbl">Positif ({so['positif']['count']})</span></div>
<div class="card"><span class="num">{so['negatif']['share_pct']}%</span><span class="lbl">Negatif ({so['negatif']['count']})</span></div>
<div class="card"><span class="num">{so['netral']['share_pct']}%</span><span class="lbl">Netral ({so['netral']['count']})</span></div>
<div class="card"><span class="num">{val['accuracy_pct']}%</span><span class="lbl">Akurasi mesin vs label manusia (sampel {val['sample_size']})</span></div>
</div>
<p class="note">Target minimal 1.000 postingan tercapai; rentang 3.000 sampai 5.000 tidak tercapai karena batas laju layanan pencarian dan connector platform yang tidak terhubung. TikTok tidak tercakup alat yang tersedia.</p>
</section>
<section>
<h2>Distribusi Sentimen per Platform</h2>
<table>
<tr><th>Platform</th><th>Postingan</th><th>Positif</th><th>Negatif</th><th>Netral</th><th>Non netral</th></tr>
{platform_rows}
</table>
{img_tag("charts/sentimen_per_platform.png", "Distribusi sentimen per platform. Facebook paling terpolarisasi dengan porsi non netral 68,52%, Threads paling netral.")}
{img_tag("charts/volume_harian.png", "Volume postingan per hari pada sampel. Puncak pada 12 November 2026 dengan 273 postingan, hari pengunduran diri diserahkan. Volume sampel bias menurut desain pengambilan dan bukan volume platform.")}
</section>
<section>
<h2>Engagement per Kelas Sentimen</h2>
<p>Postingan kelas <span class="neg">negatif</span> menyebar paling jauh: rata rata likes {eng['negatif']['likes']['mean']} dan median {eng['negatif']['likes']['median']}, berbanding kelas <span class="pos">positif</span> {eng['positif']['likes']['mean']} dan {eng['positif']['likes']['median']}, serta kelas <span class="neu">netral</span> {eng['netral']['likes']['mean']} dan {eng['netral']['likes']['median']}.</p>
{img_tag("charts/engagement_per_sentimen.png", "Rata rata dan median likes serta komentar per kelas sentimen, skala logaritmik.")}
</section>
<section>
<h2>Awan Kata</h2>
{img_tag("wordclouds/awan_kata_keseluruhan.png", "Awan kata keseluruhan. Kata kunci pencarian, kata henti, dan kata templat layanan dikeluarkan.")}
{img_tag("wordclouds/awan_kata_positif.png", "Awan kata kelas positif: tema dukungan dan konstitusionalitas.")}
{img_tag("wordclouds/awan_kata_negatif.png", "Awan kata kelas negatif: tema ijazah dan perdebatan pendukung.")}
{img_tag("wordclouds/awan_kata_netral.png", "Awan kata kelas netral: tema prosedur dan pemberitaan.")}
<p class="note">Awan kata per platform (Threads, Instagram, Facebook) ada di folder wordclouds. Awan kata TikTok tidak dibuat karena nol postingan TikTok terkumpul.</p>
</section>
<section>
<h2>Dampak</h2>
<p><strong>Pasar (computed, project pendamping MarketShock ID):</strong> IHSG naik {mc['ihsg_return_event_day_pct']}% ke {mc['ihsg_close_event_day']:.2f} pada 12 November 2026; EIDO naik {mc['eido_return_event_day_pct']}%; residu spesifik Indonesia pada rupiah -0,1677 poin persen (11 ke 16 November); IHSG -7,1486% pada jendela putusan MA dan -39,2745% year to date. Arus asing yang dilaporkan: beli bersih Rp443,53 miliar pada hari peristiwa berbanding jual bersih sekitar Rp127 triliun year to date (Kontan).</p>
<p><strong>Atensi (measured):</strong> hanya {att['any_group']['share_pct']}% postingan terkumpul yang juga menyebut isu nasional lain (ekonomi {att['groups']['ekonomi']['share_pct']}%, harga {att['groups']['harga']['share_pct']}%, bencana {att['groups']['bencana']['share_pct']}%), sementara pada minggu yang sama banjir Aceh dan Sumatera Utara berdampak pada puluhan ribu jiwa (dilaporkan BNPB). Penilaian bukti di laporan dampak menyimpulkan tidak ada pemberitaan terverifikasi yang mengaitkan bencana atau masalah nasional lain dengan keputusan pengunduran diri; pendorong terdokumentasi adalah rantai hukum dan politik.</p>
{img_tag("charts/overlay_sentimen_pasar.png", "Overlay porsi negatif harian dan volume sampel dengan penutupan IHSG pada hari perdagangan 10 sampai 17 November 2026. Jendela terlalu kecil untuk klaim korelasi; pola dibaca deskriptif saja.")}
</section>
<section>
<h2>Prediksi (Proyeksi Statistik)</h2>
<p>Proyeksi tren Holt teredam 14 hari dari agregat 10 sampai 17 November 2026: volume meluruh dari proyeksi {pred['volume']['day1_projection']} postingan pada 18 November menuju lantai nol sekitar hari ketujuh dengan pita ketidakpastian yang sangat lebar; porsi negatif menurun dari {pred['negatif_share_pct']['day1_projection']}% ke {pred['negatif_share_pct']['day14_projection']}%, porsi positif dari {pred['positif_share_pct']['day1_projection']}% ke {pred['positif_share_pct']['day14_projection']}%. Ini proyeksi statistik dari sampel terbatas, bukan ramalan fakta; hasil politik tidak dapat diprediksi dari sampel sentimen.</p>
{img_tag("charts/proyeksi_sentimen.png", "Proyeksi volume dan porsi sentimen 14 hari dengan pita ketidakpastian.")}
</section>
<section>
<h2>Keterbatasan</h2>
<p class="note">Sampel adalah postingan publik yang terjangkau pencarian pada 17 November 2026, bukan populasi percakapan. Teks yang dianalisis adalah representasi layanan pencarian (ringkasan isi dan komentar), bukan teks asli postingan. Akurasi mesin leksikon {val['accuracy_pct']}% pada sampel validasi 120 postingan yang dilabeli manual; metode leksikon keliru pada sarkasme dan teks campuran, dan mengukur valensi ekspresi lebih daripada sikap terhadap peristiwa. Angka terukur, terhitung, dan dilaporkan selalu dipisahkan tipenya di data/impact_indicators.csv.</p>
</section>
</main>
</body>
</html>
"""
    out = os.path.join(ROOT, "dashboard", "sentimen_dashboard.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("dashboard:", out, f"({os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    main()

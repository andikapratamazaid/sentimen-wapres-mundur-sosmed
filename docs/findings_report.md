# Laporan Temuan: Sentimen Publik atas Pengunduran Diri Wakil Presiden

Project: Sentimen Publik, Analisis Media Sosial Pengunduran Diri Wapres.
Tanggal analisis: 17 November 2026.
Seluruh angka pada laporan ini dihitung dari dataset terkumpul dan sama
dengan isi output/analysis_results.json.

## Pertanyaan penelitian

Bagaimana sentimen publik di media sosial terhadap pengunduran diri
Wakil Presiden Gibran Rakabuming Raka pada 12 November 2026, bagaimana
sebarannya antarplatform, tema apa yang mendominasi tiap kelas sentimen,
dan seberapa jauh tiap kelas sentimen menyebar bila diukur dari
engagement?

## Metode ringkas

Sebanyak 1.369 postingan mentah dikumpulkan pada 17 November 2026 dengan
layanan pencarian media sosial (28 panggilan, dihentikan setelah layanan
mengembalikan HTTP 429), lalu dideduplikasi menurut URL dan teks menjadi
1.201 postingan unik dari 857 pengguna unik: Facebook 413, Threads 405,
Instagram 383, TikTok 0 (tidak tercakup alat yang tersedia). Setiap
postingan diklasifikasikan oleh mesin sentimen leksikon Bahasa Indonesia
dengan penanganan negasi dan penguat, dilengkapi suplemen kata sentimen
Bahasa Inggris karena teks yang dianalisis adalah representasi layanan
yang berbahasa campuran. Label berarti sikap terhadap peristiwa
pengunduran diri. Validasi dilakukan terhadap 120 postingan sampel acak
yang dilabeli manual oleh pembaca manusia. Detail pengumpulan ada di
data/collection_notes.md.

## Deskripsi sampel

- Total setelah dedup: 1.201 postingan (target minimal 1.000 tercapai,
  rentang atas 3.000 sampai 5.000 tidak tercapai).
- Rentang tanggal: 4 Mei 2026 sampai 17 November 2026 (WIB). Konsentrasi
  sampel berada pada 10 sampai 17 November 2026 (898 postingan), sesuai
  desain pengambilan yang menargetkan jendela peristiwa.
- Volume harian tertinggi pada sampel: 12 November 2026 dengan
  273 postingan, diikuti 13 November (131) dan 10 November (128, hari
  niat mundur pertama kali dilaporkan).

## Hasil sentimen

Distribusi keseluruhan menurut mesin leksikon:

| Kelas | Jumlah | Porsi |
|---|---|---|
| Positif | 205 | 17,07% |
| Negatif | 431 | 35,89% |
| Netral | 565 | 47,04% |

Per platform:

| Platform | Positif | Negatif | Netral | Porsi non netral |
|---|---|---|---|---|
| Facebook (413) | 103 (24,94%) | 180 (43,58%) | 130 (31,48%) | 68,52% |
| Instagram (383) | 67 (17,49%) | 148 (38,64%) | 168 (43,86%) | 56,14% |
| Threads (405) | 35 (8,64%) | 103 (25,43%) | 267 (65,93%) | 34,07% |

Facebook adalah platform paling terpolarisasi pada sampel ini dan
Threads paling netral, sebagian karena Threads didominasi tautan berita
tanpa komentar. Rasio positif terhadap negatif keseluruhan adalah 0,48
(205 berbanding 431): di antara postingan yang berpendirian, nada negatif
menurut valensi teks kira kira dua kali nada positif. Makna label perlu
dibaca bersama hasil validasi di bawah, karena mesin menilai valensi
ekspresi, bukan sikap terhadap peristiwa secara sempurna.

## Bacaan awan kata dan tema

Kata dominan keseluruhan (setelah kata henti, kata kunci pencarian, dan
kata templat layanan dikeluarkan): president, political, prabowo,
indonesian, vice, mpr, news, dpr, jokowi, court, diploma, letter, debate,
impeachment, polarized, support, replacement, supreme, certificate,
education, legitimacy. Kata mentah terbanyak pada tabel frekuensi adalah
gibran (5.225 kemunculan), diikuti political (2.050) dan president
(1.798). Bigram terbanyak: "vice president" (1.190) dan "gibran
rakabuming" (731); bigram isi yang menonjol antara lain "supreme court"
(244) dan "constitutional court".

Tema per kelas sentimen, dari frekuensi kata dan bigram kelas tersebut:

- Positif: kata support, constitutional, debate, dan bigram "president
  prabowo" serta "constitutional court" menonjol. Kelas ini berisi
  dukungan pada langkah mundur sebagai keputusan yang terhormat dan
  sesuai konstitusi, termasuk pernyataan resmi partai dan warganet yang
  memuji keberanian langkah tersebut.
- Negatif: kata diploma, jokowi, court, polarized, dan bigram "comment
  section" serta "highly polarized" menonjol. Kelas ini didominasi
  ekspresi emosi negatif dalam perdebatan: kemarahan pendukung yang
  merasa dikhianati, serangan terhadap kredensial pendidikan, dan saling
  serang antarpendukung. Kata diploma adalah penanda tema ijazah yang
  menjadi latar hukum peristiwa ini.
- Netral: kata letter, mpr, article, dan bigram "people consultative"
  serta "consultative assembly" menonjol. Kelas ini didominasi
  pemberitaan faktual tentang surat pengunduran diri, mekanisme MPR,
  jadwal sidang, dan spekulasi pengganti.

Tema narasi yang berulang lintas kelas: (1) isu ijazah dan surat
keterangan penyetaraan yang dibatalkan Mahkamah Agung; (2) proses
pemakzulan dan usulan Hak Menyatakan Pendapat; (3) spekulasi pengganti
(nama nama yang beredar dalam pemberitaan antara lain Sufmi Dasco Ahmad
dan Puan Maharani, sebagai spekulasi yang diberitakan, bukan nominasi
resmi); (4) konten hoaks, terlihat dari postingan cek fakta pada sampel
Mei 2026 dan September sampai Oktober 2026; (5) rasa dikhianati pemilih
yang mengaku memilih pasangan ini karena sosok wakilnya.

## Temuan engagement

Postingan kelas negatif menyebar paling jauh pada sampel ini:

| Kelas | Rata rata likes | Median likes | Rata rata komentar | Median komentar | Total likes |
|---|---|---|---|---|---|
| Positif | 5.341 | 450 | 732 | 100 | 1.036.185 |
| Negatif | 9.799 | 1.300 | 825 | 230 | 4.086.142 |
| Netral | 2.338 | 19 | 196 | 8 | 1.070.656 |

Rata rata likes postingan negatif kira kira 1,8 kali postingan positif
dan 4,2 kali postingan netral; mediannya bahkan lebih timpang (1.300
berbanding 450 dan 19). Konten bermuatan emosi negatif, termasuk
perdebatan sengit di kolom komentar, menarik interaksi jauh lebih besar
daripada pemberitaan netral.

## Validasi mesin sentimen

Dari 120 postingan sampel acak yang dilabeli manual, mesin benar pada
63 postingan: akurasi 52,5%. Per kelas: positif 36,7% (11 dari 30),
negatif 75,0% (3 dari 4), netral 57,0% (49 dari 86). Pola kesalahan
terbesar adalah postingan yang oleh manusia dinilai netral tetapi oleh
mesin dinilai negatif (23 kasus) atau positif (14 kasus), dan postingan
yang oleh manusia dinilai positif (menyambut atau menuntut pengunduran
diri) tetapi oleh mesin dinilai negatif (12 kasus), karena teksnya penuh
kata emosi negatif yang diarahkan ke sosok atau prosesnya, bukan ke
peristiwa mundurnya. Angka ini dilaporkan apa adanya: distribusi
sentimen pada laporan ini adalah keluaran mesin leksikon dengan tingkat
kesalahan yang terukur di atas, dan paling aman dibaca sebagai peta
valensi ekspresi publik, bukan penghitungan sikap yang presisi.

## Keterbatasan

1. Sampling: postingan publik yang terjangkau pencarian pada satu hari
   pengumpulan, bukan populasi percakapan. Distribusi tanggal bias
   menurut desain pengambilan; volume harian bukan volume platform.
2. Representasi teks: yang dianalisis adalah ringkasan isi dan ringkasan
   komentar dari layanan pencarian, bukan teks asli postingan.
3. Akurasi leksikon 52,5% pada sampel validasi; metode leksikon keliru
   pada sarkasme, teks campuran, dan ekspresi emosi yang targetnya bukan
   peristiwa pengunduran diri itu sendiri.
4. Ketidakseimbangan platform: TikTok nol postingan, dan Facebook tidak
   menyediakan handle penulis pada keluaran layanan (identitas memakai
   nama penulis atau segmen URL).
5. Angka engagement adalah angka pada saat pengumpulan menurut layanan;
   sebagian postingan tidak memiliki angka likes atau komentar.

## Kesimpulan netral

Pada sampel 1.201 postingan yang terkumpul, pemberitaan netral adalah
kelas terbesar (47,04%), diikuti ekspresi negatif (35,89%) dan positif
(17,07%). Facebook paling terpolarisasi, Threads paling netral.
Percakapan didominasi tema ijazah, proses konstitusi, dan spekulasi
pengganti, dan postingan kelas negatif memperoleh engagement tertinggi.
Pengukuran ini tidak mengambil posisi atas peristiwa tersebut; ia
melaporkan distribusi sebagaimana ditemukan, dengan keterbatasan metode
yang dinyatakan terbuka. Analisis dampak kuantitatif, termasuk hubungan
dengan pasar dan dengan masalah nasional lain, dibahas di
docs/impact_analysis.md, dan proyeksi statistik di
docs/prediction_outlook.md.

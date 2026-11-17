# Catatan Pengumpulan Data

Tanggal pengumpulan: 17 November 2026.
Project: Sentimen Publik, Analisis Media Sosial Pengunduran Diri Wapres.

## Alat yang digunakan

Satu satunya alat yang benar benar mengembalikan postingan adalah layanan
pencarian media sosial (social.search), dengan kata kunci seputar
pengunduran diri Wakil Presiden Gibran Rakabuming Raka. Sebanyak 28
panggilan pencarian berhasil dijalankan sebelum layanan mengembalikan
HTTP 429 (batas laju); setelah itu pengumpulan dari sumber ini dihentikan
permanen sesuai aturan batas laju, tanpa percobaan ulang.

Faset pencarian yang dipakai antara lain: cakupan umum sejak 11 Nov 2026;
isu ijazah dan pemakzulan sejak 30 Okt 2026; pengganti dan reaksi sejak
13 Nov 2026; recency sejak 12 Nov 2026; jendela hoaks 25 Sep sampai
31 Okt 2026; jendela hoaks Mei 2026; isu gentleman agreement dan dinasti;
proses MPR dan pengganti sejak 14 Nov 2026; faset pasar; dan jendela
1 Okt sampai 10 Nov 2026.

Connector Threads, Instagram, dan Facebook diperiksa terlebih dahulu
sesuai dokumentasinya, tetapi ketiganya tidak terhubung pada lingkungan
ini (daftar akun kosong), sehingga CLI connector tidak dapat dipakai.
TikTok tidak memiliki connector dan tidak dicakup oleh layanan pencarian
(platform yang dicakup hanya Facebook, Instagram, dan Threads), sehingga
TikTok adalah platform yang paling tidak tercakup dalam project ini:
nol postingan TikTok terkumpul. Pencarian web mengonfirmasi konten TikTok
tentang peristiwa ini memang ada, tetapi dataset terstruktur TikTok tidak
dapat dikumpulkan dengan alat yang tersedia. Awan kata TikTok tidak
dibuat karena tidak ada datanya.

## Hitungan

| Tahap | Facebook | Instagram | Threads | TikTok | Total |
|---|---|---|---|---|---|
| Mentah terkumpul | 484 | 432 | 453 | 0 | 1.369 |
| Setelah dedup URL dan teks | 413 | 383 | 405 | 0 | 1.201 |

- URL unik pada data mentah: 1.201. Deduplikasi kedua menurut teks
  ternormalisasi tidak menghapus tambahan apa pun karena ringkasan
  layanan untuk postingan yang sama selalu identik per URL.
- Pengguna unik teridentifikasi: 857, dihitung dari handle, atau nama
  penulis, atau segmen URL halaman untuk Facebook, digabung per platform.
- Rentang tanggal postingan (WIB): 4 Mei 2026 sampai 17 November 2026.
- Postingan yang memiliki angka likes: 1.233 dari 1.369 mentah.
  Postingan yang memiliki angka komentar: 1.060. Postingan yang memiliki
  ringkasan komentar: 642.
- Berkas keluaran pengumpulan: data/posts_raw.csv (1.369 baris) dan
  output/collection_manifest.json (daftar berkas sumber per panggilan).

Target awal adalah minimal 1.000 postingan dengan rentang 3.000 sampai
5.000. Target minimal tercapai (1.201 postingan unik), tetapi rentang
atas tidak tercapai karena batas laju layanan dan tidak terhubungnya
connector platform. Angka ini dilaporkan apa adanya.

## Representasi teks yang dianalisis

Teks yang dianalisis untuk setiap postingan adalah gabungan tiga unsur
yang dikembalikan layanan pencarian untuk postingan tersebut: ringkasan
isi (kolom summary), ringkasan komentar publik (comment_summary), dan
fokus reaksi (focus). Ringkasan ditulis layanan sebagian besar dalam
Bahasa Inggris dan bercampur dengan kutipan verbatim komentar publik
dalam Bahasa Indonesia. Ini adalah keterbatasan mendasar representasi
data: yang diukur adalah sentimen sebagaimana terepresentasi dalam
keluaran layanan, bukan teks asli postingan kata per kata. Karena itu
leksikon sentimen dilengkapi suplemen kata Bahasa Inggris di samping
leksikon inti Bahasa Indonesia, dan frasa templat ringkasan layanan
(misalnya "overall tone" dan "culture moment") dikeluarkan dari awan
kata sebagai artefak representasi, walaupun tetap tercatat di tabel
frekuensi mentah.

Label sentimen bawaan layanan (provider_sentiment_label) disimpan di
data mentah hanya sebagai referensi dan tidak dipakai sebagai label
analisis; label analisis dihasilkan mesin leksikon project ini.

## Keterbatasan sampling

Sampel ini adalah postingan publik yang terjangkau pencarian pada
17 November 2026, bukan populasi seluruh percakapan media sosial tentang
peristiwa ini. Pencarian menargetkan jendela dan faset tertentu, sehingga
distribusi tanggal sampel bias menurut desain pengambilan: hari hari di
sekitar peristiwa (10 sampai 17 November 2026) jauh lebih padat daripada
hari lain, dan 17 November adalah hari parsial karena pengumpulan
dilakukan pada hari itu. Volume harian pada sampel tidak boleh dibaca
sebagai volume percakapan platform yang sebenarnya. Postingan yang sudah
dihapus, akun privat, dan konten yang tidak terindeks layanan tidak
masuk sampel.

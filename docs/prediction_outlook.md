# Prospek Prediksi: Proyeksi Statistik Sentimen dan Atensi

Dokumen ini adalah modul prediksi project Sentimen Publik. Bingkai
wajibnya dinyatakan di awal: angka angka di sini adalah proyeksi
statistik dari sampel yang terbatas, bukan ramalan fakta. Hasil politik
tidak dapat diprediksi secara andal dari sampel sentimen media sosial.
Modul ini mendemonstrasikan metode peramalan deret waktu dan cara
membaca ketidakpastiannya, bukan mengklaim kemampuan meramal.

## Metode

Agregat harian project ini (volume postingan, porsi negatif, porsi
positif) selama jendela peristiwa 10 sampai 17 November 2026 diproyeksi
14 hari ke depan (18 November sampai 1 Desember 2026) dengan tren linear
Holt teredam (alpha 0,5, beta 0,3, phi 0,8), diimplementasikan dengan
pustaka standar Python di analysis/run_analysis.py. Peredaman dipilih
karena deretnya pendek dan berbentuk lonjakan peristiwa yang meluruh.
Pita ketidakpastian adalah 1,96 kali simpangan baku residual satu
langkah dikali akar horizon; porsi diklip ke rentang 0 sampai 100 dan
volume ke minimum nol. Nilai harian lengkap ada di
data/prediction_sentiment.csv dan grafiknya di
charts/proyeksi_sentimen.png.

Dua kaveat metode yang menentukan cara membaca hasil: (1) deret masukan
hanya delapan titik dan hari terakhir (17 November) adalah hari parsial
pengumpulan; (2) volume sampel bias menurut desain pengambilan, sehingga
yang diproyeksi adalah pola peluruhan atensi pada sampel semacam ini,
bukan volume percakapan platform yang sebenarnya.

## Hasil proyeksi

| Metrik | Aktual 17 Nov | Proyeksi 18 Nov | Proyeksi 24 Nov | Proyeksi 1 Des |
|---|---|---|---|---|
| Volume postingan per hari | 29 | 35,95 | 0,00 | 0,00 |
| Porsi negatif | 17,24% | 17,32% | 10,26% | 8,28% |
| Porsi positif | 10,34% | 12,34% | 9,05% | 8,12% |

Bacaan: proyeksi titik volume meluruh cepat dan mencapai lantai nol
sekitar hari ketujuh, pola khas lonjakan atensi peristiwa yang telah
lewat. Namun simpangan baku residual volume sangat besar (83,95
postingan), sehingga pita atas ketidakpastian tetap berada di kisaran
ratusan postingan per hari: model pada dasarnya mengatakan atensi
kemungkinan besar meluruh, tetapi lonjakan ulang tidak dapat disingkirkan.
Porsi negatif diproyeksikan menurun bertahap dari sekitar 17% ke sekitar
8%, dan porsi positif menurun lebih landai dari sekitar 12% ke sekitar
8%. Dengan kata lain, arah yang diproyeksikan adalah percakapan yang
menyusut dan menenang, dengan ketidakpastian yang lebar.

## Skenario milestone jendela 60 hari

Tiga skenario berikut bukan ramalan; masing masing adalah pola yang
diharapkan bila milestone tertentu terjadi, didasarkan pada cara data
terkumpul berperilaku di sekitar milestone yang sudah teramati
(gelombang hoaks, putusan MA, dan hari pengunduran diri).

1. Pengganti diumumkan cepat (sidang MPR awal Desember 2026 berjalan
   sesuai jadwal yang diberitakan). Pola yang diharapkan meniru hari
   pengunduran diri: lonjakan volume satu sampai dua hari, porsi netral
   naik karena pemberitaan prosedural mendominasi, dan tema spekulasi
   pengganti bergeser menjadi tema sosok terpilih. Atensi kemudian
   meluruh seperti proyeksi dasar.
2. Proses berjalan penuh sampai tenggat sekitar 11 Januari 2027.
   Pola yang diharapkan: volume dasar rendah dengan lonjakan kecil
   berulang pada setiap perkembangan prosedural (pengajuan dua nama,
   rapat gabungan, penjadwalan ulang), mirip pola hari hari menjelang
   10 November pada sampel. Porsi negatif cenderung naik perlahan pada
   fase tanpa kepastian, meniru kenaikan nada negatif pada jendela
   putusan MA.
3. Gelombang hoaks atau kontroversi baru. Pola yang diharapkan meniru
   gelombang Mei 2026 dan September sampai Oktober 2026: klaim lama
   beredar ulang, postingan cek fakta muncul, volume naik tajam dalam
   satu dua hari dengan porsi negatif yang tinggi dan tema
   ketidakpercayaan, lalu mereda setelah bantahan resmi beredar. Pada
   sampel, gelombang hoaks justru mendahului dan membentuk respons
   publik terhadap peristiwa aslinya, jadi skenario ini bukan
   kemungkinan pinggiran.

## Yang perlu dipantau

- Waktu pengumuman pengganti: semakin dekat ke awal jendela 60 hari,
  semakin pola skenario 1 yang berlaku; keterlambatan berulang adalah
  sinyal skenario 2.
- Arah arus modal asing: project pendamping mencatat beli bersih
  Rp443,53 miliar pada hari pengunduran diri berbanding jual bersih
  sekitar Rp127 triliun year to date (reported, Kontan). Kelanjutan
  beli bersih atau kembalinya jual bersih adalah indikator penerimaan
  pasar atas proses suksesi.
- Level rupiah: spot yang dilaporkan Rp18.216 per USD pada 12 November
  2026 dan residu spesifik Indonesia -0,1677 poin persen pada
  dekomposisi project pendamping adalah titik berangkatnya; pelemahan
  rupiah yang menyimpang dari gerak dolar global pada hari hari
  milestone adalah sinyal tekanan khusus Indonesia.
- Beredarnya ulang klaim hoaks lama, yang pada dua gelombang sebelumnya
  selalu mendahului lonjakan atensi.

## Batasan

Proyeksi ini dihitung dari delapan titik agregat harian sebuah sampel
pencarian yang bias menurut desain, dengan akurasi mesin sentimen
52,5% pada validasi. Ia berguna sebagai demonstrasi metode dan sebagai
kerangka skenario untuk membaca perkembangan berikutnya. Ia tidak
berguna sebagai ramalan hasil politik, dan tidak boleh dikutip sebagai
satu.

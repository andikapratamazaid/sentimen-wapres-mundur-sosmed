# Analisis Dampak Pengunduran Diri Wakil Presiden

Dokumen ini adalah lapisan dampak dari project Sentimen Publik. Semua
angka diberi tipe yang disiplin di data/impact_indicators.csv:

- measured: diukur langsung dari dataset postingan project ini.
- computed: dihitung oleh project pendamping MarketShock ID dari data
  pasar Yahoo Finance; project ini tidak mengunduh ulang data pasar.
- reported: dilaporkan outlet atau lembaga bernama, dikutip apa adanya.

Tidak ada angka yang dicampur antar tipe tanpa label.

## 1. Dampak pasar dan ekonomi (computed dan reported)

Angka pada bagian ini adalah hasil project pendamping MarketShock ID,
event study atas data pasar asli, dan dikutip persis dari keluaran
project tersebut:

- Pada hari pengunduran diri, Kamis 12 November 2026, IHSG naik 2,6561%
  dan ditutup pada 5.250,895 (computed). Kenaikan ini terverifikasi
  silang dengan pemberitaan hari yang sama (5.250,90 dan naik 2,66%).
- EIDO, ETF saham Indonesia yang diperdagangkan di Amerika Serikat, naik
  2,5465% pada hari yang sama (computed): investor global bergerak
  searah dengan investor domestik.
- Pada hari usulan Hak Menyatakan Pendapat, 11 November 2026, IHSG
  berubah -0,2086% (computed): pasar nyaris tidak bergerak pada eskalasi
  politik itu sendiri, dan bereaksi pada kepastian resolusi sehari
  sesudahnya.
- Pada jendela putusan kasasi Mahkamah Agung (23 Oktober sampai
  6 November 2026), IHSG berubah -7,1486% (computed): tekanan pasar
  terbesar pada rangkaian ini terjadi pada fase ketidakpastian hukum,
  bukan pada hari pengunduran diri.
- Secara year to date sampai 12 November 2026, IHSG berubah -39,2745%
  (computed): peristiwa ini terjadi di tengah pasar yang sudah tertekan
  dalam.
- Yield US Treasury 10 tahun naik 10,5 basis poin pada 12 November 2026
  ke 5,103% (computed), sehingga sebagian iklim hari itu adalah faktor
  global, bukan khusus Indonesia.
- Dekomposisi 11 ke 16 November 2026: USD/IDR berubah +0,4542% dan
  indeks dolar DXY +0,6219%, menghasilkan residu spesifik Indonesia
  -0,1677 poin persen (computed). Artinya pelemahan rupiah pada jendela
  itu sedikit lebih kecil daripada yang dijelaskan dolar global, tetapi
  rupiah tetap berada di sekitar level terlemahnya (kurs spot yang
  dilaporkan pada 12 November 2026 adalah Rp18.216 per USD, reported,
  Suara.com).
- Arus asing yang dilaporkan: beli bersih Rp443,53 miliar pada
  12 November 2026, berbanding jual bersih sekitar Rp127 triliun secara
  year to date (reported, Kontan). Yield SBN 10 tahun dilaporkan 7,63%
  (reported, Bareksa).

Bacaan yang didukung angka: pasar saham menyambut resolusi ketidakpastian
dengan kenaikan tajam satu hari, sementara tekanan pada rupiah dan
posisi year to date yang dalam adalah konteks yang lebih besar daripada
peristiwa satu hari ini. Ada confounder yang dinyatakan eksplisit oleh
project pendamping: pengumuman review MSCI terjadi pada hari yang sama.

## 2. Overlay sentimen publik dan pasar (measured dan computed)

Grafik charts/overlay_sentimen_pasar.png menumpuk agregat harian project
ini dengan penutupan IHSG pada enam hari perdagangan yang tumpang tindih
(10, 11, 12, 13, 16, dan 17 November 2026). Pola yang terlihat secara
deskriptif:

- Volume sampel memuncak pada 12 November (273 postingan) tepat pada
  hari IHSG naik 2,6561%.
- Porsi negatif harian menurun sepanjang jendela: 40,62% (10 November),
  40,43% (11 November), 36,26% (12 November), 32,06% (13 November),
  16,46% (16 November), 17,24% (17 November), sementara IHSG naik dari
  5.115,04 (11 November) ke 5.250,90 (12 November) dan 5.344,41
  (13 November).

Jendela tumpang tindih hanya enam hari perdagangan dan volume sampel
bias menurut desain pengambilan, jadi sampel ini terlalu kecil untuk
klaim korelasi, apalagi kausalitas. Yang dilaporkan di sini hanyalah
kebersamaan waktu: atensi publik memuncak dan nada negatif menurun pada
hari hari ketika pasar naik. Tidak ada inferensi sebab akibat yang
dibuat.

## 3. Dampak atensi dan wacana publik (measured)

- Polarisasi per platform: porsi postingan non netral adalah 68,52% di
  Facebook, 56,14% di Instagram, dan 34,07% di Threads. Rasio positif
  terhadap negatif: Facebook 0,57, Instagram 0,45, Threads 0,34.
- Asimetri engagement: postingan kelas negatif memperoleh rata rata
  9.799 likes dan median 1.300, berbanding positif 5.341 dan 450, serta
  netral 2.338 dan 19. Konten bermuatan emosi negatif berjalan paling
  jauh dalam sampel ini.
- Tema narasi dominan per kelas, dari frekuensi kata dan bigram: kelas
  positif bertema dukungan dan konstitusionalitas (support,
  constitutional court); kelas negatif bertema ijazah dan perdebatan
  pendukung (diploma, jokowi, highly polarized); kelas netral bertema
  prosedur (letter, mpr, consultative assembly). Tema lintas kelas:
  ijazah dan suket, pemakzulan dan Hak Menyatakan Pendapat, spekulasi
  pengganti, dan rasa dikhianati pemilih.
- Dimensi hoaks: peristiwa yang benar benar terjadi pada 12 November
  2026 ini didahului versi palsunya sendiri. Klaim pengunduran diri yang
  sama beredar sebagai hoaks pada Mei 2026 dan lagi pada September
  sampai Oktober 2026 dengan memakai video lama pengunduran dirinya
  sebagai Wali Kota Solo (16 Juli 2024). Garis waktu cek fakta yang
  terverifikasi: bantahan Jabar Saber Hoaks atas video TikTok
  (29 Mei 2026), cek fakta Kompas.com (30 September 2026), bantahan
  Tribrata News Polri (13 Oktober 2026), dan cek fakta Klinik Hoaks
  Jatim atas peredaran ulang akhir September 2026. Sampel project ini
  memuat postingan cek fakta dari kedua gelombang itu. Akibat yang
  terukur dari pola ini: sebagian publik menyambut peristiwa aslinya
  dengan ketidakpercayaan awal, karena klaim yang identik sudah dua
  kali dinyatakan palsu.

## 4. Interaksi dengan masalah nasional lain

### 4.1 Kompetisi atensi yang terukur dari dataset ini (measured)

Di dalam 1.201 postingan terkumpul, penyebutan masalah nasional lain
dihitung dengan kelompok kata kunci yang didefinisikan di
analysis/run_analysis.py: bencana (bencana, banjir, gempa, longsor,
erupsi), harga (harga, bbm, sembako), dan ekonomi (ekonomi, rupiah,
pengangguran). Hasilnya:

| Kelompok isu | Postingan | Porsi |
|---|---|---|
| Ekonomi | 38 | 3,16% |
| Harga | 6 | 0,50% |
| Bencana | 1 | 0,08% |
| Salah satu kelompok di atas | 44 | 3,66% |

Per platform, kelompok ekonomi disebut pada 4,44% postingan Instagram,
2,91% Facebook, dan 2,22% Threads; kelompok bencana hanya muncul pada
satu postingan Facebook. Di dalam percakapan yang terkumpul tentang
pengunduran diri ini, isu lain nyaris tidak ikut dibicarakan: atensi di
dalam korpus ini terfokus hampir sepenuhnya pada peristiwa politiknya.
Kaveat yang wajib menyertai angka ini: korpus dikumpulkan dengan kata
kunci pengunduran diri, jadi porsi di atas mengukur kebersamaan
penyebutan di dalam percakapan ini, bukan pangsa atensi publik secara
keseluruhan di platform. Di luar korpus ini, bencana dan tekanan ekonomi
memiliki percakapannya sendiri yang besar, sebagaimana konteks berikut.

### 4.2 Konteks masalah bersamaan (reported)

Fakta berikut dilaporkan lembaga dan outlet bernama, dan dicatat sebagai
baris reported di data/impact_indicators.csv:

- Banjir dan longsor Aceh dan Sumatera Utara pada 12 sampai 15 November
  2026, dipicu bibit siklon 92B dan 96S menurut BMKG: Aceh Tamiang
  18.158 jiwa terdampak dan 5.088 mengungsi (BNPB per 15 November 2026);
  Subulussalam 7.703 jiwa terdampak dengan status tanggap darurat
  6 sampai 19 November; Langkat 3.155 jiwa terdampak pada 12 November
  2026 pukul 06.26 WIB. Longsor juga dilaporkan di Hulu Sungai Selatan
  (12 November) dan Tasikmalaya (14 November), serta kebakaran hutan dan
  lahan di Morowali Utara dan Konawe.
- Tiga gunung api berstatus Siaga Level III pada jendela yang sama:
  Anak Krakatau, Merapi, dan Semeru (PVMBG per 11 November 2026).
  Semeru mengalami erupsi pada 16 dan 17 Oktober 2026 dan awan panas
  pada 6 November 2026.
- Gempa Laut Banda bermagnitudo awal 7,1 yang dimutakhirkan menjadi 6,8
  terjadi pada 17 November 2026 pukul 04.11 WIB, tanpa potensi tsunami
  dan tanpa laporan korban atau kerusakan (BMKG). Peristiwa ini
  sepenuhnya terjadi setelah pengunduran diri.
- Tekanan ekonomi yang bersamaan: rupiah di sekitar Rp18.216 per USD
  (reported, Suara.com) dan IHSG turun 39,2745% year to date sampai
  12 November 2026 (computed, project pendamping).

### 4.3 Bacaan gabungan (netral dan analitis)

Data menunjukkan dua hal yang berjalan bersamaan, tanpa menilai kinerja
pihak mana pun: pertama, proses suksesi wakil presiden selama 60 hari
berjalan pada minggu yang sama dengan tanggap darurat banjir di Aceh
dan Sumatera Utara, tiga gunung berstatus Siaga, dan rupiah di level
terlemahnya; atensi negara, anggaran tanggap darurat, dan fokus publik
dengan sendirinya terbagi. Kedua, di dalam percakapan media sosial yang
terkumpul tentang pengunduran diri, pembagian atensi itu nyaris tidak
tercermin: hanya 3,66% postingan yang menyebut isu lain sama sekali.
Kesenjangan antara kebersamaan peristiwa di lapangan dan keterpisahan
percakapannya di media sosial adalah temuan deskriptifnya; penjelasan
sebabnya berada di luar data project ini.

## 5. Penilaian bukti: apakah masalah nasional lain memengaruhi pengunduran diri

Bagian ini menilai satu pertanyaan spesifik dengan bukti yang tersedia:
apakah bencana atau masalah nasional lain memengaruhi keputusan
pengunduran diri.

### Uji linimasa

Rantai keputusan yang terdokumentasi adalah rantai hukum dan politik:
(1) putusan kasasi Mahkamah Agung No. 742 K/TUN/2026 pada 30 Oktober
2026 membatalkan surat penyetaraan pendidikan; (2) pencabutan surat
oleh kementerian dan usulan Hak Menyatakan Pendapat oleh 120 anggota
DPR dari 8 fraksi pada 11 November 2026; (3) pengunduran diri diserahkan
pada 12 November 2026. Niat mundur dilaporkan sudah disampaikan kepada
Presiden pada pagi 10 November 2026. Terhadap linimasa ini, eskalasi
bencana pada jendela yang sama sebagian besar terjadi bersamaan atau
sesudahnya: banjir Langkat tercatat 12 November pukul 06.26 WIB, data
besar banjir Aceh terkonsolidasi 12 sampai 15 November, status Siaga
tiga gunung ditegaskan 11 sampai 13 November, dan gempa Laut Banda
terjadi 17 November, lima hari setelah pengunduran diri. Tidak ada
eskalasi bencana yang mendahului dan berimpitan dengan titik keputusan
10 sampai 12 November dengan cara yang menunjukkan kaitan.

### Alasan yang dinyatakan sendiri

Dalam pernyataan videonya pada 12 November 2026, Gibran menyebut
keputusan ini sebagai keputusan pribadi dan secara eksplisit menyatakan
keputusan tersebut tidak berkaitan dengan persoalan ijazah (dilaporkan
media, antara lain AMS News, 12 November 2026, dan dikutip afu.id serta
journalarta). Pernyataan ini dicatat sebagai pernyataan yang dilaporkan,
bukan sebagai fakta yang diverifikasi project ini.

### Kesimpulan penilaian

Dinyatakan apa adanya dan dibatasi bukti: tidak ada pemberitaan
terverifikasi yang mengaitkan bencana atau masalah nasional lain dengan
keputusan pengunduran diri ini. Pendorong yang terdokumentasi adalah
rantai hukum dan politik di atas, dari putusan Mahkamah Agung sampai
usulan Hak Menyatakan Pendapat. Masalah nasional lain berfungsi sebagai
konteks yang melingkupi peristiwa ini, yaitu konteks atensi publik dan
kapasitas negara pada minggu yang sama, bukan sebagai sebab yang
diberitakan. Apabila di kemudian hari muncul laporan kredibel yang
menunjukkan kaitan sebab, kesimpulan ini perlu direvisi mengikuti bukti
baru tersebut.

## 6. Linimasa dampak institusional (faktual)

- 12 November 2026: surat pengunduran diri diserahkan kepada MPR dan
  Presiden Prabowo.
- Jalur Hak Menyatakan Pendapat DPR, yang diusulkan 11 November 2026,
  terlewati oleh pengunduran diri itu sendiri; proses pemakzulan tidak
  berlanjut karena jabatan telah dikosongkan oleh pemegangnya.
- Pasal 8 ayat (2) UUD 1945 mewajibkan MPR mengisi kekosongan jabatan
  wakil presiden dalam waktu 60 hari, sehingga tenggatnya jatuh sekitar
  11 Januari 2027. Presiden mengajukan dua nama calon kepada MPR untuk
  dipilih.
- Nama nama yang beredar dalam diskusi publik sebagai calon pengganti,
  antara lain Sugiono, Sufmi Dasco Ahmad, dan Puan Maharani, adalah
  spekulasi yang diberitakan media dan warganet, bukan nominasi resmi
  pada saat dokumen ini ditulis (17 November 2026).

Proyeksi statistik atas perhatian dan sentimen selama jendela 60 hari
ini, beserta skenario milestone, ada di docs/prediction_outlook.md.

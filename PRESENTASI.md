# Rancangan Presentasi 10 Menit + Tanya Jawab 5 Menit

## Slide 1 — Judul dan anggota (30 detik)
Coffee Inventory Management System — COMP6991031 Cloud Services.
Isi nama dan NIM ketiga anggota kelompok.

## Slide 2 — Masalah pengguna (1 menit)
Toko kopi kecil perlu mencatat jenis biji kopi, stok, dan harga. Catatan manual sulit diperbarui dan berisiko tidak konsisten.

## Slide 3 — Fitur aplikasi (1 menit)
CRUD: Create, Read, Update, Delete. Validasi input mencegah nama kosong, stok negatif, dan harga negatif.

## Slide 4 — Diagram arsitektur (1 menit)
Browser → Flask Web/API (container, port 5000) → PostgreSQL (container di jaringan internal) → Docker named volume `postgres-data`.

## Slide 5 — Kaitan dengan materi Week 1–7 (1 menit)
Cloud/deployment plan; Git/Linux; HTTP/REST; container; Dockerfile; Compose/network/volume; database dan kontrol akses. Cocokkan detail dengan slide LMS.

## Slide 6 — Docker Compose (1 menit)
Tunjukkan `Dockerfile`, `compose.yaml`, `.env.example`, image, container, port, healthcheck, network dan volume.

## Slide 7 — Demo alur CRUD (2 menit)
Tambahkan Arabika Gayo → tampilkan di tabel → edit stok → hapus barang.

## Slide 8 — Pengujian, persistence, dan diagnosis (1 menit)
Kirim stok -2; API harus menolak dengan HTTP 400. Tambahkan barang, `docker compose down` (tanpa `-v`), lalu `docker compose up -d`; barang harus tetap ada. Tunjukkan `/health` dan logs.

## Slide 9 — Keamanan, rencana cloud, dan kesimpulan (1 menit)
Database tidak dipublikasikan ke host dan hanya dapat diakses di jaringan Compose. Data bersifat inventaris bersama, bukan data privat per pengguna; RLS dua pengguna tidak diterapkan karena tidak sesuai lingkup. Untuk cloud: managed container + managed PostgreSQL + secret management + HTTPS + monitoring.

## Kontribusi anggota (isi sesuai kenyataan)
- Anggota 1: UI/Frontend dan pengujian alur CRUD.
- Anggota 2: Flask API, validasi, endpoint health, log.
- Anggota 3: Dockerfile, Compose, database, dokumentasi dan diagram.
Jangan mencantumkan kontribusi yang tidak benar-benar dilakukan.

## Tanya jawab yang perlu dipersiapkan
1. Apa perbedaan image dan container?
2. Apa fungsi Dockerfile dan Docker Compose?
3. Mengapa PostgreSQL memakai volume?
4. Bagaimana frontend berkomunikasi dengan backend? (HTTP/JSON)
5. Bagaimana aplikasi menangani input invalid?
6. Apa yang terjadi jika database mati? Bagaimana diagnosisnya?
7. Apakah data tiap pengguna diisolasi? Tidak; ini shared inventory dan tidak mengimplementasikan akun pengguna/RLS.
8. Apa perbedaan demo lokal dengan deployment cloud?

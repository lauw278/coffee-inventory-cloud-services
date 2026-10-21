# Bukti pengujian yang perlu dikumpulkan

Jalankan setiap pengujian dan ambil screenshot terminal/browser sebagai bukti. Hasil aktual harus berasal dari pengujian di laptop kelompok; jangan mengklaim tes berhasil sebelum dijalankan.

| ID | Uji | Cara | Hasil yang diharapkan |
|---|---|---|---|
| T1 | Container aktif | `docker compose ps` | `web` dan `db` berjalan; health status terlihat |
| T2 | UI | Buka `http://localhost:5000` | Formulir dan tabel tampil |
| T3 | Create/list | Tambah barang via UI | Barang tampil di tabel |
| T4 | Update | Klik Edit, ubah stok, simpan | Perubahan tampil |
| T5 | Delete | Klik Hapus | Barang hilang dari tabel |
| T6 | Input salah | POST quantity `-2` | HTTP 400 dan pesan validasi |
| T7 | Health | Buka `/health` | Status ok saat DB tersedia |
| T8 | Persistence | `docker compose down`, lalu `up -d` | Data masih ada tanpa menghapus volume |
| T9 | Logs | `docker compose logs web db` | Log layanan dapat dilihat |

Contoh uji input salah:

```bash
curl -i -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Uji","category":"Coffee","quantity":-2,"unit_price":1000}'
```

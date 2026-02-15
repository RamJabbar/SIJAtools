# SIJAtools – Sistem Peminjaman Alat

Aplikasi desktop offline untuk manajemen peminjaman alat dengan login & role-based access control.

## ✨ Fitur Baru v2.0

- **LOGIN SYSTEM**: Username & password authentication
- **ROLE-BASED ACCESS**: 
  - **ADMIN**: Manajemen alat + lihat semua riwayat
  - **USER**: Pinjam/kembalikan + lihat riwayat pribadi

## 🚀 Quick Start

```bash
python SIJAtools.py
```

**Demo Login:**
- Admin: `admin` / `admin123`
- User: `user1` / `user123`

Database dan users otomatis dibuat: `sijatools.db`

## 📋 Akses Berdasarkan Role

### 🔐 ADMIN Role
- ✅ Tab: Manajemen Alat
- ✅ Tambah, Edit, Hapus Alat
- ✅ Lihat Riwayat Semua Peminjaman
- ❌ Tidak bisa pinjam alat

### 👤 USER Role
- ✅ Tab: Input Peminjaman
- ✅ Tab: Pengembalian Alat
- ✅ Pinjam alat (auto-fill nama dengan username)
- ✅ Kembalikan alat & lihat riwayat pribadi
- ❌ Tidak bisa manajemen alat

## 💾 Teknologi

- **Bahasa**: Python 3.x
- **UI**: Tkinter (built-in)
- **Database**: SQLite (offline, lokal)
- **Dependency**: Hanya Python standar

## 📁 File Structure

```
Desktop Python1/
├── SIJAtools.py            (Aplikasi utama - v2.0 with login)
├── sijatools.db            (Database - auto created)
├── DOKUMENTASI.txt         (Dokumentasi v1.0)
├── CHANGELOG_v2.0.txt      (Dokumentasi perubahan v2.0)
└── README.md               (File ini)
```

## 📊 Database Schema

**Tabel 1: users (NEW in v2.0)**
- id
- username (UNIQUE)
- password
- role ('admin' atau 'user')
- created_at

**Tabel 2-3: alat, peminjaman (dari v1.0)**
- Unchanged, fully preserved

## 🔄 User Flow

### Admin Flow
```
Start → Login (admin/admin123)
      → Tab: Manajemen Alat
      → CRUD Alat, Update Stok
      → Tab: Riwayat (lihat SEMUA peminjaman)
      → Logout
```

### User Flow
```
Start → Login (user1/user123)
      → Tab: Input Peminjaman (nama auto-fill)
      → Pilih alat & jumlah → Pinjam
      → Tab: Pengembalian → Kembalikan
      → Tab: Riwayat Saya (lihat peminjaman pribadi)
      → Logout
```

## 🎯 Fitur Peminjaman (UNCHANGED dari v1.0)

✓ Input peminjaman dengan validasi stok  
✓ Status otomatis: Dipinjam → Dikembalikan  
✓ Stok otomatis update saat pinjam & kembalikan  
✓ Riwayat lengkap dengan timestamp  

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Login gagal | Cek username/password (lihat demo credentials) |
| Database error | Delete sijatools.db, jalankan ulang (auto-create) |
| Tkinter error | `pip install tk` |

## ✅ Backward Compatibility

- ✓ Semua logic v1.0 preserved
- ✓ Tabel lama (alat, peminjaman) untouched
- ✓ Method lama semua tetap bekerja
- ✓ Hanya tambah fitur login, tidak hapus yang lama

## 📝 Dokumentasi

- **DOKUMENTASI.txt**: Detail fitur & struktur v1.0
- **CHANGELOG_v2.0.txt**: Detail semua perubahan v2.0

## 🎓 Status

**Production Ready** ✓
- Testing: Lengkap
- Database: Auto-initialized
- Security: Demo-level (plain text password)
- License: Open Source

---

**v2.0 Release Date**: 2026-02-07  
**Previous Version**: SIJAtools v1.0


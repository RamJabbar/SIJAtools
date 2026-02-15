"""
Database manager untuk SIJAtools
Mengelola koneksi SQLite dan semua operasi CRUD
"""

import sqlite3
from datetime import datetime
import os


class DatabaseManager:
    """Manager untuk operasi database SQLite"""
    
    def __init__(self, db_name=None):
        if db_name is None:
            # Hitung path database relative terhadap script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_name = os.path.join(script_dir, 'sijatools.db')
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan membuat tabel jika belum ada"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabel untuk data alat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_alat TEXT NOT NULL UNIQUE,
                stok INTEGER NOT NULL,
                deskripsi TEXT,
                tanggal_ditambah TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel untuk data peminjaman
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_peminjam TEXT NOT NULL,
                id_alat INTEGER NOT NULL,
                jumlah INTEGER NOT NULL,
                status TEXT DEFAULT 'Dipinjam',
                tanggal_peminjaman TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tanggal_pengembalian TIMESTAMP,
                FOREIGN KEY (id_alat) REFERENCES alat(id)
            )
        ''')
        
        # Tabel untuk users (LOGIN SYSTEM)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default users jika users table baru
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                ('admin', 'admin123', 'admin')
            )
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                ('user1', 'user123', 'user')
            )
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Buka koneksi database"""
        return sqlite3.connect(self.db_name)
    
    # ---- OPERASI ALAT ----
    
    def tambah_alat(self, nama_alat, stok, deskripsi=""):
        """Tambah alat baru"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO alat (nama_alat, stok, deskripsi) VALUES (?, ?, ?)',
                (nama_alat, stok, deskripsi)
            )
            conn.commit()
            conn.close()
            return True, "Alat berhasil ditambahkan"
        except sqlite3.IntegrityError:
            return False, "Nama alat sudah ada"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def edit_alat(self, id_alat, nama_alat, stok, deskripsi=""):
        """Edit data alat"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE alat SET nama_alat=?, stok=?, deskripsi=? WHERE id=?',
                (nama_alat, stok, deskripsi, id_alat)
            )
            conn.commit()
            conn.close()
            return True, "Alat berhasil diperbarui"
        except sqlite3.IntegrityError:
            return False, "Nama alat sudah ada"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def hapus_alat(self, id_alat):
        """Hapus alat"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM alat WHERE id=?', (id_alat,))
            conn.commit()
            conn.close()
            return True, "Alat berhasil dihapus"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_all_alat(self):
        """Ambil semua data alat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nama_alat, stok, deskripsi FROM alat ORDER BY nama_alat')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_alat_by_id(self, id_alat):
        """Ambil data alat berdasarkan ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nama_alat, stok, deskripsi FROM alat WHERE id=?', (id_alat,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def update_stok(self, id_alat, jumlah):
        """Kurangi stok alat (untuk peminjaman)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE alat SET stok = stok - ? WHERE id=?', (jumlah, id_alat))
        conn.commit()
        conn.close()
    
    def tambah_stok(self, id_alat, jumlah):
        """Tambah stok alat (untuk pengembalian)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE alat SET stok = stok + ? WHERE id=?', (jumlah, id_alat))
        conn.commit()
        conn.close()
    
    def get_stok(self, id_alat):
        """Ambil stok alat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT stok FROM alat WHERE id=?', (id_alat,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    
    # ---- OPERASI PEMINJAMAN ----
    
    def tambah_peminjaman(self, nama_peminjam, id_alat, jumlah):
        """Tambah peminjaman baru"""
        try:
            # Validasi stok
            stok = self.get_stok(id_alat)
            if stok < jumlah:
                return False, f"Stok tidak cukup. Tersedia: {stok}"
            
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO peminjaman (nama_peminjam, id_alat, jumlah, status) VALUES (?, ?, ?, ?)',
                (nama_peminjam, id_alat, jumlah, 'Dipinjam')
            )
            conn.commit()
            id_peminjaman = cursor.lastrowid
            conn.close()
            
            # Update stok
            self.update_stok(id_alat, jumlah)
            
            return True, f"Peminjaman berhasil ditambahkan (ID: {id_peminjaman})"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def kembalikan_alat(self, id_peminjaman):
        """Kembalikan alat yang dipinjam"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Ambil data peminjaman
            cursor.execute(
                'SELECT id_alat, jumlah FROM peminjaman WHERE id=?',
                (id_peminjaman,)
            )
            result = cursor.fetchone()
            
            if not result:
                return False, "Data peminjaman tidak ditemukan"
            
            id_alat, jumlah = result
            
            # Update status dan tanggal pengembalian
            cursor.execute(
                'UPDATE peminjaman SET status=?, tanggal_pengembalian=? WHERE id=?',
                ('Dikembalikan', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id_peminjaman)
            )
            conn.commit()
            conn.close()
            
            # Tambah stok
            self.tambah_stok(id_alat, jumlah)
            
            return True, "Alat berhasil dikembalikan"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_all_peminjaman(self):
        """Ambil semua data peminjaman"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.nama_peminjam, a.nama_alat, p.jumlah, p.status, 
                   p.tanggal_peminjaman
            FROM peminjaman p
            JOIN alat a ON p.id_alat = a.id
            ORDER BY p.tanggal_peminjaman DESC
        ''')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_peminjaman_by_status(self, status):
        """Ambil peminjaman berdasarkan status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.nama_peminjam, a.nama_alat, p.jumlah, p.status, 
                   p.tanggal_peminjaman
            FROM peminjaman p
            JOIN alat a ON p.id_alat = a.id
            WHERE p.status = ?
            ORDER BY p.tanggal_peminjaman DESC
        ''', (status,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    # ---- OPERASI USER / LOGIN ----
    
    def login(self, username, password):
        """Validasi login user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, username, role FROM users WHERE username=? AND password=?',
                (username, password)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return True, {'id': result[0], 'username': result[1], 'role': result[2]}
            else:
                return False, "Username atau password salah"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_role(self, username):
        """Ambil role user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT role FROM users WHERE username=?', (username,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            return None
    
    def check_username_exists(self, username):
        """Cek apakah username sudah ada di database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username=?', (username,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            return False
    
    def register(self, username, password):
        """Daftar akun user baru dengan role='user'"""
        try:
            # Validasi input
            if not username or not password:
                return False, "Username dan password tidak boleh kosong"
            
            # Cek username sudah ada
            if self.check_username_exists(username):
                return False, f"Username '{username}' sudah digunakan. Gunakan username lain"
            
            # Insert user baru dengan role='user'
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO users (username, password, role) 
                   VALUES (?, ?, 'user')''',
                (username, password)
            )
            conn.commit()
            conn.close()
            
            return True, "Akun berhasil dibuat! Silakan login dengan akun Anda"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_peminjaman_by_user(self, username):
        """Ambil peminjaman berdasarkan username peminjam"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.nama_peminjam, a.nama_alat, p.jumlah, p.status, 
                   p.tanggal_peminjaman
            FROM peminjaman p
            JOIN alat a ON p.id_alat = a.id
            WHERE p.nama_peminjam = ?
            ORDER BY p.tanggal_peminjaman DESC
        ''', (username,))
        result = cursor.fetchall()
        conn.close()
        return result

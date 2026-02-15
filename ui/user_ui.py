"""
User UI - Tabs untuk user
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.components import create_table
from database.db import DatabaseManager


class UserUI:
    """Handler untuk user tabs"""
    
    def __init__(self, notebook, current_user):
        self.notebook = notebook
        self.current_user = current_user
        self.username = current_user['username']
        self.db = DatabaseManager()
        
        # Buat tabs
        self.create_tab_peminjaman()
        self.create_tab_pengembalian()
        self.create_tab_riwayat()
    
    def create_tab_peminjaman(self):
        """Tab: Input Peminjaman"""
        tab_peminjaman = ttk.Frame(self.notebook)
        self.notebook.add(tab_peminjaman, text="Input Peminjaman")
        
        # Frame input
        input_frame = ttk.LabelFrame(tab_peminjaman, text="Input Peminjaman", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Nama Peminjam:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        label_nama = ttk.Label(input_frame, text=self.username, font=('Arial', 10, 'bold'), foreground='blue')
        label_nama.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        note = ttk.Label(
            input_frame,
            text="(Nama otomatis dari akun login Anda, tidak bisa diubah)",
            font=('Arial', 8),
            foreground='gray'
        )
        note.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=3)
        
        ttk.Label(input_frame, text="Pilih Alat:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.combo_alat = ttk.Combobox(input_frame, width=37, state='readonly')
        self.combo_alat.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.combo_alat.bind('<<ComboboxSelected>>', self.on_alat_selected)
        
        ttk.Label(input_frame, text="Jumlah:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_jumlah = ttk.Entry(input_frame, width=40)
        self.entry_jumlah.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(input_frame, text="Stok Tersedia:", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.label_stok = ttk.Label(input_frame, text="0", font=('Arial', 10))
        self.label_stok.grid(row=4, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(input_frame, text="Pinjam", command=self.pinjam_alat).grid(row=5, column=0, columnspan=2, pady=10)
        
        self.load_combo_alat()
        
        # Frame riwayat peminjaman aktif
        riwayat_frame = ttk.LabelFrame(tab_peminjaman, text="Peminjaman Aktif (Status: Dipinjam)", padding=10)
        riwayat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nama Peminjam', 'Alat', 'Jumlah', 'Tanggal')
        scrollbar, self.tree_peminjaman = create_table(riwayat_frame, columns, height=10)
        
        self.load_peminjaman_aktif()
    
    def create_tab_pengembalian(self):
        """Tab: Pengembalian Alat"""
        tab_pengembalian = ttk.Frame(self.notebook)
        self.notebook.add(tab_pengembalian, text="Pengembalian Alat")
        
        info_frame = ttk.LabelFrame(tab_pengembalian, text="Daftar Peminjaman Aktif", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nama Peminjam', 'Alat', 'Jumlah', 'Tanggal Pinjam')
        scrollbar, self.tree_kembali = create_table(info_frame, columns, height=15)
        
        button_frame = ttk.Frame(tab_pengembalian)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Kembalikan Alat", command=self.kembalikan_alat).pack()
        
        self.load_data_pengembalian()
    
    def create_tab_riwayat(self):
        """Tab: Riwayat Peminjaman Pribadi"""
        tab_riwayat = ttk.Frame(self.notebook)
        self.notebook.add(tab_riwayat, text="Riwayat Saya")
        
        table_frame = ttk.LabelFrame(tab_riwayat, text=f"Riwayat Peminjaman - {self.username}", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nama Peminjam', 'Alat', 'Jumlah', 'Status', 'Tanggal Pinjam')
        scrollbar, self.tree_riwayat = create_table(table_frame, columns, height=20)
        
        self.load_riwayat()
    
    # ---- PEMINJAMAN OPERATIONS ----
    
    def load_combo_alat(self):
        data = self.db.get_all_alat()
        self.alat_map = {f"{item[1]} (Stok: {item[2]})": item[0] for item in data}
        self.combo_alat['values'] = list(self.alat_map.keys())
    
    def on_alat_selected(self, event):
        selected = self.combo_alat.get()
        if selected:
            alat_id = self.alat_map[selected]
            stok = self.db.get_stok(alat_id)
            self.label_stok.config(text=str(stok))
    
    def pinjam_alat(self):
        nama_peminjam = self.username
        selected_alat = self.combo_alat.get()
        jumlah = self.entry_jumlah.get().strip()
        
        if not selected_alat or not jumlah:
            messagebox.showerror("Error", "Pilih alat dan isi jumlah")
            return
        
        try:
            jumlah = int(jumlah)
            if jumlah <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka positif")
            return
        
        alat_id = self.alat_map[selected_alat]
        
        success, msg = self.db.tambah_peminjaman(nama_peminjam, alat_id, jumlah)
        
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_peminjaman_input()
            self.load_peminjaman_aktif()
            self.load_data_pengembalian()
            self.load_combo_alat()
            self.load_riwayat()
        else:
            messagebox.showerror("Error", msg)
    
    def clear_peminjaman_input(self):
        self.combo_alat.set('')
        self.entry_jumlah.delete(0, tk.END)
        self.label_stok.config(text="0")
    
    def load_peminjaman_aktif(self):
        for item in self.tree_peminjaman.get_children():
            self.tree_peminjaman.delete(item)
        
        data = self.db.get_peminjaman_by_status('Dipinjam')
        for row in data:
            self.tree_peminjaman.insert('', tk.END, values=(
                row[0], row[1], row[2], row[3], row[5][:10]
            ))
    
    # ---- PENGEMBALIAN OPERATIONS ----
    
    def kembalikan_alat(self):
        selection = self.tree_kembali.selection()
        
        if not selection:
            messagebox.showerror("Error", "Pilih peminjaman yang akan dikembalikan")
            return
        
        if messagebox.askyesno("Konfirmasi", "Kembalikan alat ini?"):
            item = self.tree_kembali.item(selection[0])
            id_peminjaman = item['values'][0]
            
            success, msg = self.db.kembalikan_alat(id_peminjaman)
            
            if success:
                messagebox.showinfo("Sukses", msg)
                self.load_data_pengembalian()
                self.load_peminjaman_aktif()
                self.load_combo_alat()
                self.load_riwayat()
            else:
                messagebox.showerror("Error", msg)
    
    def load_data_pengembalian(self):
        for item in self.tree_kembali.get_children():
            self.tree_kembali.delete(item)
        
        data = self.db.get_peminjaman_by_status('Dipinjam')
        for row in data:
            self.tree_kembali.insert('', tk.END, values=(
                row[0], row[1], row[2], row[3], row[5][:10]
            ))
    
    # ---- RIWAYAT OPERATIONS ----
    
    def load_riwayat(self):
        for item in self.tree_riwayat.get_children():
            self.tree_riwayat.delete(item)
        
        data = self.db.get_peminjaman_by_user(self.username)
        for row in data:
            self.tree_riwayat.insert('', tk.END, values=(
                row[0], row[1], row[2], row[3], row[4], row[5][:10]
            ))

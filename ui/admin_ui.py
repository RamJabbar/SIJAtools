"""
Admin UI - Tab untuk admin user
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.components import create_table
from database.db import DatabaseManager


class AdminUI:
    """Handler untuk admin tabs"""
    
    def __init__(self, notebook, current_user):
        self.notebook = notebook
        self.current_user = current_user
        self.username = current_user['username']
        self.db = DatabaseManager()
        
        self.current_alat_id = None
        
        # Buat tabs
        self.create_tab_alat()
        self.create_tab_riwayat()
    
    def create_tab_alat(self):
        """Tab: Manajemen Alat"""
        tab_alat = ttk.Frame(self.notebook)
        self.notebook.add(tab_alat, text="Manajemen Alat")
        
        # Frame input
        input_frame = ttk.LabelFrame(tab_alat, text="Input Data Alat", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Nama Alat:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nama_alat = ttk.Entry(input_frame, width=40)
        self.entry_nama_alat.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(input_frame, text="Stok:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_stok = ttk.Entry(input_frame, width=40)
        self.entry_stok.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(input_frame, text="Deskripsi:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_deskripsi = ttk.Entry(input_frame, width=40)
        self.entry_deskripsi.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Tambah", command=self.tambah_alat).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Perbarui", command=self.update_alat).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Batal", command=self.batal_edit_alat).pack(side=tk.LEFT, padx=5)
        
        # Frame tabel
        table_frame = ttk.LabelFrame(tab_alat, text="Daftar Alat", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nama Alat', 'Stok', 'Deskripsi')
        scrollbar, self.tree_alat = create_table(table_frame, columns, height=12)
        
        self.tree_alat.bind('<Double-1>', self.on_alat_double_click)
        
        ttk.Button(table_frame, text="Hapus Alat", command=self.hapus_alat).pack(pady=5)
        
        self.load_data_alat()
    
    def create_tab_riwayat(self):
        """Tab: Riwayat Semua Peminjaman"""
        tab_riwayat = ttk.Frame(self.notebook)
        self.notebook.add(tab_riwayat, text="Riwayat Peminjaman")
        
        table_frame = ttk.LabelFrame(tab_riwayat, text="Riwayat Semua Peminjaman", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nama Peminjam', 'Alat', 'Jumlah', 'Status', 'Tanggal Pinjam')
        scrollbar, self.tree_riwayat = create_table(table_frame, columns, height=20)
        
        self.load_riwayat()
    
    # ---- ALAT OPERATIONS ----
    
    def tambah_alat(self):
        nama = self.entry_nama_alat.get().strip()
        stok = self.entry_stok.get().strip()
        deskripsi = self.entry_deskripsi.get().strip()
        
        if not nama or not stok:
            messagebox.showerror("Error", "Nama alat dan stok harus diisi")
            return
        
        try:
            stok = int(stok)
            if stok < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka positif")
            return
        
        success, msg = self.db.tambah_alat(nama, stok, deskripsi)
        
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_alat_input()
            self.load_data_alat()
        else:
            messagebox.showerror("Error", msg)
    
    def update_alat(self):
        if self.current_alat_id is None:
            messagebox.showerror("Error", "Pilih alat yang akan diperbarui")
            return
        
        nama = self.entry_nama_alat.get().strip()
        stok = self.entry_stok.get().strip()
        deskripsi = self.entry_deskripsi.get().strip()
        
        if not nama or not stok:
            messagebox.showerror("Error", "Nama alat dan stok harus diisi")
            return
        
        try:
            stok = int(stok)
            if stok < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka positif")
            return
        
        success, msg = self.db.edit_alat(self.current_alat_id, nama, stok, deskripsi)
        
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_alat_input()
            self.load_data_alat()
        else:
            messagebox.showerror("Error", msg)
    
    def hapus_alat(self):
        selection = self.tree_alat.selection()
        
        if not selection:
            messagebox.showerror("Error", "Pilih alat yang akan dihapus")
            return
        
        item = self.tree_alat.item(selection[0])
        id_alat = item['values'][0]
        
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus alat ini?"):
            success, msg = self.db.hapus_alat(id_alat)
            
            if success:
                messagebox.showinfo("Sukses", msg)
                self.load_data_alat()
            else:
                messagebox.showerror("Error", msg)
    
    def on_alat_double_click(self, event):
        selection = self.tree_alat.selection()
        
        if selection:
            item = self.tree_alat.item(selection[0])
            values = item['values']
            
            self.current_alat_id = values[0]
            self.entry_nama_alat.delete(0, tk.END)
            self.entry_nama_alat.insert(0, values[1])
            self.entry_stok.delete(0, tk.END)
            self.entry_stok.insert(0, values[2])
            self.entry_deskripsi.delete(0, tk.END)
            self.entry_deskripsi.insert(0, values[3])
    
    def batal_edit_alat(self):
        self.clear_alat_input()
    
    def clear_alat_input(self):
        self.entry_nama_alat.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)
        self.entry_deskripsi.delete(0, tk.END)
        self.current_alat_id = None
        self.tree_alat.selection_remove(self.tree_alat.selection())
    
    def load_data_alat(self):
        for item in self.tree_alat.get_children():
            self.tree_alat.delete(item)
        
        data = self.db.get_all_alat()
        for row in data:
            self.tree_alat.insert('', tk.END, values=row)
    
    def load_riwayat(self):
        for item in self.tree_riwayat.get_children():
            self.tree_riwayat.delete(item)
        
        data = self.db.get_all_peminjaman()
        for row in data:
            self.tree_riwayat.insert('', tk.END, values=(
                row[0], row[1], row[2], row[3], row[4], row[5][:10]
            ))

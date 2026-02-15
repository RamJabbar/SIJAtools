"""
Register window untuk SIJAtools
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.db import DatabaseManager


class RegisterWindow:
    """Window untuk register akun user baru"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SIJAtools – Daftar Akun User")
        self.root.geometry("450x360")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.db = DatabaseManager()
        self.success = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """Buat widget form register"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Daftar Akun User Baru",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Subtitle
        subtitle = ttk.Label(
            main_frame,
            text="Isi form berikut untuk membuat akun peminjam",
            font=('Arial', 9),
            foreground='gray'
        )
        subtitle.pack(pady=(0, 15))
        
        # Username
        ttk.Label(main_frame, text="Username:", font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.entry_username = ttk.Entry(main_frame, width=40)
        self.entry_username.pack(pady=(0, 12), ipady=5)
        self.entry_username.focus()
        
        # Password
        ttk.Label(main_frame, text="Password:", font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.entry_password = ttk.Entry(main_frame, width=40, show='*')
        self.entry_password.pack(pady=(0, 12), ipady=5)
        
        # Konfirmasi Password
        ttk.Label(main_frame, text="Konfirmasi Password:", font=('Arial', 10)).pack(anchor=tk.W, pady=(5, 0))
        self.entry_confirm = ttk.Entry(main_frame, width=40, show='*')
        self.entry_confirm.pack(pady=(0, 20), ipady=5)
        
        # Bind Enter key
        self.entry_username.bind('<Return>', lambda e: self.do_register())
        self.entry_password.bind('<Return>', lambda e: self.do_register())
        self.entry_confirm.bind('<Return>', lambda e: self.do_register())
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Daftar", command=self.do_register).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Batal", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        # Instructions
        info = ttk.Label(
            main_frame,
            text="• Username minimal 3 karakter\n"
                 "• Password tidak boleh kosong\n"
                 "• Akun akan ditetapkan sebagai USER (Peminjam)",
            font=('Arial', 8),
            foreground='gray',
            justify=tk.LEFT
        )
        info.pack(pady=10)
    
    def do_register(self):
        """Proses registrasi akun user baru"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        confirm = self.entry_confirm.get().strip()
        
        # Validasi form
        if not username:
            messagebox.showerror("Error", "Username tidak boleh kosong")
            self.entry_username.focus()
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username minimal 3 karakter")
            self.entry_username.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Password tidak boleh kosong")
            self.entry_password.focus()
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Password dan konfirmasi tidak sama")
            self.entry_confirm.focus()
            return
        
        # Proses register via database
        success, message = self.db.register(username, password)
        
        if success:
            messagebox.showinfo("Berhasil", message)
            self.success = True
            self.root.destroy()
        else:
            messagebox.showerror("Registrasi Gagal", message)

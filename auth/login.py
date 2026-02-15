"""
Login window dan role selection untuk SIJAtools
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.db import DatabaseManager


class RoleSelectionWindow:
    """Window untuk memilih role (USER atau ADMIN)"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SIJAtools – Login")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.selected_role = None
        self.current_user = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Buat widget role selection"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="SIJAtools – Sistem Peminjaman Alat",
            font=('Arial', 16, 'bold')
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = ttk.Label(
            main_frame,
            text="Pilih peran Anda untuk melanjutkan",
            font=('Arial', 11)
        )
        subtitle.pack(pady=(0, 30))
        
        # Frame untuk tombol
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tombol USER
        user_btn = ttk.Button(
            button_frame,
            text="👤 LOGIN SEBAGAI USER\n\n(Pinjam & Kembalikan Alat)",
            command=lambda: self.select_role('user')
        )
        user_btn.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Tombol ADMIN
        admin_btn = ttk.Button(
            button_frame,
            text="👑 LOGIN SEBAGAI ADMIN\n\n(Kelola Data Alat)",
            command=lambda: self.select_role('admin')
        )
        admin_btn.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Tombol Exit
        exit_btn = ttk.Button(main_frame, text="Exit", command=self.root.quit)
        exit_btn.pack(pady=20, fill=tk.X)
    
    def select_role(self, role):
        """Proses pemilihan role"""
        self.selected_role = role
        
        # Buka LoginWindow
        login_window = tk.Toplevel(self.root)
        login = LoginWindow(login_window, role)
        
        # Tunggu LoginWindow selesai
        login_window.wait_window()
        
        # Ambil hasil login
        self.current_user = login.current_user
        
        if self.current_user:
            self.root.destroy()


class LoginWindow:
    """Window untuk login user berdasarkan role yang dipilih"""
    
    def __init__(self, root, role='user'):
        self.root = root
        self.role = role  # 'user' atau 'admin'
        self.root.title(f"SIJAtools – Login {role.upper()}")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.db = DatabaseManager()
        self.current_user = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Buat widget login"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title dengan role indicator
        role_display = "👤 USER" if self.role == 'user' else "👑 ADMIN"
        title = ttk.Label(
            main_frame,
            text=f"SIJAtools – Login {role_display}",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=15)
        
        # Username
        ttk.Label(main_frame, text="Username:", font=('Arial', 10)).pack(anchor=tk.W, pady=(10, 0))
        self.entry_username = ttk.Entry(main_frame, width=40)
        self.entry_username.pack(pady=(0, 10), ipady=5)
        self.entry_username.focus()
        
        # Password
        ttk.Label(main_frame, text="Password:", font=('Arial', 10)).pack(anchor=tk.W, pady=(10, 0))
        self.entry_password = ttk.Entry(main_frame, width=40, show='*')
        self.entry_password.pack(pady=(0, 20), ipady=5)
        
        # Bind Enter key
        self.entry_username.bind('<Return>', lambda e: self.do_login())
        self.entry_password.bind('<Return>', lambda e: self.do_login())
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Login", command=self.do_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Kembali", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        # Tombol Daftar Akun Baru - HANYA untuk USER
        if self.role == 'user':
            from auth.register import RegisterWindow
            ttk.Button(btn_frame, text="Daftar", command=self.open_register).pack(side=tk.LEFT, padx=5)
        
        # Info text sesuai role
        if self.role == 'user':
            demo_text = "Demo USER: user1 / user123"
        else:
            demo_text = "Demo ADMIN: admin / admin123"
        
        info = ttk.Label(
            main_frame,
            text=demo_text,
            font=('Arial', 8),
            foreground='gray'
        )
        info.pack(pady=10)
    
    def do_login(self):
        """Proses login dengan validasi role"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi")
            return
        
        success, result = self.db.login(username, password)
        
        if success:
            # Validasi role sesuai dengan role yang dipilih
            user_role = result['role']
            if user_role != self.role:
                messagebox.showerror(
                    "Error",
                    f"Akun '{username}' adalah akun {user_role.upper()}, "
                    f"bukan akun {self.role.upper()}\n\n"
                    f"Gunakan akun yang sesuai dengan role yang dipilih."
                )
                return
            
            self.current_user = result
            self.root.destroy()
        else:
            messagebox.showerror("Login Gagal", result)
    
    def open_register(self):
        """Buka window register akun baru"""
        from auth.register import RegisterWindow
        register_window = tk.Toplevel(self.root)
        register = RegisterWindow(register_window)
        register_window.wait_window()
        
        # Jika registrasi sukses, clear form dan fokus ke username
        if register.success:
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus()
            messagebox.showinfo(
                "Registrasi Berhasil", 
                "Akun Anda sudah dibuat. Silakan login menggunakan akun baru Anda"
            )

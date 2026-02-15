"""
SIJAtools - Sistem Peminjaman Alat
Entry point aplikasi

Struktur:
- main.py          : Entry point
- database/db.py   : DatabaseManager
- auth/login.py    : LoginWindow, RoleSelectionWindow
- auth/register.py : RegisterWindow
- ui/components.py : Reusable UI components
- ui/admin_ui.py   : Admin UI tabs
- ui/user_ui.py    : User UI tabs
"""

import tkinter as tk
from tkinter import ttk
from auth.login import RoleSelectionWindow
from ui.components import setup_styles


class SIJAtoolsApp:
    """Aplikasi utama SIJAtools"""
    
    def __init__(self, root, current_user=None):
        self.root = root
        self.root.title("SIJAtools – Sistem Peminjaman Alat")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        self.current_user = current_user
        self.username = current_user['username'] if current_user else 'Guest'
        self.user_role = current_user['role'] if current_user else 'guest'
        
        # Setup styles
        setup_styles()
        
        # Buat interface
        self.create_widgets()
    
    def create_widgets(self):
        """Buat widget utama"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = ttk.Label(
            header_frame,
            text="SIJAtools – Sistem Peminjaman Alat",
            style='Header.TLabel'
        )
        header_label.pack(side=tk.LEFT)
        
        # User info
        user_info = ttk.Label(
            header_frame,
            text=f"User: {self.username} ({self.user_role.upper()})",
            font=('Arial', 10),
            foreground='blue'
        )
        user_info.pack(side=tk.RIGHT, padx=10)
        
        # Notebook (Tab)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load UI berdasarkan role
        if self.user_role == 'admin':
            self.load_admin_ui()
        elif self.user_role == 'user':
            self.load_user_ui()
    
    def load_admin_ui(self):
        """Load admin UI"""
        from ui.admin_ui import AdminUI
        AdminUI(self.notebook, self.current_user)
    
    def load_user_ui(self):
        """Load user UI"""
        from ui.user_ui import UserUI
        UserUI(self.notebook, self.current_user)


def main():
    """Entry point aplikasi"""
    # STEP 1: Tampilkan Role Selection Window
    root = tk.Tk()
    role_selection = RoleSelectionWindow(root)
    root.mainloop()
    
    # STEP 2: Setelah user memilih role dan login sukses, buka dashboard
    if role_selection.current_user:
        app_root = tk.Tk()
        app = SIJAtoolsApp(app_root, role_selection.current_user)
        app_root.mainloop()


if __name__ == "__main__":
    main()

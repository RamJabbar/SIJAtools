"""
Reusable UI components untuk SIJAtools
"""

import tkinter as tk
from tkinter import ttk


def create_table(parent, columns, height=10):
    """
    Helper untuk membuat treeview table
    
    Args:
        parent: parent widget
        columns: list of column names
        height: tinggi table
    
    Returns:
        scrollbar, treeview
    """
    # Scrollbar
    scrollbar = ttk.Scrollbar(parent)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Tabel
    tree = ttk.Treeview(
        parent,
        columns=columns,
        height=height,
        yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=tree.yview)
    
    tree.heading('#0', text='')
    tree.column('#0', width=0, stretch=tk.NO)
    
    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=30)
        elif col in ['Stok', 'Jumlah']:
            tree.column(col, width=50)
        elif col == 'Status':
            tree.column(col, width=80)
        else:
            tree.column(col, width=150)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    return scrollbar, tree


def setup_styles():
    """Konfigurasi style untuk Tkinter"""
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
    style.configure('Subheader.TLabel', font=('Arial', 11, 'bold'))
    style.configure('Normal.TLabel', font=('Arial', 10))
    
    return style

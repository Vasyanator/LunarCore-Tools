# tab_opencommand.py

import tkinter as tk
from tkinter import ttk

class OpenCommandTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        
        self.label = tk.Label(self.frame, text="If you know Java, please implement something like github.com/jie65535/gc-opencommand-plugin, I will be grateful and implement its support here.", justify="left")
        self.label.pack(fill="both", expand=True, padx=10, pady=10)

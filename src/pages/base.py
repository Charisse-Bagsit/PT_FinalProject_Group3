"""
pages/base.py  -  Parent class that every page inherits from.
"""
import tkinter as tk
from theme import BG, MUTED, F_TITLE, F_SUBTITLE


class Page(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def on_show(self):
        pass

    def title_block(self, title, subtitle):
        tk.Label(self, text=title, font=F_TITLE(26), bg=BG).pack(pady=(16, 0))
        tk.Label(self, text=subtitle, font=F_SUBTITLE(12), bg=BG, fg=MUTED).pack(pady=(0, 8))
"""
pages/base.py  -  Parent class that every page inherits from.
"""
import tkinter as tk
from theme import BG, MUTED, F


class Page(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def on_show(self):
        pass

    def title_block(self, title, subtitle):
        tk.Label(self, text=title, font=F(26, True), bg=BG).pack(pady=(16, 0))
        tk.Label(self, text=subtitle, font=F(12, True), bg=BG, fg=MUTED).pack(pady=(0, 8))

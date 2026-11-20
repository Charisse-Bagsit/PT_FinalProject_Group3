"""
pages/about.py  -  About page (edit TEAM below with your group's names).
"""
import tkinter as tk
from theme import BG, PINK, WHITE, BLACK, F, info_card
from pages.base import Page


TEAM = ["Member 1", "Member 2", "Member 3", "Member 4"]   # <- put your names here


# ------------------------------------------------------------------ ABOUT
class AboutPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("About Us", "")
        tk.Label(self, text="This Banker's Algorithm Simulator was built to help students understand "
                            "how an operating system avoids deadlock. It shows the background, the "
                            "formulas, and a step-by-step safety check you can try with your own data.",
                 font=F(12), bg=BG, wraplength=1000, justify="center").pack(padx=30)
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=30, pady=22)
        for c in range(3):
            row.grid_columnconfigure(c, weight=1, uniform="c")
        info_card(row, "Mission", "To make a hard operating-systems topic easy to see and try, "
                                  "one clear step at a time.", height=240
                  ).grid(row=0, column=0, sticky="ew", padx=8)
        info_card(row, "Vision", "A classroom where students learn deadlock avoidance by "
                                 "experimenting, not just memorizing.", fill=PINK, title_fg=WHITE,
                  text_fg=BLACK, height=240).grid(row=0, column=1, sticky="ew", padx=8)
        info_card(row, "Purpose", "To compute Need and Available, run the safety algorithm, and "
                                  "check resource requests so users can tell if a system is safe.",
                  height=240).grid(row=0, column=2, sticky="ew", padx=8)
        tk.Label(self, text="Developed by:  " + "   •   ".join(TEAM), font=F(12, True),
                 bg=BG).pack(pady=8)

"""
pages/how.py  -  How the program works (4 steps + formulas)
"""
import tkinter as tk
from theme import BG, HOT, LIGHT, WHITE, F, round_rect, RoundButton, Card, info_card, make_tree
from pages.base import Page


# ------------------------------------------------------------------ HOW IT WORKS
class HowPage(Page):
    STEPS = [("1", "Input", "Enter the Total resources, then the Allocation and Max matrix "
                            "of every process. Or load the Problem 1 sample."),
             ("2", "Compute", "The program calculates Need = Max - Allocation and "
                              "Available = Total - Allocated."),
             ("3", "Safety Check", "Work starts as Available. A process with Need <= Work can "
                                   "finish and gives its Allocation back to Work."),
             ("4", "Verdict", "If every process finishes, the state is SAFE and the safe "
                              "sequence is shown. Otherwise it is UNSAFE.")]
    FORMULAS = [("Need = Max - Allocation", "Resources still needed by a process"),
                ("Available = Total - Allocated", "Resources currently free"),
                ("Need <= Work", "Rule for checking if a process can finish"),
                ("New Work = Work + Allocation", "Resources released by a finished process")]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("How the Program Works", "Four simple steps from input to verdict")
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=30, pady=8)
        for c in range(4):
            row.grid_columnconfigure(c, weight=1, uniform="c")
        for c, (num, title, text) in enumerate(self.STEPS):
            card = info_card(row, title, text, height=215)
            badge = tk.Canvas(card.body, width=46, height=46, bg=WHITE, highlightthickness=0)
            round_rect(badge, 2, 2, 44, 44, 12, fill=LIGHT, outline="")
            badge.create_text(23, 23, text=num, font=F(18, True))
            badge.pack(before=card.body.winfo_children()[0], pady=(4, 0))
            card.grid(row=0, column=c, sticky="ew", padx=8)

        card = Card(self, height=230, width=10)
        card.pack(fill="both", expand=True, padx=38, pady=(8, 8))
        tk.Label(card.body, text="Important Formulas", font=F(14, True), fg=HOT,
                 bg=WHITE).pack(anchor="w")
        frame, tree = make_tree(card.body, [("f", "Formula", 300, False), ("m", "Meaning", 640, True)], 4)
        frame.pack(fill="both", expand=True, pady=(4, 0))
        for f, m in self.FORMULAS:
            tree.insert("", "end", values=(f, m))

        RoundButton(self, "Open Simulator  →", lambda: app.show("sim"), width=210,
                    fill=HOT).pack(anchor="e", padx=40, pady=(0, 12))

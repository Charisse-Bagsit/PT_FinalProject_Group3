"""
pages/background.py  -  What is the Banker's Algorithm? (background + key terms)
"""
import tkinter as tk
from theme import BG, PINK, HOT, WHITE, BLACK, F, RoundButton, Card, info_card, make_tree
from pages.base import Page


# ------------------------------------------------------------------ BACKGROUND
class BackgroundPage(Page):
    INTRO = ("The Banker's Algorithm is a deadlock-avoidance algorithm created by Edsger Dijkstra. "
             "Before an operating system gives resources to a process, it checks whether the "
             "system would still be in a safe state afterwards. If every process can still finish "
             "in some order, the request is safe. If not, the process must wait.")
    TERMS = [("Total", "Total units of each resource type in the whole system"),
             ("Allocation", "Resources each process is holding right now"),
             ("Max", "The most each process may ever need"),
             ("Need", "Max - Allocation : what a process still needs to finish"),
             ("Available", "Total - sum of Allocation : free units right now"),
             ("Work", "A temporary copy of Available used during the safety check"),
             ("Finish", "True once a process has been simulated as completed")]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("What is the Banker's Algorithm?", "Background")
        tk.Label(self, text=self.INTRO, font=F(11), bg=BG, wraplength=1000,
                 justify="center").pack(padx=30)

        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=30, pady=14)
        for c in range(3):
            row.grid_columnconfigure(c, weight=1, uniform="c")
        info_card(row, "Why \"Banker\"?",
                  "Like a bank that never lends so much that it cannot satisfy its other "
                  "customers, the OS only grants resources if every process can still be served."
                  ).grid(row=0, column=0, sticky="ew", padx=8)
        info_card(row, "Safe State",
                  "There is at least one order (a safe sequence) where every process can get "
                  "what it needs, finish, and release its resources. No deadlock.",
                  fill=PINK, title_fg=WHITE, text_fg=BLACK
                  ).grid(row=0, column=1, sticky="ew", padx=8)
        info_card(row, "Unsafe State",
                  "No such order exists. It does not always mean deadlock, but deadlock becomes "
                  "possible, so the system avoids entering this state."
                  ).grid(row=0, column=2, sticky="ew", padx=8)

        card = Card(self, height=250, width=10)
        card.pack(fill="both", expand=True, padx=38, pady=(0, 8))
        tk.Label(card.body, text="Key Terms", font=F(14, True), fg=HOT, bg=WHITE).pack(anchor="w")
        frame, tree = make_tree(card.body, [("t", "Term", 140, False), ("m", "Meaning", 800, True)], 7)
        frame.pack(fill="both", expand=True, pady=(4, 0))
        for t, m in self.TERMS:
            tree.insert("", "end", values=(t, m))

        RoundButton(self, "Next: How It Works  →", lambda: app.show("how"), width=230,
                    fill=HOT).pack(anchor="e", padx=40, pady=(0, 12))

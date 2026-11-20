"""
pages/dashboard.py  -  Summary of the last simulation.
"""
import tkinter as tk
from tkinter import ttk

from banker_logic import fmt
from theme import BG, LIGHT, SOFT, WHITE, BLACK, GREEN, RED, MUTED, F, RoundButton, Card
from pages.base import Page


# ------------------------------------------------------------------ DASHBOARD
class DashPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        tk.Label(self, text="Dashboard Overview", font=F(22, True), bg=BG).pack(anchor="w", padx=24, pady=(14, 0))
        tk.Label(self, text="Summary of the last simulation", font=F(11), bg=BG).pack(anchor="w", padx=24)

        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=16, pady=12)
        self.vars, self.val_lbls = {}, {}
        for c, title in enumerate(["Processes", "Resource Types", "Finished", "Status"]):
            row.grid_columnconfigure(c, weight=1, uniform="s")
            card = Card(row, height=100, width=10)
            card.grid(row=0, column=c, sticky="ew", padx=8)
            tk.Label(card.body, text=title, font=F(13, True), bg=WHITE).pack(anchor="w")
            self.vars[title] = tk.StringVar(value="-")
            lbl = tk.Label(card.body, textvariable=self.vars[title], font=F(24, True), bg=WHITE)
            lbl.pack(anchor="w")
            self.val_lbls[title] = lbl

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        bottom.grid_columnconfigure(0, weight=1, uniform="b")
        bottom.grid_columnconfigure(1, weight=1, uniform="b")
        bottom.grid_rowconfigure(0, weight=1)
        lc = Card(bottom, width=10, height=10)
        lc.grid(row=0, column=0, sticky="nsew", padx=8)
        tk.Label(lc.body, text="Resource Utilization", font=F(14, True), bg=WHITE).pack(anchor="w")
        self.util = tk.Frame(lc.body, bg=WHITE)
        self.util.pack(fill="both", expand=True, pady=6)
        rc = Card(bottom, width=10, height=10)
        rc.grid(row=0, column=1, sticky="nsew", padx=8)
        tk.Label(rc.body, text="Safe Sequence", font=F(14, True), bg=WHITE).pack(anchor="w")
        self.seq = tk.Frame(rc.body, bg=WHITE)
        self.seq.pack(fill="both", expand=True, pady=6)

    def on_show(self):
        for fr in (self.util, self.seq):
            for w in fr.winfo_children():
                w.destroy()
        d = self.app.data
        if d.result is None:
            for t in self.vars:
                self.vars[t].set("-")
                self.val_lbls[t].config(fg=BLACK)
            for fr in (self.util, self.seq):
                tk.Label(fr, text="No data yet. Run the Simulator first.", font=F(11),
                         fg=MUTED, bg=WHITE).pack(pady=20)
            return

        r = d.result
        self.vars["Processes"].set(str(len(d.alloc)))
        self.vars["Resource Types"].set(str(len(d.total)))
        self.vars["Finished"].set(f"{len(r['sequence'])} / {len(d.alloc)}")
        self.vars["Status"].set("SAFE" if r["safe"] else "UNSAFE")
        self.val_lbls["Status"].config(fg=GREEN if r["safe"] else RED)

        used = [sum(col) for col in zip(*d.alloc)]
        for j, name in enumerate(d.names):
            pct = round(100 * used[j] / d.total[j]) if d.total[j] else 0
            tk.Label(self.util, text=f"Resource {name}", font=F(11, True), bg=WHITE).pack(anchor="w")
            tk.Label(self.util, text=f"{used[j]} of {d.total[j]} allocated ({pct}%)   |   "
                                     f"{d.available[j]} free", font=F(9), fg=MUTED, bg=WHITE).pack(anchor="w")
            ttk.Progressbar(self.util, style="Pink.Horizontal.TProgressbar", maximum=max(d.total[j], 1),
                            value=used[j]).pack(fill="x", pady=(2, 10))

        for k, s in enumerate(r["steps"]):
            item = tk.Frame(self.seq, bg=SOFT)
            item.pack(fill="x", pady=3)
            tk.Label(item, text=f"{k + 1}", font=F(12, True), bg=LIGHT, width=3).pack(side="left", padx=8, pady=6)
            col = tk.Frame(item, bg=SOFT)
            col.pack(side="left")
            tk.Label(col, text=f"P{s['index']}", font=F(12, True), bg=SOFT).pack(anchor="w")
            tk.Label(col, text="Work → " + fmt(s["work_after"]), font=F(9), fg=MUTED, bg=SOFT).pack(anchor="w")
            RoundButton(item, "FINISHED", None, width=96, height=30, radius=14, fill=GREEN, fg=WHITE,
                        font=F(9, True), bg=SOFT, cursor="arrow").pack(side="right", padx=8)
        for i in r["stuck"]:
            item = tk.Frame(self.seq, bg=SOFT)
            item.pack(fill="x", pady=3)
            tk.Label(item, text=f"P{i}", font=F(12, True), bg=SOFT).pack(side="left", padx=12, pady=10)
            RoundButton(item, "STUCK", None, width=96, height=30, radius=14, fill=RED, fg=WHITE,
                        font=F(9, True), bg=SOFT, cursor="arrow").pack(side="right", padx=8)

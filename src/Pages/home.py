"""
pages/home.py  -  Home / hero page.
"""
import tkinter as tk
from theme import BG, PINK, HOT, LIGHT, SOFT, WHITE, BLACK, GREEN, F, round_rect, RoundButton


# ------------------------------------------------------------------ HOME
class HomePage(tk.Canvas):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG, highlightthickness=0)
        self.app = app
        self.btn_start = RoundButton(self, "Start Simulator", lambda: app.show("sim"),
                                     width=190, height=54, fill="#FF8AD8", bg=PINK)
        self.btn_learn = RoundButton(self, "Learn the Basics", lambda: app.show("background"),
                                     width=190, height=54, fill=WHITE, bg=PINK)
        self.bind("<Configure>", self.draw)

    def on_show(self):
        pass

    def draw(self, e=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 50:
            return
        self.delete("all")
        self.create_polygon(0, 0, 0.265 * w, 0, 0.60 * w, h, 0, h, fill=PINK, outline="")

        size = int(max(24, min(w / 26, h / 14)))
        head = self.create_text(0.08 * w, 0.17 * h, anchor="nw", fill=BLACK, font=F(size, True),
                                text="Avoid Deadlock,\nKeep the System\nSafe")
        y = self.bbox(head)[3] + 14
        sub = self.create_text(0.08 * w, y, anchor="nw", fill=BLACK, font=F(13, True),
                               width=0.40 * w,
                               text="A simulator that checks whether a system is in a safe state "
                                    "and finds a safe sequence, so processes never get stuck.")
        y = self.bbox(sub)[3] + 22
        self.create_window(0.08 * w, y, window=self.btn_start, anchor="nw")
        self.create_window(0.08 * w + 210, y, window=self.btn_learn, anchor="nw")
        self._illustration(w, h)

    def _illustration(self, w, h):
        cw, ch = min(0.34 * w, 430), 340
        x1, y1 = 0.60 * w + (0.36 * w - cw) / 2 + 0.02 * w, max(20, 0.5 * h - ch / 2)
        x2, y2 = x1 + cw, y1 + ch
        round_rect(self, x1 + 8, y1 + 10, x2 + 8, y2 + 10, 26, fill="#C9A3B8", outline="")
        round_rect(self, x1, y1, x2, y2, 26, fill=WHITE, outline=BLACK, width=2)
        self.create_text(x1 + 24, y1 + 26, anchor="w", text="Safety check", font=F(14, True), fill=HOT)
        self.create_text(x2 - 24, y1 + 26, anchor="e", text="Work = (3, 2, 3)", font=F(11, True))
        rows = [("P0", "3 2 1"), ("P1", "1 1 2"), ("P2", "3 1 1"), ("P3", "2 1 1")]
        for i, (p, need) in enumerate(rows):
            ry = y1 + 62 + i * 48
            round_rect(self, x1 + 20, ry, x2 - 20, ry + 40, 12, fill=SOFT, outline="")
            round_rect(self, x1 + 28, ry + 6, x1 + 76, ry + 34, 10, fill=LIGHT, outline=BLACK)
            self.create_text(x1 + 52, ry + 20, text=p, font=F(11, True))
            self.create_text(x1 + 96, ry + 20, anchor="w", text="Need  " + need, font=F(11))
            self.create_oval(x2 - 58, ry + 8, x2 - 32, ry + 34, fill=GREEN, outline="")
            self.create_text(x2 - 45, ry + 21, text="✓", fill=WHITE, font=F(12, True))
        round_rect(self, x1 + 20, y2 - 58, x2 - 20, y2 - 16, 18, fill=GREEN, outline=BLACK, width=2)
        self.create_text((x1 + x2) / 2, y2 - 37, fill=WHITE, font=F(12, True),
                         text="SAFE   P0 → P1 → P2 → P3")

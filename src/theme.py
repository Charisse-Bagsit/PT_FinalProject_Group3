"""
theme.py  -  Modern Indigo & Slate color theme, fonts and reusable widgets
(RoundButton, Card, tables). Every page imports from here, so change the look in ONE place.
"""
import tkinter as tk
from tkinter import ttk


# ------------------------------------------------------------------ theme (Modern Indigo & Slate)
BG = "#F4F6FB"        # page background (soft cool gray-white)
PINK = "#3730A3"      # primary deep indigo (logo, active tab, highlight cards)
HOT = "#4F46E5"       # royal indigo accent (section titles, primary action buttons)
LIGHT = "#E0E7FF"     # soft lavender-blue (table headers, secondary buttons)
SOFT = "#EEF2FF"      # very light indigo (hover, alternating table rows)
WHITE = "#FFFFFF"     # cards & inputs
BLACK = "#1E1B4B"     # dark midnight navy (text & borders)
GREEN = "#00BF63"     # safe state
RED = "#E8131A"       # unsafe state
MUTED = "#475569"     # slate gray subtitles
FONT = "Segoe UI"     # falls back to the default font if not installed


def F(size=11, bold=False):
    return (FONT, size, "bold") if bold else (FONT, size)


def round_rect(canvas, x1, y1, x2, y2, r=16, **kw):
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    r = max(2, min(r, w / 2.2, h / 2.2))
    pts = [
        x1 + r, y1,
        x1 + r, y1,
        x2 - r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, splinesteps=36, **kw)


def _auto_fg(fill, fg=None):
    if fg is not None:
        return fg
    return WHITE if fill in (PINK, HOT, GREEN, RED) else BLACK


# ------------------------------------------------------------------ widgets
class RoundButton(tk.Canvas):
    """Rounded button drawn on a canvas (Tk has no rounded buttons)."""

    def __init__(self, parent, text, command=None, width=140, height=44, radius=16,
                 fill=WHITE, fg=None, bg=None, font=None, cursor="hand2"):
        super().__init__(parent, width=width, height=height, highlightthickness=0,
                         bg=bg or parent.cget("bg"), cursor=cursor)
        self.text, self.command = text, command
        self.w, self.h, self.r = width, height, radius
        self._custom_fg = fg
        self.fill, self.cur = fill, fill
        self.fg = _auto_fg(fill, fg)
        self.font = font or F(11, True)
        self._draw()
        if command:
            self.bind("<Button-1>", lambda e: self.command())
            self.bind("<Enter>", lambda e: self._set(SOFT if self.fill == WHITE else self.fill))
            self.bind("<Leave>", lambda e: self._set(self.fill))

    def _set(self, color):
        self.cur = color
        self._draw()

    def _draw(self):
        self.delete("all")
        round_rect(self, 2, 2, self.w - 2, self.h - 2, self.r,
                   fill=self.cur, outline=BLACK, width=2)
        self.create_text(self.w / 2, self.h / 2, text=self.text, fill=self.fg, font=self.font)

    def restyle(self, fill, fg=None):
        self.fill = self.cur = fill
        self.fg = _auto_fg(fill, fg if fg is not None else self._custom_fg)
        self._draw()


class Card(tk.Canvas):
    """A rounded white card. Put your widgets inside  card.body ."""

    def __init__(self, parent, fill=WHITE, radius=22, pad=14, **kw):
        super().__init__(parent, bg=parent.cget("bg"), highlightthickness=0, **kw)
        self.fill, self.radius, self.pad = fill, radius, pad
        self.body = tk.Frame(self, bg=fill)
        self._win = self.create_window(pad, pad, window=self.body, anchor="nw")
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e):
        self.delete("bg")
        round_rect(self, 2, 2, e.width - 2, e.height - 2, self.radius,
                   fill=self.fill, outline=BLACK, width=2, tags="bg")
        self.tag_lower("bg")
        self.itemconfigure(self._win, width=max(e.width - 2 * self.pad, 1),
                           height=max(e.height - 2 * self.pad, 1))


def info_card(parent, title, text, fill=WHITE, title_fg=HOT, text_fg=MUTED, height=170):
    card = Card(parent, fill=fill, height=height, width=10)
    tk.Label(card.body, text=title, font=F(15, True), fg=title_fg, bg=fill).pack(pady=(6, 4))
    lbl = tk.Label(card.body, text=text, font=F(10), fg=text_fg, bg=fill,
                   justify="center", wraplength=250)
    lbl.pack()
    card.bind("<Configure>", lambda e: (card._redraw(e), lbl.config(wraplength=max(e.width - 60, 80))))
    return card


def make_tree(parent, columns, height):
    """columns = [(key, title, width, stretch), ...]  ->  (frame, tree)"""
    frame = tk.Frame(parent, bg=parent.cget("bg"))
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings",
                        height=height, selectmode="none")
    for key, title, width, stretch in columns:
        tree.heading(key, text=title)
        tree.column(key, width=width, anchor="center", stretch=stretch)
    tree.tag_configure("ok", background="#D9F7E6")
    tree.tag_configure("bad", background="#FFD6D6")
    tree.pack(fill="both", expand=True)
    return frame, tree


def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=BLACK,
                    rowheight=32, font=F(12), bordercolor=BLACK, borderwidth=1)
    style.configure("Treeview.Heading", background=LIGHT, foreground=BLACK,
                    font=F(12, True), relief="flat", borderwidth=1, bordercolor=BLACK)
    style.map("Treeview.Heading", background=[("active", LIGHT)])
    style.configure("Pink.Horizontal.TProgressbar", troughcolor=WHITE, background=HOT,
                    bordercolor=BLACK, lightcolor=HOT, darkcolor=HOT, thickness=18)

    # Tk 8.6.9 bug fix so row tag colors show up
    def fixed_map(option):
        return [e for e in style.map("Treeview", query_opt=option)
                if e[:2] != ("!disabled", "!selected")]
    style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))
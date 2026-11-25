
"""
theme.py - Modern Indigo & Slate Theme with Elegant Fonts
Reusable widgets, buttons, cards, tables and font styles.
"""

import tkinter as tk
from tkinter import ttk


# ==========================================================
# THEME COLORS
# ==========================================================

BG = "#F4F6FB"
PINK = "#3730A3"
HOT = "#4F46E5"
LIGHT = "#E0E7FF"
SOFT = "#EEF2FF"
WHITE = "#FFFFFF"
BLACK = "#1E1B4B"
GREEN = "#00BF63"
RED = "#E8131A"
MUTED = "#475569"


# ==========================================================
# FONT FAMILIES
# ==========================================================

FONT = "Segoe UI"
SERIF_FONT = "Georgia"
BODY_FONT = "Arial"
ELEGANT_FONT = "Georgia"


# ==========================================================
# DEFAULT FONT
# ==========================================================

def F(size=11, bold=False):
    return (FONT, size, "bold") if bold else (FONT, size)


# ==========================================================
# ELEGANT FONT STYLES
# ==========================================================

def F_TITLE(size=30):
    return (SERIF_FONT, size, "bold")


def F_ELEGANT(size=28):
    return (ELEGANT_FONT, size, "bold italic")


def F_LOGO(size=25):
    return (SERIF_FONT, size, "bold italic")


def F_HEADING(size=18):
    return (SERIF_FONT, size, "bold")


def F_SUBTITLE(size=14):
    return (BODY_FONT, size, "bold")


def F_BODY(size=11):
    return (BODY_FONT, size)


def F_DESCRIPTION(size=10):
    return (BODY_FONT, size)


def F_BUTTON(size=11):
    return (BODY_FONT, size, "bold")


def F_TABLE(size=11):
    return (BODY_FONT, size)


def F_LABEL(size=10):
    return (BODY_FONT, size)


def F_NAV(size=12):
    return (BODY_FONT, size, "bold")


def F_FORM(size=11):
    return (BODY_FONT, size, "bold")


# ==========================================================
# ROUNDED RECTANGLE
# ==========================================================

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

    return canvas.create_polygon(
        pts,
        smooth=True,
        splinesteps=36,
        **kw
    )


# ==========================================================
# AUTOMATIC TEXT COLOR
# ==========================================================

def _auto_fg(fill, fg=None):

    if fg is not None:
        return fg

    return WHITE if fill in (PINK, HOT, GREEN, RED) else BLACK


# ==========================================================
# ROUNDED BUTTON
# ==========================================================

class RoundButton(tk.Canvas):

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=140,
        height=44,
        radius=16,
        fill=WHITE,
        fg=None,
        bg=None,
        font=None,
        cursor="hand2"
    ):

        super().__init__(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bg=bg or parent.cget("bg"),
            cursor=cursor
        )

        self.text = text
        self.command = command
        self.w = width
        self.h = height
        self.r = radius

        self._custom_fg = fg
        self.fill = fill
        self.cur = fill
        self.fg = _auto_fg(fill, fg)

        self.font = font or F_BUTTON(11)

        self._draw()

        if command:
            self.bind(
                "<Button-1>",
                lambda e: self.command()
            )

            self.bind(
                "<Enter>",
                lambda e: self._set(
                    SOFT if self.fill == WHITE else self.fill
                )
            )

            self.bind(
                "<Leave>",
                lambda e: self._set(self.fill)
            )

    def _set(self, color):
        self.cur = color
        self._draw()

    def _draw(self):

        self.delete("all")

        round_rect(
            self,
            2, 2,
            self.w - 2,
            self.h - 2,
            self.r,
            fill=self.cur,
            outline=BLACK,
            width=2
        )

        self.create_text(
            self.w / 2,
            self.h / 2,
            text=self.text,
            fill=self.fg,
            font=self.font
        )

    def restyle(self, fill, fg=None):

        self.fill = self.cur = fill

        self.fg = _auto_fg(
            fill,
            fg if fg is not None else self._custom_fg
        )

        self._draw()


# ==========================================================
# CARD
# ==========================================================

class Card(tk.Canvas):

    def __init__(
        self,
        parent,
        fill=WHITE,
        radius=22,
        pad=14,
        **kw
    ):

        super().__init__(
            parent,
            bg=parent.cget("bg"),
            highlightthickness=0,
            **kw
        )

        self.fill = fill
        self.radius = radius
        self.pad = pad

        self.body = tk.Frame(
            self,
            bg=fill
        )

        self._win = self.create_window(
            pad,
            pad,
            window=self.body,
            anchor="nw"
        )

        self.bind("<Configure>", self._redraw)

    def _redraw(self, e):

        self.delete("bg")

        round_rect(
            self,
            2, 2,
            e.width - 2,
            e.height - 2,
            self.radius,
            fill=self.fill,
            outline=BLACK,
            width=2,
            tags="bg"
        )

        self.tag_lower("bg")

        self.itemconfigure(
            self._win,
            width=max(e.width - 2 * self.pad, 1),
            height=max(e.height - 2 * self.pad, 1)
        )


# ==========================================================
# INFORMATION CARD
# ==========================================================

def info_card(
    parent,
    title,
    text,
    fill=WHITE,
    title_fg=HOT,
    text_fg=MUTED,
    height=170
):

    card = Card(
        parent,
        fill=fill,
        height=height,
        width=10
    )

    tk.Label(
        card.body,
        text=title,
        font=F_HEADING(17),
        fg=title_fg,
        bg=fill
    ).pack(pady=(6, 4))

    lbl = tk.Label(
        card.body,
        text=text,
        font=F_BODY(11),
        fg=text_fg,
        bg=fill,
        justify="center",
        wraplength=250
    )

    lbl.pack()

    card.bind(
        "<Configure>",
        lambda e: (
            card._redraw(e),
            lbl.config(
                wraplength=max(e.width - 60, 80)
            )
        )
    )

    return card


# ==========================================================
# TABLE
# ==========================================================

def make_tree(parent, columns, height):

    frame = tk.Frame(
        parent,
        bg=parent.cget("bg")
    )

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    tree = ttk.Treeview(
        frame,
        columns=[c[0] for c in columns],
        show="headings",
        height=height,
        selectmode="none"
    )

    sb = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview
    )

    def _set(first, last):

        sb.set(first, last)

        if float(first) <= 0.0 and float(last) >= 1.0:
            sb.grid_remove()
        else:
            sb.grid()

    tree.configure(
        yscrollcommand=_set
    )

    for key, title, width, stretch in columns:

        tree.heading(key, text=title)

        tree.column(
            key,
            width=width,
            anchor="center",
            stretch=stretch
        )

    tree.tag_configure(
        "ok",
        background="#D9F7E6"
    )

    tree.tag_configure(
        "bad",
        background="#FFD6D6"
    )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    sb.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    return frame, tree


# ==========================================================
# GLOBAL TTK STYLES
# ==========================================================

def setup_styles():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=WHITE,
        fieldbackground=WHITE,
        foreground=BLACK,
        rowheight=32,
        font=F_TABLE(11),
        bordercolor=BLACK,
        borderwidth=1
    )

    style.configure(
        "Treeview.Heading",
        background=LIGHT,
        foreground=BLACK,
        font=F_SUBTITLE(11),
        relief="flat",
        borderwidth=1,
        bordercolor=BLACK
    )

    style.map(
        "Treeview.Heading",
        background=[("active", LIGHT)]
    )

    style.configure(
        "Pink.Horizontal.TProgressbar",
        troughcolor=WHITE,
        background=HOT,
        bordercolor=BLACK,
        lightcolor=HOT,
        darkcolor=HOT,
        thickness=18
    )

    # Tkinter Treeview color compatibility fix
    def fixed_map(option):

        return [
            e for e in style.map(
                "Treeview",
                query_opt=option
            )
            if e[:2] != ("!disabled", "!selected")
        ]

    style.map(
        "Treeview",
        foreground=fixed_map("foreground"),
        background=fixed_map("background")
    )

"""
pages/background.py  -  Background of the Banker's Algorithm + Deep Indigo Tinted Concept Cards + 2-Column Key Terms Grid.
"""
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from theme import BG, PINK, HOT, LIGHT, SOFT, WHITE, BLACK, MUTED, F, RoundButton, Card, round_rect
from pages.base import Page


# ------------------------------------------------------------------ BACKGROUND
class BackgroundPage(Page):
    TERMS = [("Total", "Total units of each resource type in the whole system"),
             ("Allocation", "Resources each process is holding right now"),
             ("Max", "The most each process may ever need"),
             ("Need", "Max - Allocation : what a process still needs to finish"),
             ("Available", "Total - sum of Allocation : free units right now"),
             ("Work", "A temporary copy of Available used during the safety check")]

    CONCEPTS = [
        ('Why "Banker"?',
         "Like a bank that never lends so much that it cannot satisfy its other customers, "
         "the OS only grants resources if every process can still be served.",
         "Bg1"),
        ("Safe State",
         "There is at least one order (a safe sequence) where every process can get what "
         "it needs, finish, and release its resources. No deadlock.",
         "Bg2"),
        ("Unsafe State",
         "No such order exists. It does not always mean deadlock, but deadlock becomes "
         "possible, so the system avoids entering this state.",
         "Bg3"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("What is the Banker's Algorithm?", "Background")
        self._bg_refs = []

        intro = tk.Label(
            self,
            text="The Banker's Algorithm is a deadlock-avoidance algorithm created by Edsger Dijkstra. "
                 "Before an operating system gives resources to a process, it checks whether the system "
                 "would still be in a safe state afterwards. If every process can still finish in some "
                 "order, the request is safe. If not, the process must wait.",
            font=F(10), fg=BLACK, bg=BG, justify="center", wraplength=820
        )
        intro.pack(pady=(2, 10))

        # 3 Concept Cards with Background Pictures + Deep Indigo Overlay
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=28, pady=4)
        for c in range(3):
            row.grid_columnconfigure(c, weight=1, uniform="c")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(base_dir, "images")

        for col, (title, desc, base_name) in enumerate(self.CONCEPTS):
            img_path = self._find_image(images_dir, base_name)
            self._concept_card(row, col, title, desc, img_path)

        # Key Terms Card (Custom Centered Two-Column Table)
        card = Card(self, height=265, width=10, pad=16)
        card.pack(fill="x", padx=36, pady=(10, 6))

        tk.Label(card.body, text="Key Terms", font=F(15, True), fg=HOT, bg=WHITE).pack(anchor="center", pady=(0, 8))

        tbl_border = tk.Frame(card.body, bg="#CBD5E1", padx=1, pady=1)
        tbl_border.pack(fill="x")
        tbl_border.grid_columnconfigure(0, weight=1, uniform="kt_cols")
        tbl_border.grid_columnconfigure(1, weight=1, uniform="kt_cols")

        tk.Label(tbl_border, text="Term", font=F(10, True), fg=BLACK, bg=LIGHT,
                 pady=6, anchor="center", justify="center").grid(row=0, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))
        tk.Label(tbl_border, text="Meaning", font=F(10, True), fg=BLACK, bg=LIGHT,
                 pady=6, anchor="center", justify="center").grid(row=0, column=1, sticky="nsew", pady=(0, 1))

        for r_idx, (term, meaning) in enumerate(self.TERMS, start=1):
            row_bg = WHITE if r_idx % 2 == 1 else SOFT
            bottom_pad = 0 if r_idx == len(self.TERMS) else 1

            tk.Label(tbl_border, text=term, font=F(10, True), fg=PINK, bg=row_bg,
                     pady=5, anchor="center", justify="center").grid(
                row=r_idx, column=0, sticky="nsew", padx=(0, 1), pady=(0, bottom_pad)
            )
            tk.Label(tbl_border, text=meaning, font=F(10), fg=BLACK, bg=row_bg,
                     pady=5, anchor="center", justify="center").grid(
                row=r_idx, column=1, sticky="nsew", pady=(0, bottom_pad)
            )

        RoundButton(self, "Next: How It Works  →", lambda: app.show("how"), width=220, height=44,
                    fill=PINK, fg=WHITE).pack(anchor="e", padx=36, pady=(6, 12))

    def _find_image(self, folder, base_name):
        if not os.path.isdir(folder):
            return None
        for fname in os.listdir(folder):
            name_only, ext = os.path.splitext(fname)
            if name_only.lower() == base_name.lower() and ext.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                return os.path.join(folder, fname)
        return None

    def _concept_card(self, parent, col, title, desc, img_path):
        canvas = tk.Canvas(parent, bg=BG, height=185, highlightthickness=0)
        canvas.grid(row=0, column=col, sticky="ew", padx=8)

        orig_img = Image.open(img_path).convert("RGBA") if img_path else None

        def redraw(e=None):
            w, h = canvas.winfo_width(), canvas.winfo_height()
            if w < 20:
                return
            canvas.delete("all")
            round_rect(canvas, 2, 2, w - 2, h - 2, 18, fill=PINK, outline=BLACK, width=2)

            if orig_img:
                iw, ih = max(w - 4, 10), max(h - 4, 10)
                resized = orig_img.resize((iw, ih), Image.Resampling.LANCZOS)
                indigo_overlay = Image.new("RGBA", (iw, ih), (30, 27, 75, 195))
                blended = Image.alpha_composite(resized, indigo_overlay)

                mask = Image.new("L", (iw, ih), 0)
                ImageDraw.Draw(mask).rounded_rectangle((0, 0, iw, ih), radius=16, fill=255)
                blended.putalpha(mask)

                photo = ImageTk.PhotoImage(blended)
                self._bg_refs.append(photo)
                canvas.create_image(w / 2, h / 2, image=photo)
                round_rect(canvas, 2, 2, w - 2, h - 2, 18, fill="", outline=BLACK, width=2)

            # Centered Title (Soft Periwinkle) & Description (Pure White)
            canvas.create_text(w / 2, h * 0.34, text=title, font=F(16, True), fill="#C7D2FE")
            canvas.create_text(w / 2, h * 0.47, anchor="n", text=desc, font=F(10, True),
                               fill=WHITE, width=w - 44, justify="center")

        canvas.bind("<Configure>", redraw)
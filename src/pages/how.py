"""
pages/how.py  -  How It Works (4 steps with deep indigo tinted background pictures + clean 2-column formulas grid).
"""
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from theme import BG, PINK, HOT, LIGHT, SOFT, WHITE, BLACK, MUTED, F, F_HEADING, F_BODY, F_TABLE, RoundButton, Card, round_rect
from pages.base import Page


# ------------------------------------------------------------------ HOW IT WORKS
class HowPage(Page):
    STEPS = [
        ("1", "Input", "Enter the Total resources, then the Allocation and Max matrix of every "
                       "process. Or load the Problem 1 sample.", "Step1"),
        ("2", "Compute", "The program calculates Need = Max - Allocation and "
                         "Available = Total - Allocated.", "Step2"),
        ("3", "Safety Check", "Work starts as Available. A process with Need ≤ Work can finish "
                              "and gives its Allocation back to Work.", "Step3"),
        ("4", "Verdict", "If every process finishes, the state is SAFE and the safe sequence is "
                         "shown. Otherwise it is UNSAFE.", "Step4"),
    ]
    FORMULAS = [
        ("Need = Max - Allocation", "Resources still needed by a process"),
        ("Available = Total - Allocated", "Resources currently free"),
        ("Need ≤ Work", "Rule for checking if a process can finish"),
        ("New Work = Work + Allocation", "Resources released by a finished process"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("How the Algorithm Works", "Four simple steps")
        self._bg_refs = []

        # 1. Step 1 to 4 Cards
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=28, pady=(8, 12))
        for c in range(4):
            row.grid_columnconfigure(c, weight=1, uniform="s")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(base_dir, "images")

        for i, (num, title, desc, base_name) in enumerate(self.STEPS):
            img_path = self._find_image(images_dir, base_name)
            self._step_card(row, i, num, title, desc, img_path)

        # 2. Important Formulas Card (Custom Centered Two-Column Grid)
        card = Card(self, height=255, width=10, pad=16)
        card.pack(fill="x", padx=36, pady=(6, 8))

        tk.Label(card.body, text="Important Formulas", font=F_HEADING(15), fg=HOT, bg=WHITE).pack(anchor="center", pady=(0, 10))

        # Outer border frame ng table
        tbl_border = tk.Frame(card.body, bg="#CBD5E1", padx=1, pady=1)
        tbl_border.pack(fill="x")
        tbl_border.grid_columnconfigure(0, weight=1, uniform="if_cols")
        tbl_border.grid_columnconfigure(1, weight=1, uniform="if_cols")

        # Table Header (Two Columns, Centered)
        tk.Label(tbl_border, text="Formula", font=F(10, True), fg=BLACK, bg=LIGHT,
                 pady=7, anchor="center", justify="center").grid(row=0, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))
        tk.Label(tbl_border, text="Meaning", font=F(10, True), fg=BLACK, bg=LIGHT,
                 pady=7, anchor="center", justify="center").grid(row=0, column=1, sticky="nsew", pady=(0, 1))

        # Table Rows (Lahat ng 4 formulas kita, may vertical divider, at naka-center)
        for r_idx, (formula, meaning) in enumerate(self.FORMULAS, start=1):
            row_bg = WHITE if r_idx % 2 == 1 else SOFT
            bottom_pad = 0 if r_idx == len(self.FORMULAS) else 1

            tk.Label(tbl_border, text=formula, font=F(10, True), fg=PINK, bg=row_bg,
                     pady=6, anchor="center", justify="center").grid(
                row=r_idx, column=0, sticky="nsew", padx=(0, 1), pady=(0, bottom_pad)
            )
            tk.Label(tbl_border, text=meaning, font=F_TABLE(10), fg=BLACK, bg=row_bg,
                     pady=6, anchor="center", justify="center").grid(
                row=r_idx, column=1, sticky="nsew", pady=(0, bottom_pad)
            )

        # 3. Bottom Action Button
        RoundButton(self, "Open Simulator  →", lambda: app.show("sim"), width=210, height=44,
                    fill=HOT, fg=WHITE).pack(anchor="e", padx=36, pady=(6, 14))

    def _find_image(self, folder, base_name):
        if not os.path.isdir(folder):
            return None
        for fname in os.listdir(folder):
            name_only, ext = os.path.splitext(fname)
            if name_only.lower() == base_name.lower() and ext.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                return os.path.join(folder, fname)
        return None

    def _step_card(self, parent, col, num, title, desc, img_path):
        canvas = tk.Canvas(parent, bg=BG, height=255, highlightthickness=0)
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
                indigo_overlay = Image.new("RGBA", (iw, ih), (30, 27, 75, 190))
                blended = Image.alpha_composite(resized, indigo_overlay)

                mask = Image.new("L", (iw, ih), 0)
                ImageDraw.Draw(mask).rounded_rectangle((0, 0, iw, ih), radius=16, fill=255)
                blended.putalpha(mask)

                photo = ImageTk.PhotoImage(blended)
                self._bg_refs.append(photo)
                canvas.create_image(w / 2, h / 2, image=photo)
                round_rect(canvas, 2, 2, w - 2, h - 2, 18, fill="", outline=BLACK, width=2)

            # Step number badge
            round_rect(canvas, w / 2 - 22, 30, w / 2 + 22, 70, 12, fill=WHITE, outline="")
            canvas.create_text(w / 2, 50, text=num, font=F(16, True), fill=PINK)

            # Title & Description
            canvas.create_text(w / 2, 102, text=title, font=F_HEADING(15), fill="#C7D2FE")
            canvas.create_text(w / 2, 130, anchor="n", text=desc, font=F_BODY(10),
                               fill=WHITE, width=w - 36, justify="center")

        canvas.bind("<Configure>", redraw)
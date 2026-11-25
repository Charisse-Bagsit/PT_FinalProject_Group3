"""
pages/about.py  -  About Us (Mission, Vision, Purpose with deep indigo tinted background pictures + Team section).
"""
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from theme import BG, PINK, HOT, LIGHT, SOFT, WHITE, BLACK, MUTED, F, F_HEADING, F_BODY, Card, round_rect
from pages.base import Page


# ------------------------------------------------------------------ ABOUT US
class AboutPage(Page):
    MVP = [
        ("Mission",
         "To make a hard operating-systems topic easy to see and try, one clear step at a time.",
         "About1"),
        ("Vision",
         "A classroom where students learn deadlock avoidance by experimenting, not just memorizing.",
         "About2"),
        ("Purpose",
         "To compute Need and Available, run the safety algorithm, and check resource requests "
         "so users can tell if a system is safe.",
         "About3"),
    ]

    TEAM = [
        "Charisse Bagsit",
        "Erikka Stephanie Dela Roca",
        "John Carlo Plantilla",
        "Princess Khaila Robines",
        "Joshua Servando",
    ]

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.title_block("About Us", "Project Overview & Team")
        self._bg_refs = []

        intro = tk.Label(
            self,
            text="This Banker's Algorithm Simulator was built to help students understand how an "
                 "operating system avoids deadlock. It shows the background, the formulas, and a "
                 "step-by-step safety check you can try with your own data.",
            font=F_BODY(10), fg=BLACK, bg=BG, justify="center", wraplength=780
        )
        intro.pack(pady=(2, 16))

        # 1. Mission, Vision, Purpose Cards with Deep Indigo Tinted Background Images
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", padx=28, pady=6)
        for c in range(3):
            row.grid_columnconfigure(c, weight=1, uniform="mvp")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images_dir = os.path.join(base_dir, "images")

        for col, (title, desc, base_name) in enumerate(self.MVP):
            img_path = self._find_image(images_dir, base_name)
            self._mvp_card(row, col, title, desc, img_path)

        # 2. Organized Team Card sa Ibaba
        team_card = Card(self, height=130, width=10, pad=16)
        team_card.pack(fill="x", padx=36, pady=(20, 12))

        tk.Label(team_card.body, text="Developed By", font=F_HEADING(15), fg=HOT, bg=WHITE).pack(anchor="center", pady=(0, 10))

        pills = tk.Frame(team_card.body, bg=WHITE)
        pills.pack(anchor="center")
        for member in self.TEAM:
            lbl = tk.Label(
                pills, text=member, font=F(10, True), fg=BLACK, bg=SOFT,
                padx=14, pady=6, bd=1, relief="solid"
            )
            lbl.pack(side="left", padx=6)

    def _find_image(self, folder, base_name):
        if not os.path.isdir(folder):
            return None
        for fname in os.listdir(folder):
            name_only, ext = os.path.splitext(fname)
            if name_only.lower() == base_name.lower() and ext.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                return os.path.join(folder, fname)
        return None

    def _mvp_card(self, parent, col, title, desc, img_path):
        canvas = tk.Canvas(parent, bg=BG, height=235, highlightthickness=0)
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
            canvas.create_text(w / 2, h * 0.36, text=title, font=F_HEADING(16), fill="#C7D2FE")
            canvas.create_text(w / 2, h * 0.49, anchor="n", text=desc, font=F_BODY(10),
                               fill=WHITE, width=w - 48, justify="center")

        canvas.bind("<Configure>", redraw)
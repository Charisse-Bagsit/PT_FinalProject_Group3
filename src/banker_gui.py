"""
banker_gui.py  -  Main window + navbar of Security D'Lock (Banker's Algorithm Simulator).
(Start the program by running main.py, not this file.)

Project layout  (inside src/)
    main.py           starts the program
    banker_gui.py     main window + navbar (this file)
    banker_logic.py   the algorithm (no GUI code)
    theme.py          colors, fonts, reusable widgets
    pages/            one file per page: home, background, how, simulator, dashboard, about

Flow:  Home -> Background -> How It Works -> Simulator -> Dashboard      (i) About
"""
import tkinter as tk
from theme import BG, PINK, WHITE, BLACK, F, round_rect, RoundButton, setup_styles
from pages.home import HomePage
from pages.background import BackgroundPage
from pages.how import HowPage
from pages.simulator import SimPage
from pages.dashboard import DashPage
from pages.about import AboutPage


class SharedState:
    """What the Simulator found - the Dashboard reads this."""

    def __init__(self):
        self.clear()

    def clear(self):
        self.names = []
        self.total = self.alloc = self.maxm = self.need = self.available = None
        self.result = None

    def set(self, names, total, alloc, maxm, need, available, result):
        self.names, self.total, self.alloc, self.maxm = names, total, alloc, maxm
        self.need, self.available, self.result = need, available, result


# ------------------------------------------------------------------ navbar
class NavBar(tk.Frame):
    ITEMS = [("home", "Home"), ("background", "Background"), ("how", "How It Works"),
             ("sim", "Simulator"), ("dash", "Dashboard")]

    def __init__(self, parent, on_nav):
        super().__init__(parent, bg=BG, height=72)
        self.pack_propagate(False)

        # Left Brand Logo + Title
        logo = tk.Canvas(self, width=52, height=52, bg=BG, highlightthickness=0)
        round_rect(logo, 2, 2, 50, 50, 14, fill=PINK, outline=BLACK, width=2)
        logo.create_text(26, 26, text="SD", font=F(15, True), fill=WHITE)
        logo.pack(side="left", padx=(18, 10), pady=10)
        tk.Label(self, text="Security D'Lock", font=F(15, True), fg=BLACK, bg=BG).pack(side="left")

        # Centered Navigation Buttons
        nav_group = tk.Frame(self, bg=BG)
        nav_group.place(relx=0.52, rely=0.5, anchor="center")

        self.buttons = {}
        for key, label in self.ITEMS:
            b = RoundButton(nav_group, label, lambda k=key: on_nav(k), width=128, height=46)
            b.pack(side="left", padx=5)
            self.buttons[key] = b

        # Right About (i) Button
        info = RoundButton(self, "i", lambda: on_nav("about"), width=46, height=46,
                           radius=14, font=F(16, True))
        info.pack(side="right", padx=18)
        self.buttons["about"] = info

    def set_active(self, key):
        for k, b in self.buttons.items():
            b.restyle(PINK if k == key else WHITE)


# ------------------------------------------------------------------ APP
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Security D'Lock — Banker's Algorithm Simulator")
        self.geometry("1240x780")
        self.minsize(1180, 700)
        self.configure(bg=BG)
        setup_styles()
        self.data = SharedState()

        self.nav = NavBar(self, self.show)
        self.nav.pack(fill="x")
        tk.Frame(self, bg=BLACK, height=2).pack(fill="x")
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for key, cls in (("home", HomePage), ("background", BackgroundPage), ("how", HowPage),
                         ("sim", SimPage), ("dash", DashPage), ("about", AboutPage)):
            page = cls(container, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[key] = page
        self.show("home")

    def show(self, key):
        page = self.pages[key]
        tk.Misc.tkraise(page)   # (Canvas overrides tkraise, so call the widget version)
        self.nav.set_active(key)
        page.on_show()
"""
pages/simulator.py  -  The actual program: input, Need matrix (with Finish array), safety steps,
and the Resource Request pop-up.
"""
import tkinter as tk
from tkinter import ttk, messagebox

import banker_logic as banker
from banker_logic import fmt
from theme import BG, HOT, LIGHT, WHITE, BLACK, GREEN, RED, MUTED, F, RoundButton, Card, make_tree
from pages.base import Page


# ------------------------------------------------------------------ SIMULATOR
class SimPage(Page):
    MAX_P, MAX_R = 6, 4

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.res = None
        self._revealed = 0
        self.res_names = []
        self.total_entries, self.alloc_entries, self.max_entries = [], [], []
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---- header
        head = tk.Frame(self, bg=BG)
        head.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(12, 6))
        left = tk.Frame(head, bg=BG)
        left.pack(side="left")
        tk.Label(left, text="Safety Simulator", font=F(22, True), bg=BG).pack(anchor="w")
        tk.Label(left, text="Enter the system state, then check if it is safe", font=F(11),
                 bg=BG).pack(anchor="w")
        RoundButton(head, "Resource Request", self.open_request, width=170, height=44).pack(side="right")
        RoundButton(head, "Clear", self.clear, width=90, height=44).pack(side="right", padx=8)
        RoundButton(head, "+  Load Sample", self.load_sample, width=160, height=44,
                    fill=HOT).pack(side="right")

        # ---- left card: input (maximized layout)
        lc = Card(self, width=490, height=10)
        lc.grid(row=1, column=0, sticky="ns", padx=(24, 8), pady=(0, 14))
        lc.grid_propagate(False)
        b = lc.body

        tk.Label(b, text="System Input", font=F(16, True), fg=HOT, bg=WHITE).pack(anchor="w", pady=(0, 4))

        ctl = tk.Frame(b, bg=WHITE)
        ctl.pack(fill="x", pady=(4, 10))
        tk.Label(ctl, text="Processes", font=F(11, True), bg=WHITE).pack(side="left")
        self.n_var, self.m_var = tk.IntVar(value=4), tk.IntVar(value=3)
        tk.Spinbox(ctl, from_=1, to=self.MAX_P, width=4, textvariable=self.n_var,
                   font=F(12), justify="center").pack(side="left", padx=(6, 16), ipady=3)
        tk.Label(ctl, text="Resources", font=F(11, True), bg=WHITE).pack(side="left")
        tk.Spinbox(ctl, from_=1, to=self.MAX_R, width=4, textvariable=self.m_var,
                   font=F(12), justify="center").pack(side="left", padx=(6, 14), ipady=3)
        RoundButton(ctl, "Build", self.build_clicked, width=105, height=38, radius=14,
                    fill=LIGHT, font=F(11, True)).pack(side="right")

        self.total_frame = tk.Frame(b, bg=WHITE)
        self.total_frame.pack(fill="x", pady=(6, 8))

        self.matrix_frame = tk.Frame(b, bg=WHITE)
        self.matrix_frame.pack(fill="both", expand=True, pady=(4, 8))

        btns = tk.Frame(b, bg=WHITE)
        btns.pack(side="bottom", fill="x", pady=(8, 0))
        RoundButton(btns, "Solve", lambda: self.solve(False), width=215, height=48,
                    font=F(12, True), fill=HOT).pack(side="left")
        RoundButton(btns, "Step-by-Step", lambda: self.solve(True), width=215, height=48,
                    font=F(12, True)).pack(side="right")

        # ---- right card: output
        rc = Card(self, width=10, height=10)
        rc.grid(row=1, column=1, sticky="nsew", padx=(8, 24), pady=(0, 14))
        rb = rc.body
        top = tk.Frame(rb, bg=WHITE)
        top.pack(fill="x")
        tk.Label(top, text="Need Matrix & Finish Status", font=F(14, True), fg=HOT, bg=WHITE).pack(side="left")
        # CHANGED: Available label 11 -> 13 (bigger, easier to read)
        self.avail_lbl = tk.Label(top, text="Available: -", font=F(13, True), bg=WHITE)
        self.avail_lbl.pack(side="right")

        # Finish column (False initially -> True when completed, matching class discussion)
        f1, self.tree1 = make_tree(rb, [
            ("p", "Process", 80, False),
            ("a", "Allocation", 120, True),
            ("m", "Max", 120, True),
            ("n", "Need", 120, True),
            ("f", "Finish", 110, False),
        ], 6)
        f1.pack(fill="x", pady=(4, 8))

        top2 = tk.Frame(rb, bg=WHITE)
        top2.pack(fill="x", pady=(6, 0))
        tk.Label(top2, text="Safety Check Steps", font=F(14, True), fg=HOT, bg=WHITE).pack(side="left")
        RoundButton(top2, "Show All", self.reveal_all, width=100, height=34, radius=12,
                    font=F(10, True)).pack(side="right")
        RoundButton(top2, "Next Step  ▶", self.reveal_next, width=130, height=34, radius=12,
                    fill=LIGHT, font=F(10, True)).pack(side="right", padx=6)

        # CHANGED: column widths slightly bigger so the larger font is not cut off
        f2, self.tree2 = make_tree(rb, [
            ("iter", "Iteration", 100, False),
            ("wb", "Work Before", 135, True),
            ("proc", "Process Selected", 165, True),
            ("rel", "Allocation Released", 180, True),
            ("wa", "Work After", 135, True),
        ], 6)
        f2.pack(fill="both", expand=True, pady=(4, 8))

        self.banner = tk.Label(rb, text="Press Solve or Step-by-Step to check the system.",
                               font=F(12, True), bg=LIGHT, pady=9)
        self.banner.pack(fill="x")

        self.build(4, 3)

    # ---------------- table building
    def build_clicked(self):
        try:
            n, m = int(self.n_var.get()), int(self.m_var.get())
        except (tk.TclError, ValueError):
            return messagebox.showerror("Invalid", "Processes and Resources must be whole numbers.")
        if not (1 <= n <= self.MAX_P and 1 <= m <= self.MAX_R):
            return messagebox.showerror("Invalid", f"Use 1-{self.MAX_P} processes and "
                                                   f"1-{self.MAX_R} resources.")
        self.build(n, m)

    def _entry(self, parent, width=5, font_size=12):
        e = tk.Entry(parent, width=width, justify="center", font=F(font_size), relief="flat", bg=WHITE,
                     highlightthickness=1, highlightbackground=BLACK, highlightcolor=HOT)
        return e

    def build(self, n, m):
        for fr in (self.total_frame, self.matrix_frame):
            for w in fr.winfo_children():
                w.destroy()
        self.res_names = list("ABCDEFGH")[:m]
        self.n_var.set(n)
        self.m_var.set(m)

        # ---- Total row
        tf = self.total_frame
        tk.Label(tf, text="Total", font=F(11, True), bg=WHITE,
                 width=6, anchor="w").grid(row=0, column=0, rowspan=2, sticky="w")
        self.total_entries = []
        for j, name in enumerate(self.res_names):
            tf.grid_columnconfigure(j + 1, weight=1)
            tk.Label(tf, text=name, font=F(10, True), fg=MUTED, bg=WHITE).grid(row=0, column=j + 1, pady=(0, 2))
            e = self._entry(tf, width=6, font_size=12)
            e.grid(row=1, column=j + 1, padx=4, pady=2, ipady=6, sticky="ew")
            self.total_entries.append(e)

        # ---- Allocation & Max matrices
        mf = self.matrix_frame
        mf.grid_columnconfigure(0, minsize=52)
        for j in range(m):
            mf.grid_columnconfigure(j + 1, weight=1)
            mf.grid_columnconfigure(m + 2 + j, weight=1)
        mf.grid_columnconfigure(m + 1, minsize=18)

        tk.Label(mf, text="Allocation", font=F(11, True), bg=WHITE).grid(
            row=0, column=1, columnspan=m, pady=(2, 2))
        tk.Label(mf, text="Max", font=F(11, True), bg=WHITE).grid(
            row=0, column=m + 2, columnspan=m, pady=(2, 2))

        for j, name in enumerate(self.res_names):
            tk.Label(mf, text=name, font=F(10, True), fg=MUTED, bg=WHITE).grid(row=1, column=j + 1, pady=(0, 4))
            tk.Label(mf, text=name, font=F(10, True), fg=MUTED, bg=WHITE).grid(row=1, column=m + 2 + j, pady=(0, 4))

        pad_y = 6 if n <= 4 else 4
        ipad_y = 6 if n <= 4 else 4
        box_w = 5 if m <= 3 else 4

        self.alloc_entries, self.max_entries = [], []
        for i in range(n):
            mf.grid_rowconfigure(i + 2, weight=1)
            tk.Label(mf, text=f"P{i}", font=F(11, True), bg=WHITE,
                     anchor="w").grid(row=i + 2, column=0, sticky="w")
            ar, mr = [], []
            for j in range(m):
                a = self._entry(mf, width=box_w, font_size=12)
                a.grid(row=i + 2, column=j + 1, padx=3, pady=pad_y, ipady=ipad_y, sticky="ew")
                x = self._entry(mf, width=box_w, font_size=12)
                x.grid(row=i + 2, column=m + 2 + j, padx=3, pady=pad_y, ipady=ipad_y, sticky="ew")
                ar.append(a)
                mr.append(x)
            self.alloc_entries.append(ar)
            self.max_entries.append(mr)
        self.reset_output()

    @staticmethod
    def _put(entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value))

    def load_sample(self):
        s = banker.SAMPLE
        n, m = len(s["alloc"]), len(s["total"])
        self.build(n, m)
        for j in range(m):
            self._put(self.total_entries[j], s["total"][j])
        for i in range(n):
            for j in range(m):
                self._put(self.alloc_entries[i][j], s["alloc"][i][j])
                self._put(self.max_entries[i][j], s["maxm"][i][j])

    def clear(self):
        self.build(self.n_var.get(), self.m_var.get())

    # ---------------- reading + validating the input
    def _read(self, entries, label):
        out = []
        for i, row in enumerate(entries):
            vals = []
            for j, e in enumerate(row):
                s = e.get().strip()
                try:
                    v = int(s)
                except ValueError:
                    raise ValueError(f"{label} of P{i}, resource {self.res_names[j]}: "
                                     f"'{s}' is not a whole number.")
                if v < 0:
                    raise ValueError(f"{label} of P{i}, resource {self.res_names[j]} cannot be negative.")
                vals.append(v)
            out.append(vals)
        return out

    def read_inputs(self):
        try:
            total = self._read([self.total_entries], "Total")[0]
            alloc = self._read(self.alloc_entries, "Allocation")
            maxm = self._read(self.max_entries, "Max")
            for i in range(len(alloc)):
                for j in range(len(total)):
                    if alloc[i][j] > maxm[i][j]:
                        raise ValueError(f"P{i}: Allocation of {self.res_names[j]} is bigger than its Max.")
            for j, used in enumerate(sum(col) for col in zip(*alloc)):
                if used > total[j]:
                    raise ValueError(f"Resource {self.res_names[j]}: allocated {used} is more than "
                                     f"the Total {total[j]}.")
        except ValueError as err:
            messagebox.showerror("Check your input", str(err))
            return None
        return total, alloc, maxm

    # ---------------- solving + showing steps
    def reset_output(self):
        self.res = None
        self._revealed = 0
        self.tree1.delete(*self.tree1.get_children())
        self.tree2.delete(*self.tree2.get_children())
        self.avail_lbl.config(text="Available: -")
        self.banner.config(text="Press Solve or Step-by-Step to check the system.", bg=LIGHT, fg=BLACK)
        self.app.data.clear()

    def solve(self, stepwise):
        data = self.read_inputs()
        if data is None:
            return
        total, alloc, maxm = data
        need = banker.compute_need(alloc, maxm)
        avail = banker.compute_available(total, alloc)
        self.res = banker.safety_check(alloc, need, avail)
        self.app.data.set(self.res_names[:], total, alloc, maxm, need, avail, self.res)

        self.tree1.delete(*self.tree1.get_children())
        self.tree2.delete(*self.tree2.get_children())
        self.rows1 = []
        # Initially: Finish = False for all processes
        for i in range(len(alloc)):
            self.rows1.append(self.tree1.insert("", "end", values=(
                f"P{i}", fmt(alloc[i]), fmt(maxm[i]), fmt(need[i]), "False")))
        self.avail_lbl.config(text="Available: " + fmt(avail))
        self.tree2.insert("", "end", values=(
            "Initial", fmt(avail), "—", "—", fmt(avail)
        ))
        self._revealed = 0
        if stepwise:
            self.banner.config(text="Step-by-step mode (Initially Finish = False): press  Next Step ▶", bg=LIGHT, fg=BLACK)
        else:
            self.reveal_all()

    def _total_rows(self):
        return len(self.res["steps"]) + (0 if self.res["safe"] else 1)

    def reveal_next(self):
        if self.res is None:
            return messagebox.showinfo("Nothing to show", "Press Solve or Step-by-Step first.")
        k = self._revealed
        if k >= self._total_rows():
            return
        steps = self.res["steps"]
        if k < len(steps):
            s = steps[k]
            self.tree2.insert("", "end", tags=("ok",), values=(
                k + 1,
                fmt(s["work_before"]),
                f"P{s['index']}",
                fmt(s["allocation"]),
                fmt(s["work_after"]),
            ))
            # Update Finish from False -> True
            self.tree1.item(self.rows1[s["index"]], tags=("ok",))
            self.tree1.set(self.rows1[s["index"]], "f", "True")
        else:
            stuck = ", ".join(f"P{i}" for i in self.res["stuck"])
            self.tree2.insert("", "end", tags=("bad",), values=(
                "-",
                fmt(self.res["final_work"]),
                "Stuck: " + stuck,
                "—",
                fmt(self.res["final_work"]),
            ))
            for i in self.res["stuck"]:
                self.tree1.item(self.rows1[i], tags=("bad",))
                self.tree1.set(self.rows1[i], "f", "False")
        self._revealed += 1
        if self._revealed >= self._total_rows():
            self._final_banner()

    def reveal_all(self):
        if self.res is None:
            return messagebox.showinfo("Nothing to show", "Press Solve or Step-by-Step first.")
        while self._revealed < self._total_rows():
            self.reveal_next()

    def _final_banner(self):
        if self.res["safe"]:
            seq = " → ".join(f"P{i}" for i in self.res["sequence"])
            self.banner.config(text=f"SAFE STATE (All Finish = True)    Safe Sequence:  {seq}", bg=GREEN, fg=WHITE)
        else:
            stuck = ", ".join(f"P{i}" for i in self.res["stuck"])
            self.banner.config(text=f"UNSAFE STATE (Some Finish = False)    Stuck: {stuck}", bg=RED, fg=WHITE)

    # ---------------- resource request
    def open_request(self):
        data = self.read_inputs()
        if data:
            RequestDialog(self, *data)

    def apply_request(self, pid, request):
        for j, r in enumerate(request):
            cur = int(self.alloc_entries[pid][j].get())
            self._put(self.alloc_entries[pid][j], cur + r)
        self.solve(False)


class RequestDialog(tk.Toplevel):
    """Pop-up like the 'Report Lost/Found Items' modal in the wireframe."""

    def __init__(self, sim, total, alloc, maxm):
        super().__init__(sim.app)
        self.sim, self.total, self.alloc, self.maxm = sim, total, alloc, maxm
        self.last = None
        self.title("Resource Request")
        self.configure(bg=WHITE, padx=26, pady=18)
        self.resizable(False, False)
        self.transient(sim.app)

        tk.Label(self, text="Resource Request", font=F(20, True), fg=HOT, bg=WHITE).pack(anchor="w")
        tk.Label(self, text="Can this process be given extra resources and still stay safe?",
                 font=F(10), fg=MUTED, bg=WHITE).pack(anchor="w", pady=(0, 10))

        tk.Label(self, text="Process", font=F(10, True), bg=WHITE).pack(anchor="w")
        self.proc = ttk.Combobox(self, values=[f"P{i}" for i in range(len(alloc))],
                                 state="readonly", width=10, font=F(11))
        self.proc.pack(anchor="w", pady=(2, 4))
        self.proc.bind("<<ComboboxSelected>>", self.update_hint)
        self.hint = tk.Label(self, text="", font=F(10), fg=MUTED, bg=WHITE, justify="left")
        self.hint.pack(anchor="w", pady=(0, 8))

        tk.Label(self, text="Request", font=F(10, True), bg=WHITE).pack(anchor="w")
        row = tk.Frame(self, bg=WHITE)
        row.pack(anchor="w", pady=4)
        self.entries = []
        for j, name in enumerate(sim.res_names):
            tk.Label(row, text=name, font=F(10), fg=MUTED, bg=WHITE).grid(row=0, column=j)
            e = sim._entry(row, width=5, font_size=11)
            e.grid(row=1, column=j, padx=4, ipady=4)
            e.insert(0, "0")
            self.entries.append(e)

        self.msg = tk.Label(self, text="", font=F(11, True), bg=WHITE, wraplength=380, justify="left")
        self.msg.pack(anchor="w", pady=10)
        bar = tk.Frame(self, bg=WHITE)
        bar.pack(anchor="w")
        RoundButton(bar, "Check Request", self.check, width=150, fill=HOT).pack(side="left")
        self.apply_btn = RoundButton(bar, "Apply to Table", self.apply, width=150, fill=GREEN, fg=WHITE)
        RoundButton(bar, "Close", self.destroy, width=90).pack(side="right", padx=(8, 0))

        self.update_idletasks()
        x = sim.app.winfo_x() + (sim.app.winfo_width() - self.winfo_reqwidth()) // 2
        y = sim.app.winfo_y() + (sim.app.winfo_height() - self.winfo_reqheight()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        try:
            self.grab_set()
        except tk.TclError:
            pass

    def update_hint(self, _=None):
        i = self.proc.current()
        need = banker.compute_need(self.alloc, self.maxm)[i]
        avail = banker.compute_available(self.total, self.alloc)
        self.hint.config(text=f"Need: {fmt(need)}     Available: {fmt(avail)}")

    def check(self):
        pid = self.proc.current()
        if pid < 0:
            return self.show("Please choose a process first.", RED)
        try:
            req = [int(e.get()) for e in self.entries]
            if any(r < 0 for r in req):
                raise ValueError
        except ValueError:
            return self.show("Request values must be whole numbers (0 or more).", RED)
        self.apply_btn.pack_forget()
        out = banker.request_resource(pid, req, self.total, self.alloc, self.maxm)
        self.last = (pid, req) if out["granted"] else None
        self.show(out["reason"].replace(" -> ", " → "), GREEN if out["granted"] else RED)
        if out["granted"]:
            self.apply_btn.pack(side="left", padx=8)

    def show(self, text, color):
        self.msg.config(text=text, fg=color)

    def apply(self):
        if self.last:
            self.sim.apply_request(*self.last)
        self.destroy()
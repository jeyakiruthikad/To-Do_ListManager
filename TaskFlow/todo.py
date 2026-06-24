import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
CATEGORIES = ["All", "Work", "Personal", "Urgent", "Other"]
DATE_FORMAT = "%Y-%m-%d"

BG      = "#1E1E2E"
PANEL   = "#2A2A3E"
CARD    = "#313145"
ACCENT  = "#7C6AF7"
ACCENT2 = "#F25F7A"
SUCCESS = "#3DD68C"
WARNING = "#F7C56A"
MUTED   = "#6E6E8E"
TEXT    = "#E4E4F0"
SUBTEXT = "#A0A0C0"

CAT_COLORS = {
    "Work":     "#4EA8FF",
    "Personal": "#3DD68C",
    "Urgent":   "#F25F7A",
    "Other":    "#F7C56A",
}

# ── Task model ────────────────────────────────────────────────────────────────
class Task:
    def __init__(self, title, description="", category="Other", deadline="",
                 completed=False, created_at=None):
        self.title       = title
        self.description = description
        self.category    = category
        self.deadline     = deadline  # "" or "YYYY-MM-DD"
        self.completed    = completed
        self.created_at   = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        # Defensive: ignore unknown keys, fill in missing ones via defaults
        known = {"title", "description", "category", "deadline", "completed", "created_at"}
        return cls(**{k: v for k, v in d.items() if k in known})

# ── Persistence ───────────────────────────────────────────────────────────────
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return [Task.from_dict(d) for d in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ── Styled button (plain tk.Button, works on all Python versions) ─────────────
def StyledButton(parent, text, command=None, bg=ACCENT, fg=TEXT, font_size=10):
    def lighten(hex_color):
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"
    btn = tk.Button(parent, text=text, command=command,
                    bg=bg, fg=fg,
                    activebackground=lighten(bg), activeforeground=fg,
                    relief="flat", borderwidth=0,
                    font=("Segoe UI", font_size, "bold"),
                    cursor="hand2", padx=14, pady=8)
    btn.bind("<Enter>", lambda e: btn.config(bg=lighten(bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# ── Main Application ──────────────────────────────────────────────────────────
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ TaskFlow")
        self.geometry("900x640")
        self.minsize(750, 500)
        self.configure(bg=BG)

        self.tasks          = load_tasks()
        self.active_filter  = tk.StringVar(value="All")
        self.search_var     = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh())
        self._editing_index = None
        self._search_has_placeholder = True

        self._build_ui()
        self._refresh()

    # ── UI skeleton ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=PANEL, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="✦ TaskFlow", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(pady=(28, 4), padx=20, anchor="w")
        tk.Label(self.sidebar, text="Stay focused, stay ahead.",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(padx=20, anchor="w")

        ttk.Separator(self.sidebar).pack(fill="x", padx=20, pady=18)

        tk.Label(self.sidebar, text="CATEGORIES", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(padx=20, anchor="w", pady=(0, 8))

        self._cat_btns = {}
        for cat in CATEGORIES:
            btn = tk.Label(self.sidebar, text=f"  {cat}", bg=PANEL, fg=SUBTEXT,
                           font=("Segoe UI", 10), cursor="hand2", anchor="w", pady=6)
            btn.pack(fill="x", padx=12)
            btn.bind("<Button-1>", lambda e, c=cat: self._set_filter(c))
            btn.bind("<Enter>",    lambda e, b=btn: b.config(fg=TEXT))
            btn.bind("<Leave>",    lambda e, b=btn, c=cat:
                     b.config(fg=TEXT if self.active_filter.get() == c else SUBTEXT))
            self._cat_btns[cat] = btn

        ttk.Separator(self.sidebar).pack(fill="x", padx=20, pady=18)

        self.stats_label = tk.Label(self.sidebar, text="", bg=PANEL, fg=MUTED,
                                    font=("Segoe UI", 9), justify="left")
        self.stats_label.pack(padx=20, anchor="w")

        # Main area
        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Top bar
        topbar = tk.Frame(main, bg=BG)
        topbar.pack(fill="x", padx=24, pady=(24, 0))

        self.page_title = tk.Label(topbar, text="All Tasks", bg=BG, fg=TEXT,
                                   font=("Segoe UI", 18, "bold"))
        self.page_title.pack(side="left")

        add_btn = StyledButton(topbar, "＋  New Task",
                               command=self._open_add_dialog, bg=ACCENT)
        add_btn.pack(side="right")

        # Search bar
        search_frame = tk.Frame(main, bg=CARD, padx=10, pady=6)
        search_frame.pack(fill="x", padx=24, pady=16)
        tk.Label(search_frame, text="🔍", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 11)).pack(side="left", padx=(4, 6))
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     bg=CARD, fg=MUTED, insertbackground=TEXT,
                                     relief="flat", font=("Segoe UI", 11), bd=0)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.insert(0, "Search tasks…")
        self.search_entry.bind("<FocusIn>",  self._search_focus_in)
        self.search_entry.bind("<FocusOut>", self._search_focus_out)

        # Scrollable task list
        self.list_canvas = tk.Canvas(main, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main, orient="vertical",
                                  command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 8))
        self.list_canvas.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.task_frame = tk.Frame(self.list_canvas, bg=BG)
        self._canvas_win = self.list_canvas.create_window(
            (0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>",
            lambda e: self.list_canvas.configure(
                scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.bind("<Configure>",
            lambda e: self.list_canvas.itemconfig(self._canvas_win, width=e.width))
        self.list_canvas.bind("<MouseWheel>",
            lambda e: self.list_canvas.yview_scroll(-1*(e.delta//120), "units"))

    # ── Search placeholder ────────────────────────────────────────────────────
    def _search_focus_in(self, e):
        if self._search_has_placeholder:
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=TEXT)
            self._search_has_placeholder = False

    def _search_focus_out(self, e):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search tasks…")
            self.search_entry.config(fg=MUTED)
            self._search_has_placeholder = True

    def _get_search_text(self):
        return "" if self._search_has_placeholder else self.search_var.get().lower()

    # ── Filtering ────────────────────────────────────────────────────────────
    def _set_filter(self, cat):
        self.active_filter.set(cat)
        self.page_title.config(text=f"{cat} Tasks")
        self._refresh()

    def _filtered_tasks(self):
        cat = self.active_filter.get()
        q   = self._get_search_text()
        items = [
            (i, t) for i, t in enumerate(self.tasks)
            if (cat == "All" or t.category == cat)
            and (not q or q in t.title.lower() or q in t.description.lower())
        ]

        # Sort: incomplete tasks with the nearest deadline first, then
        # incomplete tasks with no deadline, then completed tasks at the end.
        def sort_key(pair):
            _, t = pair
            if t.completed:
                return (2, "")
            if t.deadline:
                return (0, t.deadline)
            return (1, "")

        return sorted(items, key=sort_key)

    # ── Deadline helpers ─────────────────────────────────────────────────────
    @staticmethod
    def _parse_deadline(text):
        """Returns a date object or None if text is empty/invalid."""
        text = text.strip()
        if not text:
            return None
        return datetime.strptime(text, DATE_FORMAT).date()

    def _deadline_status(self, task):
        """Returns (color, suffix_text) describing how urgent the deadline is."""
        if task.completed or not task.deadline:
            return MUTED, ""
        try:
            due = datetime.strptime(task.deadline, DATE_FORMAT).date()
        except ValueError:
            return MUTED, ""
        delta = (due - datetime.now().date()).days
        if delta < 0:
            return ACCENT2, "  ·  overdue"
        elif delta == 0:
            return WARNING, "  ·  due today"
        elif delta <= 2:
            return WARNING, f"  ·  due in {delta}d"
        return SUBTEXT, ""

    # ── Render ────────────────────────────────────────────────────────────────
    def _refresh(self):
        for w in self.task_frame.winfo_children():
            w.destroy()

        for cat, btn in self._cat_btns.items():
            btn.config(fg=TEXT if cat == self.active_filter.get() else SUBTEXT)

        total = len(self.tasks)
        done  = sum(1 for t in self.tasks if t.completed)
        self.stats_label.config(text=f"{done}/{total} completed")

        items = self._filtered_tasks()
        if not items:
            tk.Label(self.task_frame,
                     text="No tasks here yet.\nClick  ＋ New Task  to begin!",
                     bg=BG, fg=MUTED, font=("Segoe UI", 12), justify="center"
                     ).pack(pady=60)
            return

        for orig_idx, task in items:
            self._render_card(orig_idx, task)

    def _render_card(self, idx, task):
        card = tk.Frame(self.task_frame, bg=CARD)
        card.pack(fill="x", pady=6)

        cat_color = CAT_COLORS.get(task.category, ACCENT)

        tk.Frame(card, bg=cat_color, width=4).pack(side="left", fill="y")

        body = tk.Frame(card, bg=CARD, padx=16, pady=12)
        body.pack(side="left", fill="both", expand=True)

        row1 = tk.Frame(body, bg=CARD)
        row1.pack(fill="x")

        title_txt = f"✓  {task.title}" if task.completed else task.title
        tk.Label(row1, text=title_txt, bg=CARD,
                 fg=MUTED if task.completed else TEXT,
                 font=("Segoe UI", 12, "normal" if task.completed else "bold"),
                 anchor="w").pack(side="left")

        tk.Label(row1, text=f"  {task.category}  ", bg=cat_color, fg=BG,
                 font=("Segoe UI", 8, "bold"), padx=4, pady=2
                 ).pack(side="left", padx=10)

        if task.description:
            tk.Label(body, text=task.description, bg=CARD, fg=SUBTEXT,
                     font=("Segoe UI", 10), anchor="w",
                     wraplength=480, justify="left").pack(fill="x", pady=(4, 0))

        meta_row = tk.Frame(body, bg=CARD)
        meta_row.pack(fill="x", pady=(8, 0))

        tk.Label(meta_row, text=f"🕐  {task.created_at}", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="left")

        if task.deadline:
            color, suffix = self._deadline_status(task)
            is_urgent = color in (ACCENT2, WARNING)
            tk.Label(meta_row, text=f"   📅  Due {task.deadline}{suffix}",
                     bg=CARD, fg=color,
                     font=("Segoe UI", 8, "bold" if is_urgent else "normal")
                     ).pack(side="left")

        # Action buttons on the right
        actions = tk.Frame(card, bg=CARD, padx=10, pady=10)
        actions.pack(side="right", fill="y", anchor="center")

        if not task.completed:
            StyledButton(actions, "✓ Done",
                         command=lambda i=idx: self._complete_task(i),
                         bg=SUCCESS, fg=BG, font_size=9
                         ).pack(fill="x", pady=3)

        StyledButton(actions, "✎ Edit",
                     command=lambda i=idx: self._open_edit_dialog(i),
                     bg=PANEL, fg=TEXT, font_size=9
                     ).pack(fill="x", pady=3)

        StyledButton(actions, "✕ Delete",
                     command=lambda i=idx: self._delete_task(i),
                     bg=ACCENT2, fg=TEXT, font_size=9
                     ).pack(fill="x", pady=3)

    # ── Task actions ─────────────────────────────────────────────────────────
    def _complete_task(self, idx):
        self.tasks[idx].mark_completed()
        save_tasks(self.tasks)
        self._refresh()

    def _delete_task(self, idx):
        task_title = self.tasks[idx].title
        if messagebox.askyesno("Delete Task", f'Delete "{task_title}"?',
                               icon="warning"):
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self._refresh()

    # ── Add / Edit dialog ─────────────────────────────────────────────────────
    def _open_add_dialog(self):
        self._editing_index = None
        self._open_dialog("Add New Task", "＋  Add Task")

    def _open_edit_dialog(self, idx):
        self._editing_index = idx
        t = self.tasks[idx]
        self._open_dialog("Edit Task", "💾  Save Changes",
                          title=t.title, desc=t.description, cat=t.category,
                          deadline=t.deadline)

    def _open_dialog(self, header, btn_label, title="", desc="", cat="Other", deadline=""):
        dlg = tk.Toplevel(self)
        dlg.title(header)
        dlg.configure(bg=PANEL)
        dlg.geometry("480x560")   # taller to fit the new deadline field
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - 480) // 2
        y = self.winfo_y() + (self.winfo_height() - 560) // 2
        dlg.geometry(f"+{x}+{y}")

        PAD = dict(padx=28, pady=6)

        tk.Label(dlg, text=header, bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=28, pady=(24, 8))

        # Title field
        tk.Label(dlg, text="Title *", bg=PANEL, fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", **PAD)
        title_entry = tk.Entry(dlg, bg=CARD, fg=TEXT,
                               insertbackground=TEXT, relief="flat",
                               font=("Segoe UI", 11), bd=8)
        title_entry.pack(fill="x", **PAD)
        if title:
            title_entry.insert(0, title)
        title_entry.focus_set()

        # Description field
        tk.Label(dlg, text="Description (optional)", bg=PANEL, fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", **PAD)
        desc_text = tk.Text(dlg, bg=CARD, fg=TEXT, insertbackground=TEXT,
                            relief="flat", font=("Segoe UI", 11),
                            height=4, bd=8, wrap="word")
        desc_text.pack(fill="x", **PAD)
        if desc:
            desc_text.insert("1.0", desc)

        # Category dropdown
        tk.Label(dlg, text="Category", bg=PANEL, fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", **PAD)
        cat_var = tk.StringVar(value=cat)
        cat_menu = ttk.Combobox(dlg, textvariable=cat_var,
                                values=CATEGORIES[1:],
                                state="readonly", font=("Segoe UI", 11))
        cat_menu.pack(fill="x", **PAD)
        # Make sure the box actually shows the right starting value
        if cat in CATEGORIES[1:]:
            cat_menu.current(CATEGORIES[1:].index(cat))

        # Deadline field
        tk.Label(dlg, text="Deadline (optional, YYYY-MM-DD)", bg=PANEL, fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", **PAD)
        deadline_entry = tk.Entry(dlg, bg=CARD, fg=TEXT,
                                  insertbackground=TEXT, relief="flat",
                                  font=("Segoe UI", 11), bd=8)
        deadline_entry.pack(fill="x", **PAD)
        if deadline:
            deadline_entry.insert(0, deadline)

        # Submit
        def submit():
            t = title_entry.get().strip()
            if not t:
                messagebox.showwarning("Missing Title",
                                       "Please enter a task title.", parent=dlg)
                title_entry.focus_set()
                return

            d = desc_text.get("1.0", "end-1c").strip()

            # Read the category straight from the widget itself (cat_menu.get())
            # rather than the bound StringVar -- this is what was causing every
            # task to save as "Other" regardless of what was picked.
            c = cat_menu.get() or "Other"

            dl_raw = deadline_entry.get().strip()
            if dl_raw:
                try:
                    datetime.strptime(dl_raw, DATE_FORMAT)
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Deadline",
                        "Please use the format YYYY-MM-DD (e.g., 2026-07-04).",
                        parent=dlg)
                    deadline_entry.focus_set()
                    return

            if self._editing_index is None:
                self.tasks.append(Task(t, d, c, dl_raw))
            else:
                task = self.tasks[self._editing_index]
                task.title, task.description, task.category, task.deadline = t, d, c, dl_raw
            save_tasks(self.tasks)
            self._refresh()
            dlg.destroy()

        dlg.bind("<Return>", lambda e: submit())

        # Button row at the bottom
        btn_frame = tk.Frame(dlg, bg=PANEL)
        btn_frame.pack(fill="x", padx=28, pady=20)

        StyledButton(btn_frame, btn_label, command=submit,
                     bg=ACCENT, fg=TEXT, font_size=11).pack(side="left")

        StyledButton(btn_frame, "Cancel", command=dlg.destroy,
                     bg=MUTED, fg=TEXT, font_size=11).pack(side="left", padx=(12, 0))


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TScrollbar", troughcolor=PANEL, background=MUTED,
                    bordercolor=PANEL, arrowcolor=MUTED)
    style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                    foreground=TEXT, selectbackground=ACCENT,
                    selectforeground=TEXT)
    style.map("TCombobox", fieldbackground=[("readonly", CARD)])

    app = TodoApp()
    app.mainloop()
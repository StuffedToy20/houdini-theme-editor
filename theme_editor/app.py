"""Tk application shell for the Houdini theme editor."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox

from .bindings import BINDINGS, KEY_TO_PRIMARY, SECTION_ORDER, Binding
from .core import (
    DEFAULT_NEW_THEME_NAME,
    HCSDocument,
    build_channel_family_palette,
    find_houdini_config_dirs,
    hex_to_rgb,
    rgb_to_hex,
)
from .previews import ThemePreviewMixin


class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc, bg: str) -> None:
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)

        self.inner.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(self.window_id, width=event.width),
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event: tk.Event) -> None:
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass


class HCSThemeEditorApp(ThemePreviewMixin):
    def __init__(self, root: tk.Tk, initial_path: Path | None) -> None:
        self.root = root
        self.root.title("Houdini HCS Theme Editor")
        self.root.geometry("1460x980")
        self.root.minsize(1180, 760)

        self.bg = "#1E2124"
        self.panel = "#272B30"
        self.panel_alt = "#23272B"
        self.line = "#373C42"
        self.text = "#D7DDE3"
        self.subtle = "#96A0AA"

        self.root.configure(bg=self.bg)

        self.document: HCSDocument | None = None
        self.current_colors: dict[str, tuple[float, float, float]] = {}
        self.entry_vars: dict[str, tk.StringVar] = {}
        self.entry_widgets: dict[str, tk.Entry] = {}
        self.swatches: dict[str, tk.Label] = {}
        self.status_var = tk.StringVar(value="Ready.")
        self.path_var = tk.StringVar()
        self.config_path_var = tk.StringVar()
        self.family_seed_var = tk.StringVar(value="#34D399")
        self.preview_canvases: dict[str, tk.Canvas] = {}
        self.detected_config_dirs: list[Path] = []
        self.family_seed_entry: tk.Entry | None = None
        self.family_seed_swatch: tk.Label | None = None
        self.document_is_generated = False

        self._build_ui()
        self.detect_houdini_config_dirs(initial_hint=initial_path)
        if initial_path is not None:
            self.load_document(initial_path)
        else:
            self.create_new_overlay_document(update_status=False)

    def _build_ui(self) -> None:
        toolbar = tk.Frame(self.root, bg=self.panel, padx=12, pady=10)
        toolbar.pack(fill="x")

        tk.Label(toolbar, text="Theme File", bg=self.panel, fg=self.text, font=("Segoe UI", 10, "bold")).pack(side="left")

        path_entry = tk.Entry(
            toolbar,
            textvariable=self.path_var,
            bg=self.panel_alt,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            width=70,
            font=("Consolas", 10),
        )
        path_entry.pack(side="left", fill="x", expand=True, padx=(10, 8))

        self._make_toolbar_button(toolbar, "New Overlay", self.create_new_overlay_document)
        self._make_toolbar_button(toolbar, "Browse", self.browse_file)
        self._make_toolbar_button(toolbar, "Load", self.reload_file)
        self._make_toolbar_button(toolbar, "Save", self.save_file)
        self._make_toolbar_button(toolbar, "Save As", self.save_as)

        deploy_bar = tk.Frame(self.root, bg=self.panel_alt, padx=12, pady=8)
        deploy_bar.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(deploy_bar, text="Houdini Config", bg=self.panel_alt, fg=self.text, font=("Segoe UI", 10, "bold")).pack(side="left")

        config_entry = tk.Entry(
            deploy_bar,
            textvariable=self.config_path_var,
            state="readonly",
            readonlybackground=self.bg,
            fg=self.text,
            relief="flat",
            width=70,
            font=("Consolas", 10),
        )
        config_entry.pack(side="left", fill="x", expand=True, padx=(10, 8))

        self._make_toolbar_button(deploy_bar, "Detect", self.detect_houdini_config_dirs)
        self._make_toolbar_button(deploy_bar, "Deploy to Config", self.deploy_to_detected_config)

        body = tk.PanedWindow(self.root, sashwidth=6, bg=self.bg, orient="horizontal")
        body.pack(fill="both", expand=True, padx=10, pady=(8, 10))

        control_shell = tk.Frame(body, bg=self.panel, width=560)
        preview_shell = tk.Frame(body, bg=self.panel)
        body.add(control_shell, minsize=420)
        body.add(preview_shell, minsize=520)

        self.controls = ScrollableFrame(control_shell, self.panel)
        self.controls.pack(fill="both", expand=True)

        tk.Label(
            self.controls.inner,
            text="Edit colors as hex. Pick a swatch to choose visually. Save writes the active values back into the .hcs file.",
            bg=self.panel,
            fg=self.subtle,
            justify="left",
            wraplength=500,
            font=("Segoe UI", 10),
            padx=14,
            pady=14,
        ).pack(fill="x")

        for section in SECTION_ORDER:
            self._build_section(section)

        preview_header = tk.Frame(preview_shell, bg=self.panel, padx=14, pady=12)
        preview_header.pack(fill="x")
        tk.Label(preview_header, text="Preview", bg=self.panel, fg=self.text, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(
            preview_header,
            text="These are simplified demos of the parameter editor, slider strip, channel editor, and node graph.",
            bg=self.panel,
            fg=self.subtle,
            wraplength=780,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        preview_scroll = ScrollableFrame(preview_shell, self.panel)
        preview_scroll.pack(fill="both", expand=True)
        self._add_preview_canvas(preview_scroll.inner, "menus", 780, 180, "Menus")
        self._add_preview_canvas(preview_scroll.inner, "parameter", 780, 300, "Parameter States")
        self._add_preview_canvas(preview_scroll.inner, "slider", 780, 180, "Slider / Keyframes")
        self._add_preview_canvas(preview_scroll.inner, "channel", 780, 220, "Channel Editor")
        self._add_preview_canvas(preview_scroll.inner, "graph", 780, 380, "Node Graph")

        tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=self.panel,
            fg=self.subtle,
            anchor="w",
            padx=12,
            pady=8,
            font=("Segoe UI", 9),
        ).pack(fill="x", side="bottom")

    def _make_toolbar_button(self, master: tk.Misc, text: str, command) -> tk.Button:
        button = tk.Button(
            master,
            text=text,
            command=command,
            bg=self.panel_alt,
            fg=self.text,
            activebackground=self.line,
            activeforeground=self.text,
            relief="flat",
            padx=12,
            pady=6,
            font=("Segoe UI", 9),
            bd=0,
            highlightthickness=0,
        )
        button.pack(side="left", padx=(0, 8))
        return button

    def _build_section(self, section: str) -> None:
        frame = tk.LabelFrame(
            self.controls.inner,
            text=section,
            bg=self.panel_alt,
            fg=self.text,
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=12,
            bd=1,
            relief="solid",
            highlightbackground=self.line,
            highlightcolor=self.line,
        )
        frame.pack(fill="x", padx=12, pady=(0, 12))
        if section == "Channel Families":
            self._build_family_palette_generator(frame)
        for binding in (item for item in BINDINGS if item.section == section):
            self._build_binding_row(frame, binding)

    def _build_family_palette_generator(self, master: tk.Misc) -> None:
        block = tk.Frame(master, bg=self.bg, padx=12, pady=12, bd=1, relief="solid", highlightbackground=self.line, highlightcolor=self.line)
        block.pack(fill="x", pady=(0, 12))

        tk.Label(block, text="Generate family palette from one base color", bg=self.bg, fg=self.text, anchor="w", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(
            block,
            text="Pick one base color, then generate 5 linked channel-family colors automatically.",
            bg=self.bg,
            fg=self.subtle,
            anchor="w",
            justify="left",
            wraplength=470,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(4, 10))

        row = tk.Frame(block, bg=self.bg)
        row.pack(fill="x")

        tk.Label(row, text="Base family color", bg=self.bg, fg=self.text, width=22, anchor="w", font=("Segoe UI", 10, "bold")).pack(side="left")

        self.family_seed_entry = tk.Entry(
            row,
            textvariable=self.family_seed_var,
            bg=self.panel_alt,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            width=12,
            font=("Consolas", 10),
        )
        self.family_seed_entry.pack(side="left", padx=(0, 8))
        self.family_seed_entry.bind("<Return>", lambda event: self.commit_family_seed())
        self.family_seed_entry.bind("<FocusOut>", lambda event: self.commit_family_seed())

        self.family_seed_swatch = tk.Label(row, text="    ", bg=self.family_seed_var.get(), relief="solid", bd=1, cursor="hand2")
        self.family_seed_swatch.pack(side="left", padx=(0, 8))
        self.family_seed_swatch.bind("<Button-1>", lambda event: self.pick_family_seed_color())

        tk.Button(
            row,
            text="Pick",
            command=self.pick_family_seed_color,
            bg=self.panel_alt,
            fg=self.text,
            activebackground=self.line,
            activeforeground=self.text,
            relief="flat",
            padx=10,
            pady=4,
            bd=0,
            highlightthickness=0,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            row,
            text="Use Green 3",
            command=self.seed_family_from_current,
            bg=self.panel_alt,
            fg=self.text,
            activebackground=self.line,
            activeforeground=self.text,
            relief="flat",
            padx=10,
            pady=4,
            bd=0,
            highlightthickness=0,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            row,
            text="Generate Palette",
            command=self.generate_channel_family_palette,
            bg=self.panel,
            fg=self.text,
            activebackground=self.line,
            activeforeground=self.text,
            relief="flat",
            padx=12,
            pady=4,
            bd=0,
            highlightthickness=0,
        ).pack(side="left")

    def _build_binding_row(self, master: tk.Misc, binding: Binding) -> None:
        row = tk.Frame(master, bg=self.panel_alt, pady=6)
        row.pack(fill="x")

        top = tk.Frame(row, bg=self.panel_alt)
        top.pack(fill="x")

        tk.Label(top, text=binding.label, bg=self.panel_alt, fg=self.text, width=22, anchor="w", font=("Segoe UI", 10, "bold")).pack(side="left")

        variable = tk.StringVar()
        entry = tk.Entry(
            top,
            textvariable=variable,
            bg=self.bg,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            width=12,
            font=("Consolas", 10),
        )
        entry.pack(side="left", padx=(0, 8))
        entry.bind("<Return>", lambda event, key=binding.primary_key: self.commit_entry(key))
        entry.bind("<FocusOut>", lambda event, key=binding.primary_key: self.commit_entry(key))

        swatch = tk.Label(top, text="    ", bg=rgb_to_hex(binding.fallback), relief="solid", bd=1, cursor="hand2")
        swatch.pack(side="left", padx=(0, 8))
        swatch.bind("<Button-1>", lambda event, item=binding: self.pick_color(item))

        tk.Button(
            top,
            text="Pick",
            command=lambda item=binding: self.pick_color(item),
            bg=self.bg,
            fg=self.text,
            activebackground=self.line,
            activeforeground=self.text,
            relief="flat",
            padx=10,
            pady=4,
            bd=0,
            highlightthickness=0,
        ).pack(side="left")

        tk.Label(
            row,
            text=", ".join(binding.keys),
            bg=self.panel_alt,
            fg=self.subtle,
            anchor="w",
            justify="left",
            wraplength=470,
            font=("Consolas", 8),
        ).pack(fill="x", pady=(3, 0))

        tk.Label(
            row,
            text=binding.note,
            bg=self.panel_alt,
            fg=self.subtle,
            anchor="w",
            justify="left",
            wraplength=470,
            font=("Segoe UI", 9),
        ).pack(fill="x", pady=(1, 0))

        self.entry_vars[binding.primary_key] = variable
        self.entry_widgets[binding.primary_key] = entry
        self.swatches[binding.primary_key] = swatch

    def _add_preview_canvas(self, master: tk.Misc, key: str, width: int, height: int, title: str) -> None:
        wrapper = tk.Frame(master, bg=self.panel, padx=14, pady=12)
        wrapper.pack(fill="x")
        tk.Label(wrapper, text=title, bg=self.panel, fg=self.text, anchor="w", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        canvas = tk.Canvas(wrapper, width=width, height=height, bg=self.bg, highlightbackground=self.line, highlightcolor=self.line, bd=1, relief="solid")
        canvas.pack(fill="x", expand=True)
        canvas.bind("<Configure>", lambda event: self.redraw_previews())
        self.preview_canvases[key] = canvas

    def create_new_overlay_document(self, update_status: bool = True) -> None:
        self.document = HCSDocument.new_overlay()
        self.document_is_generated = True
        self.path_var.set(str(self.document.path))
        self.current_colors.clear()
        for binding in BINDINGS:
            color = self._resolve_binding_color(binding)
            self.current_colors[binding.primary_key] = color
            self._set_binding_ui(binding.primary_key, color)
        self.seed_family_from_current(update_status=False)
        self.redraw_previews()
        if update_status:
            self.status_var.set("Created a new overlay theme. Save As or Deploy to write it.")

    def browse_file(self) -> None:
        selected = filedialog.askopenfilename(
            title="Open Houdini .hcs file",
            filetypes=[("Houdini Color Scheme", "*.hcs"), ("All files", "*.*")],
        )
        if selected:
            self.load_document(Path(selected))

    def reload_file(self) -> None:
        if not self.path_var.get().strip():
            self.browse_file()
            return
        self.load_document(Path(self.path_var.get().strip()))

    def load_document(self, path: Path) -> None:
        try:
            self.document = HCSDocument.load(path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Load failed", f"Could not load file:\n{path}\n\n{exc}")
            return

        self.document_is_generated = False
        self.path_var.set(str(path))
        self.current_colors.clear()
        for binding in BINDINGS:
            color = self._resolve_binding_color(binding)
            self.current_colors[binding.primary_key] = color
            self._set_binding_ui(binding.primary_key, color)
        self.seed_family_from_current(update_status=False)
        self.redraw_previews()
        self.status_var.set(f"Loaded {path}")

    def detect_houdini_config_dirs(self, initial_hint: Path | None = None) -> None:
        paths = find_houdini_config_dirs()
        preferred = None

        if initial_hint is not None:
            hinted = initial_hint.expanduser().resolve()
            for path in paths:
                try:
                    if path.resolve() == hinted.parent.resolve():
                        preferred = path
                        break
                except OSError:
                    continue

        self.detected_config_dirs = paths
        if preferred is None and paths:
            preferred = paths[0]

        if preferred is not None:
            self.config_path_var.set(str(preferred))
            if len(paths) > 1:
                self.status_var.set(f"Detected {len(paths)} Houdini config folders. Using {preferred}")
            else:
                self.status_var.set(f"Detected Houdini config folder: {preferred}")
        else:
            self.config_path_var.set("")
            self.status_var.set("No Houdini config folder detected yet.")

    def _resolve_binding_color(self, binding: Binding) -> tuple[float, float, float]:
        if self.document is not None:
            for key in binding.keys:
                parsed = self.document.get_color(key)
                if parsed is not None:
                    return parsed
        return binding.fallback

    def _set_binding_ui(self, primary_key: str, color: tuple[float, float, float]) -> None:
        self.entry_vars[primary_key].set(rgb_to_hex(color))
        self.swatches[primary_key].configure(bg=rgb_to_hex(color))
        self.entry_widgets[primary_key].configure(highlightthickness=0)

    def _set_family_seed_ui(self, color: tuple[float, float, float]) -> None:
        hex_color = rgb_to_hex(color)
        self.family_seed_var.set(hex_color)
        if self.family_seed_swatch is not None:
            self.family_seed_swatch.configure(bg=hex_color)
        if self.family_seed_entry is not None:
            self.family_seed_entry.configure(highlightthickness=0)

    def commit_family_seed(self) -> None:
        text = self.family_seed_var.get().strip()
        if not text:
            return
        if not text.startswith("#"):
            text = "#" + text
        try:
            color = hex_to_rgb(text)
        except ValueError:
            if self.family_seed_entry is not None:
                self.family_seed_entry.configure(highlightbackground="#E14640", highlightcolor="#E14640", highlightthickness=1)
            self.status_var.set(f"Invalid family seed color: {self.family_seed_var.get().strip()}")
            return
        self._set_family_seed_ui(color)
        self.status_var.set(f"Family seed set to {rgb_to_hex(color)}")

    def pick_family_seed_color(self) -> None:
        initial = self.family_seed_var.get().strip() or "#34D399"
        if not initial.startswith("#"):
            initial = "#" + initial
        rgb_tuple, hex_value = colorchooser.askcolor(color=initial, title="Base family color")
        if not hex_value:
            return
        del rgb_tuple
        self._set_family_seed_ui(hex_to_rgb(hex_value))
        self.status_var.set(f"Family seed picked: {hex_value.upper()}")

    def seed_family_from_current(self, update_status: bool = True) -> None:
        color = self.current_colors.get("ChannelColorGreen3", hex_to_rgb("#34D399"))
        self._set_family_seed_ui(color)
        if update_status:
            self.status_var.set(f"Family seed synced from Green family 3: {rgb_to_hex(color)}")

    def generate_channel_family_palette(self) -> None:
        self.commit_family_seed()
        text = self.family_seed_var.get().strip()
        if not text:
            return
        if not text.startswith("#"):
            text = "#" + text
        try:
            base_color = hex_to_rgb(text)
        except ValueError:
            return

        palette = build_channel_family_palette(base_color)
        keys = [
            "ChannelColorGreen1",
            "ChannelColorGreen2",
            "ChannelColorGreen3",
            "ChannelColorGreen4",
            "ChannelColorGreen5",
        ]
        for key, color in zip(keys, palette, strict=False):
            primary_key = KEY_TO_PRIMARY.get(key, key)
            self.current_colors[primary_key] = color
            self._set_binding_ui(primary_key, color)

        self.redraw_previews()
        self.status_var.set(f"Generated channel family palette from {rgb_to_hex(base_color)}")

    def commit_entry(self, primary_key: str) -> None:
        text = self.entry_vars[primary_key].get().strip()
        if not text:
            return
        if not text.startswith("#"):
            text = "#" + text
        try:
            color = hex_to_rgb(text)
        except ValueError:
            self.entry_widgets[primary_key].configure(highlightbackground="#E14640", highlightcolor="#E14640", highlightthickness=1)
            self.status_var.set(f"Invalid color for {primary_key}: {self.entry_vars[primary_key].get().strip()}")
            return
        self.current_colors[primary_key] = color
        self._set_binding_ui(primary_key, color)
        self.redraw_previews()
        self.status_var.set(f"Updated {primary_key} to {rgb_to_hex(color)}")

    def pick_color(self, binding: Binding) -> None:
        initial = rgb_to_hex(self.current_colors.get(binding.primary_key, binding.fallback))
        rgb_tuple, hex_value = colorchooser.askcolor(color=initial, title=binding.label)
        if not hex_value:
            return
        del rgb_tuple
        color = hex_to_rgb(hex_value)
        self.current_colors[binding.primary_key] = color
        self._set_binding_ui(binding.primary_key, color)
        self.redraw_previews()
        self.status_var.set(f"Picked {binding.label}: {hex_value.upper()}")

    def _apply_current_colors_to_document(self) -> bool:
        if self.document is None:
            self.create_new_overlay_document(update_status=False)
            if self.document is None:
                messagebox.showinfo("No file loaded", "Create or load a .hcs file first.")
                return False
        for binding in BINDINGS:
            color = self.current_colors.get(binding.primary_key, binding.fallback)
            for key in binding.keys:
                self.document.set_color(key, color)
        return True

    def save_file(self) -> None:
        if not self._apply_current_colors_to_document():
            return
        if self.document_is_generated:
            self.save_as()
            return
        try:
            assert self.document is not None
            scheme_name = self.document.sync_scheme_name_to_path(self.document.path)
            self.document.save()
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Save failed", f"Could not save file:\n{self.document.path}\n\n{exc}")
            return
        self.status_var.set(f"Saved {self.document.path} with Scheme: {scheme_name}")
        messagebox.showinfo("Saved", f"Saved theme file:\n{self.document.path}\n\nScheme: {scheme_name}")

    def save_as(self) -> None:
        if not self._apply_current_colors_to_document():
            return
        assert self.document is not None
        target = filedialog.asksaveasfilename(
            title="Save Houdini .hcs file",
            defaultextension=".hcs",
            filetypes=[("Houdini Color Scheme", "*.hcs"), ("All files", "*.*")],
            initialfile=self.document.path.name,
        )
        if not target:
            return
        try:
            scheme_name = self.document.sync_scheme_name_to_path(target)
            self.document.save(target)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Save failed", f"Could not save file:\n{target}\n\n{exc}")
            return
        self.document_is_generated = False
        self.path_var.set(str(Path(target)))
        self.status_var.set(f"Saved as {target} with Scheme: {scheme_name}")
        messagebox.showinfo("Saved", f"Saved theme file:\n{target}\n\nScheme: {scheme_name}")

    def deploy_to_detected_config(self) -> None:
        if not self._apply_current_colors_to_document():
            return

        config_text = self.config_path_var.get().strip()
        if not config_text:
            self.detect_houdini_config_dirs()
            config_text = self.config_path_var.get().strip()
            if not config_text:
                messagebox.showwarning(
                    "Config not found",
                    "Could not automatically find a Houdini config folder.\n"
                    "Make sure you have launched Houdini at least once, or save manually.",
                )
                return

        config_dir = Path(config_text)
        theme_name = self.document.path.name if self.document is not None else f"{DEFAULT_NEW_THEME_NAME}.hcs"
        target = config_dir / theme_name

        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            assert self.document is not None
            scheme_name = self.document.sync_scheme_name_to_path(target)
            self.document.write_to(target)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Deploy failed", f"Could not deploy theme to:\n{target}\n\n{exc}")
            return

        self.document.path = target
        self.document_is_generated = False
        self.path_var.set(str(target))
        self.status_var.set(f"Deployed theme to {target}")
        messagebox.showinfo(
            "Theme deployed",
            "Theme file copied to Houdini config:\n"
            f"{target}\n\n"
            f"Scheme: {scheme_name}\n\n"
            "In Houdini, click Reload in Color Settings or restart Houdini.",
        )

    def get_binding_color(self, key: str, fallback: tuple[float, float, float]) -> tuple[float, float, float]:
        primary_key = KEY_TO_PRIMARY.get(key, key)
        return self.current_colors.get(primary_key, fallback)


def guess_default_path() -> Path | None:
    candidates = sorted(path for path in Path.cwd().glob("*.hcs") if path.is_file())
    if len(candidates) == 1:
        return candidates[0]
    return None

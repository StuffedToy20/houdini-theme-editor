"""Preview drawing helpers for the Houdini theme editor."""

from __future__ import annotations

import tkinter as tk

from .core import hex_to_rgb, rgb_to_hex


def create_round_rect(canvas: tk.Canvas, x0: float, y0: float, x1: float, y1: float, radius: float, **kwargs) -> int:
    radius = max(0.0, min(radius, (x1 - x0) / 2.0, (y1 - y0) / 2.0))
    points = [
        x0 + radius, y0,
        x1 - radius, y0,
        x1, y0,
        x1, y0 + radius,
        x1, y1 - radius,
        x1, y1,
        x1 - radius, y1,
        x0 + radius, y1,
        x0, y1,
        x0, y1 - radius,
        x0, y0 + radius,
        x0, y0,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=18, **kwargs)


class ThemePreviewMixin:
    """Canvas preview methods kept separate from UI layout and document logic."""

    def redraw_previews(self) -> None:
        if "menus" in self.preview_canvases:
            self._draw_menu_preview()
        if "parameter" in self.preview_canvases:
            self._draw_parameter_preview()
        if "slider" in self.preview_canvases:
            self._draw_slider_preview()
        if "channel" in self.preview_canvases:
            self._draw_channel_preview()
        if "graph" in self.preview_canvases:
            self._draw_graph_preview()
        if "viewport" in self.preview_canvases:
            self._draw_viewport_preview()

    def _draw_menu_preview(self) -> None:
        canvas = self.preview_canvases["menus"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 180)

        menu_bg = self.get_binding_color("MenuBG", (0.23, 0.23, 0.23))
        menu_text = self.get_binding_color("MenuText", (0.80, 0.80, 0.80))
        menu_hover = self.get_binding_color("MenuHighlight", (0.58, 0.58, 0.58))
        menu_selected_bg = self.get_binding_color("MenuSelectedBG", (0.70, 0.40, 0.00))
        menu_selected_text = self.get_binding_color("MenuTextSelected", (1.0, 1.0, 1.0))
        menu_title_bg = self.get_binding_color("MenuTitleBG", (0.17, 0.17, 0.17))

        canvas.create_rectangle(0, 0, width, height, fill=self.bg, outline="")
        canvas.create_text(20, 18, anchor="nw", text="Menu preview", fill=self.subtle, font=("Segoe UI", 10, "bold"))

        top_y0 = 42
        top_y1 = 76
        canvas.create_rectangle(20, top_y0, width - 20, top_y1, fill=rgb_to_hex(menu_title_bg), outline=self.line)

        items = [("File", False), ("Edit", True), ("Render", False), ("Assets", False), ("Windows", False)]
        x = 34
        for label, selected in items:
            pad = 16 + len(label) * 7
            fill = rgb_to_hex(menu_selected_bg) if selected else rgb_to_hex(menu_title_bg)
            text_fill = rgb_to_hex(menu_selected_text) if selected else rgb_to_hex(menu_text)
            canvas.create_rectangle(x - 8, top_y0 + 2, x + pad, top_y1 - 2, fill=fill, outline="")
            canvas.create_text(x, top_y0 + 9, anchor="nw", text=label, fill=text_fill, font=("Segoe UI", 11))
            x += pad + 14

        menu_x0 = 34
        menu_y0 = top_y1
        menu_x1 = 250
        menu_y1 = 158
        canvas.create_rectangle(menu_x0, menu_y0, menu_x1, menu_y1, fill=rgb_to_hex(menu_bg), outline=self.line)

        rows = [
            ("Undo Change selection", True, False),
            ("Can't redo", False, False),
            ("Undo History...", False, True),
        ]
        row_h = 32
        for index, (label, selected, disabled) in enumerate(rows):
            y0 = menu_y0 + index * row_h
            y1 = y0 + row_h
            fill = menu_selected_bg if selected else menu_bg
            canvas.create_rectangle(menu_x0 + 1, y0 + 1, menu_x1 - 1, y1, fill=rgb_to_hex(fill), outline="")
            if disabled:
                text_fill = "#8E9398"
            else:
                text_fill = rgb_to_hex(menu_selected_text) if selected else rgb_to_hex(menu_text)
            canvas.create_text(menu_x0 + 14, y0 + 8, anchor="nw", text=label, fill=text_fill, font=("Segoe UI", 10))

        hover_x0 = 300
        hover_x1 = width - 24
        hover_y0 = 92
        hover_y1 = 124
        canvas.create_rectangle(hover_x0, hover_y0, hover_x1, hover_y1, fill=rgb_to_hex(menu_bg), outline=self.line)
        canvas.create_rectangle(hover_x0 + 1, hover_y0 + 1, hover_x1 - 1, hover_y1 - 1, fill=rgb_to_hex(menu_hover), outline="")
        canvas.create_text(hover_x0 + 12, hover_y0 + 7, anchor="nw", text="Hovered menu row sample", fill=rgb_to_hex(menu_text), font=("Segoe UI", 10))

    def _draw_parameter_preview(self) -> None:
        canvas = self.preview_canvases["parameter"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 300)

        ui_text = self.get_binding_color("ButtonText", (0.82, 0.84, 0.86))
        textbox_bg = self.get_binding_color("TextboxBG", (0.15, 0.16, 0.17))
        border = (0.27, 0.29, 0.31)
        group_base = self.get_binding_color("GroupHeader0", (0.20, 0.20, 0.20))
        group_hover = self.get_binding_color("GroupHeaderHi0", (0.32, 0.32, 0.32))
        group_open = self.get_binding_color("GroupHeaderOpen0", (0.31, 0.31, 0.31))
        expr = self.get_binding_color("IsKeyColor", hex_to_rgb("#49C8C2"))
        tween = self.get_binding_color("IsNotKeyColor", hex_to_rgb("#3FAFAA"))
        pending = self.get_binding_color("PendingColor", hex_to_rgb("#F3E16C"))
        override = self.get_binding_color("OverrideColor", hex_to_rgb("#EB4967"))
        other_lang = self.get_binding_color("OtherLanguageColor", hex_to_rgb("#EB4967"))
        accent = self.get_binding_color("NonDefAccentColor", hex_to_rgb("#EB4967"))

        canvas.create_rectangle(0, 0, width, height, fill=self.bg, outline="")
        canvas.create_text(20, 18, anchor="nw", text="Parameter editor state demo", fill=self.subtle, font=("Segoe UI", 10, "bold"))

        header_x0 = 20
        header_x1 = width - 24
        base_y = 46
        header_h = 30

        headers = [
            ("Base Group", group_open),
            ("Keep in Bounding Regions", group_base),
            ("Keep by Normals", group_hover),
        ]
        for index, (label, color) in enumerate(headers):
            y0 = base_y + index * 42
            y1 = y0 + header_h
            canvas.create_rectangle(header_x0, y0, header_x1, y1, fill=rgb_to_hex(color), outline="")
            canvas.create_text(header_x0 + 12, y0 + 8, anchor="nw", text=label, fill=rgb_to_hex(ui_text), font=("Segoe UI", 11, "bold"))

        fields = [
            ("Normal", textbox_bg, None, "0.25"),
            ("Expression / keyed", expr, accent, 'ch("height") / 2'),
            ("Animated / not on key", tween, None, 'ch("diameter") * ch("ratio")'),
            ("Pending changes", pending, None, "640"),
            ("Override by CHOP", override, None, "channel override"),
            ("Python / other lang", other_lang, accent, "hou.frame() * 0.5"),
        ]

        x = 20
        y = 176
        field_h = 34
        gap = 10

        for index, (label, bg_color, underline, value) in enumerate(fields):
            top = y + index * (field_h + gap)
            canvas.create_text(x, top + 6, anchor="nw", text=label, fill=rgb_to_hex(ui_text), font=("Segoe UI", 10))
            left = 210
            right = width - 24
            canvas.create_rectangle(left, top, right, top + field_h, fill=rgb_to_hex(bg_color), outline=rgb_to_hex(border))
            canvas.create_text(left + 10, top + 9, anchor="nw", text=value, fill="#F6F7F8", font=("Consolas", 10))
            if underline is not None:
                canvas.create_rectangle(left, top + field_h - 3, right, top + field_h, fill=rgb_to_hex(underline), outline="")

    def _draw_slider_preview(self) -> None:
        canvas = self.preview_canvases["slider"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 180)

        track = self.get_binding_color("SliderAdvancedGroove", hex_to_rgb("#3FAFAA"))
        tick = self.get_binding_color("SliderTick", (0.31, 0.33, 0.35))
        thumb_hi = self.get_binding_color("SliderThumbGradHi", (0.34, 0.37, 0.39))
        thumb_lo = self.get_binding_color("SliderThumbGradLow", (0.23, 0.25, 0.27))
        key = self.get_binding_color("KeyframeButtonCircleKey", hex_to_rgb("#F3E16C"))
        pending = self.get_binding_color("KeyframeButtonCirclePending", hex_to_rgb("#F3E16C"))
        no_key = self.get_binding_color("KeyframeButtonCircleNoKey", hex_to_rgb("#3FAFAA"))

        canvas.create_rectangle(0, 0, width, height, fill=self.bg, outline="")
        canvas.create_text(20, 18, anchor="nw", text="Slider and keyframe preview", fill=self.subtle, font=("Segoe UI", 10, "bold"))

        groove_y = 72
        groove_left = 24
        groove_right = width - 24

        for offset in range(0, 11):
            x = groove_left + (groove_right - groove_left) * offset / 10.0
            canvas.create_line(x, groove_y - 18, x, groove_y - 8, fill=rgb_to_hex(tick))

        canvas.create_line(groove_left, groove_y, groove_right, groove_y, fill="#17191B", width=8)
        canvas.create_line(groove_left, groove_y, groove_right - 120, groove_y, fill=rgb_to_hex(track), width=4)

        thumb_x = groove_right - 120
        canvas.create_rectangle(thumb_x - 6, groove_y - 18, thumb_x + 6, groove_y + 18, fill=rgb_to_hex(thumb_lo), outline=rgb_to_hex(thumb_hi))

        canvas.create_text(24, 110, anchor="nw", text="Keyframe states", fill=self.subtle, font=("Segoe UI", 9, "bold"))
        samples = [("No key", no_key), ("Key", key), ("Pending", pending)]
        sx = 24
        for label, color in samples:
            canvas.create_oval(sx, 136, sx + 18, 154, fill=rgb_to_hex(color), outline="")
            canvas.create_text(sx + 28, 136, anchor="nw", text=label, fill=self.text, font=("Segoe UI", 9))
            sx += 130

    def _draw_channel_preview(self) -> None:
        canvas = self.preview_canvases["channel"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 220)

        bg = self.get_binding_color("ChannelEditorBackground", (0.15, 0.16, 0.17))
        grid = self.get_binding_color("ChannelEditorGridLine", (0.27, 0.29, 0.31))
        dashed = self.get_binding_color("ChannelEditorGridDashedLine", (0.22, 0.24, 0.26))
        selected = self.get_binding_color("ChannelEditorHandleSelected", (0.39, 0.66, 0.65))
        frame_bar = self.get_binding_color("DopeSheetCurrentFrameBG", (0.28, 0.49, 0.53))
        green1 = self.get_binding_color("ChannelColorGreen1", hex_to_rgb("#4ADE80"))
        green4 = self.get_binding_color("ChannelColorGreen4", hex_to_rgb("#2DD4BF"))

        canvas.create_rectangle(0, 0, width, height, fill=rgb_to_hex(bg), outline="")
        canvas.create_text(20, 18, anchor="nw", text="Channel editor demo", fill=self.subtle, font=("Segoe UI", 10, "bold"))

        left = 24
        right = width - 24
        top = 42
        bottom = height - 24

        for step in range(6):
            y = top + (bottom - top) * step / 5.0
            canvas.create_line(left, y, right, y, fill=rgb_to_hex(grid))
        for step in range(1, 10):
            x = left + (right - left) * step / 10.0
            color = dashed if step % 2 else grid
            canvas.create_line(x, top, x, bottom, fill=rgb_to_hex(color), dash=(3, 5))

        frame_x = left + (right - left) * 0.62
        canvas.create_line(frame_x, top, frame_x, bottom, fill=rgb_to_hex(frame_bar), width=2)

        points1 = []
        points2 = []
        for index in range(11):
            x = left + (right - left) * index / 10.0
            y1 = top + 95 - ((index % 3) * 18) - (index * 1.5)
            y2 = top + 48 + ((index % 4) * 14)
            points1.append((x, y1))
            points2.append((x, y2))

        canvas.create_line(*[coord for point in points1 for coord in point], fill=rgb_to_hex(green1), width=2, smooth=True)
        canvas.create_line(*[coord for point in points2 for coord in point], fill=rgb_to_hex(green4), width=2, smooth=True)

        for x, y in (points1[3], points1[6], points2[5]):
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=rgb_to_hex(selected), outline="")

    def _draw_graph_preview(self) -> None:
        canvas = self.preview_canvases["graph"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 380)

        bg = self.get_binding_color("GraphBackground", (0.16, 0.17, 0.18))
        grid_lines = self.get_binding_color("GraphGridLines", (0.28, 0.30, 0.32))
        grid_points = self.get_binding_color("GraphGridPoints", (0.22, 0.24, 0.25))
        wire = self.get_binding_color("GraphWire", (0.56, 0.67, 0.71))
        connector = self.get_binding_color("GraphConnector", (0.39, 0.63, 0.67))
        connector_label = self.get_binding_color("GraphConnectorLabel", (0.72, 0.76, 0.78))
        connector_error = self.get_binding_color("GraphConnectorError", (0.83, 0.43, 0.43))
        node_border = self.get_binding_color("GraphItemBorder", (0.08, 0.09, 0.10))
        node_current_outline = self.get_binding_color("GraphItemCurrent", (1.00, 0.83, 0.00))
        node_selected_outline = self.get_binding_color("GraphItemSelection", (0.93, 0.97, 0.11))
        wire_node_selection = self.get_binding_color("GraphWireNodeSelection", (0.93, 0.97, 0.11))
        wire_selection = self.get_binding_color("GraphWireSelection", (0.93, 0.97, 0.11))
        node_text = self.get_binding_color("GraphNameText", (0.86, 0.88, 0.89))
        node_type_text = self.get_binding_color("GraphNodeTypeText", (0.61, 0.65, 0.68))
        param_text = self.get_binding_color("ButtonText", (0.82, 0.84, 0.86))

        canvas.create_rectangle(0, 0, width, height, fill=rgb_to_hex(bg), outline="")
        canvas.create_text(20, 18, anchor="nw", text="Node graph demo", fill=self.subtle, font=("Segoe UI", 10, "bold"))

        for x in range(0, width, 40):
            canvas.create_line(x, 36, x, height, fill=rgb_to_hex(grid_lines))
        for y in range(36, height, 40):
            canvas.create_line(0, y, width, y, fill=rgb_to_hex(grid_lines))
        for x in range(20, width, 40):
            for y in range(56, height, 40):
                canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill=rgb_to_hex(grid_points), outline="")

        def draw_port(x: float, y: float, radius: float = 7.0, color: tuple[float, float, float] | None = None) -> None:
            fill = rgb_to_hex(color or connector)
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline="")

        def draw_node_body(
            x0: float,
            y0: float,
            x1: float,
            y1: float,
            *,
            current: bool = False,
            selected: bool = False,
            halo: bool = False,
        ) -> None:
            outer_fill = "#CFCFD0"
            inner_fill = "#EFEFEF"
            if halo:
                canvas.create_oval(
                    x0 - 28,
                    y0 - 28,
                    x1 + 28,
                    y1 + 28,
                    fill="#5D7FD0",
                    outline="",
                    stipple="gray50",
                )
                canvas.create_arc(
                    x0 - 22,
                    y0 - 22,
                    x1 + 22,
                    y1 + 22,
                    start=25,
                    extent=130,
                    style="arc",
                    outline="#60C5D8",
                    width=6,
                )
            if current:
                create_round_rect(
                    canvas,
                    x0 - 4,
                    y0 - 4,
                    x1 + 4,
                    y1 + 4,
                    16,
                    fill="",
                    outline=rgb_to_hex(node_current_outline),
                    width=2.5,
                )
            if selected:
                create_round_rect(
                    canvas,
                    x0 - 2,
                    y0 - 2,
                    x1 + 2,
                    y1 + 2,
                    15,
                    fill="",
                    outline=rgb_to_hex(node_selected_outline),
                    width=1.2,
                )
            create_round_rect(canvas, x0, y0, x1, y1, 14, fill=outer_fill, outline=rgb_to_hex(node_border), width=1.5)
            create_round_rect(canvas, x0 + 2, y0 + 2, x1 - 2, y1 - 2, 12, fill=inner_fill, outline="")
            for stripe_x in (x0 + 30, x0 + 58, x0 + 86):
                canvas.create_line(stripe_x, y0 + 4, stripe_x - 8, y1 - 4, fill="#B8B8B8", width=1)

        def draw_boolean_icon(cx: float, cy: float) -> None:
            canvas.create_oval(cx - 22, cy - 22, cx + 22, cy + 22, fill="#E4E4E4", outline="#B6B6B6", width=1.2)
            canvas.create_polygon(
                cx - 8, cy - 10,
                cx + 5, cy - 12,
                cx + 14, cy - 4,
                cx + 1, cy - 2,
                fill="#DADADA", outline="#A8A8A8", width=1,
            )
            canvas.create_polygon(
                cx - 8, cy - 10,
                cx - 8, cy + 3,
                cx + 1, cy + 12,
                cx + 1, cy - 2,
                fill="#EDEDED", outline="#A8A8A8", width=1,
            )
            canvas.create_polygon(
                cx + 1, cy - 2,
                cx + 14, cy - 4,
                cx + 14, cy + 9,
                cx + 1, cy + 12,
                fill="#C8CFD8", outline="#A8A8A8", width=1,
            )

        def draw_simple_icon(cx: float, cy: float, kind: str) -> None:
            if kind == "group":
                canvas.create_oval(cx - 13, cy - 13, cx + 13, cy + 13, fill="#F7F2DA", outline="#F39C12", width=1.8)
            elif kind == "blast":
                canvas.create_polygon(
                    cx - 12, cy + 8, cx - 8, cy - 6, cx - 2, cy + 2,
                    cx + 2, cy - 8, cx + 7, cy + 2, cx + 12, cy - 5,
                    cx + 10, cy + 9,
                    fill="#F39C34", outline="#D36B00", width=1.0,
                )
                canvas.create_rectangle(cx - 13, cy + 6, cx + 13, cy + 10, fill="#F39C34", outline="#D36B00", width=1.0)
            elif kind == "extrude":
                canvas.create_polygon(cx - 8, cy - 10, cx + 4, cy - 12, cx + 14, cy - 4, cx + 2, cy - 2, fill="#F7B733", outline="#C47F16", width=1)
                canvas.create_polygon(cx - 8, cy - 10, cx - 8, cy + 4, cx + 2, cy + 12, cx + 2, cy - 2, fill="#FFD46B", outline="#C47F16", width=1)
                canvas.create_polygon(cx + 2, cy - 2, cx + 14, cy - 4, cx + 14, cy + 10, cx + 2, cy + 12, fill="#E4A92C", outline="#C47F16", width=1)
                canvas.create_line(cx + 10, cy + 8, cx + 18, cy + 14, fill="#E14640", width=2)
            elif kind == "tube":
                create_round_rect(canvas, cx - 10, cy - 13, cx + 10, cy + 13, 8, fill="#B7C2CB", outline="#8192A0", width=1.2)
                canvas.create_oval(cx - 10, cy - 13, cx + 10, cy - 5, fill="#CFD6DC", outline="#8192A0", width=1.0)
            elif kind == "merge":
                canvas.create_arc(cx - 24, cy - 18, cx + 24, cy + 18, start=15, extent=160, style="arc", outline="#60C5D8", width=5)
                canvas.create_oval(cx - 13, cy - 9, cx + 13, cy + 9, fill="#F0F0F0", outline="#9A9A9A", width=1)
                canvas.create_line(cx - 6, cy - 2, cx + 8, cy - 7, fill="#D9534F", width=2)
                canvas.create_line(cx - 2, cy + 5, cx + 12, cy + 1, fill="#D9534F", width=2)
            else:
                draw_boolean_icon(cx, cy)

        def draw_node(
            x0: float,
            y0: float,
            x1: float,
            y1: float,
            *,
            title: str,
            name: str,
            sublabel: str | None = None,
            icon: str = "boolean",
            title_dx: float = 14,
            title_dy: float = -12,
            current: bool = False,
            selected: bool = False,
            halo: bool = False,
        ) -> dict[str, tuple[float, float]]:
            draw_node_body(x0, y0, x1, y1, current=current, selected=selected, halo=halo)
            draw_simple_icon((x0 + x1) / 2, (y0 + y1) / 2, icon)

            top_left = (x0 + 28, y0 - 8)
            top_right = (x0 + 68, y0 - 8)
            bottom = ((x0 + x1) / 2, y1 + 8)
            draw_port(*top_left)
            draw_port(*top_right)
            draw_port(*bottom)

            text_x = x1 + title_dx
            text_y = y0 + title_dy
            if title:
                canvas.create_text(text_x, text_y, anchor="nw", text=title, fill=rgb_to_hex(node_type_text), font=("Segoe UI", 10))
            canvas.create_text(text_x, text_y + 26, anchor="nw", text=name, fill=rgb_to_hex(node_text), font=("Segoe UI", 12))
            if sublabel:
                canvas.create_text(text_x, y1 + 8, anchor="nw", text=sublabel, fill=rgb_to_hex(connector_label), font=("Segoe UI", 9))

            return {"top_left": top_left, "top_right": top_right, "bottom": bottom}

        group = draw_node(24, 62, 132, 102, title="Group Create", name="top_face1", sublabel="Top", icon="group")
        blast = draw_node(24, 142, 132, 182, title="", name="blast2", sublabel="Top", icon="blast", title_dx=14, title_dy=0)
        extrude = draw_node(412, 102, 520, 142, title="PolyExtrude", name="extrude_base", icon="extrude")
        tube = draw_node(640, 102, 748, 142, title="", name="tube1", icon="tube", title_dx=12, title_dy=8)
        boolean1 = draw_node(532, 226, 640, 266, title="", name="boolean1", icon="boolean", title_dx=12, title_dy=8)
        boolean2 = draw_node(240, 248, 348, 288, title="", name="boolean2", icon="boolean", title_dx=12, title_dy=8, current=True, selected=True)
        merge1 = draw_node(446, 308, 554, 348, title="", name="merge1", icon="merge", title_dx=12, title_dy=12, selected=True, halo=True)

        canvas.create_line(group["bottom"][0], group["bottom"][1], 78, 126, blast["top_left"][0], blast["top_left"][1], fill=rgb_to_hex(wire), width=1.5, smooth=True)
        canvas.create_line(extrude["bottom"][0], extrude["bottom"][1], 544, 188, 562, 206, boolean1["top_left"][0], boolean1["top_left"][1], fill=rgb_to_hex(wire), width=1.6, smooth=True)
        canvas.create_line(tube["bottom"][0], tube["bottom"][1], 704, 176, 676, 204, boolean1["top_right"][0], boolean1["top_right"][1], fill=rgb_to_hex(wire), width=1.6, smooth=True)
        canvas.create_line(boolean1["bottom"][0], boolean1["bottom"][1], 640, 304, 596, 328, merge1["top_left"][0], merge1["top_left"][1], fill=rgb_to_hex(wire), width=1.6, smooth=True)

        canvas.create_line(blast["bottom"][0], blast["bottom"][1], 146, 212, 214, 234, boolean2["top_left"][0], boolean2["top_left"][1], fill=rgb_to_hex(wire_node_selection), width=1.8, smooth=True)
        canvas.create_line(boolean2["bottom"][0], boolean2["bottom"][1], 356, 314, 418, 330, merge1["top_right"][0], merge1["top_right"][1], fill=rgb_to_hex(wire_node_selection), width=1.8, smooth=True)

        start_x, start_y = boolean1["bottom"]
        end_x, end_y = boolean2["top_right"]
        canvas.create_line(start_x, start_y, 618, 272, 452, 238, 362, 240, end_x, end_y, fill=rgb_to_hex(wire_selection), width=2.2, smooth=True)
        canvas.create_polygon(574, 236, 600, 226, 596, 248, fill=rgb_to_hex(wire_selection), outline="")

        canvas.create_text(500, 338, anchor="nw", text="Selected / adjacent", fill=rgb_to_hex(wire_selection), font=("Segoe UI", 9))
        canvas.create_line(616, 345, 720, 345, fill=rgb_to_hex(wire_selection), width=2.2)
        canvas.create_text(500, 358, anchor="nw", text="Normal wire", fill=rgb_to_hex(wire), font=("Segoe UI", 9))
        canvas.create_line(584, 365, 662, 365, fill=rgb_to_hex(wire), width=1.8)

        canvas.create_text(
            22,
            height - 24,
            anchor="sw",
            text="Graph preview shows normal wire color, selected / adjacent wire color, and selected node outline together.",
            fill=rgb_to_hex(param_text),
            font=("Segoe UI", 9),
        )

    def _draw_viewport_preview(self) -> None:
        canvas = self.preview_canvases["viewport"]
        canvas.delete("all")
        width = max(canvas.winfo_width(), 780)
        height = max(canvas.winfo_height(), 520)

        bg_top = self.get_binding_color("BackgroundTopColor", (0.36, 0.44, 0.49))
        bg_bottom = self.get_binding_color("BackgroundBottomColor", (0.80, 0.83, 0.84))
        grid = self.get_binding_color("GridColor", (0.40, 0.45, 0.50))
        grid_x = self.get_binding_color("GridXRulerColor", (0.70, 0.50, 0.50))
        grid_y = self.get_binding_color("GridYRulerColor", (0.50, 0.70, 0.50))
        grid_z = self.get_binding_color("GridZRulerColor", (0.50, 0.50, 0.70))
        text = self.get_binding_color("TextColor", (0.60, 0.60, 0.60))
        selected = self.get_binding_color("SelectedLabelColor", (0.80, 0.80, 0.00))

        # Gradient background.
        for row in range(height):
            t = row / max(height - 1, 1)
            mix = tuple(bg_top[i] * (1.0 - t) + bg_bottom[i] * t for i in range(3))
            canvas.create_line(0, row, width, row, fill=rgb_to_hex(mix))

        canvas.create_text(18, 18, anchor="nw", text="View", fill="#F4F4F4", font=("Segoe UI", 11, "bold"))

        horizon = height * 0.40
        vanishing_x = width * 0.52

        # Perspective grid.
        for step in range(-18, 19):
            t = (step + 18) / 36.0
            base_x = t * width
            canvas.create_line(base_x, height, vanishing_x, horizon, fill=rgb_to_hex(grid), width=1)

        for band in range(1, 18):
            t = band / 18.0
            y = horizon + ((height - horizon) * (t ** 1.35))
            x_pad = (width * 0.52) * (1.0 - t ** 1.15)
            canvas.create_line(x_pad, y, width - x_pad, y, fill=rgb_to_hex(grid), width=1)

        # Axis / ruler hints.
        labels = [
            ((width * 0.52), height * 0.50, "0", grid_x),
            ((width * 0.55), height * 0.52, "0", grid_z),
            ((width * 0.66), height * 0.68, "1", grid_x),
            ((width * 0.24), height * 0.72, "1", grid_z),
            ((width * 0.82), height * 0.90, "2", grid_x),
            ((width * 0.05), height * 0.88, "2", grid_z),
        ]
        for x, y, value, color in labels:
            canvas.create_text(x, y, text=value, fill=rgb_to_hex(color), font=("Segoe UI", 12, "bold"), angle=27)

        canvas.create_text(width - 155, 20, text="Persp", fill="#F4F4F4", font=("Segoe UI", 10))
        canvas.create_text(width - 82, 20, text="No cam", fill="#F4F4F4", font=("Segoe UI", 10))
        canvas.create_text(width - 22, height - 18, text="Education Edition", fill=rgb_to_hex(selected), font=("Segoe UI", 9), anchor="se")
        canvas.create_text(
            18,
            height - 18,
            text="Scene View preview uses 3DSceneColors-style keys, separate from .hcs UI themes.",
            fill=rgb_to_hex(text),
            font=("Segoe UI", 9),
            anchor="sw",
        )

"""Named Houdini theme bindings exposed in the editor UI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Binding:
    target: str
    section: str
    label: str
    keys: tuple[str, ...]
    fallback: tuple[float, float, float]
    note: str = ""

    @property
    def primary_key(self) -> str:
        return self.keys[0]


BINDINGS: tuple[Binding, ...] = (
    Binding(
        "hcs",
        "Parameter States",
        "Expression / keyed",
        ("IsKeyColor", "ParmFieldExpressionBG", "ParmFieldExpressionColor", "ParmFieldExprBG", "ParmExpressionBG"),
        (0.153, 0.545, 0.545),
        "Green parameter box when an expression is active on the current key.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Animated / not on key",
        ("IsSoftKeyColor", "IsNotKeyColor"),
        (0.247, 0.686, 0.667),
        "Tween / expression state when you are between keys.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Pending changes",
        ("PendingColor", "ParmFieldKeyedBG", "ParmFieldKeyframeBG", "ParmFieldKeyframedBG", "ParmFieldAnimatedBG", "ParmKeyedBG"),
        (0.216, 0.467, 0.392),
        "Changed animated parameter that has not been committed as a key.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Override by CHOP",
        ("OverrideColor", "ParmFieldOverrideBG", "ParmFieldOverrideColor", "ParmOverrideBG"),
        (0.29, 0.435, 0.643),
        "Override / CHOP-driven state. Orange in many default Houdini themes.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Other language",
        ("OtherLanguageColor",),
        (0.29, 0.435, 0.643),
        "Usually Python expression when the node default is HScript.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Reference / non-default accent",
        ("NonDefAccentColor", "ChanRefAccentColor", "ParmFieldReferenceBG", "ParmFieldReferenceColor", "ParmFieldReferencedBG", "ParmReferenceBG"),
        (0.922, 0.286, 0.404),
        "Accent and reference colors used around non-default and ch() style parameters.",
    ),
    Binding(
        "hcs",
        "Parameter States",
        "Locked parameter",
        ("LockedColor", "ChannelLockedColor"),
        (0.467, 0.596, 0.659),
        "Optional helper state for lock()/locked parameters.",
    ),
    Binding(
        "hcs",
        "Slider",
        "Slider accent",
        ("SliderAdvancedGroove", "SliderAdvancedBevel"),
        (0.247, 0.686, 0.667),
        "Main line color inside parameter sliders.",
    ),
    Binding("hcs", "Slider", "Slider thumb hi", ("SliderThumbGradHi",), (0.34, 0.37, 0.39), "Top part of the thumb."),
    Binding("hcs", "Slider", "Slider thumb low", ("SliderThumbGradLow",), (0.23, 0.25, 0.27), "Bottom part of the thumb."),
    Binding("hcs", "Slider", "Slider tick", ("SliderTick",), (0.31, 0.33, 0.35), "Tick marks and subtle scale lines."),
    Binding(
        "hcs",
        "Keyframe Buttons",
        "Keyframe dot",
        ("KeyframeButtonCircleKey",),
        (0.98, 0.573, 0.69),
        "The main keyframe dot / marker color.",
    ),
    Binding(
        "hcs",
        "Keyframe Buttons",
        "Pending key dot",
        ("KeyframeButtonCirclePending",),
        (0.502, 0.502, 0.502),
        "Pending keyframe dot color.",
    ),
    Binding(
        "hcs",
        "Keyframe Buttons",
        "Animated no-key dot",
        ("KeyframeButtonCircleNoKey",),
        (0.247, 0.686, 0.667),
        "Animated but not currently on a key.",
    ),
    Binding(
        "hcs",
        "Keyframe Buttons",
        "Some-key dot",
        ("KeyframeButtonCircleSomeKey",),
        (0.55, 0.51, 0.20),
        "Subtle mixed / secondary keyframe state.",
    ),
    Binding("hcs", "Syntax / Text", "Function syntax", ("ParmSyntaxFuncColor",), (0.286, 0.784, 0.761), "Function name color in expressions."),
    Binding("hcs", "Syntax / Text", "Reference syntax", ("ParmSyntaxRefColor",), (0.922, 0.286, 0.404), "Reference color in expressions."),
    Binding("hcs", "Syntax / Text", "Textbox background", ("TextboxBG",), (0.027, 0.035, 0.039), "Default parameter text box background."),
    Binding("hcs", "Syntax / Text", "UI text", ("ButtonText",), (0.949, 0.996, 1.0), "General text color used in previews."),
    Binding("hcs", "Parameter Groups", "Group header base", ("GroupHeader0", "GroupHeaderTop0"), (0.341, 0.478, 0.533), "Default parameter group header background."),
    Binding("hcs", "Parameter Groups", "Group header hover", ("GroupHeaderHi0", "GroupHeaderHiTop0"), (0.255, 0.388, 0.404), "Highlighted / hovered parameter group header background."),
    Binding("hcs", "Parameter Groups", "Group header open", ("GroupHeaderOpen0", "GroupHeaderOpenTop0"), (0.333, 0.451, 0.459), "Expanded parameter group header background."),
    Binding("hcs", "Parameter Groups", "Group header disabled", ("GroupHeaderDisabled0", "GroupHeaderDisabledTop0"), (0.20, 0.20, 0.20), "Disabled group header background."),
    Binding("hcs", "Parameter Groups", "Pane header hi", ("PaneHeaderGradHi",), (0.204, 0.22, 0.227), "Top part of pane / tab header gradient."),
    Binding("hcs", "Parameter Groups", "Pane header low", ("PaneHeaderGradLow",), (0.15, 0.17, 0.18), "Bottom part of pane / tab header gradient."),
    Binding("hcs", "Parameter Groups", "Tab low / inactive", ("ButtonNonActiveGradLow",), (0.14, 0.15, 0.16), "Inactive tab / subdued pane chrome background."),
    Binding("hcs", "Menus", "Menu background", ("MenuBG",), (0.23, 0.23, 0.23), "Popup menu background."),
    Binding("hcs", "Menus", "Menu text", ("MenuText",), (0.80, 0.80, 0.80), "Default menu text color."),
    Binding("hcs", "Menus", "Menu hover", ("MenuHighlight",), (0.58, 0.58, 0.58), "Hovered menu row background."),
    Binding("hcs", "Menus", "Menu selected background", ("MenuSelectedBG",), (0.992, 0.573, 0.0), "Selected / active menu background for top menus and popup rows."),
    Binding("hcs", "Menus", "Menu selected text", ("MenuTextSelected",), (1.00, 1.00, 1.00), "Text color on selected menu items."),
    Binding("hcs", "Menus", "Menu title background", ("MenuTitleBG",), (0.17, 0.17, 0.17), "Top title/menu strip background."),
    Binding("hcs", "Channel Editor", "Background", ("ChannelEditorBackground",), (0.0, 0.0, 0.0), "Channel editor / animation editor background."),
    Binding("hcs", "Channel Editor", "Grid", ("ChannelEditorGridLine",), (0.27, 0.29, 0.31), "Main channel editor grid line."),
    Binding("hcs", "Channel Editor", "Dashed grid", ("ChannelEditorGridDashedLine",), (0.22, 0.24, 0.26), "Secondary dashed grid line."),
    Binding("hcs", "Channel Editor", "Selected handle", ("ChannelEditorHandleSelected",), (0.39, 0.66, 0.65), "Current selected key / handle color in the graph editor."),
    Binding("hcs", "Channel Editor", "Current frame bar", ("DopeSheetCurrentFrameBG",), (0.471, 0.694, 0.773), "Current frame highlight in dope sheet style areas."),
    Binding("hcs", "Node Graph", "Background", ("GraphBackground",), (0.18, 0.184, 0.196), "Node graph background."),
    Binding("hcs", "Node Graph", "Grid lines", ("GraphGridLines",), (0.28, 0.30, 0.32), "Primary graph grid."),
    Binding("hcs", "Node Graph", "Grid points", ("GraphGridPoints",), (0.22, 0.24, 0.25), "Secondary graph grid points."),
    Binding("hcs", "Node Graph", "Wire", ("GraphWire",), (0.51, 0.627, 0.675), "Node wire color in the preview."),
    Binding("hcs", "Node Graph", "Connector dot", ("GraphConnector",), (0.525, 0.678, 0.835), "Port / connector dot color on nodes."),
    Binding("hcs", "Node Graph", "Connector label", ("GraphConnectorLabel",), (0.863, 0.847, 0.82), "Small label color near connectors."),
    Binding("hcs", "Node Graph", "Connector error", ("GraphConnectorError",), (0.894, 0.373, 0.373), "Error connector / invalid port color."),
    Binding("hcs", "Node Graph", "Node border", ("GraphItemBorder",), (0.212, 0.427, 0.604), "Node outline color."),
    Binding("hcs", "Node Graph", "Node current outline", ("GraphItemCurrent",), (0.996, 0.38, 0.549), "Bright outline for the active/current node."),
    Binding("hcs", "Node Graph", "Node selected outline", ("GraphItemSelection",), (0.988, 0.729, 0.055), "Selected node outline color."),
    Binding("hcs", "Node Graph", "Node selection contrast", ("GraphItemSelectionContrast",), (0.0, 0.0, 0.0), "Contrast color used against selected node outlines."),
    Binding("hcs", "Node Graph", "Connected wire highlight", ("GraphWireNodeSelection",), (0.996, 0.463, 0.773), "Highlight color for wires adjacent to the selected node."),
    Binding("hcs", "Node Graph", "Wire selected", ("GraphWireSelection",), (0.906, 0.004, 0.227), "Explicitly selected wire highlight color."),
    Binding("hcs", "Node Graph", "Node text", ("GraphNameText",), (0.86, 0.88, 0.89), "Node title text."),
    Binding("hcs", "Node Graph", "Node type text", ("GraphNodeTypeText",), (0.61, 0.65, 0.68), "Secondary node type label text."),
    Binding("hcs", "Channel Families", "Green family 1", ("ChannelColorGreen1",), (0.29, 0.871, 0.502), "Channel naming family used by y / g suffixes."),
    Binding("hcs", "Channel Families", "Green family 2", ("ChannelColorGreen2",), (0.639, 0.902, 0.208), "Alternative green family tone."),
    Binding("hcs", "Channel Families", "Green family 3", ("ChannelColorGreen3",), (0.204, 0.827, 0.6), "Alternative green family tone."),
    Binding("hcs", "Channel Families", "Green family 4", ("ChannelColorGreen4",), (0.176, 0.831, 0.749), "Alternative green family tone."),
    Binding("hcs", "Channel Families", "Green family 5", ("ChannelColorGreen5",), (0.086, 0.639, 0.29), "Alternative green family tone."),
    Binding("scene", "Viewport / Grid", "Background top", ("BackgroundTopColor",), (0.36, 0.44, 0.49), "Top of the Scene View gradient background."),
    Binding("scene", "Viewport / Grid", "Background bottom", ("BackgroundBottomColor",), (0.80, 0.83, 0.84), "Bottom of the Scene View gradient background."),
    Binding("scene", "Viewport / Grid", "Perspective grid", ("GridColor",), (0.40, 0.45, 0.50), "Main perspective reference-plane grid color."),
    Binding("scene", "Viewport / Grid", "X ruler", ("GridXRulerColor",), (0.70, 0.50, 0.50), "Reference grid X-axis ruler color."),
    Binding("scene", "Viewport / Grid", "Y ruler", ("GridYRulerColor",), (0.50, 0.70, 0.50), "Reference grid Y-axis ruler color."),
    Binding("scene", "Viewport / Grid", "Z ruler", ("GridZRulerColor",), (0.50, 0.50, 0.70), "Reference grid Z-axis ruler color."),
    Binding("scene", "Viewport / Grid", "Ortho grid", ("OrthoGridColor",), (0.40, 0.45, 0.50), "Grid color in orthographic viewports."),
    Binding("scene", "Viewport / Grid", "Ortho origin", ("OrthoGridOriginColor",), (0.30, 0.30, 0.30), "Origin line color in orthographic viewports."),
    Binding("scene", "Viewport / Grid", "UV grid", ("UVGridColor",), (0.30, 0.30, 0.30), "Grid color in UV viewports."),
    Binding("scene", "Viewport / Grid", "UV origin", ("UVGridOriginColor",), (0.35, 0.35, 0.35), "Origin line color in UV viewports."),
    Binding("scene", "Viewport / Grid", "Viewport text", ("TextColor",), (0.60, 0.60, 0.60), "Scene View label and number text."),
    Binding("scene", "Viewport / Grid", "Selected label", ("SelectedLabelColor",), (0.80, 0.80, 0.00), "Label accent in the selected viewport."),
)

SECTION_ORDER: list[str] = []
for _binding in BINDINGS:
    section_id = f"{_binding.target}:{_binding.section}"
    if section_id not in SECTION_ORDER:
        SECTION_ORDER.append(section_id)


KEY_TO_PRIMARY: dict[str, str] = {}
for _binding in BINDINGS:
    for _key in _binding.keys:
        KEY_TO_PRIMARY.setdefault(_key, _binding.primary_key)


def section_order_for_target(target: str) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for binding in BINDINGS:
        if binding.target != target or binding.section in seen:
            continue
        ordered.append(binding.section)
        seen.add(binding.section)
    return ordered

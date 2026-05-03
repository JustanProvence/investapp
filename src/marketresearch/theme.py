import flet as ft

# ── Palettes ──────────────────────────────────────────────────
_LIGHT = {
    "PRIMARY":                  "#000000",
    "ON_PRIMARY":               "#ffffff",
    "PRIMARY_CONTAINER":        "#131b2e",
    "ON_PRIMARY_CONTAINER":     "#7c839b",
    "INVERSE_PRIMARY":          "#bec6e0",
    "SECONDARY":                "#505f76",
    "ON_SECONDARY":             "#ffffff",
    "SECONDARY_CONTAINER":      "#d0e1fb",
    "ON_SECONDARY_CONTAINER":   "#54647a",
    "ERROR":                    "#ba1a1a",
    "ON_ERROR":                 "#ffffff",
    "ERROR_CONTAINER":          "#ffdad6",
    "SURFACE":                  "#f7f9fb",
    "SURFACE_CONTAINER_LOWEST": "#ffffff",
    "SURFACE_CONTAINER_LOW":    "#f2f4f6",
    "SURFACE_CONTAINER":        "#eceef0",
    "SURFACE_CONTAINER_HIGH":   "#e6e8ea",
    "ON_SURFACE":               "#191c1e",
    "ON_SURFACE_VARIANT":       "#45464d",
    "OUTLINE":                  "#76777d",
    "OUTLINE_VARIANT":          "#c6c6cd",
    "BACKGROUND":               "#f7f9fb",
    "GREEN":                    "#009668",
    "GREEN_BG":                 "#e0f5ee",
    "AMBER":                    "#c07800",
    "AMBER_BG":                 "#fef0d3",
    "CRIMSON":                  "#ba1a1a",
    "CRIMSON_BG":               "#ffdad6",
}

_DARK = {
    "PRIMARY":                  "#7aa7e0",
    "ON_PRIMARY":               "#e8ecff",
    "PRIMARY_CONTAINER":        "#1a2d4a",
    "ON_PRIMARY_CONTAINER":     "#7a9cc4",
    "INVERSE_PRIMARY":          "#1a4a8a",
    "SECONDARY":                "#8eb0d4",
    "ON_SECONDARY":             "#001d35",
    "SECONDARY_CONTAINER":      "#1a3050",
    "ON_SECONDARY_CONTAINER":   "#8eb0d4",
    "ERROR":                    "#ffb4ab",
    "ON_ERROR":                 "#690005",
    "ERROR_CONTAINER":          "#93000a",
    "SURFACE":                  "#0f1117",
    "SURFACE_CONTAINER_LOWEST": "#191c27",
    "SURFACE_CONTAINER_LOW":    "#13161f",
    "SURFACE_CONTAINER":        "#1a1d27",
    "SURFACE_CONTAINER_HIGH":   "#22263a",
    "ON_SURFACE":               "#e1e3ef",
    "ON_SURFACE_VARIANT":       "#888fa4",
    "OUTLINE":                  "#42475a",
    "OUTLINE_VARIANT":          "#2a2e3e",
    "BACKGROUND":               "#0f1117",
    "GREEN":                    "#00d496",
    "GREEN_BG":                 "#003828",
    "AMBER":                    "#ffb84d",
    "AMBER_BG":                 "#2e1a00",
    "CRIMSON":                  "#ff6b6b",
    "CRIMSON_BG":               "#3d0000",
}

# ── Active constants (default: light) ─────────────────────────
PRIMARY                  = _LIGHT["PRIMARY"]
ON_PRIMARY               = _LIGHT["ON_PRIMARY"]
PRIMARY_CONTAINER        = _LIGHT["PRIMARY_CONTAINER"]
ON_PRIMARY_CONTAINER     = _LIGHT["ON_PRIMARY_CONTAINER"]
INVERSE_PRIMARY          = _LIGHT["INVERSE_PRIMARY"]
SECONDARY                = _LIGHT["SECONDARY"]
ON_SECONDARY             = _LIGHT["ON_SECONDARY"]
SECONDARY_CONTAINER      = _LIGHT["SECONDARY_CONTAINER"]
ON_SECONDARY_CONTAINER   = _LIGHT["ON_SECONDARY_CONTAINER"]
ERROR                    = _LIGHT["ERROR"]
ON_ERROR                 = _LIGHT["ON_ERROR"]
ERROR_CONTAINER          = _LIGHT["ERROR_CONTAINER"]
SURFACE                  = _LIGHT["SURFACE"]
SURFACE_CONTAINER_LOWEST = _LIGHT["SURFACE_CONTAINER_LOWEST"]
SURFACE_CONTAINER_LOW    = _LIGHT["SURFACE_CONTAINER_LOW"]
SURFACE_CONTAINER        = _LIGHT["SURFACE_CONTAINER"]
SURFACE_CONTAINER_HIGH   = _LIGHT["SURFACE_CONTAINER_HIGH"]
ON_SURFACE               = _LIGHT["ON_SURFACE"]
ON_SURFACE_VARIANT       = _LIGHT["ON_SURFACE_VARIANT"]
OUTLINE                  = _LIGHT["OUTLINE"]
OUTLINE_VARIANT          = _LIGHT["OUTLINE_VARIANT"]
BACKGROUND               = _LIGHT["BACKGROUND"]
GREEN                    = _LIGHT["GREEN"]
GREEN_BG                 = _LIGHT["GREEN_BG"]
AMBER                    = _LIGHT["AMBER"]
AMBER_BG                 = _LIGHT["AMBER_BG"]
CRIMSON                  = _LIGHT["CRIMSON"]
CRIMSON_BG               = _LIGHT["CRIMSON_BG"]

# ── Spacing ───────────────────────────────────────────────────
XS = 4
SM = 8
MD = 16
LG = 24
XL = 32
CONTAINER_MARGIN = 20
STACK_GAP = 12

# ── Border radius ─────────────────────────────────────────────
RADIUS_SM      = 4
RADIUS_DEFAULT = 8
RADIUS_MD      = 12
RADIUS_LG      = 16
RADIUS_XL      = 24
RADIUS_FULL    = 999

# ── Typography ────────────────────────────────────────────────
FONT_FAMILY  = "Manrope"
MANROPE_URL  = (
    "https://fonts.gstatic.com/s/manrope/v15/"
    "xn7_YHE41ni1AdIRqAuZuw1Bx9mbZk79FO_F87jxeN7B.woff2"
)


def set_mode(mode: str) -> None:
    """Update all module-level color constants to the chosen palette.
    Called at the top of every route_change so every rebuilt view
    picks up the correct colors for the session's theme preference.
    """
    global PRIMARY, ON_PRIMARY, PRIMARY_CONTAINER, ON_PRIMARY_CONTAINER
    global INVERSE_PRIMARY, SECONDARY, ON_SECONDARY, SECONDARY_CONTAINER
    global ON_SECONDARY_CONTAINER, ERROR, ON_ERROR, ERROR_CONTAINER
    global SURFACE, SURFACE_CONTAINER_LOWEST, SURFACE_CONTAINER_LOW
    global SURFACE_CONTAINER, SURFACE_CONTAINER_HIGH
    global ON_SURFACE, ON_SURFACE_VARIANT, OUTLINE, OUTLINE_VARIANT
    global BACKGROUND, GREEN, GREEN_BG, AMBER, AMBER_BG, CRIMSON, CRIMSON_BG

    p = _DARK if mode == "dark" else _LIGHT
    PRIMARY                  = p["PRIMARY"]
    ON_PRIMARY               = p["ON_PRIMARY"]
    PRIMARY_CONTAINER        = p["PRIMARY_CONTAINER"]
    ON_PRIMARY_CONTAINER     = p["ON_PRIMARY_CONTAINER"]
    INVERSE_PRIMARY          = p["INVERSE_PRIMARY"]
    SECONDARY                = p["SECONDARY"]
    ON_SECONDARY             = p["ON_SECONDARY"]
    SECONDARY_CONTAINER      = p["SECONDARY_CONTAINER"]
    ON_SECONDARY_CONTAINER   = p["ON_SECONDARY_CONTAINER"]
    ERROR                    = p["ERROR"]
    ON_ERROR                 = p["ON_ERROR"]
    ERROR_CONTAINER          = p["ERROR_CONTAINER"]
    SURFACE                  = p["SURFACE"]
    SURFACE_CONTAINER_LOWEST = p["SURFACE_CONTAINER_LOWEST"]
    SURFACE_CONTAINER_LOW    = p["SURFACE_CONTAINER_LOW"]
    SURFACE_CONTAINER        = p["SURFACE_CONTAINER"]
    SURFACE_CONTAINER_HIGH   = p["SURFACE_CONTAINER_HIGH"]
    ON_SURFACE               = p["ON_SURFACE"]
    ON_SURFACE_VARIANT       = p["ON_SURFACE_VARIANT"]
    OUTLINE                  = p["OUTLINE"]
    OUTLINE_VARIANT          = p["OUTLINE_VARIANT"]
    BACKGROUND               = p["BACKGROUND"]
    GREEN                    = p["GREEN"]
    GREEN_BG                 = p["GREEN_BG"]
    AMBER                    = p["AMBER"]
    AMBER_BG                 = p["AMBER_BG"]
    CRIMSON                  = p["CRIMSON"]
    CRIMSON_BG               = p["CRIMSON_BG"]


def with_alpha(hex_color: str, opacity: float) -> str:
    """Return #AARRGGBB hex string for the given hex color and 0-1 opacity."""
    a = round(opacity * 255)
    r, g, b = hex_color[1:3], hex_color[3:5], hex_color[5:7]
    return f"#{a:02x}{r}{g}{b}"


def build_theme() -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            on_primary=ON_PRIMARY,
            primary_container=PRIMARY_CONTAINER,
            on_primary_container=ON_PRIMARY_CONTAINER,
            secondary=SECONDARY,
            on_secondary=ON_SECONDARY,
            secondary_container=SECONDARY_CONTAINER,
            on_secondary_container=ON_SECONDARY_CONTAINER,
            error=ERROR,
            on_error=ON_ERROR,
            surface=SURFACE,
            on_surface=ON_SURFACE,
            on_surface_variant=ON_SURFACE_VARIANT,
            outline=OUTLINE,
            outline_variant=OUTLINE_VARIANT,
        ),
        font_family=FONT_FAMILY,
        use_material3=True,
    )

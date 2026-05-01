import flet as ft

# ── Colors ────────────────────────────────────────────────────
PRIMARY = "#000000"
ON_PRIMARY = "#ffffff"
PRIMARY_CONTAINER = "#131b2e"
ON_PRIMARY_CONTAINER = "#7c839b"
INVERSE_PRIMARY = "#bec6e0"

SECONDARY = "#505f76"
ON_SECONDARY = "#ffffff"
SECONDARY_CONTAINER = "#d0e1fb"
ON_SECONDARY_CONTAINER = "#54647a"

ERROR = "#ba1a1a"
ON_ERROR = "#ffffff"
ERROR_CONTAINER = "#ffdad6"

SURFACE = "#f7f9fb"
SURFACE_CONTAINER_LOWEST = "#ffffff"
SURFACE_CONTAINER_LOW = "#f2f4f6"
SURFACE_CONTAINER = "#eceef0"
SURFACE_CONTAINER_HIGH = "#e6e8ea"
ON_SURFACE = "#191c1e"
ON_SURFACE_VARIANT = "#45464d"

OUTLINE = "#76777d"
OUTLINE_VARIANT = "#c6c6cd"
BACKGROUND = "#f7f9fb"

# Semantic
GREEN = "#009668"
GREEN_BG = "#e0f5ee"
AMBER = "#c07800"
AMBER_BG = "#fef0d3"
CRIMSON = "#ba1a1a"
CRIMSON_BG = "#ffdad6"

# ── Spacing ───────────────────────────────────────────────────
XS = 4
SM = 8
MD = 16
LG = 24
XL = 32
CONTAINER_MARGIN = 20
STACK_GAP = 12

# ── Border radius ─────────────────────────────────────────────
RADIUS_SM = 4
RADIUS_DEFAULT = 8
RADIUS_MD = 12
RADIUS_LG = 16
RADIUS_XL = 24
RADIUS_FULL = 999

# ── Typography ────────────────────────────────────────────────
FONT_FAMILY = "Manrope"
MANROPE_URL = (
    "https://fonts.gstatic.com/s/manrope/v15/"
    "xn7_YHE41ni1AdIRqAuZuw1Bx9mbZk79FO_F87jxeN7B.woff2"
)


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

import asyncio
import flet as ft
from my_flet_app import routes, theme as t
from my_flet_app.components.bottom_nav import build_nav_bar

_QUICK_CHIPS = ["AAPL", "TSLA", "BTC", "NVDA"]

_NAV_DEST = [routes.SUMMARY, routes.ANALYSIS, routes.HOLDINGS, routes.SETTINGS]


def _nav_handler(page):
    def handler(e):
        asyncio.create_task(page.push_route(_NAV_DEST[int(e.data)]))
    return handler


# ── Landing page ──────────────────────────────────────────────────────────────

def holdings_view(page: ft.Page) -> ft.View:
    def go_add(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS_ADD))

    def go_update(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS_UPDATE))

    def _action_card(icon, title, subtitle, on_click):
        return ft.Container(
            bgcolor=t.SURFACE_CONTAINER_LOWEST,
            border_radius=t.RADIUS_LG,
            padding=ft.padding.all(t.MD + t.XS),
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=t.with_alpha(t.PRIMARY_CONTAINER, 0.06),
                offset=ft.Offset(0, 4),
            ),
            on_click=on_click,
            ink=True,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=t.MD,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=48,
                                height=48,
                                bgcolor=t.SURFACE_CONTAINER,
                                border_radius=t.RADIUS_MD,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(icon, size=22, color=t.ON_SURFACE),
                            ),
                            ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        title,
                                        size=15,
                                        weight=ft.FontWeight.W_600,
                                        color=t.ON_SURFACE,
                                        font_family=t.FONT_FAMILY,
                                    ),
                                    ft.Text(
                                        subtitle,
                                        size=12,
                                        color=t.ON_SURFACE_VARIANT,
                                        font_family=t.FONT_FAMILY,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=t.OUTLINE),
                ],
            ),
        )

    return ft.View(
        route=routes.HOLDINGS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(2, _nav_handler(page)),
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(
                            left=t.CONTAINER_MARGIN,
                            right=t.CONTAINER_MARGIN,
                            top=t.LG + t.SM,
                            bottom=t.MD,
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Holdings",
                                    size=26,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                ),
                                ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, size=22, color=t.ON_SURFACE),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Text(
                            "Manage your portfolio positions.",
                            size=14,
                            color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                        ),
                    ),
                    ft.Container(height=t.XL),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                _action_card(
                                    ft.Icons.ADD_CIRCLE_OUTLINE,
                                    "Add Ticker",
                                    "Search and add a new asset to your portfolio",
                                    go_add,
                                ),
                                _action_card(
                                    ft.Icons.EDIT_OUTLINED,
                                    "Update Holdings",
                                    "Update shares or cost basis for an existing position",
                                    go_update,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


# ── Add Ticker ────────────────────────────────────────────────────────────────

def add_ticker_view(page: ft.Page) -> ft.View:
    chip_containers: list[ft.Container] = []

    def _build_chip(label: str, selected: bool, on_click) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                label,
                size=13,
                weight=ft.FontWeight.W_600,
                color=t.ON_SURFACE if not selected else t.ON_PRIMARY,
                font_family=t.FONT_FAMILY,
            ),
            border=ft.border.all(1, t.OUTLINE_VARIANT if not selected else t.PRIMARY),
            border_radius=t.RADIUS_FULL,
            bgcolor=t.PRIMARY if selected else t.SURFACE_CONTAINER_LOWEST,
            padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM),
            on_click=on_click,
            ink=True,
        )

    def make_chip_click(label):
        def handler(_):
            for i, chip_label in enumerate(_QUICK_CHIPS):
                is_sel = chip_label == label
                chip_containers[i].border = ft.border.all(1, t.PRIMARY if is_sel else t.OUTLINE_VARIANT)
                chip_containers[i].bgcolor = t.PRIMARY if is_sel else t.SURFACE_CONTAINER_LOWEST
                chip_containers[i].content.color = t.ON_PRIMARY if is_sel else t.ON_SURFACE
            page.update()
        return handler

    for label in _QUICK_CHIPS:
        chip_containers.append(_build_chip(label, False, make_chip_click(label)))

    def go_back(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS))

    return ft.View(
        route=routes.HOLDINGS_ADD,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(2, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    # App bar
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.SM, vertical=t.MD),
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=t.XS,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(
                                            ft.Icons.ARROW_BACK,
                                            icon_color=t.ON_SURFACE,
                                            icon_size=22,
                                            on_click=go_back,
                                        ),
                                        ft.Text(
                                            "Add Ticker",
                                            size=16,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ],
                                ),
                                ft.IconButton(
                                    ft.Icons.HELP_OUTLINE,
                                    icon_color=t.ON_SURFACE_VARIANT,
                                    icon_size=22,
                                    on_click=lambda _: None,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.all(t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                ft.Text(
                                    "FIND ASSET",
                                    size=11,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY,
                                    style=ft.TextStyle(letter_spacing=1.2),
                                ),
                                ft.TextField(
                                    hint_text="Search by symbol or company name",
                                    prefix_icon=ft.Icons.SEARCH,
                                    border_color=t.OUTLINE_VARIANT,
                                    focused_border_color=t.PRIMARY,
                                    border_radius=t.RADIUS_FULL,
                                    border_width=1,
                                    focused_border_width=2,
                                    bgcolor=t.SURFACE_CONTAINER_LOW,
                                    filled=True,
                                    fill_color=t.SURFACE_CONTAINER_LOW,
                                    hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY, size=13),
                                    text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=13, color=t.ON_SURFACE),
                                ),
                                ft.Row(spacing=t.SM, controls=chip_containers),
                                # Asset card
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Stack(
                                        controls=[
                                            ft.Column(
                                                spacing=t.SM,
                                                controls=[
                                                    ft.Text("Verified", size=11, weight=ft.FontWeight.W_700, color=t.GREEN, font_family=t.FONT_FAMILY),
                                                    ft.Text("WealthShield Corp", size=18, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                                    ft.Text("Ticker: WSHD • NYSE", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                    ft.Column(
                                                        spacing=t.XS,
                                                        controls=[
                                                            ft.Row(
                                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                controls=[
                                                                    ft.Text("Market Price / $142.84", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                                    ft.Text("+2.4%", size=13, weight=ft.FontWeight.W_600, color=t.GREEN, font_family=t.FONT_FAMILY),
                                                                ],
                                                            ),
                                                            ft.ProgressBar(value=0.80, bgcolor=t.OUTLINE_VARIANT, color=t.GREEN, height=6),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            ft.Container(
                                                right=0, top=0, width=36, height=36,
                                                bgcolor=t.PRIMARY_CONTAINER,
                                                border_radius=t.RADIUS_MD,
                                                alignment=ft.Alignment(0, 0),
                                                content=ft.Icon(ft.Icons.SHIELD_OUTLINED, size=18, color=t.ON_PRIMARY_CONTAINER),
                                            ),
                                        ],
                                    ),
                                ),
                                # Enter details
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Enter Details", size=16, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                        ft.Text("Specify your position to track performance metrics automatically.", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                # Form
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Column(
                                        spacing=t.MD,
                                        controls=[
                                            ft.Column(
                                                spacing=t.XS,
                                                controls=[
                                                    ft.Text("Number of Shares (Optional)", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                    ft.TextField(
                                                        hint_text="0.00",
                                                        border_color=t.OUTLINE_VARIANT,
                                                        focused_border_color=t.PRIMARY,
                                                        border_radius=t.RADIUS_MD,
                                                        border_width=1,
                                                        focused_border_width=2,
                                                        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
                                                        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
                                                        keyboard_type=ft.KeyboardType.NUMBER,
                                                    ),
                                                ],
                                            ),
                                            ft.Column(
                                                spacing=t.XS,
                                                controls=[
                                                    ft.Text("Average Cost Basis", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                    ft.TextField(
                                                        prefix=ft.Text("$ ", size=14, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                        hint_text="0.00",
                                                        border_color=t.OUTLINE_VARIANT,
                                                        focused_border_color=t.PRIMARY,
                                                        border_radius=t.RADIUS_MD,
                                                        border_width=1,
                                                        focused_border_width=2,
                                                        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
                                                        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
                                                        keyboard_type=ft.KeyboardType.NUMBER,
                                                    ),
                                                ],
                                            ),
                                            ft.ElevatedButton(
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    spacing=t.SM,
                                                    controls=[
                                                        ft.Icon(ft.Icons.SAVE_OUTLINED, color=t.ON_PRIMARY, size=18),
                                                        ft.Text("Save Ticker", color=t.ON_PRIMARY, size=14, weight=ft.FontWeight.W_600, font_family=t.FONT_FAMILY),
                                                    ],
                                                ),
                                                width=float("inf"),
                                                height=52,
                                                bgcolor=t.PRIMARY,
                                                elevation=0,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD)),
                                                on_click=lambda _: None,
                                            ),
                                            ft.Text("Positions are encrypted and private to you.", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY, text_align=ft.TextAlign.CENTER),
                                        ],
                                    ),
                                ),
                                # Info card
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Row(
                                        spacing=t.MD,
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        controls=[
                                            ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=t.ON_SURFACE_VARIANT),
                                            ft.Text(
                                                "WealthShield uses real-time market data to calculate your portfolio's health score and defensive rating.",
                                                size=12,
                                                color=t.ON_SURFACE_VARIANT,
                                                font_family=t.FONT_FAMILY,
                                                expand=True,
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(height=t.SM),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


# ── Update Holding ────────────────────────────────────────────────────────────

def update_holding_view(page: ft.Page) -> ft.View:
    def go_back(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS))

    def _event_card(icon, label, subtitle):
        return ft.Container(
            width=float("inf"),
            bgcolor=t.SURFACE_CONTAINER_LOWEST,
            border_radius=t.RADIUS_LG,
            padding=ft.padding.all(t.MD),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color=t.with_alpha(t.PRIMARY_CONTAINER, 0.05),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                spacing=t.XS,
                controls=[
                    ft.Container(
                        width=32,
                        height=32,
                        border_radius=t.RADIUS_FULL,
                        border=ft.border.all(1.5, t.ON_SURFACE),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon, size=16, color=t.ON_SURFACE),
                    ),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ft.Text(subtitle, size=11, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                ],
            ),
        )

    return ft.View(
        route=routes.HOLDINGS_UPDATE,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(2, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    # App bar
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=t.XS,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color=t.ON_SURFACE, icon_size=22, on_click=go_back),
                                        ft.Text("Update AAPL", size=16, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.Text("WealthShield", size=14, weight=ft.FontWeight.W_600, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                # Stock card
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    shadow=ft.BoxShadow(blur_radius=12, color=t.with_alpha(t.PRIMARY_CONTAINER, 0.06), offset=ft.Offset(0, 4)),
                                    content=ft.Column(
                                        spacing=t.SM,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                vertical_alignment=ft.CrossAxisAlignment.START,
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Row(
                                                            spacing=t.XS,
                                                            controls=[
                                                                ft.Icon(ft.Icons.VERIFIED_OUTLINED, size=13, color=t.GREEN),
                                                                ft.Text("PORTFOLIO CORE", size=11, weight=ft.FontWeight.W_700, color=t.GREEN, font_family=t.FONT_FAMILY),
                                                            ],
                                                        ),
                                                        bgcolor=t.GREEN_BG,
                                                        border_radius=t.RADIUS_FULL,
                                                        padding=ft.padding.symmetric(horizontal=t.SM, vertical=3),
                                                    ),
                                                    ft.Column(
                                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text("CURRENT POSITION", size=10, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                            ft.Row(
                                                                spacing=4,
                                                                vertical_alignment=ft.CrossAxisAlignment.END,
                                                                controls=[
                                                                    ft.Text("142.50", size=22, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                                                    ft.Text("shares", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            ft.Text("AAPL", size=28, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                            ft.Text("Apple Inc.", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                            ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Allocation", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                                    ft.Text("12.4%", size=13, weight=ft.FontWeight.W_600, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                                # Number of Shares
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Number of Shares", size=16, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                        ft.TextField(
                                            hint_text="0.00",
                                            suffix=ft.Text("SHARES", size=12, weight=ft.FontWeight.W_600, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                            border_color=t.OUTLINE_VARIANT,
                                            focused_border_color=t.PRIMARY,
                                            border_radius=t.RADIUS_MD,
                                            border_width=1,
                                            focused_border_width=2,
                                            text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
                                            hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
                                            keyboard_type=ft.KeyboardType.NUMBER,
                                        ),
                                        ft.Text("Enter the total updated balance for this ticker. This will adjust your portfolio distribution metrics.", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                # Average Cost Basis
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Average Cost Basis", size=16, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                        ft.TextField(
                                            prefix=ft.Text("$ ", size=14, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                            hint_text="0.00",
                                            border_color=t.OUTLINE_VARIANT,
                                            focused_border_color=t.PRIMARY,
                                            border_radius=t.RADIUS_MD,
                                            border_width=1,
                                            focused_border_width=2,
                                            text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
                                            hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
                                            keyboard_type=ft.KeyboardType.NUMBER,
                                        ),
                                        ft.Text("Adjust your original purchase price to recalculate unrealized gains.", size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                # Buy / Sell event cards
                                ft.Row(
                                    spacing=t.MD,
                                    controls=[
                                        _event_card(ft.Icons.ADD, "Buy Event", "Log new purchase"),
                                        _event_card(ft.Icons.REMOVE, "Sell Event", "Log position reduction"),
                                    ],
                                ),
                                # Confirm button
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=t.SM,
                                        controls=[
                                            ft.Text("Confirm Update", color=t.ON_PRIMARY, size=15, weight=ft.FontWeight.W_600, font_family=t.FONT_FAMILY),
                                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=t.ON_PRIMARY, size=18),
                                        ],
                                    ),
                                    width=float("inf"),
                                    height=52,
                                    bgcolor=t.PRIMARY,
                                    elevation=0,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD)),
                                    on_click=lambda _: None,
                                ),
                                ft.Container(
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.TextButton(
                                        "Cancel and Return",
                                        style=ft.ButtonStyle(
                                            color=t.ON_SURFACE_VARIANT,
                                            overlay_color=ft.Colors.TRANSPARENT,
                                            text_style=ft.TextStyle(size=13, font_family=t.FONT_FAMILY),
                                        ),
                                        on_click=go_back,
                                    ),
                                ),
                                # Chart placeholder
                                ft.Container(
                                    height=110,
                                    border_radius=t.RADIUS_LG,
                                    bgcolor=t.PRIMARY_CONTAINER,
                                ),
                                ft.Container(height=t.SM),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

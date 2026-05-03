import flet as ft
from marketresearch import theme as t, routes
ASSETS = []
PORTFOLIO = {"total_value": 0.0, "daily_change": 0.0, "daily_change_pct": 0.0}
from marketresearch.components.investment_card import investment_card
from marketresearch.components.asset_list_item import asset_list_item
from marketresearch.components.bottom_nav import build_nav_bar


def dashboard_view(page: ft.Page) -> ft.View:
    pct = PORTFOLIO["daily_change_pct"]
    is_positive = pct >= 0
    sign = "+" if is_positive else ""
    delta_color = t.GREEN if is_positive else t.CRIMSON
    delta_bg = t.with_alpha(t.GREEN if is_positive else t.CRIMSON, 0.18)

    def on_asset_click(asset_id: str):
        def handler(_):
            import asyncio
            asyncio.create_task(page.push_route(routes.asset(asset_id)))
        return handler

    def on_nav_change(e):
        pass  # only Home is implemented

    return ft.View(
        route=routes.DASHBOARD,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(0, on_nav_change),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    # ── App bar ───────────────────────────────────────────
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
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "Good morning,",
                                            size=13,
                                            color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                        ft.Text(
                                            "Market Research",
                                            size=20,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY,
                                            style=ft.TextStyle(letter_spacing=-0.3),
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.NOTIFICATIONS_OUTLINED,
                                        size=21,
                                        color=t.ON_SURFACE,
                                    ),
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_FULL,
                                    width=44,
                                    height=44,
                                    alignment=ft.Alignment(0, 0),
                                    shadow=ft.BoxShadow(
                                        blur_radius=8,
                                        color=t.with_alpha(t.PRIMARY_CONTAINER, 0.06),
                                        offset=ft.Offset(0, 2),
                                    ),
                                    on_click=lambda _: None,
                                    ink=True,
                                ),
                            ],
                        ),
                    ),
                    # ── Portfolio summary card ────────────────────────────
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        padding=ft.padding.all(t.LG),
                        bgcolor=t.PRIMARY_CONTAINER,
                        border_radius=t.RADIUS_LG,
                        content=ft.Column(
                            spacing=t.SM,
                            controls=[
                                ft.Text(
                                    "Total Portfolio Value",
                                    size=12,
                                    color=t.ON_PRIMARY_CONTAINER,
                                    font_family=t.FONT_FAMILY,
                                    style=ft.TextStyle(letter_spacing=0.2),
                                ),
                                ft.Text(
                                    f"${PORTFOLIO['total_value']:,.2f}",
                                    size=34,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_PRIMARY,
                                    font_family=t.FONT_FAMILY,
                                    style=ft.TextStyle(letter_spacing=-0.7),
                                ),
                                ft.Row(
                                    spacing=t.SM,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(
                                                f"{sign}${PORTFOLIO['daily_change']:,.2f}"
                                                f"  ({sign}{pct:.2f}%)",
                                                size=12,
                                                weight=ft.FontWeight.W_600,
                                                color=delta_color,
                                                font_family=t.FONT_FAMILY,
                                            ),
                                            bgcolor=delta_bg,
                                            border_radius=t.RADIUS_FULL,
                                            padding=ft.padding.symmetric(
                                                horizontal=t.SM + 2, vertical=3
                                            ),
                                        ),
                                        ft.Text(
                                            "Today",
                                            size=12,
                                            color=t.ON_PRIMARY_CONTAINER,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL),
                    # ── Horizontal investment cards ───────────────────────
                    ft.Container(
                        padding=ft.padding.only(
                            left=t.CONTAINER_MARGIN, bottom=t.SM
                        ),
                        content=ft.Text(
                            "Your Assets",
                            size=17,
                            weight=ft.FontWeight.W_600,
                            color=t.ON_SURFACE,
                            font_family=t.FONT_FAMILY,
                            style=ft.TextStyle(letter_spacing=-0.2),
                        ),
                    ),
                    ft.Container(
                        height=168,
                        content=ft.ListView(
                            horizontal=True,
                            spacing=t.SM + 2,
                            padding=ft.padding.symmetric(
                                horizontal=t.CONTAINER_MARGIN
                            ),
                            controls=[
                                investment_card(
                                    asset,
                                    on_click=on_asset_click(asset["id"]),
                                )
                                for asset in ASSETS
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL),
                    # ── Asset list ────────────────────────────────────────
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "My Assets",
                                    size=17,
                                    weight=ft.FontWeight.W_600,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                    style=ft.TextStyle(letter_spacing=-0.2),
                                ),
                                ft.TextButton(
                                    "View All",
                                    style=ft.ButtonStyle(
                                        color=t.ON_SURFACE_VARIANT,
                                        overlay_color=ft.Colors.TRANSPARENT,
                                        padding=ft.padding.symmetric(horizontal=0),
                                        text_style=ft.TextStyle(
                                            size=13,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ),
                                    on_click=lambda _: None,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.SM),
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN
                        ),
                        content=ft.Column(
                            spacing=t.STACK_GAP,
                            controls=[
                                asset_list_item(
                                    asset,
                                    on_click=on_asset_click(asset["id"]),
                                )
                                for asset in ASSETS
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL + t.LG),
                ],
            ),
        ],
    )

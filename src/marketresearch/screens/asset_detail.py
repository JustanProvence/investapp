import flet as ft
from marketresearch import theme as t, routes
ASSETS = []
from marketresearch.components.chip import category_chip, semantic_chip


def _stat_card(label: str, value: str) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=ft.padding.all(t.MD),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border_radius=t.RADIUS_MD,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.04),
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(
                    label,
                    size=11,
                    color=t.ON_SURFACE_VARIANT,
                    font_family=t.FONT_FAMILY,
                ),
                ft.Text(
                    value,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=t.ON_SURFACE,
                    font_family=t.FONT_FAMILY,
                ),
            ],
        ),
    )


def asset_detail_view(page: ft.Page, asset_id: str) -> ft.View:
    asset = next((a for a in ASSETS if a["id"] == asset_id), ASSETS[0])
    pct = asset["change_pct"]
    is_positive = pct >= 0
    sign = "+" if is_positive else ""

    def go_back(_):
        import asyncio
        asyncio.create_task(page.push_route(routes.DASHBOARD))

    return ft.View(
        route=routes.asset(asset_id),
        bgcolor=t.BACKGROUND,
        padding=0,
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=t.ON_SURFACE,
                on_click=go_back,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.TRANSPARENT,
                ),
            ),
            title=ft.Text(
                asset["name"],
                size=16,
                weight=ft.FontWeight.W_600,
                color=t.ON_SURFACE,
                font_family=t.FONT_FAMILY,
            ),
            center_title=True,
            bgcolor=t.BACKGROUND,
            elevation=0,

        ),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    # ── Hero ──────────────────────────────────────────────
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN, vertical=t.LG
                        ),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=t.SM,
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        asset["ticker"],
                                        size=13,
                                        weight=ft.FontWeight.W_700,
                                        color=t.INVERSE_PRIMARY,
                                        font_family=t.FONT_FAMILY,
                                    ),
                                    bgcolor=t.PRIMARY_CONTAINER,
                                    border_radius=t.RADIUS_MD,
                                    width=54,
                                    height=54,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(height=t.XS),
                                ft.Text(
                                    f"${asset['price']:,.2f}",
                                    size=38,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                    style=ft.TextStyle(letter_spacing=-0.8),
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=t.SM,
                                    controls=[
                                        category_chip(asset["category"]),
                                        semantic_chip(
                                            f"{sign}{pct:.2f}%", is_positive
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    # ── Sparkline placeholder ─────────────────────────────
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        height=120,
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        border_radius=t.RADIUS_LG,
                        shadow=ft.BoxShadow(
                            blur_radius=12,
                            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.05),
                            offset=ft.Offset(0, 4),
                        ),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=t.SM,
                            controls=[
                                ft.Icon(
                                    ft.Icons.SHOW_CHART,
                                    size=30,
                                    color=t.OUTLINE_VARIANT,
                                ),
                                ft.Text(
                                    "Chart coming soon",
                                    size=12,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.LG),
                    # ── Stats row ─────────────────────────────────────────
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN
                        ),
                        content=ft.Row(
                            spacing=t.SM,
                            controls=[
                                _stat_card(
                                    "24h High",
                                    f"${asset['high_24h']:,.2f}",
                                ),
                                _stat_card(
                                    "24h Low",
                                    f"${asset['low_24h']:,.2f}",
                                ),
                                _stat_card("Volume", asset["volume"]),
                            ],
                        ),
                    ),
                    ft.Container(height=t.MD),
                    # ── Position card ─────────────────────────────────────
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        padding=ft.padding.all(t.MD),
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        border_radius=t.RADIUS_LG,
                        shadow=ft.BoxShadow(
                            blur_radius=12,
                            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.05),
                            offset=ft.Offset(0, 4),
                        ),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                ft.Text(
                                    "Your Position",
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                ),
                                ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(
                                            "Holdings",
                                            size=14,
                                            color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                        ft.Text(
                                            f"{asset['quantity']:,} {asset['ticker']}",
                                            size=14,
                                            weight=ft.FontWeight.W_600,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(
                                            "Market Value",
                                            size=14,
                                            color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                        ft.Text(
                                            f"${asset['value']:,.2f}",
                                            size=14,
                                            weight=ft.FontWeight.W_600,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL),
                    # ── Buy / Sell buttons ────────────────────────────────
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN
                        ),
                        content=ft.Row(
                            spacing=t.MD,
                            controls=[
                                ft.ElevatedButton(
                                    "Buy",
                                    expand=True,
                                    height=52,
                                    bgcolor=t.PRIMARY,
                                    color=t.ON_PRIMARY,
                                    elevation=0,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=t.RADIUS_MD
                                        ),
                                        text_style=ft.TextStyle(
                                            size=15,
                                            weight=ft.FontWeight.W_600,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ),
                                    on_click=lambda _: None,
                                ),
                                ft.OutlinedButton(
                                    "Sell",
                                    expand=True,
                                    height=52,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=t.RADIUS_MD
                                        ),
                                        side=ft.BorderSide(1, t.OUTLINE_VARIANT),
                                        color=t.ON_SURFACE,
                                        text_style=ft.TextStyle(
                                            size=15,
                                            weight=ft.FontWeight.W_600,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ),
                                    on_click=lambda _: None,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL),
                ],
            ),
        ],
    )

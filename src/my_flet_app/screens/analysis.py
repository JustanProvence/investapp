import asyncio
import flet as ft
from my_flet_app import routes, theme as t
from my_flet_app.components.bottom_nav import build_nav_bar

_METRICS = [
    ("FCF > Dividends", "1.62x", "good",
     "Free cash flow comfortably covers all dividend obligations with substantial margin for reinvestment."),
    ("Payout Ratio (DPS/EPS)", "64.2%", "warn",
     "The current payout ratio is slightly above the historical median, indicating limited room for aggressive hikes."),
    ("Debt to Equity", "0.34", "good",
     "Pristine balance sheet with conservative leverage ratios compared to software industry peers."),
    ("Interest Sensitivity", "1.0x", "good",
     "Fixed-rate debt profile and massive cash reserves make the company resilient to interest rate spikes."),
    ("Revenue Trend (10yr)", "+14.2%", "good",
     "Strong upward trajectory maintained for over a decade, driven by cloud and enterprise solutions."),
    ("Dividend Growth (10yr)", "+1.5%", "good",
     "Consistent double-digit CAGR demonstrates management's commitment to returning capital."),
    ("OCF > Net Income", "High Quality", "good",
     "Operating cash flow exceeds net income, signaling high earnings quality and accrual integrity."),
    ("OCF Growth (3-5yr)", "-5.8%", "bad",
     "Cash flow growth has decelerated recently due to significant CapEx investments in AI infrastructure."),
    ("Chowder Rule", "9.4", "bad",
     "Combined yield and growth score falls below the target of 12 for high-growth dividend stocks."),
]

_STATUS_MAP = {
    "good": (ft.Icons.CHECK_CIRCLE, t.GREEN, t.GREEN_BG),
    "warn": (ft.Icons.WARNING, t.AMBER, t.AMBER_BG),
    "bad":  (ft.Icons.CANCEL,  t.CRIMSON, t.CRIMSON_BG),
}


def _metric_card(name: str, value: str, status: str, description: str) -> ft.Container:
    icon_name, color, bg = _STATUS_MAP[status]
    return ft.Container(
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border_radius=t.RADIUS_LG,
        padding=ft.padding.all(t.MD),
        margin=ft.margin.only(bottom=t.SM),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=t.MD,
            controls=[
                ft.Container(
                    width=36,
                    height=36,
                    bgcolor=bg,
                    border_radius=t.RADIUS_FULL,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon_name, size=18, color=color),
                ),
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    name,
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                ),
                                ft.Text(
                                    value,
                                    size=14,
                                    weight=ft.FontWeight.W_700,
                                    color=color,
                                    font_family=t.FONT_FAMILY,
                                ),
                            ],
                        ),
                        ft.Text(
                            description,
                            size=12,
                            color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
            ],
        ),
    )


def analysis_view(page: ft.Page) -> ft.View:
    def on_nav(e):
        dest = [routes.SUMMARY, routes.ANALYSIS, routes.HOLDINGS, routes.SETTINGS]
        asyncio.create_task(page.push_route(dest[int(e.data)]))

    app_bar_row = ft.Container(
        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=t.SM,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.PUSH_PIN_OUTLINED, size=20, color=t.ON_SURFACE),
                        ft.Text(
                            "WealthShield",
                            size=16,
                            weight=ft.FontWeight.W_700,
                            color=t.ON_SURFACE,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
                ft.Row(
                    spacing=t.XS,
                    controls=[
                        ft.IconButton(ft.Icons.SEARCH, icon_color=t.ON_SURFACE, icon_size=22),
                        ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color=t.ON_SURFACE, icon_size=22),
                    ],
                ),
            ],
        ),
    )

    stock_heading = ft.Container(
        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
        content=ft.Column(
            spacing=t.XS,
            controls=[
                ft.Text(
                    "Microsoft Corp.",
                    size=26,
                    weight=ft.FontWeight.W_700,
                    color=t.ON_SURFACE,
                    font_family=t.FONT_FAMILY,
                    style=ft.TextStyle(letter_spacing=-0.5),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "NASDAQ: MSFT",
                            size=13,
                            color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                        ),
                        ft.Text(
                            "$415.32 / +1.24% today",
                            size=13,
                            color=t.GREEN,
                            weight=ft.FontWeight.W_600,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
                ft.Container(height=t.XS),
                ft.Text(
                    "WealthShield Health Analysis: Based on trailing 10-year data and current valuation metrics.",
                    size=12,
                    color=t.ON_SURFACE_VARIANT,
                    font_family=t.FONT_FAMILY,
                ),
            ],
        ),
    )

    metric_cards = [_metric_card(n, v, s, d) for n, v, s, d in _METRICS]

    download_btn = ft.Container(
        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
        content=ft.ElevatedButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=t.SM,
                controls=[
                    ft.Icon(ft.Icons.DOWNLOAD_OUTLINED, color=t.ON_PRIMARY, size=18),
                    ft.Text(
                        "Download Detailed PDF",
                        color=t.ON_PRIMARY,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        font_family=t.FONT_FAMILY,
                    ),
                ],
            ),
            width=float("inf"),
            height=52,
            bgcolor=t.PRIMARY,
            elevation=0,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD),
            ),
            on_click=lambda _: None,
        ),
    )

    return ft.View(
        route=routes.ANALYSIS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(1, on_nav),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    app_bar_row,
                    stock_heading,
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=0,
                            controls=metric_cards,
                        ),
                    ),
                    download_btn,
                    ft.Container(height=t.MD),
                ],
            ),
        ],
    )

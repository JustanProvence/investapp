import asyncio
import flet as ft
from my_flet_app import routes, theme as t
from my_flet_app.components.bottom_nav import build_nav_bar
from my_flet_app.components.app_bar import build_app_bar
from my_flet_app.api_client import get_quote, get_metrics

_STATUS_MAP = {
    "good": (ft.Icons.CHECK_CIRCLE, t.GREEN,   t.GREEN_BG),
    "warn": (ft.Icons.WARNING,      t.AMBER,   t.AMBER_BG),
    "bad":  (ft.Icons.CANCEL,       t.CRIMSON, t.CRIMSON_BG),
}

_ACRONYMS = {
    "FCF":    "Free Cash Flow — cash remaining after capital expenditures",
    "OCF":    "Operating Cash Flow — cash generated from core business operations",
    "DPS":    "Dividends Per Share — total dividends paid divided by shares outstanding",
    "EPS":    "Earnings Per Share — net income divided by shares outstanding",
    "AUM":    "Assets Under Management — total market value of assets the fund manages",
    "YTD":    "Year to Date — performance since the start of the current calendar year",
    "CAGR":   "Compound Annual Growth Rate — annualised rate of growth over a period",
    "NAV":    "Net Asset Value — per-share value of a fund's assets minus liabilities",
}


def _acronym_tip(name: str) -> str | None:
    hits = [tip for key, tip in _ACRONYMS.items() if key in name]
    return "\n".join(hits) if hits else None


def _metric_card(name: str, value: str, status: str, description: str) -> ft.Container:
    icon_name, color, bg = _STATUS_MAP.get(status, _STATUS_MAP["warn"])
    tip = _acronym_tip(name)
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
                    width=36, height=36, bgcolor=bg,
                    border_radius=t.RADIUS_FULL, alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon_name, size=18, color=color),
                ),
                ft.Column(
                    expand=True, spacing=4,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(name, size=14, weight=ft.FontWeight.W_600,
                                        color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
                                        tooltip=tip),
                                ft.Text(value, size=14, weight=ft.FontWeight.W_700,
                                        color=color, font_family=t.FONT_FAMILY),
                            ],
                        ),
                        ft.Text(description, size=12,
                                color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                    ],
                ),
            ],
        ),
    )


def analysis_view(page: ft.Page, ticker: str = "MSFT") -> ft.View:
    ticker = ticker.upper()

    def on_nav(e):
        dest = [routes.SUMMARY, routes.HOLDINGS, routes.SETTINGS]
        asyncio.create_task(page.push_route(dest[int(e.data)]))

    heading_col = ft.Column(
        spacing=t.XS,
        controls=[
            ft.Container(
                alignment=ft.Alignment(0, 0),
                padding=ft.padding.all(t.LG),
                content=ft.ProgressRing(color=t.PRIMARY, width=32, height=32),
            )
        ],
    )
    metrics_col = ft.Column(spacing=0, controls=[])

    async def load():
        quote, metrics_data = await asyncio.gather(
            get_quote(ticker),
            get_metrics(ticker),
        )
        metric_list   = metrics_data.get("metrics", [])
        issuer_ticker = metrics_data.get("issuer_ticker")

        if quote:
            chg = quote.get("change_pct") or 0
            price_color = t.GREEN if chg >= 0 else t.CRIMSON
            heading_col.controls = [
                ft.Text(quote.get("name", ticker), size=26,
                        weight=ft.FontWeight.W_700, color=t.ON_SURFACE,
                        font_family=t.FONT_FAMILY,
                        style=ft.TextStyle(letter_spacing=-0.5)),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"{quote.get('exchange', '')}: {ticker}",
                                size=13, color=t.ON_SURFACE_VARIANT,
                                font_family=t.FONT_FAMILY),
                        ft.Text(f"${quote.get('price', 0):.2f} / {chg:+.2f}%",
                                size=13, color=price_color,
                                weight=ft.FontWeight.W_600,
                                font_family=t.FONT_FAMILY),
                    ],
                ),
                ft.Container(height=t.XS),
                ft.Text("Market Research Health Analysis: Based on trailing data "
                        "and current valuation metrics.",
                        size=12, color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY),
            ]
            if issuer_ticker:
                heading_col.controls.append(
                    ft.Container(
                        bgcolor=t.AMBER_BG,
                        border_radius=t.RADIUS_MD,
                        padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM),
                        margin=ft.margin.only(top=t.SM),
                        content=ft.Row(
                            spacing=t.SM,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=t.AMBER),
                                ft.Text(
                                    f"Preferred stock — Debt/Equity and Interest Coverage "
                                    f"metrics are sourced from the issuer ({issuer_ticker}).",
                                    size=12, color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY, expand=True,
                                ),
                            ],
                        ),
                    )
                )
        if metric_list:
            metrics_col.controls = [
                _metric_card(m["name"], m["value"], m["status"], m["description"])
                for m in metric_list
            ]
        page.update()

    asyncio.create_task(load())

    return ft.View(
        route=routes.ANALYSIS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(0, on_nav),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    build_app_bar(),
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
                        content=heading_col,
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=metrics_col,
                    ),
                    ft.Container(
                        margin=ft.margin.symmetric(
                            horizontal=t.CONTAINER_MARGIN, vertical=t.MD),
                        content=ft.ElevatedButton(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=t.SM,
                                controls=[
                                    ft.Icon(ft.Icons.DOWNLOAD_OUTLINED,
                                            color=t.ON_PRIMARY, size=18),
                                    ft.Text("Download Detailed PDF",
                                            color=t.ON_PRIMARY, size=14,
                                            weight=ft.FontWeight.W_600,
                                            font_family=t.FONT_FAMILY),
                                ],
                            ),
                            width=float("inf"), height=52,
                            bgcolor=t.PRIMARY, elevation=0,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD)),
                            on_click=lambda _: None,
                        ),
                    ),
                    ft.Container(height=t.MD),
                ],
            ),
        ],
    )

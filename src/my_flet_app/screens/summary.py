import asyncio
import math
import flet as ft
import flet.canvas as canvas
from my_flet_app import routes, theme as t
from my_flet_app.components.bottom_nav import build_nav_bar
from my_flet_app.components.app_bar import build_app_bar
from my_flet_app.api_client import get_portfolio_summary

_CHART_COLORS = [
    t.PRIMARY_CONTAINER,
    t.GREEN,
    t.OUTLINE,
    t.OUTLINE_VARIANT,
    "#F59E0B",
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
]


def _section_heading(title: str, right_widget=None) -> ft.Row:
    controls = [
        ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
    ]
    if right_widget:
        controls.append(right_widget)
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=controls,
    )


def _build_donut_canvas(
    sections: list[tuple[float, str]],
    size: float,
    center_space_radius: float,
    gap_rad: float = 0.05,
) -> canvas.Canvas:
    total = sum(v for v, _ in sections)
    outer_r = size / 2 - 4
    inner_r = center_space_radius
    mid_r = (outer_r + inner_r) / 2
    stroke_w = outer_r - inner_r
    shapes = []
    angle = -math.pi / 2
    for value, color in sections:
        sweep = (value / total) * 2 * math.pi
        effective_sweep = max(sweep - gap_rad, 0.01)
        paint = ft.Paint(color=color, style=ft.PaintingStyle.STROKE, stroke_width=stroke_w, anti_alias=True)
        cx = size / 2
        cy = size / 2
        shapes.append(canvas.Arc(
            x=cx - mid_r, y=cy - mid_r,
            width=mid_r * 2, height=mid_r * 2,
            start_angle=angle, sweep_angle=effective_sweep,
            paint=paint,
        ))
        angle += sweep
    return canvas.Canvas(shapes=shapes, width=size, height=size)


def _spinner() -> ft.Container:
    return ft.Container(
        alignment=ft.Alignment(0, 0),
        content=ft.ProgressRing(width=32, height=32, color=t.PRIMARY),
    )


def _build_sector_section(sector_alloc: list[dict]) -> ft.Column:
    pie_sections = [
        (item["allocation_pct"], _CHART_COLORS[i % len(_CHART_COLORS)])
        for i, item in enumerate(sector_alloc)
    ]
    pie_size = 140.0
    pie_chart = _build_donut_canvas(pie_sections, pie_size, center_space_radius=0.0, gap_rad=0.03)
    legend_col = ft.Column(
        spacing=t.SM,
        controls=[
            ft.Row(
                spacing=t.XS,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=10, height=10,
                                 bgcolor=_CHART_COLORS[i % len(_CHART_COLORS)],
                                 border_radius=t.RADIUS_FULL),
                    ft.Text(
                        f"{item['sector']}  {item['allocation_pct']:.1f}%",
                        size=12, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY,
                    ),
                ],
            )
            for i, item in enumerate(sector_alloc)
        ],
    )
    return ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading("Sector Allocation"),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=t.LG,
                controls=[pie_chart, legend_col],
            ),
        ],
    )


def _build_forecast_section() -> ft.Column:
    def _stacked_bar(tech_h, health_h, reit_h, max_h=100):
        total = tech_h + health_h + reit_h
        spacer_h = max(0, max_h - total)
        bar_controls = []
        if spacer_h > 0:
            bar_controls.append(ft.Container(height=spacer_h))
        if reit_h > 0:
            bar_controls.append(ft.Container(height=reit_h, bgcolor=t.OUTLINE_VARIANT, border_radius=ft.border_radius.only(top_left=3, top_right=3)))
        if health_h > 0:
            bar_controls.append(ft.Container(height=health_h, bgcolor=t.GREEN))
        if tech_h > 0:
            bar_controls.append(ft.Container(height=tech_h, bgcolor=t.PRIMARY_CONTAINER))
        return ft.Container(width=40, height=max_h, content=ft.Column(spacing=0, controls=bar_controls))

    quarters = [("Q1", 20, 15, 10), ("Q2", 30, 20, 12), ("Q3", 40, 25, 15), ("Q4", 50, 30, 18)]
    bar_cols = [
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=t.XS,
            controls=[_stacked_bar(tech, health, reit), ft.Text(label, size=11, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)],
        )
        for label, tech, health, reit in quarters
    ]
    legend_items = [(t.PRIMARY_CONTAINER, "Tech"), (t.GREEN, "Health"), (t.OUTLINE_VARIANT, "REIT")]
    legend = ft.Row(
        spacing=t.MD,
        controls=[
            ft.Row(
                spacing=t.XS,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.Container(width=10, height=10, bgcolor=c, border_radius=2), ft.Text(label, size=11, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)],
            )
            for c, label in legend_items
        ],
    )
    return ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading("Sector Growth Forecast"),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END, controls=bar_cols),
            legend,
        ],
    )


def summary_view(page: ft.Page) -> ft.View:
    def on_nav(e):
        dest = [routes.SUMMARY, routes.HOLDINGS, routes.SETTINGS]
        asyncio.create_task(page.push_route(dest[int(e.data)]))

    # ── Mutable hero card controls ────────────────────────────────────────────
    yield_text = ft.Text(
        "...",
        size=38,
        weight=ft.FontWeight.W_700,
        color=t.ON_PRIMARY,
        font_family=t.FONT_FAMILY,
        style=ft.TextStyle(letter_spacing=-1.0),
    )
    portfolio_value_text = ft.Text(
        "Loading portfolio data…",
        size=13,
        color=t.ON_PRIMARY_CONTAINER,
        font_family=t.FONT_FAMILY,
    )

    # ── Mutable donut section controls ────────────────────────────────────────
    donut_container = ft.Container(
        alignment=ft.Alignment(0, 0),
        content=_spinner(),
    )
    legend_row = ft.Row(wrap=True, spacing=t.LG, controls=[])

    # ── Mutable income section controls ───────────────────────────────────────
    income_col = ft.Column(spacing=t.MD, controls=[_spinner()])
    income_mode    = ["monthly"]
    _income_cache  = [[]]   # [(ticker, annual_income), ...]

    monthly_btn = ft.Container(
        content=ft.Text("Monthly", size=12, weight=ft.FontWeight.W_600,
                         color=t.ON_PRIMARY, font_family=t.FONT_FAMILY),
        bgcolor=t.PRIMARY, border_radius=t.RADIUS_FULL,
        padding=ft.padding.symmetric(horizontal=t.MD, vertical=4),
        on_click=lambda _: _set_income_mode("monthly"), ink=True,
    )
    yearly_btn = ft.Container(
        content=ft.Text("Yearly", size=12, weight=ft.FontWeight.W_600,
                         color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border=ft.border.all(1, t.OUTLINE_VARIANT),
        border_radius=t.RADIUS_FULL,
        padding=ft.padding.symmetric(horizontal=t.MD, vertical=4),
        on_click=lambda _: _set_income_mode("yearly"), ink=True,
    )

    def _render_income():
        items = _income_cache[0]
        mode  = income_mode[0]
        monthly_btn.bgcolor = t.PRIMARY if mode == "monthly" else t.SURFACE_CONTAINER_LOWEST
        monthly_btn.content.color = t.ON_PRIMARY if mode == "monthly" else t.ON_SURFACE
        monthly_btn.border = None if mode == "monthly" else ft.border.all(1, t.OUTLINE_VARIANT)
        yearly_btn.bgcolor = t.PRIMARY if mode == "yearly" else t.SURFACE_CONTAINER_LOWEST
        yearly_btn.content.color = t.ON_PRIMARY if mode == "yearly" else t.ON_SURFACE
        yearly_btn.border = None if mode == "yearly" else ft.border.all(1, t.OUTLINE_VARIANT)
        if not items:
            income_col.controls = [
                ft.Text("No dividend income data available", size=13,
                        color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)
            ]
            page.update()
            return
        max_income = items[0][1]
        divisor = 12 if mode == "monthly" else 1
        suffix  = "/mo" if mode == "monthly" else "/yr"
        rows = [
            ft.Column(spacing=t.XS, controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(tk, size=14, weight=ft.FontWeight.W_600,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                        ft.Text(f"${ann / divisor:,.2f}{suffix}", size=14,
                                weight=ft.FontWeight.W_600,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ],
                ),
                ft.ProgressBar(
                    value=ann / max_income if max_income > 0 else 0,
                    bgcolor=t.OUTLINE_VARIANT, color=t.PRIMARY, height=6,
                ),
            ])
            for tk, ann in items
        ]
        total = sum(a for _, a in items)
        rows.append(ft.Divider(height=1, color=t.OUTLINE_VARIANT, thickness=1))
        rows.append(ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Total", size=14, weight=ft.FontWeight.W_700,
                        color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                ft.Text(f"${total / divisor:,.2f}{suffix}", size=14,
                        weight=ft.FontWeight.W_700,
                        color=t.GREEN, font_family=t.FONT_FAMILY),
            ],
        ))
        income_col.controls = rows
        page.update()

    def _set_income_mode(mode: str):
        income_mode[0] = mode
        _render_income()

    # ── Mutable sector section ────────────────────────────────────────────────
    # Empty column takes zero space; populated in _load() when sector data arrives.
    sector_col = ft.Column(spacing=0, controls=[])

    # ── Mutable total-return section ──────────────────────────────────────────
    return_col = ft.Column(spacing=t.MD, controls=[_spinner()])

    async def _load():
        uid  = (page.session.store.get("user") or {}).get("id", "")
        data = await get_portfolio_summary(uid)
        if data is None or not data.get("holdings"):
            no_assets = ft.Text("No assets yet — add holdings to get started.",
                                size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)
            yield_text.value = "—"
            portfolio_value_text.value = "No holdings in your portfolio."
            donut_container.content = ft.Text("No assets", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)
            income_col.controls = [no_assets]
            return_col.controls = [ft.Text("No assets", size=13, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY)]
            page.update()
            return

        portfolio_yield = data.get("portfolio_yield") or 0
        total_value = data.get("total_value") or 0
        holdings = data.get("holdings") or []

        yield_text.value = f"{portfolio_yield:.2f}%"
        portfolio_value_text.value = f"Total portfolio value: ${total_value:,.0f}. Blended dividend yield across all holdings."

        # ── Holdings pie (same layout as Sector Allocation) ───────────────────
        if holdings:
            sections = []
            legend_items = []
            for i, h in enumerate(holdings):
                alloc = h.get("allocation_pct") or 0
                color = _CHART_COLORS[i % len(_CHART_COLORS)]
                sections.append((max(alloc, 0.1), color))
                legend_items.append((color, h["ticker"], f"{alloc:.1f}%"))

            pie_size  = 140.0
            pie_chart = _build_donut_canvas(sections, pie_size, center_space_radius=0.0, gap_rad=0.03)
            legend_col = ft.Column(
                spacing=t.SM,
                controls=[
                    ft.Row(
                        spacing=t.XS,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(width=10, height=10, bgcolor=color,
                                         border_radius=t.RADIUS_FULL),
                            ft.Text(f"{tk}  {pct}", size=12,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY),
                        ],
                    )
                    for color, tk, pct in legend_items
                ],
            )
            donut_container.content = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=t.LG,
                controls=[pie_chart, legend_col],
            )
        else:
            donut_container.content = ft.Text(
                "No holdings", size=13,
                color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY,
            )
        legend_row.controls = []

        # ── Sector allocation ─────────────────────────────────────────────────
        sector_alloc = data.get("sector_allocation") or []
        if sector_alloc:
            sector_col.controls = [
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                    content=_build_sector_section(sector_alloc),
                ),
                ft.Container(height=t.LG),
            ]
        else:
            sector_col.controls = []

        # ── Income per asset ──────────────────────────────────────────────────
        income_items = [
            (h["ticker"], (h.get("annual_income") or 0))
            for h in holdings
            if (h.get("annual_income") or 0) > 0
        ]
        income_items.sort(key=lambda x: x[1], reverse=True)
        _income_cache[0] = income_items
        _render_income()

        # ── Total return ──────────────────────────────────────────────────────
        invested  = data.get("total_invested") or 0
        gain      = data.get("unrealized_gain")
        gain_pct  = data.get("unrealized_pct")
        est_income = data.get("estimated_annual_income") or 0

        if invested > 0:
            gain_color = t.GREEN if (gain or 0) >= 0 else t.CRIMSON
            gain_str   = (f"${gain:+,.2f}  ({gain_pct:+.2f}%)"
                          if gain is not None and gain_pct is not None else "N/A")
            combined   = (gain or 0) + est_income
            comb_color = t.GREEN if combined >= 0 else t.CRIMSON

            def _stat_row(label: str, value: str, value_color=None) -> ft.Row:
                return ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(label, size=13, color=t.ON_SURFACE_VARIANT,
                                font_family=t.FONT_FAMILY),
                        ft.Text(value, size=13, weight=ft.FontWeight.W_600,
                                color=value_color or t.ON_SURFACE,
                                font_family=t.FONT_FAMILY),
                    ],
                )

            return_col.controls = [
                ft.Container(
                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                    border_radius=t.RADIUS_LG,
                    padding=ft.padding.all(t.MD),
                    content=ft.Column(spacing=t.SM, controls=[
                        ft.Row(
                            controls=[
                                ft.Column(expand=True, spacing=2, controls=[
                                    ft.Text("INVESTED", size=10, weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY,
                                            style=ft.TextStyle(letter_spacing=0.8)),
                                    ft.Text(f"${invested:,.2f}", size=18,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY),
                                ]),
                                ft.Column(expand=True, spacing=2,
                                          horizontal_alignment=ft.CrossAxisAlignment.END,
                                          controls=[
                                    ft.Text("CURRENT VALUE", size=10,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY,
                                            style=ft.TextStyle(letter_spacing=0.8)),
                                    ft.Text(f"${total_value:,.2f}", size=18,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY),
                                ]),
                            ],
                        ),
                        ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                        _stat_row("Price Return", gain_str, gain_color),
                        _stat_row("Est. Annual Income",
                                  f"${est_income:,.2f}/yr", t.GREEN if est_income > 0 else None),
                        ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Total Return", size=14,
                                        weight=ft.FontWeight.W_700,
                                        color=t.ON_SURFACE,
                                        font_family=t.FONT_FAMILY),
                                ft.Text(f"${combined:+,.2f}", size=14,
                                        weight=ft.FontWeight.W_700,
                                        color=comb_color,
                                        font_family=t.FONT_FAMILY),
                            ],
                        ),
                    ]),
                ),
            ]
        else:
            return_col.controls = [
                ft.Text("Add holdings to see total return.",
                        size=13, color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY),
            ]

        page.update()

    asyncio.create_task(_load())

    app_bar_row = build_app_bar()

    hero_card = ft.Row(
        spacing=0,
        controls=[
            ft.Container(width=5),
            ft.Container(
                expand=True,
                padding=ft.padding.all(t.LG),
                bgcolor=t.PRIMARY_CONTAINER,
                border_radius=t.RADIUS_LG,
                content=ft.Column(
                    spacing=t.SM,
                    controls=[
                        ft.Text(
                            "PORTFOLIO YIELD",
                            size=11,
                            weight=ft.FontWeight.W_600,
                            color=t.ON_PRIMARY_CONTAINER,
                            font_family=t.FONT_FAMILY,
                            style=ft.TextStyle(letter_spacing=1.2),
                        ),
                        yield_text,
                        portfolio_value_text,
                    ],
                ),
            ),
            ft.Container(width=5),
        ],
    )

    donut_section = ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading("Holdings Distribution"),
            donut_container,
            legend_row,
        ],
    )

    income_section = ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading(
                "Income per Asset",
                ft.Row(spacing=t.XS, controls=[monthly_btn, yearly_btn]),
            ),
            income_col,
        ],
    )

    return ft.View(
        route=routes.SUMMARY,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(0, on_nav),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    app_bar_row,
                    ft.Container(height=t.SM),
                    hero_card,
                    ft.Container(height=t.LG),
                    ft.Container(padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN), content=donut_section),
                    ft.Container(height=t.LG),
                    sector_col,
                    ft.Container(padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN), content=income_section),
                    ft.Container(height=t.LG),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Column(spacing=t.MD, controls=[
                            _section_heading("Total Return"),
                            return_col,
                        ]),
                    ),
                    ft.Container(height=t.LG),
                ],
            ),
        ],
    )

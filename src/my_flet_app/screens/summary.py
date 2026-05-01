import asyncio
import math
import flet as ft
import flet.canvas as canvas
from my_flet_app import routes, theme as t
from my_flet_app.components.bottom_nav import build_nav_bar


def _section_heading(title: str, right_widget=None) -> ft.Row:
    controls = [
        ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.W_700,
            color=t.ON_SURFACE,
            font_family=t.FONT_FAMILY,
        ),
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
    """Build a donut chart using canvas arcs."""
    total = sum(v for v, _ in sections)
    outer_r = size / 2 - 4
    inner_r = center_space_radius
    mid_r = (outer_r + inner_r) / 2
    stroke_w = outer_r - inner_r

    shapes = []
    angle = -math.pi / 2  # start at top

    for value, color in sections:
        sweep = (value / total) * 2 * math.pi
        effective_sweep = max(sweep - gap_rad, 0.01)
        paint = ft.Paint(
            color=color,
            style=ft.PaintingStyle.STROKE,
            stroke_width=stroke_w,
            anti_alias=True,
        )
        cx = size / 2
        cy = size / 2
        shapes.append(canvas.Arc(
            x=cx - mid_r,
            y=cy - mid_r,
            width=mid_r * 2,
            height=mid_r * 2,
            start_angle=angle,
            sweep_angle=effective_sweep,
            paint=paint,
        ))
        angle += sweep

    return canvas.Canvas(shapes=shapes, width=size, height=size)


def _build_hero_card() -> ft.Container:
    return ft.Container(
        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
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
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=t.SM,
                    controls=[
                        ft.Text(
                            "3.45%",
                            size=38,
                            weight=ft.FontWeight.W_700,
                            color=t.ON_PRIMARY,
                            font_family=t.FONT_FAMILY,
                            style=ft.TextStyle(letter_spacing=-1.0),
                        ),
                        ft.Container(
                            content=ft.Text(
                                "+0.12%",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=t.GREEN,
                                font_family=t.FONT_FAMILY,
                            ),
                            bgcolor=t.GREEN_BG,
                            border_radius=t.RADIUS_FULL,
                            padding=ft.padding.symmetric(horizontal=t.SM, vertical=t.XS),
                        ),
                    ],
                ),
                ft.Text(
                    "Blended dividend yield across all tracked holdings. Calculated from trailing 12-month distributions.",
                    size=13,
                    color=t.ON_PRIMARY_CONTAINER,
                    font_family=t.FONT_FAMILY,
                ),
            ],
        ),
    )


def _build_donut_section() -> ft.Column:
    donut_sections = [
        (40, t.PRIMARY_CONTAINER),
        (25, t.GREEN),
        (20, t.OUTLINE),
        (15, t.OUTLINE_VARIANT),
    ]
    donut_size = 220.0
    center_r = 55.0

    donut_chart = _build_donut_canvas(donut_sections, donut_size, center_r)

    donut_with_label = ft.Stack(
        width=donut_size,
        height=donut_size,
        controls=[
            donut_chart,
            ft.Container(
                width=donut_size,
                height=donut_size,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Text(
                            "AAPL",
                            size=14,
                            weight=ft.FontWeight.W_700,
                            color=t.ON_SURFACE,
                            font_family=t.FONT_FAMILY,
                        ),
                        ft.Text(
                            "40%",
                            size=12,
                            color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
            ),
        ],
    )

    legend_items = [
        (t.PRIMARY_CONTAINER, "AAPL", "40%"),
        (t.GREEN, "MSFT", "25%"),
        (t.OUTLINE, "JNJ", "20%"),
        (t.OUTLINE_VARIANT, "Other", "15%"),
    ]

    def _legend_item(color, ticker, pct):
        return ft.Row(
            spacing=t.XS,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=10, height=10,
                    bgcolor=color,
                    border_radius=t.RADIUS_FULL,
                ),
                ft.Text(
                    f"{ticker}  {pct}",
                    size=12,
                    color=t.ON_SURFACE_VARIANT,
                    font_family=t.FONT_FAMILY,
                ),
            ],
        )

    legend_grid = ft.Row(
        wrap=True,
        spacing=t.LG,
        controls=[_legend_item(c, tk, p) for c, tk, p in legend_items],
    )

    return ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading("Holdings Distribution"),
            ft.Container(
                alignment=ft.Alignment(0, 0),
                content=donut_with_label,
            ),
            legend_grid,
        ],
    )


def _build_sector_section() -> ft.Column:
    pie_sections = [
        (35, t.PRIMARY_CONTAINER),
        (50, t.GREEN),
        (15, t.OUTLINE_VARIANT),
    ]
    pie_size = 140.0
    # Solid pie: center_space_radius = 0 means full pie
    # Use small center radius to approximate solid pie with arc
    pie_chart = _build_donut_canvas(pie_sections, pie_size, center_space_radius=0.0, gap_rad=0.03)

    legend_items = [
        (t.PRIMARY_CONTAINER, "Tech", "35%"),
        (t.GREEN, "Finance", "50%"),
        (t.OUTLINE_VARIANT, "Energy", "15%"),
    ]

    legend_col = ft.Column(
        spacing=t.SM,
        controls=[
            ft.Row(
                spacing=t.XS,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=10, height=10, bgcolor=c, border_radius=t.RADIUS_FULL),
                    ft.Text(
                        f"{label}  {pct}",
                        size=12,
                        color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY,
                    ),
                ],
            )
            for c, label, pct in legend_items
        ],
    )

    return ft.Column(
        spacing=t.MD,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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


def _build_income_section() -> ft.Column:
    assets = [
        ("AAPL", "$125.40", 1.0),
        ("MSFT", "$84.20", 0.67),
        ("O", "$42.15", 0.34),
    ]
    rows = []
    for ticker, amount, progress in assets:
        rows.append(
            ft.Column(
                spacing=t.XS,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                ticker,
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=t.ON_SURFACE,
                                font_family=t.FONT_FAMILY,
                            ),
                            ft.Text(
                                amount,
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=t.ON_SURFACE,
                                font_family=t.FONT_FAMILY,
                            ),
                        ],
                    ),
                    ft.ProgressBar(
                        value=progress,
                        bgcolor=t.OUTLINE_VARIANT,
                        color=t.PRIMARY,
                        height=6,
                    ),
                ],
            )
        )

    return ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading(
                "Income per Asset",
                ft.Text(
                    "Monthly Est.",
                    size=12,
                    color=t.GREEN,
                    weight=ft.FontWeight.W_600,
                    font_family=t.FONT_FAMILY,
                ),
            ),
            ft.Column(spacing=t.MD, controls=rows),
        ],
    )


def _stacked_bar(tech_h: int, health_h: int, reit_h: int, max_h: int = 100) -> ft.Container:
    total = tech_h + health_h + reit_h
    spacer_h = max(0, max_h - total)

    bar_controls = []
    if spacer_h > 0:
        bar_controls.append(ft.Container(height=spacer_h))

    if reit_h > 0:
        bar_controls.append(
            ft.Container(
                height=reit_h,
                bgcolor=t.OUTLINE_VARIANT,
                border_radius=ft.border_radius.only(top_left=3, top_right=3),
            )
        )
    if health_h > 0:
        bar_controls.append(ft.Container(height=health_h, bgcolor=t.GREEN))
    if tech_h > 0:
        bar_controls.append(ft.Container(height=tech_h, bgcolor=t.PRIMARY_CONTAINER))

    return ft.Container(
        width=40,
        height=max_h,
        content=ft.Column(spacing=0, controls=bar_controls),
    )


def _build_forecast_section() -> ft.Column:
    quarters = [
        ("Q1", 20, 15, 10),
        ("Q2", 30, 20, 12),
        ("Q3", 40, 25, 15),
        ("Q4", 50, 30, 18),
    ]
    bar_cols = []
    for label, tech, health, reit in quarters:
        bar_cols.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=t.XS,
                controls=[
                    _stacked_bar(tech, health, reit),
                    ft.Text(
                        label,
                        size=11,
                        color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY,
                    ),
                ],
            )
        )

    legend_items = [
        (t.PRIMARY_CONTAINER, "Tech"),
        (t.GREEN, "Health"),
        (t.OUTLINE_VARIANT, "REIT"),
    ]
    legend = ft.Row(
        spacing=t.MD,
        controls=[
            ft.Row(
                spacing=t.XS,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=10, height=10, bgcolor=c, border_radius=2),
                    ft.Text(label, size=11, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                ],
            )
            for c, label in legend_items
        ],
    )

    return ft.Column(
        spacing=t.MD,
        controls=[
            _section_heading("Sector Growth Forecast"),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.END,
                controls=bar_cols,
            ),
            legend,
        ],
    )


def summary_view(page: ft.Page) -> ft.View:
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
                ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color=t.ON_SURFACE, icon_size=22),
            ],
        ),
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
                    ft.Container(height=t.MD),
                    _build_hero_card(),
                    ft.Container(height=t.LG),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=_build_donut_section(),
                    ),
                    ft.Container(height=t.LG),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=_build_sector_section(),
                    ),
                    ft.Container(height=t.LG),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=_build_income_section(),
                    ),
                    ft.Container(height=t.LG),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=_build_forecast_section(),
                    ),
                    ft.Container(height=t.LG),
                    ft.Container(
                        height=120,
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        bgcolor=t.PRIMARY_CONTAINER,
                        border_radius=t.RADIUS_LG,
                    ),
                    ft.Container(height=t.LG),
                ],
            ),
        ],
    )

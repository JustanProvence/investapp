import flet as ft
from marketresearch import theme as t
from marketresearch.components.chip import semantic_chip


def investment_card(asset: dict, on_click=None) -> ft.Container:
    pct = asset["change_pct"]
    sign = "+" if pct >= 0 else ""
    change_label = f"{sign}{pct:.2f}%"

    return ft.Container(
        width=172,
        padding=ft.padding.all(t.MD),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border_radius=t.RADIUS_LG,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.06),
            offset=ft.Offset(0, 4),
        ),
        on_click=on_click,
        content=ft.Column(
            spacing=t.SM,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    asset["ticker"],
                                    size=14,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                ),
                                ft.Text(
                                    asset["category"],
                                    size=11,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY,
                                ),
                            ],
                        ),
                        ft.Container(
                            content=ft.Text(
                                asset["ticker"][:2],
                                size=12,
                                weight=ft.FontWeight.W_700,
                                color=t.INVERSE_PRIMARY,
                                font_family=t.FONT_FAMILY,
                            ),
                            bgcolor=t.PRIMARY_CONTAINER,
                            border_radius=t.RADIUS_DEFAULT,
                            width=34,
                            height=34,
                            alignment=ft.Alignment(0, 0),
                        ),
                    ],
                ),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            f"${asset['value']:,.0f}",
                            size=17,
                            weight=ft.FontWeight.W_700,
                            color=t.ON_SURFACE,
                            font_family=t.FONT_FAMILY,
                        ),
                        ft.Text(
                            asset["name"],
                            size=11,
                            color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                ),
                semantic_chip(change_label, pct >= 0),
            ],
        ),
    )

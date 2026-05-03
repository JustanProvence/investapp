import flet as ft
from marketresearch import theme as t
from marketresearch.components.chip import category_chip


def asset_list_item(asset: dict, on_click=None) -> ft.Container:
    pct = asset["change_pct"]
    sign = "+" if pct >= 0 else ""
    change_color = t.GREEN if pct >= 0 else t.CRIMSON

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM + 2),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border_radius=t.RADIUS_LG,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.05),
            offset=ft.Offset(0, 4),
        ),
        on_click=on_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=t.MD,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                asset["ticker"][:2],
                                size=12,
                                weight=ft.FontWeight.W_700,
                                color=t.INVERSE_PRIMARY,
                                font_family=t.FONT_FAMILY,
                            ),
                            bgcolor=t.PRIMARY_CONTAINER,
                            border_radius=t.RADIUS_MD,
                            width=44,
                            height=44,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    asset["name"],
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                category_chip(asset["category"]),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=4,
                    controls=[
                        ft.Text(
                            f"${asset['value']:,.0f}",
                            size=15,
                            weight=ft.FontWeight.W_700,
                            color=t.ON_SURFACE,
                            font_family=t.FONT_FAMILY,
                        ),
                        ft.Text(
                            f"{sign}{pct:.2f}%",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=change_color,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
            ],
        ),
    )

import flet as ft
from marketresearch import theme as t


def category_chip(label: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(
            label,
            size=11,
            weight=ft.FontWeight.W_500,
            color=t.ON_SURFACE_VARIANT,
            font_family=t.FONT_FAMILY,
        ),
        bgcolor=t.SURFACE_CONTAINER_HIGH,
        border_radius=t.RADIUS_FULL,
        padding=ft.padding.symmetric(horizontal=t.SM + 2, vertical=3),
    )


def semantic_chip(label: str, positive: bool | None = None) -> ft.Container:
    if positive is True:
        text_color, bg_color = t.GREEN, t.GREEN_BG
    elif positive is False:
        text_color, bg_color = t.CRIMSON, t.CRIMSON_BG
    else:
        text_color, bg_color = t.AMBER, t.AMBER_BG

    return ft.Container(
        content=ft.Text(
            label,
            size=11,
            weight=ft.FontWeight.W_600,
            color=text_color,
            font_family=t.FONT_FAMILY,
        ),
        bgcolor=bg_color,
        border_radius=t.RADIUS_FULL,
        padding=ft.padding.symmetric(horizontal=t.SM + 2, vertical=3),
    )

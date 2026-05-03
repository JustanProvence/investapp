import flet as ft
from marketresearch import theme as t
from marketresearch.logo_b64 import LOGO_SRC, LOGO_SRC_DARK


def build_app_bar(page=None, right_widget=None) -> ft.Container:
    theme_mode = (page.session.store.get("theme_mode") if page else None) or \
                 (str(page.platform_brightness.value) if page and page.platform_brightness else "light")
    logo_src = LOGO_SRC_DARK if theme_mode == "dark" else LOGO_SRC
    return ft.Container(
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
                        ft.Image(src=logo_src, width=32, height=32),
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text("Market", size=14, weight=ft.FontWeight.W_700,
                                        color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                ft.Text("Research", size=14, weight=ft.FontWeight.W_500,
                                        color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                            ],
                        ),
                    ],
                ),
                right_widget or ft.IconButton(
                    ft.Icons.NOTIFICATIONS_OUTLINED,
                    icon_color=t.ON_SURFACE,
                    icon_size=22,
                ),
            ],
        ),
    )

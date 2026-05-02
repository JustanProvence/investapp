import flet as ft
from my_flet_app import theme as t
from my_flet_app.logo_b64 import LOGO_SRC


def build_app_bar(right_widget=None) -> ft.Container:
    """Branded top app bar with shield logo and Market Research name."""
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
                        ft.Image(src=LOGO_SRC, width=32, height=32),
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

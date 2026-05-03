import asyncio
import os
import flet as ft
from marketresearch import theme as t, routes
from marketresearch.logo_b64 import LOGO_SRC, LOGO_SRC_DARK, GOOGLE_LOGO_SRC, GOOGLE_LOGO_SRC_DARK

_GOOGLE_AUTH_URL = os.getenv("GOOGLE_AUTH_URL", "http://localhost:8000/auth/google/authorize")


def _oauth_button(label: str, logo_char: str, logo_bg: str, on_click, logo_src: str = None) -> ft.Container:
    logo = ft.Image(src=logo_src, width=22, height=22) if logo_src else ft.Container(
        content=ft.Text(
            logo_char,
            size=11,
            weight=ft.FontWeight.W_700,
            color=t.ON_PRIMARY,
            font_family=t.FONT_FAMILY,
        ),
        bgcolor=logo_bg,
        border_radius=t.RADIUS_SM,
        width=22,
        height=22,
        alignment=ft.Alignment(0, 0),
    )
    return ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=t.SM + 2,
            controls=[
                logo,
                ft.Text(
                    label,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=t.ON_SURFACE,
                    font_family=t.FONT_FAMILY,
                ),
            ],
        ),
        border=ft.border.all(1, t.OUTLINE_VARIANT),
        border_radius=t.RADIUS_MD,
        padding=ft.padding.symmetric(vertical=t.SM + 4),
        on_click=on_click,
        ink=True,
    )


def login_view(page: ft.Page) -> ft.View:
    theme_mode = page.session.store.get("theme_mode") or str(page.platform_brightness.value if page.platform_brightness else "light")
    is_dark = theme_mode == "dark"
    logo_src = LOGO_SRC_DARK if is_dark else LOGO_SRC
    google_logo_src = GOOGLE_LOGO_SRC_DARK if is_dark else GOOGLE_LOGO_SRC

    return ft.View(
        route=routes.LOGIN,
        bgcolor=t.BACKGROUND,
        padding=0,
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(height=t.XL + t.MD),
                    # Logo + brand name
                    ft.Container(
                        alignment=ft.Alignment(0, 0),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=t.SM,
                            controls=[
                                ft.Image(src=logo_src, width=56, height=56),
                                ft.Column(
                                    spacing=0,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Market", size=15, weight=ft.FontWeight.W_700,
                                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
                                                text_align=ft.TextAlign.CENTER),
                                        ft.Text("Research", size=15, weight=ft.FontWeight.W_500,
                                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
                                                text_align=ft.TextAlign.CENTER),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.LG),
                    # Headline
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=t.SM,
                            controls=[
                                ft.Text(
                                    "Welcome Back",
                                    size=38,
                                    weight=ft.FontWeight.W_700,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                    text_align=ft.TextAlign.CENTER,
                                    style=ft.TextStyle(letter_spacing=-0.8),
                                ),
                                ft.Text(
                                    "Secure access to your institutional-grade\nportfolio intelligence.",
                                    size=15,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.XL),
                    # Form card
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        padding=ft.padding.all(t.MD + t.XS),
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        border_radius=t.RADIUS_LG,
                        shadow=ft.BoxShadow(
                            blur_radius=24,
                            color=t.with_alpha(t.PRIMARY_CONTAINER, 0.08),
                            offset=ft.Offset(0, 8),
                        ),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                _oauth_button(
                                    "Login with Google",
                                    "G",
                                    "#4285F4",
                                    lambda _: asyncio.create_task(
                                        ft.UrlLauncher().launch_url(
                                            _GOOGLE_AUTH_URL,
                                            web_only_window_name="_self",
                                        )
                                    ),
                                    logo_src=google_logo_src,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

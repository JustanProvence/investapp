import asyncio
import flet as ft
from my_flet_app import theme as t, routes
from my_flet_app import api_client as api
from my_flet_app.logo_b64 import LOGO_SRC, GOOGLE_LOGO_SRC


def _divider_row() -> ft.Row:
    line = ft.Container(expand=True, height=1, bgcolor=t.OUTLINE_VARIANT)
    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=t.MD,
        controls=[
            line,
            ft.Text(
                "OR CONTINUE WITH",
                size=10,
                weight=ft.FontWeight.W_500,
                color=t.ON_SURFACE_VARIANT,
                font_family=t.FONT_FAMILY,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(expand=True, height=1, bgcolor=t.OUTLINE_VARIANT),
        ],
    )


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
    email_field = ft.TextField(
        label="Email Address",
        hint_text="name@company.com",
        prefix_icon=ft.Icons.MAIL_OUTLINE,
        border_color=t.OUTLINE_VARIANT,
        focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD,
        border_width=1,
        focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        label_style=ft.TextStyle(color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY, size=12),
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY, size=14),
        cursor_color=t.PRIMARY,
    )

    password_field = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_color=t.OUTLINE_VARIANT,
        focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD,
        border_width=1,
        focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        label_style=ft.TextStyle(color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY, size=12),
        cursor_color=t.PRIMARY,
    )

    error_text = ft.Text(
        "",
        color="#D32F2F",
        size=13,
        font_family=t.FONT_FAMILY,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    async def _do_login():
        email = email_field.value.strip().lower()
        if not email:
            error_text.value = "Please enter your email address."
            error_text.visible = True
            page.update()
            return
        user = await api.login(email)
        if user:
            page.session.store.set("user", user)
            page.session.store.set("theme_mode", user.get("theme_mode") or "light")
            await page.push_route(routes.SUMMARY)
        else:
            error_text.value = "Email not recognised. Please try again."
            error_text.visible = True
            page.update()

    def on_login(_):
        asyncio.create_task(_do_login())

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
                                ft.Image(src=LOGO_SRC, width=56, height=56),
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
                                email_field,
                                password_field,
                                error_text,
                                ft.ElevatedButton(
                                    "Login  →",
                                    width=float("inf"),
                                    height=52,
                                    bgcolor=t.PRIMARY,
                                    color=t.ON_PRIMARY,
                                    elevation=0,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD),
                                        text_style=ft.TextStyle(
                                            size=15,
                                            weight=ft.FontWeight.W_600,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ),
                                    on_click=on_login,
                                ),
                                _divider_row(),
                                _oauth_button(
                                    "Google",
                                    "G",
                                    "#4285F4",
                                    lambda _: None,
                                    logo_src=GOOGLE_LOGO_SRC,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

import flet as ft
from my_flet_app import theme as t, routes


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


def _oauth_button(label: str, logo_char: str, logo_bg: str, on_click) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=t.SM + 2,
            controls=[
                ft.Container(
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
                ),
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

    def on_login(_):
        import asyncio
        asyncio.create_task(page.push_route(routes.SUMMARY))

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
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.SHIELD_OUTLINED,
                                        size=26,
                                        color=t.ON_SURFACE,
                                    ),
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    width=56,
                                    height=56,
                                    alignment=ft.Alignment(0, 0),
                                    shadow=ft.BoxShadow(
                                        blur_radius=16,
                                        color=t.with_alpha(t.PRIMARY_CONTAINER, 0.10),
                                        offset=ft.Offset(0, 4),
                                    ),
                                ),
                                ft.Text(
                                    "WealthShield",
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.LG),
                    # Headline
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
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
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        password_field,
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            controls=[
                                                ft.TextButton(
                                                    "Forgot Password?",
                                                    style=ft.ButtonStyle(
                                                        color=t.ON_SURFACE_VARIANT,
                                                        overlay_color=ft.Colors.TRANSPARENT,
                                                        text_style=ft.TextStyle(
                                                            size=13,
                                                            font_family=t.FONT_FAMILY,
                                                        ),
                                                        padding=ft.padding.symmetric(horizontal=0),
                                                    ),
                                                    on_click=lambda _: None,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
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
                                ),
                                _oauth_button(
                                    "Apple ID",
                                    "",
                                    t.PRIMARY,
                                    lambda _: None,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.LG),
                    # Sign-up link
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Don't have an account?  ",
                                size=14,
                                color=t.ON_SURFACE_VARIANT,
                                font_family=t.FONT_FAMILY,
                            ),
                            ft.TextButton(
                                "Sign Up",
                                style=ft.ButtonStyle(
                                    color=t.ON_SURFACE,
                                    overlay_color=ft.Colors.TRANSPARENT,
                                    padding=ft.padding.symmetric(horizontal=0),
                                    text_style=ft.TextStyle(
                                        size=14,
                                        weight=ft.FontWeight.W_700,
                                        font_family=t.FONT_FAMILY,
                                    ),
                                ),
                                on_click=lambda _: None,
                            ),
                        ],
                    ),
                    ft.Container(height=t.LG),
                    # Bottom "Precision Intelligence" branding peek
                    ft.Container(
                        height=72,
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        border_radius=ft.border_radius.only(
                            top_left=t.RADIUS_LG,
                            top_right=t.RADIUS_LG,
                        ),
                        bgcolor=t.SURFACE_CONTAINER,
                        padding=ft.padding.all(t.MD),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Precision Intelligence",
                                    size=12,
                                    color=t.ON_SURFACE_VARIANT,
                                    font_family=t.FONT_FAMILY,
                                ),
                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Container(
                                            width=5, height=5,
                                            bgcolor=t.OUTLINE_VARIANT,
                                            border_radius=t.RADIUS_FULL,
                                        )
                                        for _ in range(3)
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

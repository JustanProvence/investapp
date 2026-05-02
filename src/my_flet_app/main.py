import asyncio
import flet as ft
from my_flet_app import routes, theme as t
from my_flet_app import api_client
from my_flet_app.screens.login import login_view
from my_flet_app.screens.dashboard import dashboard_view
from my_flet_app.screens.asset_detail import asset_detail_view
from my_flet_app.screens.summary import summary_view
from my_flet_app.screens.analysis import analysis_view
from my_flet_app.screens.holdings import holdings_view, add_ticker_view, update_holding_view, ticker_detail_view


def _settings_view(page):
    import asyncio
    from my_flet_app.components.bottom_nav import build_nav_bar
    from my_flet_app.components.app_bar import build_app_bar

    def on_nav(e):
        dest = [routes.SUMMARY, routes.HOLDINGS, routes.SETTINGS]
        asyncio.create_task(page.push_route(dest[int(e.data)]))

    async def on_logout(_):
        page.session.store.remove("user")
        await page.push_route(routes.LOGIN)

    def on_theme_toggle(e):
        new_mode = "dark" if e.control.value else "light"
        page.session.store.set("theme_mode", new_mode)
        uid = (page.session.store.get("user") or {}).get("id", "")
        asyncio.create_task(api_client.set_theme_preference(new_mode, uid))
        page.go(routes.SETTINGS)

    user = page.session.store.get("user") or {}
    dark = (page.session.store.get("theme_mode") or "light") == "dark"

    return ft.View(
        route=routes.SETTINGS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(2, on_nav),
        controls=[
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                controls=[
                    build_app_bar(),
                    ft.Container(height=t.XL),
                    ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=48, color=t.OUTLINE),
                    ft.Container(height=t.SM),
                    ft.Text("Settings", size=20, weight=ft.FontWeight.W_600, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ft.Container(height=t.XS),
                    ft.Text(
                        f"Signed in as {user.get('name', '')} ({user.get('email', '')})",
                        size=13,
                        color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY,
                    ),
                    ft.Container(height=t.LG),
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM),
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        border_radius=t.RADIUS_MD,
                        border=ft.border.all(1, t.OUTLINE_VARIANT),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=t.SM,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE_OUTLINED, size=20, color=t.ON_SURFACE_VARIANT),
                                        ft.Text("Dark Mode", size=15, weight=ft.FontWeight.W_500,
                                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.Switch(
                                    value=dark,
                                    active_color=t.PRIMARY,
                                    on_change=on_theme_toggle,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=t.MD),
                    ft.Container(
                        margin=ft.margin.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.OutlinedButton(
                            "Logout",
                            icon=ft.Icons.LOGOUT,
                            width=float("inf"),
                            on_click=on_logout,
                            style=ft.ButtonStyle(
                                color="#D32F2F",
                                side=ft.BorderSide(1, "#D32F2F"),
                                shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD),
                                text_style=ft.TextStyle(
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    font_family=t.FONT_FAMILY,
                                ),
                            ),
                        ),
                    ),
                ],
            )
        ],
    )


def main(page: ft.Page):
    print(f"[DEBUG] main() called, route={page.route!r}", flush=True)
    page.title = "Market Research"
    page.bgcolor = t.BACKGROUND
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = t.build_theme()
    page.fonts = {t.FONT_FAMILY: t.MANROPE_URL}

    def route_change():
        print(f"[DEBUG] route_change() called, page.route={page.route!r}", flush=True)
        try:
            mode = page.session.store.get("theme_mode") or "light"
            t.set_mode(mode)
            page.theme = t.build_theme()
            page.theme_mode = ft.ThemeMode.DARK if mode == "dark" else ft.ThemeMode.LIGHT

            page.views.clear()
            r = page.route
            logged_in = bool(page.session.store.get("user"))

            # Auth guard — unauthenticated users always land on login
            if not logged_in and r not in (routes.LOGIN, "/"):
                page.go(routes.LOGIN)
                return

            if r in (routes.LOGIN, "/"):
                page.views.append(login_view(page))
            elif r == routes.SUMMARY or r == routes.DASHBOARD:
                page.views.append(summary_view(page))
            elif r == routes.ANALYSIS:
                page.views.append(analysis_view(page))
            elif r == routes.HOLDINGS:
                page.views.append(holdings_view(page))
            elif r == routes.HOLDINGS_ADD:
                page.views.append(add_ticker_view(page))
            elif r.startswith(routes.HOLDINGS_UPDATE + "/"):
                ticker_id = r.split("/")[-1]
                page.views.append(update_holding_view(page, ticker_id))
            elif r == routes.HOLDINGS_UPDATE:
                page.views.append(update_holding_view(page, ""))
            elif r.startswith(routes.HOLDINGS_TICKER + "/"):
                holding_id = r.split("/")[-1]
                page.views.append(ticker_detail_view(page, holding_id))
            elif r == routes.SETTINGS:
                page.views.append(_settings_view(page))
            elif r.startswith("/asset/"):
                asset_id = r.split("/")[-1]
                page.views.append(dashboard_view(page))
                page.views.append(asset_detail_view(page, asset_id))
            else:
                page.views.append(login_view(page))
            page.update()
        except Exception as e:
            import traceback
            traceback.print_exc()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550, web_renderer=ft.WebRenderer.CANVAS_KIT, no_cdn=True, assets_dir="my_flet_app/assets")

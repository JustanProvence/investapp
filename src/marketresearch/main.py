import asyncio
import flet as ft
from marketresearch import routes, theme as t
from marketresearch import api_client
from marketresearch.screens.login import login_view
from marketresearch.screens.dashboard import dashboard_view
from marketresearch.screens.asset_detail import asset_detail_view
from marketresearch.screens.summary import summary_view
from marketresearch.screens.holdings import holdings_view, add_ticker_view, update_holding_view, ticker_detail_view
from marketresearch.screens.watchlist import watchlist_view, add_watchlist_view, watchlist_ticker_view


def _settings_view(page):
    import asyncio
    from marketresearch.components.bottom_nav import build_nav_bar
    from marketresearch.components.app_bar import build_app_bar

    def on_nav(e):
        dest = [routes.SUMMARY, routes.HOLDINGS, routes.ANALYSIS, routes.SETTINGS]
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
        navigation_bar=build_nav_bar(3, on_nav),
        controls=[
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
                controls=[
                    build_app_bar(page),
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

            # OAuth callback — decode JWT, set session, redirect to summary
            if r.startswith("/auth/callback/"):
                import base64, json as _json
                jwt_token = r[len("/auth/callback/"):]
                try:
                    payload_b64 = jwt_token.split(".")[1]
                    payload_b64 += "=" * (4 - len(payload_b64) % 4)
                    payload = _json.loads(base64.urlsafe_b64decode(payload_b64))
                    user = {
                        "id":         payload["sub"],
                        "email":      payload["email"],
                        "name":       payload.get("name", ""),
                        "picture":    payload.get("picture", ""),
                        "theme_mode": payload.get("theme_mode", "light"),
                    }
                    page.session.store.set("user", user)
                    page.session.store.set("jwt_token", jwt_token)
                    page.session.store.set("theme_mode", user["theme_mode"])
                except Exception:
                    pass
                page.go(routes.SUMMARY)
                return

            # Auth guard — unauthenticated users always land on login
            if not logged_in and r not in (routes.LOGIN, "/"):
                page.go(routes.LOGIN)
                return

            if r in (routes.LOGIN, "/"):
                page.views.append(login_view(page))
            elif r == routes.SUMMARY or r == routes.DASHBOARD:
                page.views.append(summary_view(page))
            elif r == routes.ANALYSIS:
                page.views.append(watchlist_view(page))
            elif r == routes.ANALYSIS_ADD:
                page.views.append(add_watchlist_view(page))
            elif r.startswith(routes.ANALYSIS_TICKER + "/"):
                ticker_id = r.split("/")[-1]
                page.views.append(watchlist_ticker_view(page, ticker_id))
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
    import os as _os
    _assets = _os.path.join(_os.path.dirname(__file__), "assets")
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550, web_renderer=ft.WebRenderer.CANVAS_KIT, no_cdn=True, assets_dir=_assets)

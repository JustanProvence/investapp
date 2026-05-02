import asyncio
import flet as ft
from my_flet_app import routes, theme as t
from my_flet_app.screens.login import login_view
from my_flet_app.screens.dashboard import dashboard_view
from my_flet_app.screens.asset_detail import asset_detail_view
from my_flet_app.screens.summary import summary_view
from my_flet_app.screens.analysis import analysis_view
from my_flet_app.screens.holdings import holdings_view, add_ticker_view, update_holding_view, ticker_detail_view


def _settings_view(page):
    import asyncio
    from my_flet_app.components.bottom_nav import build_nav_bar
    def on_nav(e):
        dest = [routes.SUMMARY, routes.HOLDINGS, routes.SETTINGS]
        asyncio.create_task(page.push_route(dest[int(e.data)]))
    return ft.View(
        route=routes.SETTINGS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(2, on_nav),
        controls=[
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=48, color=t.OUTLINE),
                    ft.Container(height=t.SM),
                    ft.Text("Settings", size=20, weight=ft.FontWeight.W_600, color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ft.Text("Coming soon", size=14, color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                ],
            )
        ],
    )


def main(page: ft.Page):
    print(f"[DEBUG] main() called, route={page.route!r}", flush=True)
    page.title = "WealthShield"
    page.bgcolor = t.BACKGROUND
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = t.build_theme()
    page.fonts = {t.FONT_FAMILY: t.MANROPE_URL}

    def route_change():
        print(f"[DEBUG] route_change() called, page.route={page.route!r}", flush=True)
        try:
            page.views.clear()
            r = page.route
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
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550, web_renderer=ft.WebRenderer.CANVAS_KIT, no_cdn=True)

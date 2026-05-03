import asyncio
import flet as ft
from marketresearch import routes, theme as t, api_client
from marketresearch.components.bottom_nav import build_nav_bar
from marketresearch.components.app_bar import build_app_bar

_QUICK_CHIPS = ["OVL", "QQQI", "GPIQ", "O", "BTCI", "SGOV"]
_NAV_DEST    = [routes.SUMMARY, routes.HOLDINGS, routes.ANALYSIS, routes.SETTINGS]

_STATUS_MAP = {
    "good": (ft.Icons.CHECK_CIRCLE, t.GREEN,   t.GREEN_BG),
    "warn": (ft.Icons.WARNING,      t.AMBER,   t.AMBER_BG),
    "bad":  (ft.Icons.CANCEL,       t.CRIMSON, t.CRIMSON_BG),
}

_ACRONYMS = {
    "FCF":    "Free Cash Flow — cash remaining after capital expenditures",
    "OCF":    "Operating Cash Flow — cash generated from core business operations",
    "DPS":    "Dividends Per Share — total dividends paid divided by shares outstanding",
    "EPS":    "Earnings Per Share — net income divided by shares outstanding",
    "AUM":    "Assets Under Management — total market value of assets the fund manages",
    "YTD":    "Year to Date — performance since the start of the current calendar year",
    "CAGR":   "Compound Annual Growth Rate — annualised rate of growth over a period",
    "NAV":    "Net Asset Value — per-share value of a fund's assets minus liabilities",
}


def _acronym_tip(name: str) -> str | None:
    hits = [tip for key, tip in _ACRONYMS.items() if key in name]
    return "\n".join(hits) if hits else None


def _nav_handler(page):
    def handler(e):
        asyncio.create_task(page.push_route(_NAV_DEST[int(e.data)]))
    return handler


def _spinner() -> ft.Container:
    return ft.Container(
        padding=ft.padding.all(t.XL),
        alignment=ft.Alignment(0, 0),
        content=ft.ProgressRing(color=t.PRIMARY),
    )


def _metric_card(name: str, value: str, status: str, description: str) -> ft.Container:
    icon_name, color, bg = _STATUS_MAP[status]
    tip = _acronym_tip(name)
    return ft.Container(
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border_radius=t.RADIUS_LG,
        padding=ft.padding.all(t.MD),
        margin=ft.margin.only(bottom=t.SM),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=t.MD,
            controls=[
                ft.Container(
                    width=36, height=36, bgcolor=bg,
                    border_radius=t.RADIUS_FULL, alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon_name, size=18, color=color),
                ),
                ft.Column(
                    expand=True, spacing=4,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(name, size=14, weight=ft.FontWeight.W_600,
                                        color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
                                        tooltip=tip),
                                ft.Text(value, size=14, weight=ft.FontWeight.W_700,
                                        color=color, font_family=t.FONT_FAMILY),
                            ],
                        ),
                        ft.Text(description, size=12,
                                color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
                    ],
                ),
            ],
        ),
    )


# ── Holdings landing ──────────────────────────────────────────────────────────

def holdings_view(page: ft.Page) -> ft.View:
    cards_col = ft.Column(spacing=t.SM, controls=[_spinner()])

    def _make_card(h: dict) -> ft.Container:
        ticker     = h["ticker"]
        cost_basis = h.get("cost_basis") or 0
        price      = h.get("price") or 0
        shares     = h.get("shares") or 0
        market_val = h.get("market_value")
        div_yield  = h.get("dividend_yield")

        tr_pct   = ((price - cost_basis) / cost_basis * 100
                    if cost_basis > 0 and price > 0 else None)
        tr_color = t.GREEN if (tr_pct or 0) >= 0 else t.CRIMSON

        shares_str = (f"{shares:g} share" + ("s" if shares != 1 else "")
                      if shares else "—")
        val_str    = f"${market_val:,.2f}" if market_val else "—"
        cost_str   = f"${cost_basis:,.2f}/sh" if cost_basis else "—"
        tr_str     = f"{tr_pct:+.1f}%" if tr_pct is not None else "—"
        dist_str   = f"{div_yield:.2f}%" if div_yield else "—"

        def _stat_col(label, val, color=None):
            return ft.Column(
                expand=True, spacing=2,
                controls=[
                    ft.Text(label, size=10, weight=ft.FontWeight.W_600,
                            color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY,
                            style=ft.TextStyle(letter_spacing=0.5)),
                    ft.Text(val, size=12, weight=ft.FontWeight.W_700,
                            color=color or t.ON_SURFACE, font_family=t.FONT_FAMILY),
                ],
            )

        card: list[ft.Container] = [None]

        async def _delete(_):
            uid = (page.session.store.get("user") or {}).get("id", "")
            ok = await api_client.delete_holding(ticker, uid)
            if ok and card[0] in cards_col.controls:
                cards_col.controls.remove(card[0])
                page.update()

        card[0] = ft.Container(
            bgcolor=t.SURFACE_CONTAINER_LOWEST,
            border_radius=t.RADIUS_LG,
            border=ft.border.all(1, t.OUTLINE_VARIANT),
            padding=ft.padding.all(t.MD),
            on_click=lambda _, tk=ticker: asyncio.create_task(
                page.push_route(routes.ticker(tk))
            ),
            ink=True,
            content=ft.Column(
                spacing=t.SM,
                controls=[
                    # ── Identity row ──────────────────────────────────────────
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=t.MD, expand=True,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        width=40, height=40,
                                        bgcolor=t.PRIMARY_CONTAINER,
                                        border_radius=t.RADIUS_MD,
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Text(
                                            ticker[:2], size=13,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_PRIMARY_CONTAINER,
                                            font_family=t.FONT_FAMILY,
                                        ),
                                    ),
                                    ft.Column(
                                        spacing=2, expand=True,
                                        controls=[
                                            ft.Text(ticker, size=15,
                                                    weight=ft.FontWeight.W_700,
                                                    color=t.ON_SURFACE,
                                                    font_family=t.FONT_FAMILY),
                                            ft.Text(h.get("name", ""), size=12,
                                                    color=t.ON_SURFACE_VARIANT,
                                                    font_family=t.FONT_FAMILY,
                                                    overflow=ft.TextOverflow.ELLIPSIS,
                                                    max_lines=1),
                                            ft.Text(shares_str, size=11,
                                                    color=t.ON_SURFACE_VARIANT,
                                                    font_family=t.FONT_FAMILY),
                                        ],
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=t.XS,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(val_str, size=14,
                                            weight=ft.FontWeight.W_700,
                                            color=t.ON_SURFACE,
                                            font_family=t.FONT_FAMILY),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=t.CRIMSON, icon_size=18,
                                        tooltip="Remove holding",
                                        on_click=_delete,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # ── Stats strip ───────────────────────────────────────────
                    ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                    ft.Row(
                        controls=[
                            _stat_col("COST BASIS", cost_str),
                            ft.VerticalDivider(width=1, color=t.OUTLINE_VARIANT),
                            _stat_col("TOTAL RETURN", tr_str, tr_color),
                            ft.VerticalDivider(width=1, color=t.OUTLINE_VARIANT),
                            _stat_col("DISTRIBUTION",
                                      dist_str,
                                      t.GREEN if div_yield else None),
                        ],
                    ),
                ],
            ),
        )
        return card[0]

    async def load():
        uid     = (page.session.store.get("user") or {}).get("id", "")
        summary = await api_client.get_portfolio_summary(uid)
        if not summary or not summary.get("holdings"):
            cards_col.controls = [ft.Container(
                padding=ft.padding.all(t.LG),
                alignment=ft.Alignment(0, 0),
                content=ft.Text(
                    "No holdings yet. Tap Add Ticker to get started.",
                    color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY,
                ),
            )]
        else:
            cards_col.controls = [_make_card(h) for h in summary["holdings"]]
        page.update()

    asyncio.create_task(load())

    return ft.View(
        route=routes.HOLDINGS,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(1, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    build_app_bar(page),
                    ft.Container(
                        padding=ft.padding.only(
                            left=t.CONTAINER_MARGIN, right=t.CONTAINER_MARGIN,
                            top=t.MD, bottom=t.MD,
                        ),
                        content=ft.Text("Holdings", size=26,
                                        weight=ft.FontWeight.W_700,
                                        color=t.ON_SURFACE,
                                        font_family=t.FONT_FAMILY),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Container(
                            height=48, border_radius=t.RADIUS_MD,
                            border=ft.border.all(1.5, t.PRIMARY),
                            alignment=ft.Alignment(0, 0),
                            on_click=lambda _: asyncio.create_task(
                                page.push_route(routes.HOLDINGS_ADD)
                            ),
                            ink=True,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=t.SM,
                                controls=[
                                    ft.Icon(ft.Icons.ADD, color=t.PRIMARY, size=18),
                                    ft.Text("Add Ticker", color=t.PRIMARY, size=14,
                                            weight=ft.FontWeight.W_600,
                                            font_family=t.FONT_FAMILY),
                                ],
                            ),
                        ),
                    ),
                    ft.Container(height=t.MD),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=cards_col,
                    ),
                    ft.Container(height=t.LG),
                ],
            ),
        ],
    )


# ── Ticker detail (health report) ─────────────────────────────────────────────

def ticker_detail_view(page: ft.Page, holding_id: str) -> ft.View:
    ticker = holding_id.upper()

    heading_col  = ft.Column(spacing=t.XS, controls=[_spinner()])
    metrics_col  = ft.Column(spacing=0, controls=[])

    def go_back(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS))

    def go_update(_):
        asyncio.create_task(page.push_route(routes.holding_update(ticker)))

    app_bar = ft.Container(
        padding=ft.padding.symmetric(horizontal=t.SM, vertical=t.MD),
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=t.XS,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color=t.ON_SURFACE,
                                      icon_size=22, on_click=go_back),
                        ft.Text(ticker, size=18, weight=ft.FontWeight.W_700,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ],
                ),
                ft.Container(
                    height=38, border_radius=t.RADIUS_MD, bgcolor=t.PRIMARY,
                    padding=ft.padding.symmetric(horizontal=t.MD),
                    alignment=ft.Alignment(0, 0),
                    on_click=go_update, ink=True,
                    content=ft.Row(
                        spacing=t.XS,
                        controls=[
                            ft.Icon(ft.Icons.EDIT_OUTLINED, color=t.ON_PRIMARY, size=16),
                            ft.Text("Update", color=t.ON_PRIMARY, size=13,
                                    weight=ft.FontWeight.W_600,
                                    font_family=t.FONT_FAMILY),
                        ],
                    ),
                ),
            ],
        ),
    )

    async def load():
        quote, metrics_data = await asyncio.gather(
            api_client.get_quote(ticker),
            api_client.get_metrics(ticker),
        )
        metrics       = metrics_data.get("metrics", [])
        issuer_ticker = metrics_data.get("issuer_ticker")

        if quote:
            chg = quote.get("change_pct") or 0
            price_color = t.GREEN if chg >= 0 else t.CRIMSON
            heading_col.controls = [
                ft.Text(
                    quote.get("name", ticker), size=26,
                    weight=ft.FontWeight.W_700, color=t.ON_SURFACE,
                    font_family=t.FONT_FAMILY,
                    style=ft.TextStyle(letter_spacing=-0.5),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            f"{quote.get('exchange', '')}: {ticker}",
                            size=13, color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY,
                        ),
                        ft.Text(
                            f"${quote.get('price', 0):.2f} / {chg:+.2f}%",
                            size=13, color=price_color,
                            weight=ft.FontWeight.W_600,
                            font_family=t.FONT_FAMILY,
                        ),
                    ],
                ),
                ft.Container(height=t.XS),
                ft.Text(
                    "Market Research Health Analysis: Based on trailing data "
                    "and current valuation metrics.",
                    size=12, color=t.ON_SURFACE_VARIANT,
                    font_family=t.FONT_FAMILY,
                ),
            ]
            if issuer_ticker:
                heading_col.controls.append(
                    ft.Container(
                        bgcolor=t.AMBER_BG,
                        border_radius=t.RADIUS_MD,
                        padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM),
                        margin=ft.margin.only(top=t.SM),
                        content=ft.Row(
                            spacing=t.SM,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=t.AMBER),
                                ft.Text(
                                    f"Preferred stock — Debt/Equity and Interest Coverage "
                                    f"metrics are sourced from the issuer ({issuer_ticker}).",
                                    size=12, color=t.ON_SURFACE,
                                    font_family=t.FONT_FAMILY, expand=True,
                                ),
                            ],
                        ),
                    )
                )

        if metrics:
            metrics_col.controls = [
                _metric_card(m["name"], m["value"], m["status"], m["description"])
                for m in metrics
            ]

        page.update()

    asyncio.create_task(load())

    return ft.View(
        route=routes.ticker(holding_id),
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(1, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    app_bar,
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN, vertical=t.MD,
                        ),
                        content=heading_col,
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=metrics_col,
                    ),
                    ft.Container(height=t.MD),
                ],
            ),
        ],
    )


# ── Add Ticker ────────────────────────────────────────────────────────────────

def add_ticker_view(page: ft.Page) -> ft.View:
    prefill_ticker  = page.session.store.get("holdings_prefill_ticker") or ""
    from_watchlist  = bool(page.session.store.get("holdings_from_watchlist"))
    if prefill_ticker:
        page.session.store.remove("holdings_prefill_ticker")
    if from_watchlist:
        page.session.store.remove("holdings_from_watchlist")

    selected_ticker = [None]
    chip_containers: list[ft.Container] = []

    # Asset card — mutable text widgets updated on chip/search select
    asset_status_text  = ft.Text("Search for an asset above", size=11,
                                  weight=ft.FontWeight.W_700,
                                  color=t.ON_SURFACE_VARIANT,
                                  font_family=t.FONT_FAMILY)
    asset_name_text    = ft.Text("—", size=18, weight=ft.FontWeight.W_700,
                                  color=t.ON_SURFACE, font_family=t.FONT_FAMILY)
    asset_sub_text     = ft.Text("", size=13, color=t.ON_SURFACE_VARIANT,
                                  font_family=t.FONT_FAMILY)
    asset_price_text   = ft.Text("", size=13, color=t.ON_SURFACE_VARIANT,
                                  font_family=t.FONT_FAMILY)
    asset_change_text  = ft.Text("", size=13, weight=ft.FontWeight.W_600,
                                  color=t.GREEN, font_family=t.FONT_FAMILY)
    asset_progress_bar = ft.ProgressBar(value=0, bgcolor=t.OUTLINE_VARIANT,
                                         color=t.GREEN, height=6)

    shares_field = ft.TextField(
        hint_text="0.00",
        border_color=t.OUTLINE_VARIANT, focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD, border_width=1, focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    cost_field = ft.TextField(
        prefix=ft.Text("$ ", size=14, color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY),
        hint_text="0.00",
        border_color=t.OUTLINE_VARIANT, focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD, border_width=1, focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    # Autocomplete dropdown
    suggestions_col = ft.Column(spacing=0, controls=[])
    suggestions_box = ft.Container(
        visible=False,
        bgcolor=t.SURFACE_CONTAINER_LOWEST,
        border=ft.border.all(1, t.OUTLINE_VARIANT),
        border_radius=t.RADIUS_MD,
        shadow=ft.BoxShadow(blur_radius=12,
                            color=t.with_alpha(t.ON_SURFACE, 0.10),
                            offset=ft.Offset(0, 4)),
        content=suggestions_col,
    )

    _pending_search: list = [None]

    search_field = ft.TextField(
        hint_text="Search by symbol or company name",
        prefix_icon=ft.Icons.SEARCH,
        border_color=t.OUTLINE_VARIANT,
        focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_FULL,
        border_width=1, focused_border_width=2,
        bgcolor=t.SURFACE_CONTAINER_LOW, filled=True,
        fill_color=t.SURFACE_CONTAINER_LOW,
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY, size=13),
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=13, color=t.ON_SURFACE),
        on_submit=lambda e: asyncio.create_task(_select_ticker(e.control.value)) if e.control.value.strip() else None,
    )

    error_text = ft.Text(
        "", size=13, color=t.CRIMSON,
        font_family=t.FONT_FAMILY, visible=False,
    )

    async def _select_ticker(label: str):
        label = label.strip().upper()
        if not label:
            return
        selected_ticker[0] = label
        search_field.value = label
        suggestions_box.visible = False
        error_text.visible = False
        for i, chip_label in enumerate(_QUICK_CHIPS):
            is_sel = chip_label == label
            chip_containers[i].border = ft.border.all(
                1, t.PRIMARY if is_sel else t.OUTLINE_VARIANT)
            chip_containers[i].bgcolor = t.PRIMARY if is_sel else t.SURFACE_CONTAINER_LOWEST
            chip_containers[i].content.color = t.ON_PRIMARY if is_sel else t.ON_SURFACE
        asset_status_text.value = f"Loading {label}…"
        asset_status_text.color = t.ON_SURFACE_VARIANT
        page.update()

        quote = await api_client.get_quote(label)
        if quote:
            chg = quote.get("change_pct") or 0
            asset_status_text.value = "Verified"
            asset_status_text.color = t.GREEN
            asset_name_text.value   = quote.get("name", label)
            asset_sub_text.value    = f"Ticker: {label} • {quote.get('exchange', '')}"
            asset_price_text.value  = f"Market Price / ${quote.get('price', 0):.2f}"
            asset_change_text.value = f"{chg:+.2f}%"
            asset_change_text.color = t.GREEN if chg >= 0 else t.CRIMSON
            asset_progress_bar.value = min(max((chg + 5) / 10, 0), 1)
        else:
            asset_status_text.value = f"'{label}' not found — check the symbol"
            asset_status_text.color = t.CRIMSON
            asset_name_text.value   = "—"
            asset_sub_text.value    = ""
            asset_price_text.value  = ""
            asset_change_text.value = ""
            selected_ticker[0] = None
        page.update()

    def _make_suggestion(symbol: str, name: str) -> ft.Container:
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM + 2),
            on_click=lambda _, s=symbol: asyncio.create_task(_select_ticker(s)),
            ink=True,
            content=ft.Row(
                spacing=t.SM,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(symbol, size=13, weight=ft.FontWeight.W_700,
                            color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
                            width=52),
                    ft.Text(name, size=12, color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY, expand=True,
                            overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                ],
            ),
        )

    def _on_search_change(e):
        query = e.control.value.strip()
        if _pending_search[0]:
            _pending_search[0].cancel()
        if not query:
            suggestions_box.visible = False
            page.update()
            return

        async def _debounced():
            await asyncio.sleep(0.35)
            results = await api_client.search_tickers(query)
            if not results:
                suggestions_box.visible = False
            else:
                suggestions_col.controls = [
                    _make_suggestion(r["symbol"], r["name"]) for r in results
                ]
                suggestions_box.visible = True
            page.update()

        _pending_search[0] = asyncio.create_task(_debounced())

    search_field.on_change = _on_search_change

    def _make_chip(label: str) -> ft.Container:
        return ft.Container(
            content=ft.Text(label, size=13, weight=ft.FontWeight.W_600,
                             color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
            border=ft.border.all(1, t.OUTLINE_VARIANT),
            border_radius=t.RADIUS_FULL,
            bgcolor=t.SURFACE_CONTAINER_LOWEST,
            padding=ft.padding.symmetric(horizontal=t.MD, vertical=t.SM),
            on_click=lambda _, lbl=label: asyncio.create_task(_select_ticker(lbl)),
            ink=True,
        )

    for label in _QUICK_CHIPS:
        chip_containers.append(_make_chip(label))

    async def go_back(_):
        await page.push_route(routes.ANALYSIS if from_watchlist else routes.HOLDINGS)

    async def on_save(_):
        await _do_save()

    async def _do_save():
        # If the user typed a symbol but didn't press Enter, resolve it now
        typed = search_field.value.strip().upper()
        ticker = selected_ticker[0] or typed
        if not ticker:
            error_text.value = "Please select or search for a ticker first."
            error_text.visible = True
            page.update()
            return
        # If typed but never verified, verify now before saving
        if ticker != selected_ticker[0]:
            await _select_ticker(ticker)
            if selected_ticker[0] != ticker:
                return  # invalid ticker — error already shown

        try:
            shares = float(shares_field.value or "0")
            cost   = float(cost_field.value or "0")
        except ValueError:
            error_text.value = "Shares and cost must be numbers."
            error_text.visible = True
            page.update()
            return

        uid    = (page.session.store.get("user") or {}).get("id", "")
        result = await api_client.add_holding(ticker, shares, cost, uid)
        if result:
            if from_watchlist:
                await api_client.delete_watchlist_item(ticker, uid)
                await page.push_route(routes.ANALYSIS)
            else:
                await page.push_route(routes.HOLDINGS)
        else:
            error_text.value = f"{ticker} already exists. Use Update to change it."
            error_text.visible = True
            page.update()

    if prefill_ticker:
        asyncio.create_task(_select_ticker(prefill_ticker))

    return ft.View(
        route=routes.HOLDINGS_ADD,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(1, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.SM, vertical=t.MD),
                        bgcolor=t.SURFACE_CONTAINER_LOWEST,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=t.XS,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(ft.Icons.ARROW_BACK,
                                                      icon_color=t.ON_SURFACE,
                                                      icon_size=22, on_click=go_back),
                                        ft.Text("Add Ticker", size=16,
                                                weight=ft.FontWeight.W_700,
                                                color=t.ON_SURFACE,
                                                font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.IconButton(ft.Icons.HELP_OUTLINE,
                                              icon_color=t.ON_SURFACE_VARIANT,
                                              icon_size=22,
                                              on_click=lambda _: None),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.all(t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                ft.Text("FIND ASSET", size=11,
                                        weight=ft.FontWeight.W_700,
                                        color=t.ON_SURFACE_VARIANT,
                                        font_family=t.FONT_FAMILY,
                                        style=ft.TextStyle(letter_spacing=1.2)),
                                ft.Row(
                                    spacing=t.SM,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(content=search_field, expand=True),
                                        ft.Container(
                                            height=48,
                                            bgcolor=t.PRIMARY,
                                            border_radius=t.RADIUS_FULL,
                                            padding=ft.padding.symmetric(horizontal=t.MD),
                                            alignment=ft.Alignment(0, 0),
                                            on_click=lambda _: asyncio.create_task(
                                                _select_ticker(search_field.value)
                                            ),
                                            ink=True,
                                            content=ft.Text(
                                                "Look up",
                                                size=13,
                                                weight=ft.FontWeight.W_600,
                                                color=t.ON_PRIMARY,
                                                font_family=t.FONT_FAMILY,
                                            ),
                                        ),
                                    ],
                                ),
                                suggestions_box,
                                ft.Row(spacing=t.SM, controls=chip_containers),
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Stack(
                                        controls=[
                                            ft.Column(
                                                spacing=t.SM,
                                                controls=[
                                                    asset_status_text,
                                                    asset_name_text,
                                                    asset_sub_text,
                                                    ft.Column(
                                                        spacing=t.XS,
                                                        controls=[
                                                            ft.Row(
                                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                                controls=[
                                                                    asset_price_text,
                                                                    asset_change_text,
                                                                ],
                                                            ),
                                                            asset_progress_bar,
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            ft.Container(
                                                right=0, top=0, width=36, height=36,
                                                bgcolor=t.PRIMARY_CONTAINER,
                                                border_radius=t.RADIUS_MD,
                                                alignment=ft.Alignment(0, 0),
                                                content=ft.Icon(ft.Icons.SHIELD_OUTLINED,
                                                                size=18,
                                                                color=t.ON_PRIMARY_CONTAINER),
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Enter Details", size=16,
                                                weight=ft.FontWeight.W_700,
                                                color=t.ON_SURFACE,
                                                font_family=t.FONT_FAMILY),
                                        ft.Text(
                                            "Specify your position to track "
                                            "performance metrics automatically.",
                                            size=13, color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Column(
                                        spacing=t.MD,
                                        controls=[
                                            ft.Column(
                                                spacing=t.XS,
                                                controls=[
                                                    ft.Text("Number of Shares (Optional)",
                                                            size=12,
                                                            color=t.ON_SURFACE_VARIANT,
                                                            font_family=t.FONT_FAMILY),
                                                    shares_field,
                                                ],
                                            ),
                                            ft.Column(
                                                spacing=t.XS,
                                                controls=[
                                                    ft.Text("Average Cost Basis", size=12,
                                                            color=t.ON_SURFACE_VARIANT,
                                                            font_family=t.FONT_FAMILY),
                                                    cost_field,
                                                ],
                                            ),
                                            error_text,
                                            ft.ElevatedButton(
                                                content=ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    spacing=t.SM,
                                                    controls=[
                                                        ft.Icon(ft.Icons.SAVE_OUTLINED,
                                                                color=t.ON_PRIMARY, size=18),
                                                        ft.Text("Save Ticker",
                                                                color=t.ON_PRIMARY, size=14,
                                                                weight=ft.FontWeight.W_600,
                                                                font_family=t.FONT_FAMILY),
                                                    ],
                                                ),
                                                width=float("inf"), height=52,
                                                bgcolor=t.PRIMARY, elevation=0,
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(
                                                        radius=t.RADIUS_MD),
                                                ),
                                                on_click=on_save,
                                            ),
                                            ft.Text(
                                                "Positions are encrypted and private to you.",
                                                size=12, color=t.ON_SURFACE_VARIANT,
                                                font_family=t.FONT_FAMILY,
                                                text_align=ft.TextAlign.CENTER),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    content=ft.Row(
                                        spacing=t.MD,
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        controls=[
                                            ft.Icon(ft.Icons.INFO_OUTLINE, size=20,
                                                    color=t.ON_SURFACE_VARIANT),
                                            ft.Text(
                                                "Market Research uses real-time market data "
                                                "to calculate your portfolio's health score "
                                                "and defensive rating.",
                                                size=12, color=t.ON_SURFACE_VARIANT,
                                                font_family=t.FONT_FAMILY, expand=True),
                                        ],
                                    ),
                                ),
                                ft.Container(height=t.SM),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


# ── Update Holding ────────────────────────────────────────────────────────────

def update_holding_view(page: ft.Page, ticker: str = "") -> ft.View:
    ticker = ticker.upper()

    def go_back(_):
        asyncio.create_task(page.push_route(routes.HOLDINGS))

    header_text = ft.Text(
        f"Update {ticker}" if ticker else "Update Holding",
        size=16, weight=ft.FontWeight.W_700,
        color=t.ON_SURFACE, font_family=t.FONT_FAMILY,
    )

    shares_field = ft.TextField(
        hint_text="0.00",
        suffix=ft.Text("SHARES", size=12, weight=ft.FontWeight.W_600,
                        color=t.ON_SURFACE_VARIANT, font_family=t.FONT_FAMILY),
        border_color=t.OUTLINE_VARIANT, focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD, border_width=1, focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    cost_field = ft.TextField(
        prefix=ft.Text("$ ", size=14, color=t.ON_SURFACE_VARIANT,
                        font_family=t.FONT_FAMILY),
        hint_text="0.00",
        border_color=t.OUTLINE_VARIANT, focused_border_color=t.PRIMARY,
        border_radius=t.RADIUS_MD, border_width=1, focused_border_width=2,
        text_style=ft.TextStyle(font_family=t.FONT_FAMILY, size=14, color=t.ON_SURFACE),
        hint_style=ft.TextStyle(color=t.OUTLINE, font_family=t.FONT_FAMILY),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    stock_name_text  = ft.Text("—", size=28, weight=ft.FontWeight.W_700,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY)
    stock_sub_text   = ft.Text("", size=13, color=t.ON_SURFACE_VARIANT,
                                font_family=t.FONT_FAMILY)
    alloc_text       = ft.Text("—", size=13, weight=ft.FontWeight.W_600,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY)
    shares_info_text = ft.Text("—", size=22, weight=ft.FontWeight.W_700,
                                color=t.ON_SURFACE, font_family=t.FONT_FAMILY)

    async def prefill():
        uid     = (page.session.store.get("user") or {}).get("id", "")
        holding = await api_client.get_holdings(uid)
        match = next((h for h in holding if h["ticker"] == ticker), None)
        if match:
            shares_field.value = str(match["shares"])
            cost_field.value   = str(match["cost_basis"])
            shares_info_text.value = str(match["shares"])
        summary = await api_client.get_portfolio_summary(uid)
        if summary:
            h = next((h for h in summary["holdings"] if h["ticker"] == ticker), None)
            if h:
                stock_name_text.value = h.get("name", ticker)
                stock_sub_text.value  = ticker
                alloc_text.value      = f"{h.get('allocation_pct', 0):.1f}%"
        page.update()

    if ticker:
        asyncio.create_task(prefill())

    def on_confirm(_):
        asyncio.create_task(_do_confirm())

    async def _do_confirm():
        try:
            shares = float(shares_field.value or "0")
            cost   = float(cost_field.value or "0")
        except ValueError:
            return
        uid    = (page.session.store.get("user") or {}).get("id", "")
        result = await api_client.update_holding(ticker, shares, cost, uid)
        if result:
            await page.push_route(routes.ticker(ticker))

    def _event_card(icon, label, subtitle):
        return ft.Container(
            width=float("inf"),
            bgcolor=t.SURFACE_CONTAINER_LOWEST,
            border_radius=t.RADIUS_LG,
            padding=ft.padding.all(t.MD),
            shadow=ft.BoxShadow(blur_radius=8,
                                color=t.with_alpha(t.PRIMARY_CONTAINER, 0.05),
                                offset=ft.Offset(0, 2)),
            content=ft.Column(
                spacing=t.XS,
                controls=[
                    ft.Container(
                        width=32, height=32,
                        border_radius=t.RADIUS_FULL,
                        border=ft.border.all(1.5, t.ON_SURFACE),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon, size=16, color=t.ON_SURFACE),
                    ),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600,
                            color=t.ON_SURFACE, font_family=t.FONT_FAMILY),
                    ft.Text(subtitle, size=11, color=t.ON_SURFACE_VARIANT,
                            font_family=t.FONT_FAMILY),
                ],
            ),
        )

    return ft.View(
        route=routes.holding_update(ticker) if ticker else routes.HOLDINGS_UPDATE,
        bgcolor=t.BACKGROUND,
        padding=0,
        navigation_bar=build_nav_bar(1, _nav_handler(page)),
        controls=[
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=t.CONTAINER_MARGIN, vertical=t.MD,
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    spacing=t.XS,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(ft.Icons.ARROW_BACK,
                                                      icon_color=t.ON_SURFACE,
                                                      icon_size=22, on_click=go_back),
                                        header_text,
                                    ],
                                ),
                                ft.Text("Market Research", size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=t.ON_SURFACE,
                                        font_family=t.FONT_FAMILY),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=t.CONTAINER_MARGIN),
                        content=ft.Column(
                            spacing=t.MD,
                            controls=[
                                ft.Container(
                                    bgcolor=t.SURFACE_CONTAINER_LOWEST,
                                    border_radius=t.RADIUS_LG,
                                    padding=ft.padding.all(t.MD),
                                    shadow=ft.BoxShadow(
                                        blur_radius=12,
                                        color=t.with_alpha(t.PRIMARY_CONTAINER, 0.06),
                                        offset=ft.Offset(0, 4),
                                    ),
                                    content=ft.Column(
                                        spacing=t.SM,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                vertical_alignment=ft.CrossAxisAlignment.START,
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Row(
                                                            spacing=t.XS,
                                                            controls=[
                                                                ft.Icon(ft.Icons.VERIFIED_OUTLINED,
                                                                        size=13, color=t.GREEN),
                                                                ft.Text("PORTFOLIO CORE", size=11,
                                                                        weight=ft.FontWeight.W_700,
                                                                        color=t.GREEN,
                                                                        font_family=t.FONT_FAMILY),
                                                            ],
                                                        ),
                                                        bgcolor=t.GREEN_BG,
                                                        border_radius=t.RADIUS_FULL,
                                                        padding=ft.padding.symmetric(
                                                            horizontal=t.SM, vertical=3),
                                                    ),
                                                    ft.Column(
                                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text("CURRENT POSITION", size=10,
                                                                    color=t.ON_SURFACE_VARIANT,
                                                                    font_family=t.FONT_FAMILY),
                                                            ft.Row(
                                                                spacing=4,
                                                                vertical_alignment=ft.CrossAxisAlignment.END,
                                                                controls=[
                                                                    shares_info_text,
                                                                    ft.Text("shares", size=12,
                                                                            color=t.ON_SURFACE_VARIANT,
                                                                            font_family=t.FONT_FAMILY),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            stock_name_text,
                                            stock_sub_text,
                                            ft.Divider(height=1, color=t.OUTLINE_VARIANT),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Allocation", size=13,
                                                            color=t.ON_SURFACE_VARIANT,
                                                            font_family=t.FONT_FAMILY),
                                                    alloc_text,
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Number of Shares", size=16,
                                                weight=ft.FontWeight.W_700,
                                                color=t.ON_SURFACE,
                                                font_family=t.FONT_FAMILY),
                                        shares_field,
                                        ft.Text(
                                            "Enter the total updated balance for this ticker.",
                                            size=12, color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.Column(
                                    spacing=t.XS,
                                    controls=[
                                        ft.Text("Average Cost Basis", size=16,
                                                weight=ft.FontWeight.W_700,
                                                color=t.ON_SURFACE,
                                                font_family=t.FONT_FAMILY),
                                        cost_field,
                                        ft.Text(
                                            "Adjust your original purchase price to "
                                            "recalculate unrealized gains.",
                                            size=12, color=t.ON_SURFACE_VARIANT,
                                            font_family=t.FONT_FAMILY),
                                    ],
                                ),
                                ft.Row(
                                    spacing=t.MD,
                                    controls=[
                                        _event_card(ft.Icons.ADD, "Buy Event",
                                                    "Log new purchase"),
                                        _event_card(ft.Icons.REMOVE, "Sell Event",
                                                    "Log position reduction"),
                                    ],
                                ),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=t.SM,
                                        controls=[
                                            ft.Text("Confirm Update", color=t.ON_PRIMARY,
                                                    size=15, weight=ft.FontWeight.W_600,
                                                    font_family=t.FONT_FAMILY),
                                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE,
                                                    color=t.ON_PRIMARY, size=18),
                                        ],
                                    ),
                                    width=float("inf"), height=52,
                                    bgcolor=t.PRIMARY, elevation=0,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=t.RADIUS_MD),
                                    ),
                                    on_click=on_confirm,
                                ),
                                ft.Container(
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.TextButton(
                                        "Cancel and Return",
                                        style=ft.ButtonStyle(
                                            color=t.ON_SURFACE_VARIANT,
                                            overlay_color=ft.Colors.TRANSPARENT,
                                            text_style=ft.TextStyle(
                                                size=13, font_family=t.FONT_FAMILY),
                                        ),
                                        on_click=go_back,
                                    ),
                                ),
                                ft.Container(height=t.SM),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

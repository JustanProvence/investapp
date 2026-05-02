import flet as ft
from my_flet_app import theme as t

_DESTINATIONS = [
    ("Summary",  ft.Icons.DASHBOARD_OUTLINED,              ft.Icons.DASHBOARD),
    ("Holdings", ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, ft.Icons.ACCOUNT_BALANCE_WALLET),
    ("Settings", ft.Icons.SETTINGS_OUTLINED,               ft.Icons.SETTINGS),
]


def build_nav_bar(selected_index: int, on_change) -> ft.NavigationBar:
    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=on_change,
        bgcolor=t.with_alpha(t.SURFACE_CONTAINER_LOWEST, 0.95),

        indicator_color=t.SURFACE_CONTAINER_HIGH,
        destinations=[
            ft.NavigationBarDestination(
                icon=icon,
                selected_icon=selected_icon,
                label=label,
            )
            for label, icon, selected_icon in _DESTINATIONS
        ],
    )

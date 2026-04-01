import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.on_error = lambda e: print("Page error:", e.data)

    solitaire = Solitaire()
    
    restart_button = ft.Button(
        content=ft.Text("Restart Game"),
        icon=ft.Icons.RESTART_ALT,
        on_click=solitaire.restart_game
    )

    page.add(solitaire, restart_button)


ft.run(main, assets_dir="assets")

import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.on_error = lambda e: print("Page error:", e.data)

    solitaire = Solitaire()
    
    restart_button = ft.Button(
        content=ft.Text("Restart Game"),
        icon=ft.Icons.RESTART_ALT,
        on_click=solitaire.restart_game,
    )
    
    undo_button = ft.Button(
        content=ft.Text("Undo Move"),
        icon=ft.Icons.UNDO,
        on_click=solitaire.undo_move
    )
    
    save_button = ft.Button(
        content=ft.Text("Save Game"),
        icon=ft.Icons.SAVE,
        on_click=solitaire.save_game
    )
    
    load_button = ft.Button(
        content=ft.Text("Load Game"),
        icon=ft.Icons.CLOUD_UPLOAD,
        on_click=solitaire.load_game
    )

    page.add(ft.Row([restart_button, undo_button, save_button, load_button]), solitaire)


ft.run(main, assets_dir="assets")

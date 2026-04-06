import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.on_error = lambda e: print("Page error:", e.data)
    page.adaptive = True
    solitaire = Solitaire()
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.CASINO),
        leading_width=40,
        title=ft.Text("Solitaire"),
        center_title=False,
        actions=[
            ft.IconButton(ft.Icons.RESTART_ALT, on_click=solitaire.restart_game, tooltip="Restart"),
            ft.IconButton(ft.Icons.UNDO, on_click=solitaire.undo_move, tooltip="Undo"),
            ft.IconButton(ft.Icons.LIGHTBULB, on_click=solitaire.give_hint, tooltip="Hint"),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content=ft.Text("Save Game"), icon=ft.Icons.SAVE, on_click=solitaire.save_game),
                    ft.PopupMenuItem(content=ft.Text("Load Game"), icon=ft.Icons.CLOUD_UPLOAD, on_click=solitaire.open_save_menu),
                    ft.PopupMenuItem(content=ft.Text("Card Style"), icon=ft.Icons.DESIGN_SERVICES, on_click=solitaire.open_deck_menu),
                    ft.PopupMenuItem(content=ft.Text("Game Rules"), icon=ft.Icons.BOOK, on_click=solitaire.show_rules),
                ]
            ),
        ],
    )
    stats_row = ft.Row(
        [solitaire.score_text, solitaire.timer_text, solitaire.moves_text],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    page.add(stats_row, solitaire)


ft.run(main, assets_dir="assets")

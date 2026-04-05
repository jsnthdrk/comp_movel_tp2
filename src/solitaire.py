SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import asyncio
import random

import flet as ft
from card import Card, CARD_OFFSET
from slot import Slot
import json
import datetime


class Suite:
    def __init__(self, suite_name, suite_color):
        """skeleton of our class"""
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        """skeleton of our class"""
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self):
        """skeleton of our class"""
        super().__init__()
        self.controls = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        self.history = [] # for the undo functionality, will function as a stack of moves to iterate from when undoing
        self.current_save_name = None
        self.current_card_back = "/images/card0.png"
        
        # components regarding timer and scoring
        self.score = 0
        self.timer_seconds = 0
        self.is_timer_running = False
        self.score_text = ft.Text("Score: 0", size=18, weight="bold")
        self.timer_text = ft.Text("Time: 00:00", size=18, weight="bold")

    def did_mount(self):
        """initializer of the game, creates the deck, slots and deals the cards to the board"""
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()
        self.is_timer_running = True
        self.page.run_task(self.update_timer)

    def create_card_deck(self):
        """inits our card deck with the 52 cards, from 4 suits and 13 ranks"""
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))

    def create_slots(self):
        """creates the slots that will hold the cards, pile to draw from, waste pile, foundations and tableau(playing area)"""
        self.stock = Slot(solitaire=self, top=0, left=0, border=ft.border.all(1))

        self.waste = Slot(solitaire=self, top=0, left=100, border=None)

        self.foundations = []
        x = 300
        for i in range(4):
            self.foundations.append(
                Slot(solitaire=self, top=0, left=x, border=ft.border.all(1, "outline"))
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(solitaire=self, top=150, left=x, border=None))
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        """shuffles the cards and deals them to the board according to the defined rules of solitaire"""
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        # deal to tableau
        first_slot = 0
        remaining_cards = self.cards.copy()

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = remaining_cards[0]
                top_card.place(slot)
                remaining_cards.remove(top_card)
            first_slot += 1

        # place remaining cards to stock pile
        for card in remaining_cards:
            card.place(self.stock)
            print(f"Card in stock: {card.rank.name} {card.suite.name}")

        self.update()

        for slot in self.tableau:
            slot.get_top_card().turn_face_up()

        self.update()

    def check_foundations_rules(self, card, slot):
        """ensures that we can place the card on the foundation according to the following conditions:
        - if the target slot has no cards, only an Ace of any suit/color can be placed
        - if the target slot has cards, the card being moved MUST be of the SAME SUIT, SAME COLOR and 1 RANK HIGHER than the current card
        - logically, the card must be placed face up"""
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.name == top_card.suite.name
                and card.rank.value - top_card.rank.value == 1
            )
        else:
            return card.rank.name == "Ace"

    def check_tableau_rules(self, card, slot):
        """ensures that we can place the card on the target according to the following conditions:
        - if the target slot has cards, the card being placed must be of opposite color and 1 rank lower than the card already in the slot
        - if the target slot is empty, only a King (of any suit/color) can be placed
        - logically, the card must be placed face up"""
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.color != top_card.suite.color
                and top_card.rank.value - card.rank.value == 1
                and top_card.face_up
            )
        else:
            return card.rank.name == "King"

    def restart_stock(self):
        """when the stock is clicked, recycles cards"""
        cards_in_waste = self.waste.pile.copy()
        self.history.append({
            "action": "recycle_stock",
            "cards": cards_in_waste
        })
        while len(self.waste.pile) > 0:
            card = self.waste.get_top_card()
            card.turn_face_down()
            card.move_on_top()
            card.draggable_pile = [card]
            card.place(self.stock)

    def restart_game(self, e=None):
        """restarts the game/board, shuffles the cards, resets timer, move counter, etc."""
        self.controls.clear() # wipes visual elements
        
        # reconstruct the game data from scratch (new game)
        self.history.clear()
        self.current_save_name = None
        self.score = 0
        self.timer_seconds = 0
        self.update_score(0)
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()
        
        # updates interface
        self.update()

    def undo_move(self, e=None):
        """undoes the last move, if last movement made any card turn face up, it'll be turned face down again.
        if the move moved a card from slot A to slot B, it'll be moved back from slot B to slot A and so on"""
        if len(self.history) == 0: # if there are no moves to undo, do nothing
            print("No moves to undo") # debug
            return
        
        last_move = self.history.pop()
        self.update_score(-last_move.get("points", 0)) # subtracts the points for whatever was added before undoing
        action = last_move["action"]
        print(f"Action: {action}") # debug
        
        if action == "flip": # if a card was flipped face up, flip it back face down
            last_move["card"].turn_face_down()
        
        elif action == "move" or action == "move_to_foundation": # if a card was moved from a slot to another, let's move it back to the source slot
            cards = last_move["cards"]
            source_slot = last_move["source_slot"]
            lead_card = cards[0]
            lead_card.draggable_pile = cards
            lead_card.move_on_top()
            lead_card.place(source_slot)
        
        elif action == "move_stock_waste": # put the card back on the deck face down
            card = last_move["card"]
            source_slot = last_move["source_slot"]
            card.turn_face_down()
            card.draggable_pile = [card]
            card.place(source_slot)
        
        elif action == "recycle_stock": # restarted deck, place back cards face up in waste
            cards = last_move["cards"]
            for card in reversed(cards): # reversed order to maintain stack integrity
                card.turn_face_up()
                card.move_on_top()
                card.draggable_pile = [card]
                card.place(self.waste)
        
        self.update()
    
    def check_win(self):
        """checks win condition"""
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False

    def winning_sequence(self):
        """plays a winning animation"""
        for slot in self.foundations:
            for card in slot.pile:
                card.animate_position = 2000
                card.move_on_top()
                card.top = random.randint(0, SOLITAIRE_HEIGHT)
                card.left = random.randint(0, SOLITAIRE_WIDTH)
                self.update()
        self.controls.append(
            ft.AlertDialog(title=ft.Text("Congratulations! You won!"), open=True)
        )
    
    async def _perform_save(self, save_name):
        """core logic to serialize and save the board state to a specific filename."""
        save_data = {
            "score": self.score,
            "timer_seconds": self.timer_seconds,
            "cards": {}
        }
        for card in self.cards:
            card_id = f"{card.rank.name}_{card.suite.name}"
            
            if card.slot == self.stock: slot_name = "stock"
            elif card.slot == self.waste: slot_name = "waste"
            elif card.slot in self.foundations: slot_name = f"foundation_{self.foundations.index(card.slot)}"
            elif card.slot in self.tableau: slot_name = f"tableau_{self.tableau.index(card.slot)}"
            else: continue
            
            save_data["cards"][card_id] = {
                "slot": slot_name,
                "face_up": card.face_up,
                "pile_index": card.slot.pile.index(card)
            }
            
        save_string = json.dumps(save_data)
        await ft.SharedPreferences().set(save_name, save_string)
        self.current_save_name = save_name
        print(f"Game saved successfully to: {save_name}")

    async def _generate_new_save(self):
        """helper to calculate the next ID and create a fresh save file."""
        prefs = ft.SharedPreferences()
        keys = await prefs.get_keys("solitaire_save_")
        
        if keys:
            ids = [int(k.split("_")[2]) for k in keys if len(k.split("_")) >= 3 and k.split("_")[2].isdigit()]
            next_id = max(ids) + 1 if ids else 0
        else:
            next_id = 0
            
        date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
        new_save_name = f"solitaire_save_{next_id:04d}_{date_str}"
        await self._perform_save(new_save_name)

    async def save_game(self, e=None):
        """triggered by save button. opens dialog when a save is already loaded, then prompts the user to eitehr overwrite or create a new file."""
        if self.current_save_name:
            dlg = ft.AlertDialog(
                title=ft.Text("Save Options"),
                content=ft.Text(f"You are currently playing on '{self.current_save_name}'.\nWould you like to overwrite it or create a brand new save file?")
            )
            
            async def close_dialog(e=None):
                dlg.open = False
                self.page.update()
                
            async def overwrite_save(e):
                await self._perform_save(self.current_save_name)
                await close_dialog()
                
            async def create_new(e):
                await self._generate_new_save()
                await close_dialog()
                
            dlg.actions = [
                ft.TextButton("Overwrite", on_click=overwrite_save),
                ft.TextButton("Create New", on_click=create_new),
                ft.TextButton("Cancel", on_click=close_dialog)
            ]
            
            self.page.overlay.append(dlg)
            dlg.open = True
            self.page.update()
        else:
            # if no save is currently loaded, creates new one
            await self._generate_new_save()
                
    async def load_game(self, save_name):
        """loads a previously saved game state from client's storage, reloads the game state using the values from the save,
        if no save is found, does nothing"""
        prefs = ft.SharedPreferences()
        save_string = await prefs.get(save_name)
        
        if not save_string:
            print("No save data found")
            return

        save_data = json.loads(save_string)
        
        # if by chance we have old files without scoring and timer data, we set them to default values to avoid breaking the loading process
        if "cards" in save_data:
            card_states = save_data["cards"]
            self.score = save_data.get("score", 0)
            self.timer_seconds = save_data.get("timer_seconds", 0)
        else:
            card_states = save_data
            self.score = 0
            self.timer_seconds = 0
        
        self.update_score(0)
        self.clear_game_state()
        self.controls = [c for c in self.controls if c not in self.cards]

        slots_data = {"stock": [], "waste": []}
        for i in range(4): slots_data[f"foundation_{i}"] = []
        for i in range(7): slots_data[f"tableau_{i}"] = []

        for card in self.cards:
            card_id = f"{card.rank.name}_{card.suite.name}"
            if card_id in card_states:
                state = card_states[card_id]
                slots_data[state["slot"]].append((state["pile_index"], card, state["face_up"]))

        for slot_name, card_tuples in slots_data.items():
            card_tuples.sort(key=lambda x: x[0])
            
            if slot_name == "stock": target_slot = self.stock
            elif slot_name == "waste": target_slot = self.waste
            elif slot_name.startswith("foundation_"): 
                target_slot = self.foundations[int(slot_name.split("_")[1])]
            elif slot_name.startswith("tableau_"):
                target_slot = self.tableau[int(slot_name.split("_")[1])]

            for _, card, face_up in card_tuples:
                if face_up:
                    card.turn_face_up()
                else:
                    card.turn_face_down()
                
                card.slot = target_slot
                target_slot.pile.append(card)
                
                if target_slot in self.tableau:
                    card.top = target_slot.top + target_slot.pile.index(card) * CARD_OFFSET
                else:
                    card.top = target_slot.top
                card.left = target_slot.left
                
                self.controls.append(card)

        self.update()
        self.current_save_name = save_name
        print(f"{save_name} loaded successfully!")
    
    async def open_save_menu(self, e=None):
        """handles the save menu, which is a dialog that shows the list of saved games and allows the user to manage the saves, has the following functions inside:
        - close_dialog: cloes the save menu dialog
        - load_selected: loads the selected save and then closes the dialog
        - delete_selected: deletes the selected save from the storage, thus removes it from the list, then closes the dialog"""
        prefs = ft.SharedPreferences()
        keys = await prefs.get_keys("solitaire_save_")
        
        saves_list = ft.ListView(expand=True, spacing=10, padding=10)
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Saved Games ({len(keys) if keys else 0})"),
            content=ft.Container(width=400, height=300, content=saves_list)
        )
        
        async def close_dialog(e=None):
            dialog.open = False
            self.page.update()
            
        dialog.actions = [ft.TextButton("Close", on_click=close_dialog)]
        
        async def load_selected(e, save_name):
            await self.load_game(save_name)
            await close_dialog()
            
        async def delete_selected(e, save_name, row):
            await prefs.remove(save_name)
            saves_list.controls.remove(row)
            dialog.title.value = f"Saved Games ({len(saves_list.controls)})"
            self.page.update()

        if keys:
            def create_load_handler(save_name):
                async def handler(e):
                    await load_selected(e, save_name)
                return handler

            def create_delete_handler(save_name, target_row):
                async def handler(e):
                    await delete_selected(e, save_name, target_row)
                return handler
            # build a row for each save file
            for key in sorted(keys, reverse=True): # shows newest saves at the top
                row = ft.Row(
                    controls=[
                        ft.Text(key, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DOWNLOAD,
                            on_click=create_load_handler(key)
                            ),
                    ]
                )
                
                row.controls.append(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="RED",
                        on_click=create_delete_handler(key,row)
                    )
                )
                
                saves_list.controls.append(row)
            
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def clear_game_state(self, e=None):
        """clears the game state by emptying all appropriate game data"""
        self.stock.pile.clear()
        self.waste.pile.clear()
        for slot in self.foundations: slot.pile.clear()
        for slot in self.tableau: slot.pile.clear()
        self.history.clear()
  
    async def open_deck_menu(self, e=None):
        """opens a visual menu to select card back design
        - close_dialog: helper to close menu
        - create_select_handler: factory function to avoid lambda async
        - handler: when a design is selected, manipulates SharedPreferences to save it, then updates all cards with the new back design"""
        
        deck_options = [
            "/images/card0.png",
            "/images/card1.jpg",
            "/images/card2.jpg",
            "/images/card3.jpg",
            "/images/card4.jpg",
        ]
        
        dlg = ft.AlertDialog(title=ft.Text("Select Deck Style"))
        
        async def close_dialog(e=None):
            dlg.open = False
            self.page.update()
            
        dlg.actions = [ft.TextButton("Close", on_click=close_dialog)]
        
        options_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        
        def create_select_handler(selected_deck):
            async def handler(e):
                self.current_card_back = selected_deck
                await ft.SharedPreferences().set("preferred_deck", selected_deck)
                
                for card in self.cards:
                    if not card.face_up:
                        card.content.content.src = selected_deck
                        card.update()
                    
                self.update()
                await close_dialog()
            return handler
        
        # build clickable flet container for each img
        for src in deck_options:
            options_row.controls.append(
                ft.Container(
                    content=ft.Image(src=src, width=70, height=100, fit=ft.BoxFit.COVER),
                    border_radius=6,
                    border=ft.Border.all(2, ft.Colors.BLUE_400) if self.current_card_back == src else None,
                    ink=True,
                    on_click=create_select_handler(src)
                )
            )
        
        dlg.content = options_row
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
        
    async def load_user_deck_preferences(self):
        """loads user's deck preferences"""
        prefs = ft.SharedPreferences()
        saved_deck = await prefs.get("preferred_deck")
        if saved_deck:
            self.current_card_back = saved_deck
    
    async def update_timer(self):
        """background loop that updates the clock every second"""
        while self.is_timer_running:
            await asyncio.sleep(1)
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_text.value = f"Time: {minutes:02d}:{seconds:02d}"
            try:
                self.timer_text.update()
            except Exception as e:
                pass
    
    def update_score(self, points):
        """central function hub to manipulate the scoring"""
        self.score += points
        if self.score < 0:
            self.score = 0
        self.score_text.value = f"Score: {self.score}"
        try:
            self.score_text.update()
        except Exception as e:
            pass
    
    def show_rules(self, e=None):
        """opens a modal to display game rules and scoring system"""
        rules_text = (
            "Solitaire, or Klondike, is played with a standard 52-card deck, thus, we have 52! possible combinations when starting a new game.\n\n"
            "When the game starts, we are presented with our deck of cards to draw from, our waste, 4 foundations and 7 columns on the tableau.\n\n"
            "The game's goal is to have all the cards ordered from lowest to highest in rank (Ace to King) and by suit in all 4 foundations, leaving our tableau empty.\n\n"
            "Only the King card (of any suit) can be moved to an empty column, whereas we can/must move the Ace cards to the foundations to start sorting throughout the game.\n\n"
            "The cards are then dealt as follows throughout the 7 columns (left to right), incrementing by 1 the number of cards face down on each column, leaving the top card face up:\n"
            "* **Column 1:** 1 card face up\n"
            "* **Column 2:** 1 card face up and 1 card face down\n"
            "* **Column 3:** 1 card face up and 2 cards face down\n"
            "* **Column 4:** 1 card face up and 3 cards face down\n"
            "* **Column 5:** 1 card face up and 4 cards face down\n"
            "* **Column 6:** 1 card face up and 5 cards face down\n"
            "* **Column 7:** 1 card face up and 6 cards face down\n\n"
            "### Scoring system\n"
            "The scoring system starts at 0, and the following moves award points:\n"
            "* **+5 points:** Moving a waste card to the tableau\n"
            "* **+10 points:** Moving a card to a foundation slot\n"
            "* **+5 points:** Flipping a card face up\n\n"
            "### Main game loop\n"
            "When moving cards between columns, the card you're moving must be a rank lower and different in color (e.g.: You can place a Red 4 beneath a Black 5)."
        )
        
        dlg = ft.AlertDialog(
            title=ft.Text("Klondike Solitaire Rules"),
            content=ft.Container(
                content=ft.Column(
                    [ft.Markdown(rules_text)],
                    scroll=ft.ScrollMode.AUTO
                )
            ),
            actions=[ft.TextButton("Understood", on_click=lambda e: self.close_rules(dlg))]
        )
        
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def close_rules(self,dlg):
        dlg.open = False
        self.page.update()

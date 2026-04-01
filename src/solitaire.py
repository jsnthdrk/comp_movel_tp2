SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import random

import flet as ft
from card import Card
from slot import Slot


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        self.history = [] # for the undo functionality, will function as a stack of moves to iterate from when undoing

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
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
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        # deal to tableau
        first_slot = 0
        remaining_cards = self.cards

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
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.name == top_card.suite.name
                and card.rank.value - top_card.rank.value == 1
            )
        else:
            return card.rank.name == "Ace"

    def check_tableau_rules(self, card, slot):
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
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False

    def winning_sequence(self):
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

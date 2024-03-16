from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.modalview import ModalView
import holdem_calc

Window.size = (400, 800)
value_key = {'A': 'ace', 'K': 'king', 'Q': 'queen', 'J': 'jack', 'T': 'ten', '9': 'nine', '8': 'eight',
             '7': 'seven', '6': 'six', '5': 'five', '4': 'four', '3': 'three', '2': 'two'}
suit_key = {'c': 'clubs', 'd': 'diamonds', 'h': 'hearts', 's': 'spades'}
color = 0.08

class ImageButton(ButtonBehavior, Image):
    pass

class HoleCards(BoxLayout):
    pass

class Flop(BoxLayout):
    pass

class Turn(BoxLayout):
    pass

class River(BoxLayout):
    pass

class CardButton(ButtonBehavior, Image):
    pass

class CommunityCard(ButtonBehavior, Image):
    pass

class HomeScreen(Screen):
    pass

class OddsLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(color, color, color, 0.8)
            Rectangle(pos=self.pos, size=self.size)

class SettingsScreen(Screen):
    pass


GUI = Builder.load_file("main.kv")
class PokerApp(App):
    def build(self):
        return GUI

    def on_start(self):
        self.layout = self.root.ids['home_screen'].ids['float_layout']
        self.under_labels = self.root.ids['home_screen'].ids['under_labels']
        self.red_border = self.root.ids['home_screen'].ids['red_border']
        self.blue_border = self.root.ids['home_screen'].ids['blue_border']
        self.deck = {}
        self.flop = {}
        self.turn = {}
        self.river = {}
        self.holecards = {}
        self.labels = []
        self.community_cards = {}
        self.clear_selection()

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def clear_selection(self):
        """CLEARS THE SELECTED CARD"""
        self.current_selection = None
        self.current_holecard = None
        self.layout.remove_widget(self.red_border)
        self.under_labels.remove_widget(self.blue_border)

    def selector(self, position, selection):
        """WHEN A CARD IS SELECTED:"""
        self.clear_selection()
        if isinstance(selection, CardButton):
            self.red_border.pos = position
            self.layout.add_widget(self.red_border)
        else:
            self.blue_border.pos = position
            self.under_labels.add_widget(self.blue_border)
        if selection not in self.deck:
            self.deck[selection] = ['', '']
        self.current_selection = selection
        self.current_holecard = selection.parent

    def clear_button(self):
        """WHEN CLEAR BUTTON IS PRESSED."""
        self.clear_selection()
        for card in self.deck:
            if isinstance(card, CardButton):
                card.source = "icons/cards/empty.png"
            else:
                card.source = "icons/cards/border_white_plus.png"
        self.deck = {}
        self.flop = {}
        self.turn = {}
        self.river = {}
        self.holecards = {}
        self.community_cards = {}
        for i in self.labels:  # REMOVES RESULTS
            self.layout.remove_widget(i)

    def update_deck(self, value=None, suit=None):
        """WHEN SUITS OR VALUE BUTTONS ARE PRESSED:"""
        if self.current_selection:
            if value:
                self.deck[self.current_selection][0] = value

            if suit:
                self.deck[self.current_selection][1] = suit

            if self.deck[self.current_selection][0] != '' and self.deck[self.current_selection][1] != '' and\
                    isinstance(self.current_selection, CardButton):
                self.current_selection.source = 'icons/deck/{}_{}.png'.format(
                    value_key[self.deck[self.current_selection][0]],
                    suit_key[self.deck[self.current_selection][1]])
                if self.current_selection.parent not in self.holecards:
                    self.holecards[self.current_selection.parent] = {}
                self.holecards[self.current_selection.parent][self.current_selection] = self.deck[self.current_selection]

            elif isinstance(self.current_selection, CommunityCard) and self.deck[self.current_selection][0] != '' and \
                    self.deck[self.current_selection][1] != '':
                if isinstance(self.current_selection.parent, Flop):
                    self.current_selection.source = 'icons/deck/{}_{}.png'.format(
                        value_key[self.deck[self.current_selection][0]],
                        suit_key[self.deck[self.current_selection][1]])
                    self.flop[self.current_selection] = self.deck[self.current_selection]
                    self.community_cards[self.current_selection] = self.deck[self.current_selection]
                elif isinstance(self.current_selection.parent, Turn) and len(self.flop) == 3:
                    self.current_selection.source = 'icons/deck/{}_{}.png'.format(
                        value_key[self.deck[self.current_selection][0]],
                        suit_key[self.deck[self.current_selection][1]])
                    self.turn[self.current_selection] = self.deck[self.current_selection]
                    self.community_cards[self.current_selection] = self.deck[self.current_selection]
                elif isinstance(self.current_selection.parent, River) and len(self.flop) == 3 and len(self.turn) == 1:
                    self.current_selection.source = 'icons/deck/{}_{}.png'.format(
                        value_key[self.deck[self.current_selection][0]],
                        suit_key[self.deck[self.current_selection][1]])
                    self.river[self.current_selection] = self.deck[self.current_selection]
                    self.community_cards[self.current_selection] = self.deck[self.current_selection]
                else:
                    self.pop_up("Fill previous community cards.")

    def check_selection(self):
        # FOR TESTING
        print(len(self.list_deck_cards()))
        print(len(set(self.list_deck_cards())))

    def pop_up(self, message):
        # POP UP MESSAGE
        instance = ModalView(size_hint=(None, None), size=(350, 150), background_color=(color, color, color, 1))
        instance.add_widget(Label(text=message))
        instance.open()

    def list_holecards(self):
        self.holecards_list = []
        for holecards in self.holecards.values():
            for card in holecards.values():
                self.holecards_list.append(''.join(card))
        return self.holecards_list

    def list_community_cards(self):
        self.community_list = []
        for card in self.community_cards.values():
            self.community_list.append(''.join(card))
        return self.community_list

    def list_deck_cards(self):
        self.deck_list = []
        for card in self.deck.values():
            self.deck_list.append(''.join(card))
        return self.deck_list

    def check_community_cards_length(self):
        if len(self.list_community_cards()) >= 3:
            return self.list_community_cards()
        elif 1 <= len(self.list_community_cards()) < 3:
            self.community_cards = {}
            for card in self.deck:
                if isinstance(card, CommunityCard):
                    card.source = "icons/cards/border_white_plus.png"
                    self.deck[card] = ['', '']
            self.pop_up("Please have valid number of community cards.")
            return None
        else:
            return None

    def calculate_button(self):
        for i in self.labels:
            self.layout.remove_widget(i)
        results = []
        counter = 0
        if len(self.list_deck_cards()) == len(set(self.list_deck_cards())):
            if self.list_holecards() != [] and (all(len(hc) == 2 for hc in self.holecards.values())):
                for i in holdem_calc.calculate(self.check_community_cards_length(), True, 1, None, self.list_holecards(), False):
                    results.append(str(round(i*100, 2)) + "%")
                for hc in self.holecards:
                    counter += 1
                    label = OddsLabel(text="Win: {}\nTie: {}".format(results[counter], results[0]), pos=(hc.x-1, hc.y-20))
                    self.layout.add_widget(label)
                    self.labels.append(label)
            else:
                self.pop_up("Please fill holecards.")
        else:
            self.pop_up("Cards given must be unique.")


if __name__ == '__main__':
    PokerApp().run()

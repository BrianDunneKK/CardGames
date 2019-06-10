import sys
from random import shuffle
sys.path.append("../pygame-cdkk")
from cdkkPyGameApp import *

### --------------------------------------------------

class Card:
    _suit_names = ['Club', 'Diamond', 'Heart', 'Spade']
    _suit_abbrevs = ['C', 'D', 'H', 'S']
    _suit_symbols = [chr(0x2663), chr(0x2666), chr(0x2665), chr(0x2660)]
    _value_names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    _value_abbrevs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    @staticmethod
    def ListSuits():
        return Card._suit_abbrevs

    @staticmethod
    def ListValues():
        return Card._value_abbrevs

    def __init__(self, value, suit):
        if value.lower() == "joker":
            self._value = value.lower()
            self._suit = ""
        else:
            self._value = Card._value_abbrevs.index(value)
            self._suit = Card._suit_abbrevs.index(suit)

    @property
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit

    @property
    def name(self):
        if self._suit == "":
            n = self._value
        else:
            v = Card._value_names[self._value]
            s = Card._suit_names[self._suit]
            n = v + " of " + s + "s"
        return n

    @property
    def abbrev(self):
        if self._suit == "":
            a = self._value[0] + self._value[0]
        else:
            v = Card._value_abbrevs[self._value]
            s = Card._suit_abbrevs[self._suit]
            a = v + s
        return a
    
    @property
    def symbol(self):
        if self._value == "joker":
            sy = chr(0x2600) + chr(0x2600)
        # elif self._value == "deck":
        #     sy = chr(0x26EA) + chr(0x26EA)
        # elif self._value == "back":
        #     sy = chr(0x2610) + chr(0x2610)
        else:
            v = Card._value_abbrevs[self._value]
            s = Card._suit_symbols[self._suit]
            sy = s+v
        return sy

    def str(self, as_symbol=True):
        return self.symbol if as_symbol else self.abbrev

### --------------------------------------------------

class CardSet:
    def __init__(self, init_cards = []):
        if (len(init_cards) == 0):
            self._cards = []
        else:
            self._cards = init_cards

    def add(self, card):
        return self._cards.append(card)

    @property
    def count(self):
        return len(self._cards)

    @property
    def cards(self):
        return self._cards

    def __iter__(self):
        return iter(self._cards)

    def str(self, as_symbol=True):
        s = ""
        for c in self._cards:
            s = s + c.str(as_symbol) + " "
        return s

    def clear(self):
        self._cards = []

    def shuffle(self):
        shuffle(self._cards)
        return(self._cards)

    def deal(self, count):
        cards_dealt = self._cards[0:count]
        self._cards = self._cards[count:]
        return CardSet(cards_dealt)

    def dealone(self):
        card_dealt = self._cards[0]
        self._cards = self._cards[1:]
        return card_dealt

    def deck(self):
        self.clear()
        for s in Card.ListSuits():
            for v in Card.ListValues():
                self.add(Card(v, s))

### --------------------------------------------------

class Sprite_Card(Sprite):
    default_style = { "width":(691//4), "height":(1056//4) }

    def __init__(self, card, topleft, style=None):
        super().__init__(card.abbrev, style=merge_dicts(Sprite_Card.default_style, style))
        self.card = card
        self.load_image_from_file(self.image_file, scale_to="style")
        self.rect.topleft = topleft

    @property
    def image_file(self):
        if self.card.value == "joker":
            f = "joker"
        else:
            f = self.card.abbrev
        return "Images\\"+f+".png"

# --------------------

class Manager_Card(SpriteManager):
    def __init__(self, name = "Card Manager"):
        super().__init__(name)
        self.deck = CardSet()
        self.deck.deck()
        self.deck.shuffle()

        self.hand = self.deck.deal(52)
        i = 0
        for c in self.hand:
            self.add(Sprite_Card(c, (20+(i%13)*50, 20+(i//13)*100)))
            i = i + 1

### --------------------------------------------------

class CardGameApp(PyGameApp):
    def init(self):
        super().init()
        self.add_sprite_mgr(Manager_Card())
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

app_config = {
    "width":1200, "height":800,
    "background_fill":"burlywood",
    "caption":"Card Game"
    }
theApp = CardGameApp(app_config)
theApp.execute()

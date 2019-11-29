from random import shuffle
import cdkk
import pygame


app_styles = {
    "Card": {"width": (691//4), "height": (1056//4)}
}
cdkk.stylesheet.add_stylesheet(app_styles)

# --------------------------------------------------


class Card:
    _suit_names = ['Club', 'Diamond', 'Heart', 'Spade']
    _suit_abbrevs = ['C', 'D', 'H', 'S']
    _suit_symbols = [chr(0x2663), chr(0x2666), chr(0x2665), chr(0x2660)]
    _value_names = ['Ace', '2', '3', '4', '5', '6', '7',
                    '8', '9', '10', 'Jack', 'Queen', 'King']
    _value_abbrevs = ['A', '2', '3', '4', '5', '6', '7',
                      '8', '9', 'T', 'J', 'Q', 'K']
    _value_as_int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

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
        # return self._value
        return Card._value_abbrevs[self._value]

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

    def as_str(self, as_symbol=False):
        return self.symbol if as_symbol else self.abbrev

    def as_int(self):
        return Card._value_as_int[self._value]

# --------------------------------------------------


class CardSet:
    def __init__(self, init_cards=[], deck=False, shuffle=False):
        if (len(init_cards) == 0):
            self._cards = []
        else:
            self._cards = init_cards
        if deck:
            self.deck(False)
        if shuffle:
            self.shuffle()

    def add(self, card):
        if type(card) is CardSet:
            for c in card.cards:
                self.add(c)
            return self.cards
        else:
            return self._cards.append(card)

    @property
    def count(self):
        return len(self._cards)

    @property
    def cards(self):
        return self._cards

    def __iter__(self):
        return iter(self._cards)

    def as_str(self, as_symbol=False):
        s = ""
        for c in self._cards:
            s = s + c.as_str(as_symbol) + " "
        return s

    def as_int(self):
        v = 0
        for c in self._cards:
            cv = c.as_int()
            v = v + c.as_int()
        return v

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

    def deck(self, shuffle=False):
        self.clear()
        for s in Card.ListSuits():
            for v in Card.ListValues():
                self.add(Card(v, s))
        if shuffle:
            self.shuffle()

# --------------------------------------------------


class CardSet_TwentyOne(CardSet):
    def as_int(self):
        v = super().as_int()
        for c in self._cards:
            if c.value == "A" and v < 12:
                v += 10
        return v

    def as_int21(self):
        v = self.as_int()
        aces = 0
        for c in self._cards:
            if c.value == "A":
                aces += 1
        return (v, aces)

# --------------------------------------------------

class Sprite_Card(cdkk.Sprite):
    def __init__(self, card, topleft, style=None):
        super().__init__(card.abbrev, style=cdkk.merge_dicts(cdkk.stylesheet.style("Card"), style))
        self.card = card
        self.load_image_from_file(self.image_file, scale_to="style")
        self.rect.topleft = topleft

    @property
    def image_file(self):
        if self.card.value == "joker":
            f = "joker"
        else:
            f = self.card.abbrev
        return f+".png"

# --------------------

import Cards

def print_cards(card_set):
    msg = "{:22s}{}".format(card_set.as_str(as_symbol=False), card_set.as_int())
    print(msg)

deck = Cards.CardSet()
deck.deck()

hand = Cards.CardSet_TwentyOne()
hand.add(deck.deal(2))
print_cards(hand)

hand.add(deck.dealone())
print_cards(hand)

hand.add(deck.dealone())
print_cards(hand)

hand.add(deck.dealone())
print_cards(hand)

hand.add(deck.dealone())
print_cards(hand)

hand.add(deck.dealone())
print_cards(hand)

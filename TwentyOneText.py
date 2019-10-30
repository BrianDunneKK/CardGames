import Cards
import msvcrt
import time

# --------------------------------------------------

def print_cards(reveal):
    msg = "Player: {:16s}({})        Banker: ".format(
        player.as_str(), player.as_int())
    if reveal:
        msg += "{:16s}({})".format(banker.as_str(), banker.as_int())
    else:
        msg += "{} ??".format(banker.cards[0].as_str())
    print(msg)

# --------------------------------------------------

deck = Cards.CardSet(deck=True, shuffle=True)
print("\n[S]tick or [T]wist\n")

player = Cards.CardSet_TwentyOne()
banker = Cards.CardSet_TwentyOne()
player.add(deck.deal(2))
banker.add(deck.deal(2))

# Play the Player cards
print_cards(False)
while player.as_int() <= 21:
    ch = msvcrt.getch()
    if ch == b't':
        player.add(deck.dealone())
        print_cards(False)
    else:
        break

# Play the Banker cards
if player.as_int() <= 21:
    print("\nBanker")
    print_cards(True)
    while banker.as_int() < player.as_int():
        time.sleep(2)
        banker.add(deck.dealone())
        print_cards(True)

# Display result
if player.as_int() > 21:
    print("Player Bust! You lost.")
elif banker.as_int() > 21:
    print("Banker Bust! You win.")
elif banker.as_int() == player.as_int():
    print("Draw. Banker wins.")
elif banker.as_int() > player.as_int():
    print("Banker wins")
else:
    print("Player win!")
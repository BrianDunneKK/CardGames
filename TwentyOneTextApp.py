import time
import Cards
import cdkk


class TwentyOne(cdkk.cdkkApp):
    def start_game(self):
        super().start_game()
        self.deck = Cards.CardSet(deck=True, shuffle=True)
        self.player = Cards.CardSet_TwentyOne()
        self.banker = Cards.CardSet_TwentyOne()
        self.player.add(self.deck.deal(2))
        self.banker.add(self.deck.deal(2))
        self.player_turn = 1
        print("\n[S]tick or [T]wist\n")
        self.draw()

    def manage_events(self):
        self._next_action = None
        if self.player_turn > 0:
            ch = cdkk.getch(True)
            if ch == 'T':
                self._next_action = "Twist"
            elif ch == 'S':
                self._next_action = "Stick"

    def update(self):
        if self._next_action == "Twist":
            self.player.add(self.deck.dealone())
        elif self._next_action == "Stick":
            self.player_turn = 0
        elif self.player_turn == 0 and self.banker.as_int() < self.player.as_int():
            self.banker.add(self.deck.dealone())

    def draw(self, flip=True):
        msg = "Player: {:16s}({:02d})".format(
            self.player.as_str(), self.player.as_int())
        if self.player_turn > 0:
            msg += "        Banker: {} ??".format(
                self.banker.cards[0].as_str())
        else:
            msg += "        Banker: {:16s}({})".format(
                self.banker.as_str(), self.banker.as_int())
        print(msg)

    def manage_loop(self):
        if self.player_turn > 0 and self.player.as_int() > 21:
            self.end_game()
        elif self.player_turn == 0:
            if self.banker.as_int() >= self.player.as_int():
                self.end_game()
            else:
                time.sleep(2)

    def end_game(self):
        if self.player.as_int() > 21:
            msg = "Player Bust! You lost."
        elif self.banker.as_int() > 21:
            msg = "Banker Bust! You win."
        elif self.banker.as_int() == self.player.as_int():
            msg = "Draw. Banker wins."
        elif self.banker.as_int() > self.player.as_int():
            msg = "Banker wins"
        else:
            msg = "Player win!"
        print(msg+"\n")
        self.exit_app()


TwentyOne().execute()

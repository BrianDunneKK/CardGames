import cdkk
import pygame
import Cards

class Manager_Card(cdkk.SpriteManager):
    def __init__(self, name = "Card Manager"):
        super().__init__(name)

    def start_game(self):
        super().start_game()
        self.deck = Cards.CardSet()
        self.deck.deck()
        self.deck.shuffle()

        self.hand = self.deck.deal(52)
        self.empty()
        i = 0
        for c in self.hand:
            self.add(Cards.Sprite_Card(c, (20+(i%13)*50, 20+(i//13)*100)))
            i = i + 1

### --------------------------------------------------

class CardGameApp(cdkk.PyGameApp):
    def init(self):
        super().init()
        self.add_sprite_mgr(Manager_Card())
        key_map = {
            pygame.K_q: "Quit",
            pygame.K_d: "StartGame" # Deal
        }
        self.event_mgr.event_map(key_event_map=key_map)

### --------------------------------------------------

app_config = {
    "width":1200, "height":800,
    "background_fill":"burlywood",
    "caption":"Card Game",
    "image_path": "CardGames\\Images\\"
    }
CardGameApp(app_config).execute()

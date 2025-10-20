# yung game state to, ito yung minamanipulate natin dapat pag nagcocommand
# yung state ng cards, kalaban, yung command history andito
from dataclasses import dataclass


@dataclass
class State:
    started: bool = False
    exited: bool = False
    in_game: bool = False

    # Siguro dito yung laman ng list is dict ng {cardid:CardId, cardType: str}
    player_deck = []
    enemy_deck = []
    player_hand = []
    enemy_hand = []
                         # Dito siguro mas isa pa na laman yung dict kung
    community_cards = [] # revealed siya or hindi

    player_health: int = 0
    enemy_health: int = 0

    #Betting
    enemy_last_bet: int = 0
    player_last_bet: int = 0

    #Pera
    player_chips: int = 0
    enemy_chips: int = 0

    shop_items = []
    pot: int = 0
    # di ko alam rn pano to, pero probably gagamitin for the ai
    # enemy_state: str

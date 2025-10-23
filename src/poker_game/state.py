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
    community_deck = []

    player_health: int = 0
    enemy_health: int = 0

    #Betting
    enemy_last_bet: int = 0
    player_last_bet: int = 0

    #Pera
    player_chips: int = 0
    enemy_chips: int = 0

    #Cards in play
    player_play = []
    enemy_play = []

    #Damage Calculation
    enemy_damage: int = 0
    player_damage: int = 0

    round_state: int = 0

    #Folded meaning:
    # 0 - nothing happened
    # 1 - player folded
    # 2 - enemy folded
    folded: int = 0

    shop_items = []
    pot: int = 0
    # di ko alam rn pano to, pero probably gagamitin for the ai
    # enemy_state: str
    enemy = None

# yung game state to, ito yung minamanipulate natin dapat pag nagcocommand
# yung state ng cards, kalaban, yung command history andito
from dataclasses import dataclass


@dataclass
class State:
    started: bool = False
    exited: bool = False
    in_game: bool = False

    # Siguro dito yung laman ng list is dict ng {cardid:CardId, cardType: str}
    player_cards = []
    enemy_cards = []  # Dito siguro mas isa pa na laman yung dict kung
    community_cards = [] # revealed siya or hindi

    player_health: int = 0
    enemy_health: int = 0

    player_chips: int = 0
    enemy_chips: int = 0

    # di ko alam rn pano to, pero probably gagamitin for the ai
    # enemy_state: str

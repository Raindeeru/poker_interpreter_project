# yung game state to, ito yung minamanipulate natin dapat pag nagcocommand
# yung state ng cards, kalaban, yung command history andito
from poker_game.card import Card
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
    community_cards = []
    community_deck = []

    player_health: int = 0
    enemy_health: int = 0

    enemy_max_health: int = 0  # for ui

    # Betting
    enemy_last_bet: int = 0
    player_last_bet: int = 0

    # Pera
    player_chips: int = 0
    enemy_chips: int = 0

    # Cards in play
    player_play = []
    enemy_play = []

    # Damage Calculation
    enemy_damage: int = 0
    player_damage: int = 0

    round_state: int = 0

    # Folded meaning:
    # 0 - nothing happened
    # 1 - player folded
    # 2 - enemy folded
    folded: int = 0

    has_bet:bool = False

    lead: int = 0

    shop_items = []
    pot: int = 0
    # di ko alam rn pano to, pero probably gagamitin for the ai
    # enemy_state: str
    enemy = None

    player_all_in:bool = False
    enemy_all_in:bool = False

    inspect_target: Card = None
    win_check_available: bool = False
    
    #Checks if the damage round has passed, use for checking if a game is won/lost after
    game_finish_check_available:bool = False
    game_lost:bool = False
    
    win_count:int = 0
    in_shop:bool = False

    has_checked: bool = False

    last_winner: int = 0
    last_winning_hand = None
    last_player_hand = None
    last_enemy_hand = None
    last_player_pattern = None
    last_enemy_pattern = None

    view_prio:str = "hello"

    cheats_enabled: bool = False

    valid_moves = []

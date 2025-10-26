from poker_game.commands import *
from poker_game.state import State
from poker_game.damage_calculations import *
from poker_game.poker_hands import *
# from poker_game.special_commands import *
from poker_game.enemy import *
from poker_game.shop import *

test_state = State()
# test_state.enemy = Enemy(name='jerome', base_aggressiveness=0,fold_threshold=0,call_threshold=0,special_probability=0)

test_state.player_deck = [Card(suit="h", value=10, special="change", revealed=False),
                              Card(suit="d", value=10, special=None, revealed=False),
                              Card(suit="c", value=10, special=None, revealed=False),
                              Card(suit="s", value=2, special=None, revealed=False),
                              Card(suit="s", value=9, special=None, revealed=False)]

test_state = populate_shop(test_state)

print(test_state.shop_items)

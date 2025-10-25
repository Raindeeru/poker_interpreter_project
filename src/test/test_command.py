from poker_game.commands import *
from poker_game.state import State
from poker_game.damage_calculations import *
from poker_game.poker_hands import *
# from poker_game.special_commands import *
from poker_game.enemy import *

test_state = State()
# test_state.enemy = Enemy(name='jerome', base_aggressiveness=0,fold_threshold=0,call_threshold=0,special_probability=0)

test_state.player_hand = [Card(suit="h", value=10, special="change", revealed=False),
                              Card(suit="d", value=2, special=None, revealed=False),
                              Card(suit="c", value="j", special=None, revealed=False),
                              Card(suit="s", value=2, special=None, revealed=False),
                              Card(suit="s", value=3, special=None, revealed=False)]

test_state.enemy_hand = [Card(suit="h", value=9, special="exchange", revealed=False),
                              Card(suit="c", value=2, special=None, revealed=False),
                              Card(suit="s", value=2, special="change", revealed=False),
                              Card(suit="c", value="a", special=None, revealed=False),
                              Card(suit="c", value="j", special=None, revealed=False)]

# state, success, out = Change_Value(test_state, Card(suit="h", value=9, special="change", revealed=False), Card(suit="c", value="j", special=None, revealed=False))


# print(Exchange(test_state, 0, Card(suit="c", value=2, special=None, revealed=False), Card(suit="h", value=9, special="exchange", revealed=False)))
# print(Exchange(test_state, 2, Card(suit="c", value=2, special=None, revealed=False), Card(suit="h", value=10, special="exchange", revealed=False)))
print(Change_Value(test_state, Card(suit="s", value=2, special="change", revealed=False), Card(suit="c", value="j", special=None, revealed=False)))
from poker_game.commands import *
from poker_game.state import State
from poker_game.damage_calculations import *
from poker_game.poker_hands import *
from poker_game.special_commands import *

test_state = State()

test_state.player_hand = [Card(suit="h", value=9, special="change", revealed=False),
                              Card(suit="c", value=2, special=None, revealed=False),
                              Card(suit="s", value=10, special=None, revealed=False),
                              Card(suit="c", value="a", special=None, revealed=False),
                              Card(suit="c", value="j", special=None, revealed=False)]

state, success, out = Change_Value(test_state, Card(suit="h", value=9, special="change", revealed=False), Card(suit="c", value="j", special=None, revealed=False))

print(out)


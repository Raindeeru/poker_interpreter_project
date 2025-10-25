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

test_state_new = Change_Value(test_state, Card(suit="h", value=9, special="change", revealed=False), Card(suit="c", value="j", special=None, revealed=False))

print("debug_info", test_state_new[2])
print("after command:", test_state_new[0].player_hand)
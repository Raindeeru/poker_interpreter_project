from poker_game.commands import *
from poker_game.state import State
from poker_game.damage_calculations import *

from poker_game.poker_hands import *

test_state = State()
test_state.player_play = [Card(suit="s", value=9, special=None, revealed=False),
                          Card(suit="d", value='k', special=None, revealed=False)]
test_state.community_cards = [Card(suit="h", value=9, special=None, revealed=False),
                              Card(suit="c", value=5, special=None, revealed=False),
                              Card(suit="s", value=5, special=None, revealed=False)]


# test = Find_Best_Pattern(test_state)

damage_calculation(test_state)

# Give_Cards_Initial(test_state)
# Fold(test_state)
# Call(test_state)




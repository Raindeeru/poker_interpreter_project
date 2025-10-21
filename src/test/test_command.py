from poker_game.commands import *
from poker_game.state import State

test_state = State()
test_state.player_hand = [Card(suit="h", value="a", special=None, revealed=False),Card(suit="h", value="k", special=None, revealed=False)]
test_state.community_cards = [Card(suit="h", value="q", special=None, revealed=False),Card(suit="c", value=2, special=None, revealed=False),Card(suit="h", value="j", special=None, revealed=False)]


# test = Find_Best_Pattern(test_state)

Find_Best_Pattern(test_state)

# Give_Cards_Initial(test_state)
# Fold(test_state)
# Call(test_state)




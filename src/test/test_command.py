from poker_game.commands import *
from poker_game.state import State

test_state = State()
test_state.player_play = [Card(suit="s", value=2, special=None, revealed=False),
                          Card(suit="d", value=7, special=None, revealed=False)]
test_state.community_cards = [Card(suit="h", value=8, special=None, revealed=False),
                              Card(suit="c", value=6, special=None, revealed=False),
                              Card(suit="s", value='k', special=None, revealed=False)]


# test = Find_Best_Pattern(test_state)

Find_Best_Pattern(test_state)

# Give_Cards_Initial(test_state)
# Fold(test_state)
# Call(test_state)




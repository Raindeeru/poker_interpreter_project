from poker_game.commands import Give_Cards_Initial, Bet, Fold
from poker_game.state import State

test_state = State()

Give_Cards_Initial(test_state)
Bet(test_state, 101)
Fold(test_state)



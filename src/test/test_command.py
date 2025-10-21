from poker_game.commands import Give_Cards_Initial, Bet, Fold, Call
from poker_game.state import State

test_state = State()

Give_Cards_Initial(test_state)
Fold(test_state)
Call(test_state)



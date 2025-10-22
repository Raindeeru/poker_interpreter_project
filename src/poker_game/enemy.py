from dataclasses import dataclass
from poker_game.state import State


@dataclass
class Enemy:
    name: str
    state: int


def Bet(state: State, bet: int):
    if bet <= state.enemy_chips:
        state.enemy_chips -= bet
        state.enemy_last_bet = bet
        return (state, True, f"{state.enemy.name} bet {bet}")
    else:
        return (state, False, "Insufficient Chips!")


def Fold(state: State):
    state.round_state = 3
    state.folded = 2
    return (state, True, "Enemy Folded")


def Call(state: State):
    if state.player_chips >= state.enemy_last_bet:
        state.player_last_bet = state.enemy_last_bet
        state.player_chips -= state.player_last_bet
        return(state, True, "Call Successful")
    else:
        return(state, False, "Insufficient Chips!")

def All(state: State):
    if state.enemy_last_bet == 0 or state.player_chips + state.player_last_bet >= state.enemy_last_bet:
        state.player_last_bet += state.player_chips
        state.player_chips = 0
    else:
        state.player_last_bet += state.player_chips
        state.enemy_chips += state.enemy_last_bet - state.player_last_bet
        state.player_chips = 0
    return(state, True, "You went All in")

def Raise(state: State, raise_val:int):
    if raise_val > state.enemy_last_bet and raise_val <= state.player_last_bet + state.player_chips:
        state.player_chips -= raise_val
        state.player_last_bet = raise_val 
        return(state, True, f"You raised by {raise_val}")
    else:
        return(state, False,"Insufficient funds to raise")

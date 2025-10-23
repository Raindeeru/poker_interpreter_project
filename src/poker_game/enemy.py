from dataclasses import dataclass
from poker_game.state import State
from random import random


@dataclass
class Enemy:
    name: str
    base_aggressiveness: int
    fold_threshold: int
    call_threshold: int
    special_probability: float

    base_hand_multiplier: int = 1
    base_pot_multiplier: int = 1
    base_round_multiplier: int = 1

    def decide_next_move(self, state: State):
        total_aggro = self.base_aggressiveness

        special_sample = random()
        if special_sample <= self.special_probability:
            return
        # do basic move
        return


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
    if state.enemy_chips >= state.player_last_bet:
        state.enemy_last_bet = state.player_last_bet
        state.enemy_chips -= state.enemy_last_bet
        return state, True, f"{state.enemy.name} called"
    else:
        return state, False, "Insufficient Chips!"


def All(state: State):
    if state.player_last_bet == 0 \
            or state.enemy_chips + state.enemy_last_bet \
            >= state.player_last_bet:
        state.enemy_last_bet += state.enemy_chips
        state.enemy_chips = 0
    else:
        state.enemy_last_bet += state.enemy_chips
        state.player_chips += state.player_last_bet - state.enemy_last_bet
        state.enemy_chips = 0
    return state, True, f"{state.enemy.name} went all in!"


def Raise(state: State, raise_val: int):
    if raise_val > state.player_last_bet and \
            raise_val <= state.enemy_last_bet + state.enemy_chips:
        state.enemy_chips -= raise_val
        state.enemy_last_bet = raise_val
        return (state, True, f"{state.enemy.name} raised by {raise_val}")

    else:
        return (state, False, "Insufficient funds to raise")

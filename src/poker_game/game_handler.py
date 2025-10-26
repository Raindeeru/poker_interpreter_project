from poker_game.state import State 
from poker_game.card import Card

def reveal_community(state: State):
    for card in state.community_cards:
        card.revealed = True
    return state


def draw_card(state: State, number_of_cards: int):

    while len(state.player_hand) != number_of_cards:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    while len(state.enemy_hand) != number_of_cards:
        if state.enemy_hand[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    return state


def update_round(state: State):
    if state.round_state == 0 and \
        state.has_bet and \
            state.player_last_bet == state.enemy_last_bet:

        state.pot = state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state = reveal_community(state)
 
        state = draw_card(state, 4)

        state.round_state = 1

        return (state, True)
    elif state.round_state == 1 and \
        state.has_bet and \
            state.player_last_bet == state.enemy_last_bet:

        state.pot += state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state.round_state = 2

        return (state, True)

    elif state.round_state == 2 and \
        state.has_bet and \
            (state.player_last_bet == state.enemy_last_bet or
                (state.player_all_in and state.enemy_all_in)):

        state.pot += state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state.round_state = 3
        return (state, True)
    else:
        return (state, False)


def update_game(state):
    match state.round_state:
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
    pass

from poker_game.state import State
from poker_game.card import Card

import copy
import random


# This populates enemy, player and community deck
def Give_Cards_Initial(state: State):
    card_value = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    card_suit = ["d", "h", "s", "c"]
    deck = []

    for card in card_value:
        for suit in card_suit:
            deck.append(Card(suit=suit, value=card,
                             special=None, revealed=False))

    state.player_deck = copy.deepcopy(deck)
    state.enemy_deck = copy.deepcopy(deck)
    state.community_deck = copy.deepcopy(deck)

    random.shuffle(state.player_deck)
    random.shuffle(state.enemy_deck)
    random.shuffle(state.community_deck)

    for card in state.player_deck:
        card.revealed = True

    # Testing lang to para sa ui
    # state.enemy_deck[1].revealed = True

    # Selects the 3 community cards at the start of the game
    for _ in range(3):
        state.community_cards.append(state.community_deck.pop(0))

    # Gives the player 3 random cards
    while len(state.player_hand) != 3:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    #Special Test
    state.player_hand[0].special = "exchange"
    state.player_hand[1].special = "reveal"
    state.player_hand[2].special = "change"

    # Gives the enemy 3 random cards
    while len(state.enemy_hand) != 3:
        if state.enemy_deck[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    state.player_health = 1000
    state.enemy_health = 1000

    state.player_chips = 1000
    state.enemy_chips = 1000

    return (state, True, "Successfull gave Initial Cards!")


def Start(state: State):
    if state.started:
        return (state, False, "You're already in the Game")
    state.started = True
    state = Give_Cards_Initial(state)

    return (state, True, "Started a game of Gayagoy Gamblers! Goodluck")


def Bet(state: State, bet: int):
    if bet <= state.player_chips:
        state.player_chips -= bet
        state.player_last_bet = bet
        return (state, True, f"You bet {bet}")
    else:
        return (state, False, "Insufficient Chips!")


def Fold(state: State):
    state.round_state = 3
    state.folded = 1
    return (state, True, "Fold Successful!")


def Call(state: State):
    if state.player_chips >= state.enemy_last_bet:
        state.player_last_bet = state.enemy_last_bet
        state.player_chips -= state.player_last_bet
        return (state, True, "Call Successful")
    else:
        return (state, False, "Insufficient Chips!")


def All(state: State):
    if state.enemy_last_bet == 0 or \
            state.player_chips + state.player_last_bet >= state.enemy_last_bet:
        state.player_last_bet += state.player_chips
        state.player_chips = 0
    else:
        state.player_last_bet += state.player_chips
        state.enemy_chips += state.enemy_last_bet - state.player_last_bet
        state.player_chips = 0
    return (state, True, "You went All in")


def Raise(state: State, raise_val: int):
    if raise_val > state.enemy_last_bet and \
            raise_val <= state.player_last_bet + state.player_chips:
        state.player_chips -= raise_val - state.player_last_bet
        state.player_last_bet = raise_val
        return (state, True, f"You raised by {raise_val}")
    elif raise_val <= state.enemy_last_bet
        return (state, False, f"Raise Commad Invalid! must be above {state.enemy_last_bet}")
    else:
        return (state, False, "Insufficient funds to raise")


def Buy(state: State, shop_index: int):
    # state.player_chips -= state.shop_items[shop_index].price
    # state.player_deck.append(state.shop_items[shop_index].card)
    pass


def Quit(state: State):
    state.exited = True
    return state, True, "Goodbye!"

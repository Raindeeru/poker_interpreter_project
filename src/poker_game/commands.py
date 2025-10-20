from poker_game.state import State
from poker_game.card import Card

import copy
import random

#This populates enemy, player and community deck
def Give_Cards_Initial(state: State):
    card_value = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    card_suit = ["d", "h", "s", "c"]
   
    deck = []

    for card in card_value:
        for suit in card_suit:
            deck.append(Card(suit=suit, value=card, special=None, revealed=False))


    state.player_deck = copy.deepcopy(deck)
    state.enemy_deck = copy.deepcopy(deck)
    state.community_deck = copy.deepcopy(deck)

    random.shuffle(state.player_deck)
    random.shuffle(state.enemy_deck)
    random.shuffle(state.community_deck)

    #Selects the 3 community cards at the start of the game
    for _ in range(3):
        state.community_cards.append(state.community_deck.pop(0))

    #Gives the player 3 random cards
    while len(state.player_hand) != 3:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    #Gives the enemy 3 random cards
    while len(state.enemy_hand) != 3:
        if state.enemy_deck[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    state.player_health = 1000
    state.enemy_health = 1000
    
    state.player_chips = 1000
    state.enemy_chips = 1000

    return state
    
    
def Start(state: State):    
    state.started = True
    card = Card(suit="h", value=1, special=None, revealed=False)
    print(card)

    return state

def Bet(state: State, bet:int):
    if bet <= state.player_chips:
        state.player_chips -= bet
        state.pot += bet
        state.player_last_bet = bet
        return state
    else:
        print("Insufficient Chips")

def Fold(state: State):
    state.enemy_chips += state.pot
    state.player_hand 
    state.pot = 0
    state.round_state = 3
    print(state.round_state)
    print(state.pot)
    print(state.enemy_chips)
    Play(state, True)
    return state

def Call(state: State):
    state.pot += state.enemy_last_bet
    state.player_chips -= state.enemy_last_bet
    return state

def All(state: State):
    state.pot += state.player_chips
    state.player_chips = 0
    return state

def Raise(state: State, raise_val:int):
    state.pot += state.enemy_last_bet + raise_val
    state.player_chips -= state.enemy_last_bet + raise_val
    return state

def Buy(state: State, shop_index:int):
    # state.player_chips -= state.shop_items[shop_index].price
    # state.player_deck.append(state.shop_items[shop_index].card)
    pass

def Inspect(state: State):
    pass

def Play(state: State, folded=False):
    if not folded:
        pass
    if folded:
        state.player_play = []

        print(state.player_play)
        
        

def Quit(state: State):
    pass


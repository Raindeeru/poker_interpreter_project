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

    for card in state.player_deck:
        card.revealed = True

    # Testing lang to para sa ui
    # state.enemy_deck[1].revealed = True

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

    state = Give_Cards_Initial(state)

    return state

def Bet(state: State, bet:int):
    if state.enemy_last_bet == 0 and bet <= state.player_chips:
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
    state.enemy_last_bet = 100
    if state.player_chips >= state.enemy_last_bet:
        state.player_last_bet = state.enemy_last_bet
        state.pot += state.player_last_bet
        state.player_chips -= state.player_last_bet
        
        print(state.enemy_last_bet)
        print(state.pot)
        print(state.player_last_bet)
        print(state.player_chips)
    else:
        print("Insufficient Chips")

    return state

def All(state: State):
    if state.enemy_last_bet == 0 or state.player_chips + state.player_last_bet >= state.enemy_last_bet:
        state.pot += state.player_chips
        state.player_last_bet += state.player_chips
        state.player_chips = 0
    else:
        state.pot += state.player_chips
        state.player_last_bet += state.player_chips
        state.enemy_chips += state.enemy_last_bet - state.player_last_bet
        state.player_chips = 0

    return state

def Raise(state: State, raise_val:int):
    if raise_val > state.enemy_last_bet and raise_val <= state.player_last_bet + state.player_chips:
        state.pot += raise_val
        state.player_chips -= raise_val
        state.player_last_bet = raise_val 
    else:
        print("Insufficient funds to raise")
    return state

def Buy(state: State, shop_index:int):
    # state.player_chips -= state.shop_items[shop_index].price
    # state.player_deck.append(state.shop_items[shop_index].card)
    pass

##################################################################################
def check_same_suit(play_in_hand):
    if all(card.suit == play_in_hand[2].suit for card in play_in_hand):
        return True
    else:
        return False

def check_in_order(play_in_hand):
    values = [card.value for card in play_in_hand]
    values = sorted(values)

    def is_consecutive(lst):
        return all(b - a == 1 for a, b in zip(lst, lst[1:]))

    if 14 in values:

        if is_consecutive(values):
            return True

        values_low_ace = [1 if v == 14 else v for v in values]
        values_low_ace.sort()
        return is_consecutive(values_low_ace)
    else:

        return is_consecutive(values)

def check_royal_flush_order(play_in_hand):
    values = [card.value for card in play_in_hand]

    if all(v in values for v in range(10, 15)):
        return True
    else:
        return False

def Royal_Flush(play_in_hand):
    if check_same_suit(play_in_hand) and check_royal_flush_order(play_in_hand):
        return True
    else:
        return False

def Straight_Flush(play_in_hand):
    print(len(play_in_hand))
    if check_same_suit(play_in_hand) and check_in_order(play_in_hand):
        return True
    else:
        return False

def Four_of_a_Kind(play_in_hand):
    count = {}
    print(len(play_in_hand))
    for card in play_in_hand:  
        value = card.value   
        count[value] = count.get(value, 0) + 1
        if count[value] == 4:  
            return True
    return False

def Full_House(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 2:
        return True
    else:
        return False

def Flush(play_in_hand):
    if check_same_suit(play_in_hand):
        return True
    else:
        return False

def Straight(play_in_hand):
    if check_in_order(play_in_hand):
        return True
    else:
        return False

def Three_of_a_Kind(play_in_hand):
    count = {}
    print(len(play_in_hand))
    for card in play_in_hand:  
        value = card.value   
        count[value] = count.get(value, 0) + 1
        if count[value] == 3:  
            return True
    return False

def Two_Pair(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 3:
        return True
    else:
        return False

def Pair(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 4:
        return True
    else:
        return False

def Find_Best_Pattern(state: State):
    holder = state.player_play + state.community_cards
    play_in_hand = copy.deepcopy(holder)
    
    #Convert alpha values
    alpha_convert = {
        "j" : 11,
        "q" : 12,
        "k" : 13,
        "a" : 14
    }

    for card in play_in_hand:
        if not isinstance(card.value, int):
            print(alpha_convert[card.value])
            card.value = alpha_convert[card.value]
        else:
            continue

    #Sort hand
    play_in_hand = sorted(play_in_hand, key=lambda card: card.value)

    #For debugging
    for i in play_in_hand:
        print(i)

    if play_in_hand == []:
        print("Folded")

    elif Royal_Flush(play_in_hand):
        print("Royal Flush")

    elif Straight_Flush(play_in_hand):
        print("Straight Flush")

    elif Four_of_a_Kind(play_in_hand):
        print("Four of a Kind")

    elif Full_House(play_in_hand):
        print("Full House")

    elif Flush(play_in_hand):
        print("Flush")

    elif Straight(play_in_hand):
        print("Straight")

    elif Three_of_a_Kind(play_in_hand):
        print("Three of a Kind")

    elif Two_Pair(play_in_hand):
        print("Two Pair")

    elif Pair(play_in_hand):
        print("Pair")
    else:
        print("High Card")

    # return state

############################################################################################

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


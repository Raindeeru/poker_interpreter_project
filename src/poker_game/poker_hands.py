from poker_game.state import State
from poker_game.card import Card
import copy


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
        return (state, "Folded", play_in_hand)

    elif Royal_Flush(play_in_hand):
        print("Royal Flush")
        return (state, "Royal_Flush", play_in_hand)

    elif Straight_Flush(play_in_hand):
        print("Straight Flush")
        return (state, "Straight_Flush", play_in_hand)

    elif Four_of_a_Kind(play_in_hand):
        print("Four of a Kind")
        return (state, "Four_of_a_Kind", play_in_hand)

    elif Full_House(play_in_hand):
        print("Full House")
        return (state, "Full_House", play_in_hand)

    elif Flush(play_in_hand):
        print("Flush")
        return (state, "Flush", play_in_hand)

    elif Straight(play_in_hand):
        print("Straight")
        return (state, "Straight", play_in_hand)

    elif Three_of_a_Kind(play_in_hand):
        print("Three of a Kind")
        return (state, "Three_of_a_Kind", play_in_hand)

    elif Two_Pair(play_in_hand):
        print("Two Pair")
        return (state, "Two_Pair", play_in_hand)

    elif Pair(play_in_hand):
        print("Pair")
        return (state, "Pair", play_in_hand)

    else:
        print("High Card")
        return (state, "High_Card", play_in_hand)

    # return state

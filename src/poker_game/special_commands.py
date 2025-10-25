from poker_game.state import State
from poker_game.card import Card
import random


def get_card_string(card: Card):
    value_map = {
            "a": "Ace",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            "j": "Jack",
            "q": "Queen",
            "k": "King",
            }

    suit_map = {
            "d": "Diamonds",
            "h": "Hearts",
            "s": "Spades",
            "c": "Clubs",
            }

    return f"{value_map[card.value]} of {suit_map[card.suit]}"


def check_if_special_card_exists(state: State, card: Card):
    exists = any(
        c.suit == card.suit and
        c.value == card.value and
        c.special == card.special
        for c in state.player_hand
    )
    return exists

def check_if_card_in_hand(state: State, card: Card):
    exists = any(
        c.suit == card.suit and
        c.value == card.value 
        for c in state.player_hand
    )
    return exists

def Reveal(state: State, index: int, card: Card):
    if not check_if_special_card_exists(state, card):
        return (state, False, "You don't have that special card")
    if state.enemy_hand[index].revealed:
        return (state, False, "That Card is already revealed")

    state.enemy_hand[index].revealed = True

    for i, c in enumerate(state.player_hand):
        if c.value == card.value and c.suit == card.suit:
            state.player_hand[i].special = None

    return (state, False,
            f"Revealed {get_card_string(state.enemy_hand[index])}")


def Exchange(state: State, index: int, card: Card, special_card: Card):

    if not check_if_special_card_exists(state, special_card):
        return (state, False, "You don't have that special card")  
    elif not check_if_card_in_hand(state, card):
        return (state, False, "You do not have this card")
    else:
        for i, c in enumerate(state.player_hand):
            if c.value == special_card.value and c.suit == special_card.suit:
                state.player_hand[i].special = None
        
        player_index = next((i for i, c in enumerate(state.player_hand) if c.value == card.value))
        temp = state.player_hand[player_index]
        state.player_hand[player_index] = state.enemy_hand[index]
        state.player_hand[player_index].revealed = True
        state.enemy_hand[index] = temp
        state.enemy_hand[index].revealed = False
        return(state, True, 
               f"You Exchanged your {get_card_string(card)} with the enemy's {get_card_string(state.player_hand[player_index])}")


def Change_Suit(state: State, card_special: Card, card_target: Card, suit=None):
    
    suits = ["d","h","s","c"]
    
    if not check_if_special_card_exists(state, card_special):
        return (state, False, "You don't have that special card")
    
    if card_special.special != "change":
        return (state, False, "Not a valid card for change command")
    
    if not check_if_card_in_hand(state, card_target):
        return (state, False, "That card does not exist in your hand")
    
    for index, card in enumerate(state.player_hand):
        if card.value == card_special.value and card.suit == card_special.suit:
            state.player_hand[index].special = None
            
    
    if suit is None:
        for index, card in enumerate(state.player_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                suits_temp =  [s for s in suits if s != card_target.suit]
                random.shuffle(suits_temp)
                state.player_hand[index].suit = str(suits_temp[0])
                
        return (state, True, f"Changed {card_target}'s suit into a random suit '{suits_temp[0]}'")
    
    else:
        for index, card in enumerate(state.player_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                state.player_hand[index].suit = str(suit)
                
        return (state, True, f"Changed {card_target}'s suit into {suit}")
                

def Change_Value(state: State, card_special: Card, card_target: Card, value=None):
    
    values = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    
    if not check_if_special_card_exists(state, card_special):
        return (state, False, "You don't have that special card")
    
    if card_special.special != "change":
        return (state, False, "Not a valid card for change command")
    
    if not check_if_card_in_hand(state, card_target):
        return (state, False, "That card does not exist in your hand")
    
    for index, card in enumerate(state.player_hand):
        if card.value == card_special.value and card.suit == card_special.suit:
            state.player_hand[index].special = None
            
    
    if value is None:
        for index, card in enumerate(state.player_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                value_temp = [v for v in values if v != card_target.value]
                random.shuffle(value_temp)
                state.player_hand[index].value = value_temp[0]
                
        return (state, True, f"Changed {card_target}'s suit into a random value '{value_temp[0]}'")
    
    else:
        for index, card in enumerate(state.player_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                state.player_hand[index].value = value
                
        return (state, True, f"Changed {card_target}'s suit into {value}")

from poker_game.state import State
from poker_game.card import Card
from poker_game.item import Item
import copy
import random

def populate_shop(state: State):
    
    deck = copy.deepcopy(state.player_deck)
    random.shuffle(deck)
    
    
    while len(state.shop_items) != 3:
        if deck[0].special is None:
            state.shop_items.append(deck.pop(0))
        else:
            deck.append(deck.pop(0))
            
    return state
    



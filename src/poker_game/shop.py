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
            state.shop_items.append(Item(card=deck.pop(0),price=0,effect=None))
        else:
            deck.append(deck.pop(0))
            
    effects = ["reveal", "exchange","change"]
    price = [100, 300, 500]
    
    for i, item in enumerate(state.shop_items):      
        item.effect = effects[i]
        item.price = price[i]
            
    return state
    



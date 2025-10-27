from poker_game.state import State
from poker_game.card import Card
from poker_game.item import Item
import copy
import random


def populate_shop(state: State):
    state.shop_items.clear()
    deck = copy.deepcopy(state.player_deck)
    random.shuffle(deck)

    effects = [("reveal", 10, 400), ("exchange", 5, 500), ("change", 3, 600)]

    for e in effects:
        new_item = Item(effect=e[0], price=e[2])
        while len(new_item.cards) < e[1]:
            if deck[0].special is None:
                new_item.cards.append(deck.pop(0))
            else:
                deck.append(deck.pop(0))
        state.shop_items.append(new_item)

    return state

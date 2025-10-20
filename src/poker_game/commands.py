from poker_game.state import State
from poker_game.card import Card

#This populates enemy, player and community deck
def Give_Cards(state: State):
    card_value = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    card_suit = ["d", "h", "s", "c"]
   
    deck = []

    for card in card_value:
        for suit in card_suit:
            deck.append(Card(suit=suit, value=card, special=None, revealed=False))
    
    print(deck)

    
def Start(state: State):    
    state.started = True
    card = Card(suit="h", value=1, special=None, revealed=False)
    print(card)

    return state

def Bet(state: State, bet:int):
    state.player_chips -= bet
    state.pot += bet
    state.player_last_bet = bet
    return state

def Fold(state: State):
    pass

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

def Play(state: State):
    pass

def Quit(state: State):
    pass


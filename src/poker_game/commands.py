from poker_game.state import State


def Start(state: State):
    state.started = True
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

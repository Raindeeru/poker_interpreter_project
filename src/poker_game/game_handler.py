from poker_game.state import State 

def update_round(state: State):
    if state.round_state == 0 and \
        state.has_bet and \
            state.player_last_bet == state.enemy_last_bet:
                
        state.pot = state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0
        
        state.round_state = 1
        
        print("changed round state to 1")
        return (state, True)
    
    return (state, False)
        
        


def update_enemy(state):
    pass


def update_game(state):
    match state.round_state:
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
    pass

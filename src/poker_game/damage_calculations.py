from poker_game.poker_hands import *

def calculate_Royal_Flush(state: State, cards_held):
    state.player_damage = 600
    return (state)

def calculate_Straight_Flush(state: State, cards_held):
    if cards_held[4].value == 14:
        cards_held[4].value = 1

    for card in cards_held:
        state.player_damage += card.value
        
    state.player_damage = state.player_damage * 9
    print(state.player_damage)
    return (state)

def calculate_Straight(state: State, cards_held):
    for card in cards_held:
        if cards_held[0].value == 2 and cards_held[4].value == 14:
            cards_held[4].value = 1
        else:
            break

    for card in cards_held:
        state.player_damage += card.value

    state.player_damage = state.player_damage * 5
    print(state.player_damage)
    return (state)

def damage_calculation(state: State):

    pattern_Found = Find_Best_Pattern(state)[1]
    cards_held = Find_Best_Pattern(state)[2]
    print(f"Pattern Found: {pattern_Found}")
    print(f"Cards: {cards_held}")

    if pattern_Found == "Royal_Flush":
        return calculate_Royal_Flush(state, cards_held)
    elif pattern_Found == "Straight_Flush":

        return calculate_Straight_Flush(state, cards_held)

    elif pattern_Found == Four_of_a_Kind:
        pass 

    elif pattern_Found == Full_House:
        pass 

    elif pattern_Found == Flush:
        pass 

    elif pattern_Found == "Straight":
        return calculate_Straight(state, cards_held)

    elif pattern_Found == Three_of_a_Kind:
        pass 
    elif pattern_Found == Two_Pair:
        pass 

    elif pattern_Found == Pair:
        pass 
    else:
        pass
    

    

    

    
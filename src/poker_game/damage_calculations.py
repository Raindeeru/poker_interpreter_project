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

def calculate_Four_of_a_Kind(state: State, cards_held):
    count = {}
    print(len(cards_held))
    for card in cards_held:  
        value = card.value   
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 4:
            state.player_damage += value * 4
            state.player_damage = state.player_damage * 8
            print(state.player_damage)
            break
    return (state)

def calculate_Full_House(state: State, cards_held):
    for card in cards_held:
        state.player_damage += card.value
    state.player_damage = state.player_damage * 7
    print(state.player_damage)
    return (state)

def calculate_Flush(state: State, cards_held):
    for card in cards_held:
        state.player_damage += card.value
    state.player_damage = state.player_damage * 6
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

def calculate_Three_of_a_kind(state: State, cards_held):
    count = {}
    print(len(cards_held))
    for card in cards_held:  
        value = card.value   
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 3:
            state.player_damage += value * 3
            state.player_damage = state.player_damage * 4
            print(state.player_damage)
            break
    return (state)

def calculate_Two_Pair(state: State, cards_held):
    pass

def calculate_Pair(state: State, cards_held):
    count = {}
    print(len(cards_held))
    for card in cards_held:  
        value = card.value   
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 2:
            state.player_damage += value * 2
            state.player_damage = state.player_damage * 2
            print(state.player_damage)
            break
    return (state)

def calculate_High_Card(state: State, cards_held):
    state.player_damage = cards_held[4].value
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

    elif pattern_Found == "Four_of_a_Kind":
        return calculate_Four_of_a_Kind(state, cards_held)

    elif pattern_Found == "Full_House":
        return calculate_Full_House(state, cards_held)

    elif pattern_Found == "Flush":
        return calculate_Flush(state, cards_held) 

    elif pattern_Found == "Straight":
        return calculate_Straight(state, cards_held)

    elif pattern_Found == "Three_of_a_Kind":
        return calculate_Three_of_a_kind(state, cards_held)
    
    elif pattern_Found == "Two_Pair":
        return calculate_Two_Pair(state, cards_held) 

    elif pattern_Found == "Pair":
        return calculate_Pair(state, cards_held)
    else:
        return calculate_High_Card(state, cards_held)
    

    

    

    
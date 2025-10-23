from poker_game.poker_hands import Find_Best_Pattern
from poker_game.state import State
import copy 


def calculate_Royal_Flush(cards_held):
    return 600


def calculate_Straight_Flush(cards_held):
    damage = 0
    if cards_held[4].value == 14:
        cards_held[4].value = 1

    for card in cards_held:
        damage += card.value

    damage *= 9
    return damage


def calculate_Four_of_a_Kind(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 4:
            damage += value * 4
            damage *= 8
            break
    return damage


def calculate_Full_House(cards_held):
    damage = 0
    for card in cards_held:
        damage += card.value
    damage *= 7
    return damage


def calculate_Flush(cards_held):
    damage = 0
    for card in cards_held:
        damage += card.value
    damage *= 6
    return damage


def calculate_Straight(cards_held):
    damage = 0
    for card in cards_held:
        if cards_held[0].value == 2 and cards_held[4].value == 14:
            cards_held[4].value = 1
        else:
            break

    for card in cards_held:
        damage += card.value

    damage *= 5
    return damage


def calculate_Three_of_a_kind(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 3:
            damage += value * 3
            damage = damage * 4
            break
    return damage


def calculate_Two_Pair(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1
    pairs = []
    for value in count:
        if count[value] == 2:
            pairs.append(value)
    damage += (pairs[0] * 2) + (pairs[1] * 2)
    damage *= 3
    return damage


def calculate_Pair(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 2:
            damage += value * 2
            damage = damage * 2
            break
    return damage


def calculate_High_Card(cards_held):
    damage = cards_held[4].value
    return damage


def damage_calculation(hand):
    pattern_found = Find_Best_Pattern(hand)[0]
    cards_held = Find_Best_Pattern(hand)[1]

    match pattern_found:
        case "Royal_Flush":
            return calculate_Royal_Flush(cards_held)

        case "Straight_Flush":
            return calculate_Straight_Flush(cards_held)

        case "Four_of_a_Kind":
            return calculate_Four_of_a_Kind(cards_held)

        case "Full_House":
            return calculate_Full_House(cards_held)

        case "Flush":
            return calculate_Flush(cards_held)

        case "Straight":
            return calculate_Straight(cards_held)

        case "Three_of_a_Kind":
            return calculate_Three_of_a_kind(cards_held)

        case "Two_Pair":
            return calculate_Two_Pair(cards_held)

        case "Pair":
            return calculate_Pair(cards_held)

        case _:
            return calculate_High_Card(cards_held)


def update_player_damage(state: State):
    full_hand = copy.deepcopy(state.player_hand + state.community_cards)
    damage = damage_calculation(full_hand)
    state.player_damage = damage


def update_enemy_damage(state: State):
    full_hand = copy.deepcopy(state.enemy_hand + state.community_cards)
    damage = damage_calculation(full_hand)
    state.enemy_damage = damage

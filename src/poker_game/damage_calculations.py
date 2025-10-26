from poker_game.poker_hands import Find_Best_Pattern
from poker_game.state import State
import copy


def calculate_Royal_Flush(cards_held):
    return 1000, 1000


def calculate_Straight_Flush(cards_held):
    damage = 0
    if cards_held[4].value == 14:
        cards_held[4].value = 1

    for card in cards_held:
        damage += card.value

    damage += 850

    return damage, damage


def calculate_Four_of_a_Kind(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1
    for value in count:
        if count[value] == 4:
            damage += value * 4
            damage += 680
            break
    return damage, damage


def calculate_Full_House(cards_held):
    damage = 0
    for card in cards_held:
        damage += card.value
    damage += 520
    return damage, damage


def calculate_Flush(cards_held):
    damage = 0
    for card in cards_held:
        damage += card.value
    damage += 400
    return damage, damage


def calculate_Straight(cards_held):
    damage = 0
    for card in cards_held:
        if cards_held[0].value == 2 and cards_held[4].value == 14:
            cards_held[4].value = 1
        else:
            break

    for card in cards_held:
        damage += card.value

    damage += 300
    return damage, damage


def calculate_Three_of_a_kind(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1

    trio_val = 0
    for value in count:
        if count[value] == 3:
            damage += value * 3
            damage += 200
            trio_val = value
            break
    player_kicker = max(i for i in count if i != trio_val)
    player_kicker += damage

    return damage, player_kicker


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
    damage += 120

    player_kicker = max(i for i in count if i not in pairs)
    player_kicker += damage
    
    return damage, player_kicker

def calculate_Pair(cards_held):
    damage = 0
    count = {}
    for card in cards_held:
        value = card.value
        count[value] = count.get(value, 0) + 1

    pair_val = 0
    for value in count:
        if count[value] == 2:
            damage += value * 2
            damage += 40
            pair_val = value
            break

    player_kicker = max(i for i in count if i != pair_val)
    player_kicker += damage
    return damage, player_kicker


def calculate_High_Card(cards_held):
    damage = cards_held[4].value + 20
    player_kicker = cards_held[3].value + damage

    return damage, player_kicker


def damage_calculation(hand):
    pattern_found = Find_Best_Pattern(hand)[0]
    cards_held = Find_Best_Pattern(hand)[1]

    match pattern_found:
        case "Folded":
            return 0

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
    full_hand = copy.deepcopy(state.player_play + state.community_cards)
    damage, kicker = damage_calculation(full_hand)
    state.player_damage = damage
    return kicker


def update_enemy_damage(state: State):
    full_hand = copy.deepcopy(state.enemy_play + state.community_cards)
    damage, kicker = damage_calculation(full_hand)
    state.enemy_damage = damage
    return kicker

def check_same_suit(play_in_hand):
    if all(card.suit == play_in_hand[2].suit for card in play_in_hand):
        return True
    else:
        return False


def check_in_order(play_in_hand):
    values = [card.value for card in play_in_hand]
    values = sorted(values)

    def is_consecutive(lst):
        return all(b - a == 1 for a, b in zip(lst, lst[1:]))

    if 14 in values:

        if is_consecutive(values):
            return True

        values_low_ace = [1 if v == 14 else v for v in values]
        values_low_ace.sort()
        return is_consecutive(values_low_ace)
    else:

        return is_consecutive(values)


def check_royal_flush_order(play_in_hand):
    values = [card.value for card in play_in_hand]

    if all(v in values for v in range(10, 15)):
        return True
    else:
        return False


def Royal_Flush(play_in_hand):
    if check_same_suit(play_in_hand) and check_royal_flush_order(play_in_hand):
        return True
    else:
        return False


def Straight_Flush(play_in_hand):
    if check_same_suit(play_in_hand) and check_in_order(play_in_hand):
        return True
    else:
        return False


def Four_of_a_Kind(play_in_hand):
    count = {}
    for card in play_in_hand:
        value = card.value
        count[value] = count.get(value, 0) + 1
        if count[value] == 4:
            return True
    return False


def Full_House(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 2:
        return True
    else:
        return False


def Flush(play_in_hand):
    if check_same_suit(play_in_hand):
        return True
    else:
        return False


def Straight(play_in_hand):
    if check_in_order(play_in_hand):
        return True
    else:
        return False


def Three_of_a_Kind(play_in_hand):
    count = {}
    for card in play_in_hand:
        value = card.value
        count[value] = count.get(value, 0) + 1
        if count[value] == 3:
            return True
    return False


def Two_Pair(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 3:
        return True
    else:
        return False


def Pair(play_in_hand):
    unique = set(card.value for card in play_in_hand)
    if len(unique) == 4:
        return True
    else:
        return False


def Find_Best_Pattern(play_in_hand):
    # Convert alpha values
    alpha_convert = {
        "j": 11,
        "q": 12,
        "k": 13,
        "a": 14
    }

    for card in play_in_hand:
        if not isinstance(card.value, int):
            card.value = alpha_convert[card.value]
        else:
            continue

    # Sort hand
    play_in_hand = sorted(play_in_hand, key=lambda card: card.value)

    # For debugging
    # for i in play_in_hand:
    # print(i)

    if play_in_hand == []:
        return "Folded", play_in_hand

    elif Royal_Flush(play_in_hand):
        return "Royal_Flush", play_in_hand

    elif Straight_Flush(play_in_hand):
        return "Straight_Flush", play_in_hand

    elif Four_of_a_Kind(play_in_hand):
        return "Four_of_a_Kind", play_in_hand

    elif Full_House(play_in_hand):
        return "Full_House", play_in_hand

    elif Flush(play_in_hand):
        return "Flush", play_in_hand

    elif Straight(play_in_hand):
        return "Straight", play_in_hand

    elif Three_of_a_Kind(play_in_hand):
        return "Three_of_a_Kind", play_in_hand

    elif Two_Pair(play_in_hand):
        return "Two_Pair", play_in_hand

    elif Pair(play_in_hand):
        return "Pair", play_in_hand

    else:
        return "High_Card", play_in_hand

    # return state

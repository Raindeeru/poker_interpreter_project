from poker_game.state import State
from poker_game.card import Card


def get_card_string(card: Card):
    value_map = {
            "a": "Ace",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            "j": "Jack",
            "q": "Queen",
            "k": "King",
            }

    suit_map = {
            "d": "Diamonds",
            "h": "Hearts",
            "s": "Spades",
            "c": "Clubs",
            }

    return f"{value_map[card.value]} of {suit_map[card.suit]}"


def check_if_special_card_exists(state: State, card: Card):
    exists = any(
        c.suit == card.suit and
        c.value == card.value and
        c.special == card.special
        for c in state.player_hand
    )
    return exists


def Reveal(state: State, index: int, card: Card):
    if not check_if_special_card_exists(state, card):
        return (state, False, "You don't have that special card")
    if state.enemy_hand[index].revealed:
        return (state, False, "That Card is already revealed")

    state.enemy_hand[index].revealed = True

    return (state, False,
            f"Revealed {get_card_string(state.enemy_hand[index])}")


def Exchange(state: State):
    pass


def Change(state: State):
    pass

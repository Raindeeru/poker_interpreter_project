from dataclasses import dataclass
from poker_game.state import State
from poker_game.card import Card
import random
from ui.terminal import add_terminal_output
from poker_game.damage_calculations import damage_calculation
import itertools

@dataclass
class Enemy:
    name: str
    base_aggressiveness: int = 150
    fold_threshold: int = 100
    call_threshold: int = 170
    special_probability: float = 0

    base_hand_multiplier: int = 5
    base_pot_multiplier: int = 0.1
    base_round_multiplier: int = 10

    def do_basic_move(self, aggro: int, state):
        bet = state.player_last_bet + int(aggro)//10
        if aggro < self.fold_threshold:
            state, success, out = Fold(state)
            return success, out
        elif state.player_all_in:
            state, success, out = All(state)
            return success, out
        elif aggro > self.call_threshold:
            if state.player_last_bet >= state.enemy_chips:
                state, success, out = All(state)
                return success, out
            if state.lead == 1 and not state.has_bet:
                state, success, out = Bet(state, int(aggro)/5)
                return success, out
            state, success, out = Raise(state, bet)
            return success, out
        else:
            if state.lead == 1:
                state, success, out = Bet(state, 0)
                return success, out
            state, success, out = Call(state)
            return success, out

    def do_special_move(self, aggro: int, state: State):
        bet = state.player_last_bet + aggro
        if aggro < self.fold_threshold:
            state, success, out = Fold(state)
            return success, out
        elif state.player_all_in:
            state, success, out = All(state)
            return success, out
        elif aggro > self.call_threshold:
            if state.player_last_bet >= state.enemy_chips:
                state, success, out = All(state)
            state, success, out = Raise(state, bet)
            return success, out
        else:
            state, success, out = Call(state)
            return success, out

    def calculate_best_hand(self, hand, community):
        best = None
        highest_damage = 0
        for play in itertools.combinations(hand, 2):
            cards = list(play) + community
            current, kicker = damage_calculation(cards)
            if best is None or current > highest_damage:
                best = list(play)
                highest_damage = current
        return best

    def decide_play(self, state: State):
        unique = []
        seen = set()

        for c in state.enemy_hand:
            key = (c.suit, c.value)
            if key not in seen:
                seen.add(key)
                unique.append(c)

        if len(unique) < 2:
            state, success, out = Fold(state)
            return success, out

        best_play = self.calculate_best_hand(unique, state.community_cards)

        state, success, out = Play(state, best_play[0], best_play[1])
        return success, out

    def decide_next_move(self, state: State):
        if state.round_state == 3:
            success, out = self.decide_play(state)
            add_terminal_output(out)
            return

        visible_cards = state.enemy_hand + \
            [card for card in state.community_cards
                if card.revealed_to_enemy]

        current_damage = 0

        if len(visible_cards) >= 5:
            best = self.calculate_best_hand(state.enemy_hand, state.community_cards)
            current_damage += damage_calculation(best +  state.community_cards)[0]


        total_aggro = self.base_aggressiveness + current_damage \
            - state.round_state * self.base_round_multiplier \
            - state.pot * self.base_pot_multiplier

        if any(card.special for card in state.enemy_hand):
            special_sample = random.random()
            if special_sample < self.special_probability:
                return
        # do basic move
        success, out = self.do_basic_move(total_aggro, state)

        add_terminal_output(out)


def Bet(state: State, bet: int):
    if bet <= state.enemy_chips:
        state.enemy_chips -= bet
        state.enemy_last_bet = bet
        state.has_bet = True
        if bet == 0:
            state.has_checked = True
        else:
            state.has_checked = False
        return (state, True, f"{state.enemy.name} bet {bet}")
    else:
        return (state, False, "Insufficient Chips!")


def Fold(state: State):
    state.round_state = 3
    state.folded = 2
    return (state, True, "Enemy Folded")


def Call(state: State):
    if state.enemy_chips + state.enemy_last_bet >= state.player_last_bet:

        state.enemy_chips -= state.player_last_bet - state.enemy_last_bet
        state.enemy_last_bet = state.player_last_bet
        state.has_bet = False
        state.has_checked = False
        state.lead = 0
        return state, True, f"{state.enemy.name} called"
    else:
        return state, False, "Insufficient Chips!"


def All(state: State):
    if state.player_last_bet == 0:
        state.enemy_last_bet += state.enemy_chips
        state.enemy_chips = 0

    elif state.enemy_chips + state.enemy_last_bet < state.player_last_bet:
        state.enemy_last_bet += state.enemy_chips
        state.enemy_chips = 0
        state.player_chips += state.player_last_bet - state.enemy_last_bet
        state.player_last_bet = state.enemy_last_bet

    elif state.enemy_chips + state.enemy_last_bet > state.player_last_bet or \
        (state.player_chips == 0 and state.player_last_bet > 0):

        state.enemy_chips -= state.player_last_bet - state.enemy_last_bet
        state.enemy_last_bet = state.player_last_bet
    else:
        pass
    state.enemy_all_in = True
    state.round_state = 2
    state.has_bet = True
    return state, True, f"{state.enemy.name} went all in!"


def Raise(state: State, raise_val: int):
    if raise_val > state.player_last_bet and \
            raise_val <= state.enemy_last_bet + state.enemy_chips:
        state.enemy_chips -= raise_val - state.enemy_last_bet
        state.enemy_last_bet = raise_val
        return (state, True, f"{state.enemy.name} raised by {raise_val}")

    else:
        return (state, False, "Insufficient funds to raise")


def Play(state: State, card1:Card, card2:Card):
    if card1 == card2:
        return state, False, f"{state.enemy.name} played two same cards"

    for i, c in enumerate(state.enemy_hand):
        if card1.value == c.value and c.suit == card1.suit:
            break
        if i == len(state.enemy_hand) - 1:
            return (state, False, "Card is not in Hand!")

    for i, c in enumerate(state.enemy_hand):
        if card2.value == c.value and c.suit == card2.suit:
            break
        if i == len(state.enemy_hand) - 1:
            return (state, False, "Card is not in Hand!")

    state.enemy_play = [card1, card2]
    return state, True, f"{state.enemy.name} played his hand"


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
        for c in state.enemy_hand
    )
    return exists

def check_if_card_in_hand(state: State, card: Card):
    exists = any(
        c.suit == card.suit and
        c.value == card.value 
        for c in state.enemy_hand
    )
    return exists

def Reveal(state: State, index: int, card: Card):
    if not check_if_special_card_exists(state, card):
        return (state, False, f"{state.enemy.name} doesn't have that special card")
    if state.player_hand[index].revealed:
        return (state, False, "That Card is already revealed")

    state.player_hand[index].revealed_to_enemy = True

    for i, c in enumerate(state.enemy_hand):
        if c.value == card.value and c.suit == card.suit:
            state.enemy_hand[index].special = None
    
    return (state, False,
            f"Revealed {get_card_string(state.player_hand[index])}")
            


def Exchange(state: State, index: int, card: Card, special_card: Card):

    if not check_if_special_card_exists(state, special_card):
        return (state, False, "You don't have that special card")  
    elif not check_if_card_in_hand(state, card):
        return (state, False, "You do not have this card")
    else:
        for i, c in enumerate(state.enemy_hand):
            if c.value == special_card.value and c.suit == special_card.suit:
                state.enemy_hand[i].special = None
        
        enemy_index = next((i for i, c in enumerate(state.enemy_hand) if c.value == card.value))
        temp = state.enemy_hand[enemy_index]
        state.enemy_hand[enemy_index] = state.player_hand[index]
        state.enemy_hand[enemy_index].revealed = True
        state.player_hand[index] = temp
        state.player_hand[index].revealed = False
        return(state, True, 
               f"{state.enemy.name} Exchange {get_card_string(card)} with the player's {get_card_string(state.enemy_hand[enemy_index])}")
        

def Change_Suit(state: State, card_special: Card, card_target: Card, suit=None):
    suits = ["d","h","s","c"]
    
    if not check_if_special_card_exists(state, card_special):
        return (state, False, "You don't have that special card")
    if card_special.special != "change":
        return (state, False, "Not a valid card for change command")
    if not check_if_card_in_hand(state, card_target):
        return (state, False, "That card does not exist in your hand")
    for index, card in enumerate(state.enemy_hand):
        if card.value == card_special.value and card.suit == card_special.suit:
            state.enemy_hand[index].special = None
    if suit is None:
        for index, card in enumerate(state.enemy_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                suits_temp =  [s for s in suits if s != card_target.suit]
                random.shuffle(suits_temp)
                state.enemy_hand[index].suit = str(suits_temp[0])
        return (state, True, f"Changed {card_target}'s suit into a random suit '{suits_temp[0]}'")
    else:
        for index, card in enumerate(state.enemy_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                state.enemy_hand[index].suit = str(suit)
        return (state, True, f"Changed {card_target}'s suit into {suit}")
                

def Change_Value(state: State, card_special: Card, card_target: Card, value=None):
    
    values = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    
    if not check_if_special_card_exists(state, card_special):
        return (state, False, "You don't have that special card")
    
    if card_special.special != "change":
        return (state, False, "Not a valid card for change command")
    
    if not check_if_card_in_hand(state, card_target):
        return (state, False, "That card does not exist in your hand")
    
    for index, card in enumerate(state.enemy_hand):
        if card.value == card_special.value and card.suit == card_special.suit:
            state.enemy_hand[index].special = None
            
    
    if value is None:
        for index, card in enumerate(state.enemy_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                value_temp = [v for v in values if v != card_target.value]
                random.shuffle(value_temp)
                state.enemy_hand[index].value = value_temp[0]
                
        return (state, True, f"Changed {card_target}'s suit into a random value '{value_temp[0]}'")
    
    else:
        for index, card in enumerate(state.enemy_hand):
            if card.value == card_target.value and card.suit == card_target.suit:
                state.enemy_hand[index].value = value
                
        return (state, True, f"Changed {card_target}'s suit into {value}")


# Enemies
def LoadJeremy(state):
    state.enemy = Enemy(name="Jeremy")


def LoadBogart(state: State):
    state.enemy = Enemy(name="Bogart", base_aggressiveness=170)
    state.enemy_chips = 1000
    state.enemy_health = 1000


def LoadRicardoTolentinoGayagoy(state):
    state.enemy = Enemy(name="Ricardo Gayagoy", base_aggressiveness=200)
    state.enemy_chips = 3000
    state.enemy_health = 2000
    initial_cards = [
            Card(value="q", suit="h", revealed=False),
            Card(value="q", suit="s", revealed=False)
            ]

    state.enemy_deck += state.enemy_hand
    state.enemy_hand.clear()

    for card in initial_cards:
        card.revealed_to_enemy = True

    state.enemy_deck = [card for card in state.enemy_deck if card not in initial_cards]

    state.enemy_hand = initial_cards.copy()

    while len(state.enemy_hand) < 3:
        if state.enemy_deck[0] not in state.community_cards and state.enemy_deck[0] not in state.enemy_hand:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

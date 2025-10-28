from poker_game.state import State
from poker_game.card import Card
from poker_game.shop import populate_shop
from poker_game.game_handler import reset
from poker_game.enemy import LoadJeremy
from poker_game.enemy import LoadBogart
from poker_game.enemy import LoadRicardoTolentinoGayagoy
import curses

import copy
import random

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


# This populates enemy, player and community deck
def Give_Cards_Initial(state: State):
    card_value = ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]
    card_suit = ["d", "h", "s", "c"]
    deck = []

    for card in card_value:
        for suit in card_suit:
            deck.append(Card(suit=suit, value=card,
                             special=None, revealed=False))

    state.player_deck = copy.deepcopy(deck)
    state.enemy_deck = copy.deepcopy(deck)
    state.community_deck = copy.deepcopy(deck)

    random.shuffle(state.player_deck)
    random.shuffle(state.enemy_deck)
    random.shuffle(state.community_deck)

    for card in state.player_deck:
        card.revealed = True

    # Testing lang to para sa ui
    # state.enemy_deck[1].revealed = True

    # Selects the 3 community cards at the start of the game
    for _ in range(3):
        state.community_cards.append(state.community_deck.pop(0))

    # Gives the player 3 random cards
    while len(state.player_hand) != 3:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    #Special Test
    if state.cheats_enabled:
        state.player_hand[0].special = "exchange"
        state.player_hand[1].special = "reveal"
        state.player_hand[2].special = "change"

    # Gives the enemy 3 random cards
    while len(state.enemy_hand) != 3:
        if state.enemy_deck[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    state.player_health = 1000
    state.enemy_health = 1000

    state.player_chips = 1000
    state.enemy_chips = 1000

    return (state, True, "Successfull gave Initial Cards!")


def Start(state: State):
    if state.started and not state.game_lost:
        
        return (state, False, "You're already in the Game")
    if state.game_lost:
        state.win_count = 0
        state.game_lost = False
        state.in_game = True
        Give_Cards_Initial(state)
        return (state, True, "You've Restarted your Game")
    Give_Cards_Initial(state)
    LoadJeremy(state)
    state.view_prio = 'enemy'
    state.started = True
    state.in_game = True

    # Shop Development
    # state.in_game = False
    # state.in_shop = True
    # populate_shop(state)

    return (state, True, "Started a game of Gayagoy Gamblers! Goodluck")


def Bet(state: State, bet: int):
    if bet <= state.player_chips:
        state.player_chips -= bet
        state.player_last_bet = bet
        state.has_bet = True
        if bet == 0:
            state.has_checked = True
        return (state, True, f"You bet {bet}")
    else:
        
        return (state, False, "Insufficient Chips!")


def Fold(state: State):
    state.round_state = 3
    state.folded = 1
    state.has_bet = True
    return (state, True, "Fold Successful!")


def Call(state: State):
    if state.player_chips + state.player_last_bet >= state.enemy_last_bet:
        state.player_chips -= state.enemy_last_bet - state.player_last_bet 
        state.player_last_bet = state.enemy_last_bet
        state.lead = 1
        state.has_bet = False
        state.has_checked = False
        return (state, True, "Call Successful")
    else:
        
        return (state, False, "Insufficient Chips!")


def All(state: State):
    if state.enemy_last_bet == 0:
        state.player_last_bet += state.player_chips
        state.player_chips = 0

    elif state.player_chips + state.player_last_bet < state.enemy_last_bet:
        state.player_last_bet += state.player_chips
        state.player_chips = 0
        state.enemy_chips += state.enemy_last_bet - state.player_last_bet
        state.enemy_last_bet = state.player_last_bet

    elif (state.player_chips + state.player_last_bet > state.enemy_last_bet) or \
        (state.enemy_chips == 0 and state.enemy_last_bet > 0):
        state.player_chips -= state.enemy_last_bet - state.player_last_bet
        state.player_last_bet = state.enemy_last_bet

    else:
        pass

    state.player_all_in = True
    state.round_state = 2
    state.has_bet = True
    return (state, True, "You went All in")


def Raise(state: State, raise_val: int):
    if raise_val > state.enemy_last_bet and \
            raise_val <= state.player_last_bet + state.player_chips:
        state.player_chips -= raise_val - state.player_last_bet
        state.player_last_bet = raise_val
        return (state, True, f"You raised by {raise_val}")
    elif raise_val <= state.enemy_last_bet:
        
        return (state, False, f"Raise Commad Invalid! must be above {state.enemy_last_bet}")
    else:
        
        return (state, False, "Insufficient funds to raise")

def Play(state: State, card1:Card, card2:Card):
    if card1 == card2:
        
        return state, False, "You played two same cards"

    for i, c in enumerate(state.player_hand):
        if card1.value == c.value and c.suit == card1.suit:
            break
        if i == len(state.player_hand) - 1:
            
            return (state, False, "Card is not in Hand!")

    for i, c in enumerate(state.player_hand):
        if card2.value == c.value and c.suit == card2.suit:
            break
        if i == len(state.player_hand) - 1:
            
            return (state, False, "Card is not in Hand!")

    state.player_play = [card1, card2]
    return state, True, f"You played {get_card_string(card1)} and {get_card_string(card2)}"


def Buy(state: State, item_index: int):
    if item_index >= 3:
        
        return (state, False, f"Item {item_index} doesn't exist")
    item = state.shop_items[item_index]

    if item.price <= state.player_chips:
        state.player_chips -= item.price

        for item_card in item.cards:
            for card in state.player_deck:
                if card.value == item_card.value and card.suit == item_card.suit:
                    card.special = item.effect

        state.in_shop = False
        state.in_game = True
        reset(state)

        if state.win_count == 0:
            LoadJeremy(state)
        if state.win_count == 1:
            LoadBogart(state)
        if state.win_count == 2:
            LoadRicardoTolentinoGayagoy(state)

        return (state, True, f"You have bought an Item")
    else:
        
        return (state, False, "Insufficient Chips to Buy This Item")


def Inspect(state: State, card: Card):
    for i, c in enumerate(state.player_hand):
        if card.value == c.value and c.suit == card.suit:
            state.inspect_target = c
            state.view_prio = 'inspect'
            return (state, False, f"Inspecting {get_card_string(c)}")
        if i == len(state.player_hand) - 1:
            return (state, False, "Can't Inspect a card you don't have")
    
    return (state, False, "Empty Hand")


def Quit(state: State):
    state.exited = True
    return state, True, "Goodbye!"


def Help(state, command:str):
    help_string = ""
    match command:
        case 'start':
            help_string = ">start: This command starts the game."
        case 'help':
            help_string = ">help: Use help command to find out what this means."
        case 'bet':
            help_string = ">bet [value of chips to bet in int]: This commands bets a select number of chips."
        case 'fold':
            help_string = ">fold: This commands forfeits your hand for the round."
        case 'call':
            help_string = '''>call [value of chips to bet in int]: This commands matches the 
                             current bet of your opponent.'''
        case 'all':
            help_string = ">all: This commands bets all of your chips."
        case 'raise':
            help_string = '''>raise [value of chips to bet in int]: This command raise the value 
                             of your current bet.'''
        case 'buy':
            help_string = '''>buy [id of item in shop]: This command is used to purchase items 
                              within the shop menu.'''
        case 'play':
            help_string = '''>play [card identifier] [card identifier]: This command is used to play 2 
                              cards within your hand for the showdown of hands.'''
        case 'quit':
            help_string = ">quit: This command ends the program/game."
        case 'use':
            help_string = '''
            >use [card identifier] to change suit of [card identifier] to [(H,D,S,C)]
            >use [card identifier] to change value of  [card identifier] to [(1-10)|(J,Q,K,A)]
            >use [card identifier] to reveal [int(0-4)] 
            >use [card identifier] to exchange [int(0-4)] with [card identifier]
            >use [card identifier] to exchange [card identifier] with  [int(0-4)]:
            These commands use special card effects to modify cards within the game.'''
        case _:
            help_string = '''
            Multiline Test
            Hello
            '''

    return state, False, help_string

from poker_game.state import State 
from poker_game.card import Card
from poker_game.poker_hands import Find_Best_Pattern
from poker_game.damage_calculations import damage_calculation
from poker_game.damage_calculations import update_enemy_damage
from poker_game.damage_calculations import update_player_damage
import random


def reset(state: State):
    state.player_deck += state.player_hand
    state.enemy_deck += state.enemy_hand
    state.community_deck += state.community_cards

    state.player_hand.clear()
    state.enemy_hand.clear()
    state.community_cards.clear()

    random.shuffle(state.player_deck)
    random.shuffle(state.enemy_deck)
    random.shuffle(state.community_deck)

    for card in state.player_deck:
        card.revealed = True
        card.revealed_to_enemy = False

    for card in state.enemy_deck:
        card.revealed_to_enemy = True
        card.revealed = False

    for card in state.community_deck:
        card.revealed_to_enemy = False
        card.revealed = False

    for _ in range(3):
        state.community_cards.append(state.community_deck.pop(0))
        

    while len(state.player_hand) != 3:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    while len(state.enemy_hand) != 3:
        if state.enemy_deck[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    state.folded = 0
    state.has_bet = False
    state.player_all_in = False
    state.enemy_all_in = False
    state.win_check_available = False
    state.pot = 0
    state.round_state = 0
    state.enemy_damage = 0
    state.player_damage = 0
    state.player_last_bet = 0
    state.enemy_last_bet = 0


def reveal_community(state: State):
    for card in state.community_cards:
        card.revealed = True
        card.revealed_to_enemy = True
    return state


def draw_card(state: State, number_of_cards: int):

    while len(state.player_hand) != number_of_cards:
        if state.player_deck[0] not in state.community_cards:
            state.player_hand.append(state.player_deck.pop(0))
        else:
            state.player_deck.append(state.player_deck.pop(0))

    while len(state.enemy_hand) != number_of_cards:
        if state.enemy_hand[0] not in state.community_cards:
            state.enemy_hand.append(state.enemy_deck.pop(0))
        else:
            state.enemy_deck.append(state.enemy_deck.pop(0))

    return state


def update_round(state: State):
    if state.round_state == 0 and \
        state.has_bet and \
            (state.player_last_bet == state.enemy_last_bet
             and not state.has_checked):

        state.pot += state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state = reveal_community(state)
 
        state = draw_card(state, 4)

        state.round_state = 1
        state.has_bet = False

        return (state, True)
    elif state.round_state == 1 and \
        state.has_bet and \
            (state.player_last_bet == state.enemy_last_bet
             and not state.has_checked):

        state.pot += state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state.round_state = 2
        state = draw_card(state, 5)
        state.has_bet = False

        return (state, True)

    elif state.round_state == 2 and \
        state.has_bet and \
            ((state.player_last_bet == state.enemy_last_bet
             and not state.has_checked) or
                (state.player_all_in and state.enemy_all_in) or
                state.folded > 0):

        state.pot += state.player_last_bet + state.enemy_last_bet
        state.player_last_bet, state.enemy_last_bet = 0, 0

        state.round_state = 3
        
        return (state, True)
    elif state.round_state == 3 and \
            ((state.folded == 1 and not state.enemy_play) or
                (state.folded == 2 and not state.player_play) or
                    (not state.player_play and not state.enemy_play)):
        state = reveal_community(state)
        return (state, False)
    
    elif state.round_state == 3 and \
            ((state.folded == 1 and state.enemy_play) or
                (state.folded == 2 and state.player_play) or
                    (state.player_play and state.enemy_play)):
        state.win_check_available = True
        return (state, True)
    else:
        return (state, False)


def check_win(state: State):
    p_hand = state.player_play + state.community_cards
    e_hand = state.enemy_play + state.community_cards

    p_kicker = 0
    e_kicker = 0

    p_pattern = 'a ' + Find_Best_Pattern(p_hand)[0] \
        if state.folded != 1 else 'Folded'
    e_pattern = 'a ' + Find_Best_Pattern(e_hand)[0] \
        if state.folded != 2 else 'Folded'
    
    if state.folded != 1:
        p_kicker = update_player_damage(state)
        
    if state.folded != 2:
        e_kicker = update_enemy_damage(state)

    total_damage = state.player_damage - state.enemy_damage
    if total_damage == 0:
        total_damage = p_kicker - e_kicker
    damage_string = ""
    indiv_damage_string = ""

    if total_damage == 0:
        state.player_chips += state.pot//2
        state.enemy_chips += state.pot//2
        damage_string = f"You Have Tied! No Damage Dealt"
        indiv_damage_string = f"Enemy: {state.enemy_damage} Player: {state.player_damage}"

    if total_damage > 0:
        damage_string = f"You have damaged {state.enemy.name} for {abs(total_damage)}"
        indiv_damage_string = f"Enemy: {state.enemy_damage} Player: {state.player_damage}"
        state.enemy_health -= abs(total_damage)
        state.player_chips += state.pot
    else:
        indiv_damage_string = f"Enemy: {state.enemy_damage} Player: {state.player_damage}"
        damage_string = f"{state.enemy.name} has Damaged You for {abs(total_damage)}"
        state.player_health -= abs(total_damage)
        state.enemy_chips += state.pot

    state.game_finish_check_available = True
    state.win_check_available = False
    state.view_prio = 'last_win'
    reset(state)
    return f"You have {p_pattern} and the enemy has {e_pattern}", damage_string, indiv_damage_string


def check_if_game_finished(state: State):
    if state.player_chips <= 0 or \
        state.player_health <= 0 :
        return (state,"lost","You Lost the Game!")
    
    if state.enemy_chips <=  0 or \
        state.enemy_health <= 0:
        return (state,"won","You Won this Match")
    
    return (state,"ingame","Still in Game")
    

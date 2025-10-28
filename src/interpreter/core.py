from poker_game.state import State
from interpreter.parser import parser
from interpreter.tokenizer import lexer
import interpreter.semantic_analyzer as s
import interpreter.tokenizer as t
import poker_game.commands as commands
from poker_game.card import Card
import poker_game.special_commands as special_commands
from interpreter.parser import CardID
from interpreter.parser import AlphabetValue
from interpreter.parser import Number
import poker_game.special_commands as s_commands
from copy import deepcopy
import curses

round_to_move_map ={
        0: ['start', 'use', 'call', 'bet', 'all', 'fold'],
        1: ['start', 'use', 'call','bet', 'all', 'raise', 'fold'],
        2: ['start', 'use', 'call','bet', 'all', 'raise', 'fold'],
        3: ['start', 'use', 'play'],
        }

def get_card_from_string(cardstr: str):
    value = cardstr[:-1]
    suit = cardstr[-1]

    if value.isdigit():
        value = int(value)

    card = Card(suit=suit, value=value, revealed = False)
    return card


def interpret_command(input: str, state: State):
    input = input.lower()

    lexer.input(input)

    ast = parser.parse(input)

    if t.error:
        
        error = t.error
        t.error = None
        return False, str(error)

    if not ast:
        
        return False, "Syntax Error"

    valid = s.valid_semantics(ast)

    if not valid[0]:
        
        return False, valid[1]

    command = ast.command

    valid_moves = deepcopy(round_to_move_map[state.round_state])

    if not state.started:
        valid_moves = ['start']

    valid_moves.append('quit')
    valid_moves.append('help')

    if not state.has_bet and "call" in valid_moves:
        valid_moves.remove('call')

    if state.has_bet and "bet" in valid_moves:
        valid_moves.remove('bet')

    if not state.has_bet and "raise" in valid_moves:
        valid_moves.remove('raise')

    if state.in_shop:
        valid_moves = ['buy', 'quit']

    if command not in valid_moves:
        
        return False, f"You can't {command} right now"

    match command:
        case "start":
            state, is_success, out = commands.Start(state)
            return is_success, out
        case "bet":
            bet_amt = ast.target.num
            state, is_success, out = commands.Bet(state, bet_amt)
            return is_success, out
        case "fold":
            state, is_success, out = commands.Fold(state)
            return is_success, out
        case "call":
            state, is_success, out = commands.Call(state)
            return is_success, out
        case "all":
            state, is_success, out = commands.All(state)
            return is_success, out
        case "raise":
            raise_val = ast.target.num
            state, is_success, out = commands.Raise(state, raise_val)
            return is_success, out
        case "buy":
            item_index = int(ast.target.item[1])
            state, is_success, out = commands.Buy(state, item_index)
            return is_success, out
            pass
        case "inspect":
            # Inspect return false because it should be ignored by the enemy 
            # and game
            card = get_card_from_string(ast.target.value)
            state, success, out = commands.Inspect(state, card)
            return False, out 
        case "play":
            cards_str = ast.target
            cards = [get_card_from_string(c.value) for c in cards_str]
            state, is_success, out = commands.Play(state, cards[0], cards[1])
            return is_success, out
            pass
        case "quit":
            state, is_success, out = commands.Quit(state)
            return is_success, out
            pass
        case "use":
            special_card_command = ast.target
            action = special_card_command.action
            special_card = special_card_command.special_card
            action_name = action.action
            action_target = action.target

            special_card = get_card_from_string(special_card.value)

            match action_name:
                case "exchange":
                    special_card.special = "exchange"
                    index = None
                    card = None
                    if isinstance(action_target.target1, CardID):
                        index = action_target.target2.num
                        card = action_target.target1.value

                        card = get_card_from_string(card)
                    else:
                        index = action_target.target1.num
                        card = action_target.target2.value

                        card = get_card_from_string(card)

                    state, is_success, out = s_commands.Exchange(
                            state, index, card, special_card)
                    return False, out
                case "reveal":
                    special_card.special = "reveal"
                    index = action_target.num
                    state, is_success, out = s_commands.Reveal(
                            state, index, special_card)
                    return False, out
                case "change":
                    special_card.special = "change"
                    card = action_target.card_id.value
                    card = get_card_from_string(card)

                    change_value = None
                    change_key = action_target.change_key

                    if isinstance(action_target.change_value, Number):
                        change_value = action_target.change_value.num
                    else:
                        if action_target.change_value == "random":
                            change_value = None
                        else:
                            change_value = action_target.change_value.value

                    if action_target.change_key == "suit":
                        state, is_success, out = s_commands.Change_Suit(
                                state, special_card, card, change_value)
                        return False, out
                    else:
                        state, is_success, out = s_commands.Change_Value(
                                state, special_card, card, change_value)
                        return False, out

            return False, "You used a special command"
            pass
        case 'help':
            state, is_success, out = commands.Help(state, ast.target.value)
            return is_success, out
        case _:
            # if tapos na lahat ng commands, dapat unreachble toh
            return False, "Unknown Valid Command"

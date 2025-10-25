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
            return True, f"You bought Item {item_index}"
            pass
        case "inspect":
            # Inspect return false because it should be ignored by the enemy 
            # and game
            return False, "You inspected a card"
        case "play":
            return True, "You played your hand"
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

            value = special_card.value[:-1] 
            suit = special_card.value[-1]

            if value.isdigit():
                value = int(value)

            special_card = Card(suit=suit, value=value, revealed = False)

            match action_name:
                case "exchange":
                    special_card.special = "exchange"
                    index = None
                    card = None
                    if isinstance(action_target.target1, CardID):
                        index = action_target.target2.num
                        card = action_target.target1.value
                        value = card[:-1]  # everything except the last char
                        suit = card[-1]    # last char

                        if value.isdigit():
                            value = int(value)

                        card = Card(suit=suit, value=value, revealed = False)
                    else:
                        index = action_target.target1.num
                        card = action_target.target2.value

                        value = card[:-1]  # everything except the last char
                        suit = card[-1]    # last char

                        if value.isdigit():
                            value = int(value)

                        card = Card(suit=suit, value=value, revealed = False)

                    state, is_success, out = s_commands.Exchange(
                            state, index, card, special_card)
                    return is_success, out
                case "reveal":
                    special_card.special = "reveal"
                    index = action_target.num
                    state, is_success, out = s_commands.Reveal(
                            state, index, special_card)
                    return is_success, out
                case "change":
                    special_card.special = "change"
                    card = action_target.card_id.value
                    value = card[:-1]  # everything except the last char
                    suit = card[-1]    # last char

                    if value.isdigit():
                        value = int(value)

                    card = Card(suit=suit, value=value, revealed = False)

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
                        return is_success, out
                    else:
                        state, is_success, out = s_commands.Change_Value(
                                state, special_card, card, change_value)
                        return is_success, out

            return False, "You used a special command"
            pass
        case _:
            # if tapos na lahat ng commands, dapat unreachble toh
            return False, "Unknown Valid Command"

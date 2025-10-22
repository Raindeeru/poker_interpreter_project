from poker_game.state import State
from interpreter.parser import parser
from interpreter.tokenizer import lexer
import interpreter.semantic_analyzer as s
import interpreter.tokenizer as t
import poker_game.commands as commands
import poker_game.special_commands as special_commands


def interpret_command(input: str, state: State):
    input = input.lower()

    lexer.input(input)

    ast = parser.parse(input)

    if t.error:
        error = t.error
        t.error = None
        return str(error)

    if not ast:
        return "Syntax Error"

    valid = s.valid_semantics(ast)

    if not valid[0]:
        return valid[1]

    command = ast.command

    match command:
        case "start":
            state, is_success, out = commands.Start(state)
            return is_success, out
        case "bet":
            bet_amt = ast.target.num
            state, is_success, out  = commands.Bet(state, bet_amt)
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
            return is_succes, out
        case "buy": 
            item_index = int(ast.target.item[1])
            return f"You bought Item {item_index}"
            pass
        case "inspect":
            return "You inspected a card"
            pass
        case "play":
            return "You played your hand"
            pass
        case "quit ":
            return "Goodbye"
            pass
        case "use":
            special_command = ast.target.command
            return "You used a special command"
            pass
        case _:
            # if tapos na lahat ng commands, dapat unreachble toh
            return "Unknown Valid Command"

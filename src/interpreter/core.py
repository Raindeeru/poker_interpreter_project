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
            special_command = ast.target.command
            return False, "You used a special command"
            pass
        case _:
            # if tapos na lahat ng commands, dapat unreachble toh
            return False, "Unknown Valid Command"

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
            commands.Start(state)
            return "Started a game of Gayagoy Gamblers! Goodluck"
        case "bet":
            bet_amt = ast.target.num
            commands.Bet(state, bet_amt)
            return f"You bet {bet_amt}"
        case "fold":
            commands.Fold(state)
            return "You Folded!"
        case "call":
            commands.Call(state)
            return "You Called"
            pass
        case "all":
            commands.All(state)
            return "You went All In!"
            pass
        case "raise":
            raise_val = ast.target
            commands.Raise(state, raise_val)
            return f"You raised by {raise_val}"
            pass
        case "buy": 
            item_index = int(ast.target.item[1])
            commands.Buy(state, item_index)
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

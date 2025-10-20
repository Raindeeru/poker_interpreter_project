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
            return f"Game Started is {state.started}"
        case _:
            # if tapos na lahat ng commands, dapat unreachble toh
            return "Unknown Valid Command"

from poker_game.state import State
from interpreter.parser import parser
from interpreter.tokenizer import lexer
import interpreter.semantic_analyzer as s
import interpreter.tokenizer as t


def interpret_command(input: str, state: State):
    input = input.lower()

    lexer.input(input)

    parsed = parser.parse(input)

    if t.error:
        error = t.error
        t.error = None
        return str(error)

    if not parsed:
        return "Syntax Error"

    valid = s.valid_semantics(parsed)

    if not valid[0]:
        return valid[1]

    return "Valid Command"

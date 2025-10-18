import ply.lex as lex
from dataclasses import dataclass


@dataclass
class TokError:
    value: object
    position: int

error = None
error_found = False

tokens = (
    'COMMAND',
    'NUMBER',
    'ALPHA_VAL',
    'CARD_ID',
    'ITEM_ID',
    'SUIT',
    'CHANGE_KEY',
    'ACTION',
    'TO',
    'OF',
    'WITH',
)

t_ignore = ' \t'

def t_COMMAND(t):
    r'\b(start|bet|fold|call|all|raise|buy|inspect|play|quit|use)\b'
    return t

def t_NUMBER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_ALPHA_VAL(t):
    r'\b[jqka]\b'
    return t

def t_CARD_ID(t):
    r'\b(?:[2-9]|10|[jqka])[hdsc]\b'
    return t

def t_ITEM_ID(t):
    r'\bi\d+\b'
    return t


def t_SUIT(t):
    r'\b[hdsc]\b'
    return t

def t_CHANGE_KEY(t):
    r'\b(suit|value)\b'
    return t


def t_ACTION(t):
    r'\b(change|reveal|exchange)\b'
    return t


def t_TO(t):
    r'\bto\b'
    return t

def t_OF(t):
    r'\bof\b'
    return t

def t_WITH(t):
    r'\bwith\b'
    return t

def t_error(t):
    global error
    error = TokError(value=t.value[0], position=t.lexpos)
    error_found
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    while True:
        data = input("Enter command: ")
        if data == "exit":
            break
        
        lexer.input(data)
        for tok in lexer:
            print(tok)

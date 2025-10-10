from ply.lex import LexToken

rules = [
    #START
    ('S', ['COMMAND', 'U']),

    #U
    ('U', ['A']),
    ('U', ['CARD_ID', 'TO', 'P']),

    #A
    ('A', ['']),
    ('A', ['NUMBER']),
    ('A', ['ITEM_ID']),
    ('A', ['CARD_ID', 'A']),

    #P
    ('P', ['']),
    ('P', ['ACTION']),
    ('P', ['ACTION', 'C']),
    ('P', ['ACTION', 'E']),

    #C
    ('C', ['CHANGE_KEY', 'OF', 'CARD_ID', 'K']),
    #K
    ('K', ['']),
    ('K', ['TO', 'R']),
    #R
    ('R', ['NUMBER']),
    ('R', ['SUIT']),

    #E
    ('E', ['F', 'WITH', 'F']),
    #F
    ('F', ['CARD_ID']),
    ('F', ['NUMBER']),
]


def shift_reduce(tokens):
    stack = []

    def make_eof_token():
        t = LexToken()
        t.type = 'EOF'
        t.value = ''
        t.lineno = 0
        t.lexpos = 0
        return t

    input_tokens = list(tokens) + [make_eof_token()]
    pos = 0

    while pos < len(input_tokens):
        print(input_tokens[pos])
        stack.append(input_tokens[pos].type)
        pos += 1

        reduced = True
        while reduced:
            reduced = False
            for lhs, pattern in rules:

                if pattern and stack[-len(pattern):] == pattern:
                    stack[-len(pattern):] = [lhs]
                    reduced = True
                    break

                elif pattern == [] and lhs not in stack:
                    stack.append(lhs)
                    reduced = True
                    break

    return stack

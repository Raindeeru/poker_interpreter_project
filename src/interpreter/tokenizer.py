import string
import re
from dataclasses import dataclass
from typing import List, Optional
alphabet = list(string.ascii_letters + string.digits + " ")
@dataclass
class Token:
    type: str
    value: str
    line: int = 1
    column: int = 1
class Poker:
    def __init__(self):
        TOKENS = [
            ('START', r'\bstart\b', True),
            ('BET', r'\bbet\b', True),
            ('RAISE', r'\braise\b', True),
            ('FOLD', r'\bfold\b', True),
            ('CALL', r'\bcall\b', True),
            ('ALLIN', r'\ball\s+in\b', True),
            ('BUY', r'\bbuy\b', True),
            ('INSPECT', r'\binspect\b', True),
            ('PLAY', r'\bplay\b', True),
            ('QUIT', r'\bquit\b', True),
            ('USE', r'\buse\b', True),
            ('TO', r'\bto\b', True),
            ('OF', r'\bof\b', True),
            ('RANDOM', r'\brandom\b', True),
            ('REVEAL', r'\breveal\b', True),
            ('EXCHANGE', r'\bexchange\b', True),
            ('CARDS', r'[2-9TJQKA][CDHS]', False),
            ('RANK', r'[2-9TJQKA]', False)
            ('SUIT', r'[CDHS]', False)
            ('NUMBER', r'\d+', False),
            ('SHOP', r'[a-zA-Z_][a-zA-Z0-9_]*', False),
            ('WHITESPACE', r'\s+', False),
            ('COMMENT', r'#.*', False),
        ]
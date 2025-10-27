from dataclasses import dataclass, field
from typing import Union
from poker_game.state import State
from poker_game.card import Card
from typing import List

@dataclass
class Item:
    effect: str
    price: int
    cards : List[Card] = field(default_factory=list)

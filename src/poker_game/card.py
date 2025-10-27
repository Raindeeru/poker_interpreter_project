from dataclasses import dataclass
from typing import Union


@dataclass
class Card:
    suit: str
    value: Union[int, str]
    revealed: bool
    special: str = None
    revealed_to_enemy: bool = False 
    def __eq__(self, other):
            return isinstance(other, Card) and self.value == other.value and self.suit == other.suit

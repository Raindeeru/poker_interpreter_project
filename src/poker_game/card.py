from dataclasses import dataclass
from typing import Union


@dataclass
class Card:
    suit: str
    value: Union[int, str]
    special: str = None
    revealed: bool

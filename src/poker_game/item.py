from dataclasses import dataclass
from typing import Union
from poker_game.state import State
from poker_game.card import Card

@dataclass
class Item:
    card: Card
    price: int
    effect: str
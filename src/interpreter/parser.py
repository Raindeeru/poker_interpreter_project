from ply.lex import LexToken
from interpreter.tokenizer import tokens
import ply.yacc as yacc
from dataclasses import dataclass


@dataclass
class Command:
    command: str
    target: object = None


@dataclass
class Number:
    num: int


@dataclass
class AlphabetValue:
    value: str


@dataclass
class Suit:
    value: str


@dataclass
class ItemID:
    item: str


@dataclass
class CardID:
    value: str


@dataclass
class Action:
    action: str
    target: object = None


@dataclass
class SpecialCardCommand:
    special_card: CardID
    action: Action


@dataclass
class ChangeTarget:
    change_key: str
    card_id: CardID
    change_value: str = 'random'


@dataclass
class ExchangeTarget:
    target1: object
    target2: object


'''
Grammar:
S -> command U | command .
U -> number | item_id | card_id A | card_id | card_id to P .
A -> card_id A | card_id .
P -> action | action C | act E .
C -> change_key of card_id K| change_key of card_id .
K -> to R .
R -> number | suit | alpha_val .
E -> F with F .
F -> card_id | number.
'''


def p_s1(p):
    'S :  COMMAND U'
    p[0] = Command(command=p[1], target=p[2])


def p_s2(p):
    'S : COMMAND'
    p[0] = Command(command=p[1])


def p_u1(p):
    'U : NUMBER'
    p[0] = Number(p[1])


def p_u2(p):
    'U : ITEM_ID'
    p[0] = ItemID(p[1])


def p_u3(p):
    'U : CARD_ID A'
    p[0] = [CardID(value=p[1])] + p[2]


def p_u4(p):
    'U : CARD_ID'
    p[0] = CardID(value=p[1])


def p_u5(p):
    'U : CARD_ID TO P'
    p[0] = SpecialCardCommand(CardID(p[1]), p[3])


def p_a1(p):
    'A : CARD_ID A'
    p[0] = [CardID(value=p[1])] + p[2]


def p_a2(p):
    'A : CARD_ID'
    p[0] = [CardID(value=p[1])]


def p_p1(p):
    'P : ACTION'
    p[0] = Action(action=p[1])


def p_p2(p):
    'P : ACTION C'
    p[0] = Action(action=p[1], target=p[2])


def p_p3(p):
    'P : ACTION E'
    p[0] = Action(action=p[1], target=p[2])


def p_c1(p):
    'C : CHANGE_KEY OF CARD_ID K'
    p[0] = ChangeTarget(change_key=p[1], card_id=p[3], change_value=p[4])


def p_c2(p):
    'C : CHANGE_KEY OF CARD_ID'
    p[0] = ChangeTarget(change_key=p[1], card_id=p[3])


def p_k(p):
    'K : TO R'
    p[0] = p[2]


def p_r1(p):
    'R : NUMBER'
    p[0] = Number(num=p[1])


def p_r2(p):
    'R : SUIT'
    p[0] = Suit(value=p[1])


def p_r3(p):
    'R : ALPHA_VAL'
    p[0] = AlphabetValue(value=p[1])


def p_e(p):
    'E : F WITH F'
    p[0] = ExchangeTarget(p[1], p[3])


def p_f1(p):
    'F : NUMBER'
    p[0] = Number(num=p[1])


def p_f2(p):
    'F : CARD_ID'
    p[0] = CardID(value=p[1])


parser = yacc.yacc(debug=True)
# use 5h to change suit of 5h to s


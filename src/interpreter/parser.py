from ply.lex import LexToken
from interpreter.tokenizer import tokens
import ply.yacc as yacc

'''
Grammar:
S -> command U | command .
U -> number | item_id | card_id U | card_id | card_id to P .
P -> action | action C | act E .
C -> change_key of card_id K| change_key of card_id .
K -> to R .
R -> number | suit | alpha_val .
E -> F with F .
F -> card_id | number.
'''


def p_s1(p):
    'S :  COMMAND U'
    p[0] = (p[1], p[2])


def p_s2(p):
    'S : COMMAND'
    p[0] = (p[1])


def p_u1(p):
    'U : NUMBER'
    p[0] = (p[1])


def p_u2(p):
    'U : ITEM_ID'
    p[0] = (p[1])


def p_u3(p):
    'U : CARD_ID U'
    p[0] = (p[1], p[2])


def p_u4(p):
    'U : CARD_ID'
    p[0] = (p[1])


def p_u5(p):
    'U : CARD_ID TO P'
    p[0] = (p[1], p[2], p[3])


def p_p1(p):
    'P : ACTION'
    p[0] = (p[1])


def p_p2(p):
    'P : ACTION C'
    p[0] = (p[1], p[2])


def p_p3(p):
    'P : ACTION E'
    p[0] = (p[1], p[2])


def p_c1(p):
    'C : CHANGE_KEY OF CARD_ID K'
    p[0] = (p[1], p[2], p[3], p[4])


def p_c2(p):
    'C : CHANGE_KEY OF CARD_ID'
    p[0] = (p[1], p[2], p[3])


def p_k(p):
    'K : TO R'
    p[0] = (p[1], p[2])


def p_r1(p):
    'R : NUMBER'
    p[0] = (p[1])


def p_r2(p):
    'R : SUIT'
    p[0] = (p[1])


def p_r3(p):
    'R : ALPHA_VAL'
    p[0] = (p[1])


def p_e(p):
    'E : F WITH F'
    p[0] = (p[1], p[2], p[3])


def p_f1(p):
    'F : NUMBER'
    p[0] = (p[1])


def p_f2(p):
    'F : CARD_ID'
    p[0] = (p[1])


parser = yacc.yacc(debug=True)
# use 5h to change suit of 5h to s

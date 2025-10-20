import curses
import ui.layout as layout
from pathlib import Path
import interpreter.parser as p
from poker_game.state import State
import math

ART = Path(__file__).parent / "art"

OUT_OF_SCREEN_LENGTH = 20

card_border = None
special_card_border = None

start_screen = None

count = 0

cards = {}


def draw_art(pad, y, x, art):
    for i, line in enumerate(art.splitlines()):
        pad.addstr(y + i, x, line)

def draw_on_screen(pad, x, y, art):
    x += OUT_OF_SCREEN_LENGTH
    y += OUT_OF_SCREEN_LENGTH
    draw_art(pad, y, x, art)


def game_space_to_screen_space(x, y):
    center_x = (layout.MAIN_SCREEN_W + 2*OUT_OF_SCREEN_LENGTH)//2
    center_y = (layout.MAIN_SCREEN_H + 2*OUT_OF_SCREEN_LENGTH)//2

    return center_x + x, center_y - y


def draw_on_game(pad, x, y, art):
    x, y = game_space_to_screen_space(x, y)
    draw_art(pad, y, x, art)


def draw_card(pad, suit, value, y, x):
    global card_border
    global cards
    card_art = cards[suit][value]
    draw_on_game(pad, x, y, card_border)
    draw_on_game(pad, x+1, y+1, card_art)


def load_art():
    global card_border
    global special_card_border
    global start_screen
    content = (ART/"borders.txt").read_text(encoding="utf-8")

    parts = content.split('#')

    card_border = parts[0]
    special_card_border = parts[1]

    for suit in ["s", "c", "h", "d"]:
        card_value = {}
        for value in ["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]:

            card_value[value] = str(value) + " of " + suit

        cards[suit] = card_value

    start_screen = (ART/"start_screen.txt").read_text(encoding="utf-8")


load_art()


def draw_screen_pad():
    pad = curses.newpad(layout.MAIN_SCREEN_H + 2*OUT_OF_SCREEN_LENGTH,
                        layout.MAIN_SCREEN_W + 2*OUT_OF_SCREEN_LENGTH)

    for i in range(100):
        pad.addch((i % 26) + ord("a"))

    pad.noutrefresh(OUT_OF_SCREEN_LENGTH, OUT_OF_SCREEN_LENGTH,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad




def draw_start_screen(pad):
    global count
    global card_border

    pad.border()

    for x in [x * 0.1 for x in range(0, 10)]:
        y = int(math.sin(x))
        try:
            draw_on_game(pad, x*10, y*10, f"({x}, {y})")
        except:
            continue


def update_screen_pad(pad, state: State):
    global count
    global card_border
    count += 1
    pad.erase()

    if not state.started:
        draw_start_screen(pad)
    else:
        # dito na irerender yung in game stuff
        pad.addstr(0, 0, "Game Started!")
        pass

    pad.noutrefresh(OUT_OF_SCREEN_LENGTH, OUT_OF_SCREEN_LENGTH,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

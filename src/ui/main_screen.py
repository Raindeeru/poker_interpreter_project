import curses
import ui.layout as layout
from pathlib import Path
import interpreter.parser as p
from poker_game.state import State

ART = Path(__file__).parent / "art"

card_border = None
special_card_border = None

start_screen = None

count = 0

cards = {}


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
    pad = curses.newpad(100, 100)

    for i in range(100):
        pad.addch((i % 26) + ord("a"))

    pad.noutrefresh(0, 0,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad


def draw_art(pad, y, x, art):
    for i, line in enumerate(art.splitlines()):
        pad.addstr(y + i, x, line)


def draw_card(pad, suit, value, y, x):
    global card_border
    global cards
    card_art = cards[suit][value]
    draw_art(pad, y, x, card_border)
    draw_art(pad, y+1, x+1, card_art)


def draw_start_screen(pad):
    global count
    global card_border

    draw_art(pad, 0, layout.MAIN_SCREEN_W - ((count//800) % layout.MAIN_SCREEN_W), card_border)
    draw_art(pad, (count//1000) % layout.MAIN_SCREEN_H, (count//1000) % layout.MAIN_SCREEN_W, special_card_border)
    draw_card(pad, "h", "a", 4, layout.MAIN_SCREEN_W - ((count//1000) % layout.MAIN_SCREEN_W))
    draw_art(pad, 4, (count//500) % layout.MAIN_SCREEN_W, special_card_border)

    draw_art(pad, 2, 10, start_screen)


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

    pad.noutrefresh(0, 0,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

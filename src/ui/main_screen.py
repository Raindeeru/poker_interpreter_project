import curses
import ui.layout as layout
from pathlib import Path
import interpreter.parser as p
from poker_game.state import State
import math
import random

ART = Path(__file__).parent / "art"

OUT_OF_SCREEN_LENGTH = 40

FULL_WIDTH = 0
FULL_LENGTH = 0

card_border = None
special_card_border = None

start_screen = None

count = 0

cards = {}


def draw_art(pad, x, y, art):
    for i, line in enumerate(art.splitlines()):
        pad.addstr(y + i, x, line)


def get_art_dimensions(pad, x, y, art):
    width = 0
    height = 0
    for i, line in enumerate(art.splitlines()):
        width = max(width, len(line))
        height = i

    return width, height


def draw_art_centered(pad, x, y, art):
    x_offset, y_offset = get_art_dimensions(pad, x, y, art)
    draw_art(pad, x-(x_offset//2), y-(y_offset//2), art)


def draw_on_screen(pad, x, y, art):
    x += OUT_OF_SCREEN_LENGTH//2
    y += OUT_OF_SCREEN_LENGTH//2
    draw_art(pad, x, y, art)


def game_space_to_screen_space(x, y):
    center_x = (layout.MAIN_SCREEN_W + OUT_OF_SCREEN_LENGTH - 1)//2 - 1
    center_y = (layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH - 1)//2 - 1

    return center_x + x, center_y - y


def draw_on_game(pad, x, y, art):
    x, y = game_space_to_screen_space(x, y)
    draw_art(pad, x, y, art)


def draw_on_game_centered(pad, x, y, art):
    x, y = game_space_to_screen_space(x, y)
    draw_art_centered(pad, x, y, art)


def draw_card(pad, value, suit, x, y):
    global card_border
    global cards
    card_art = cards[suit][value]
    w, h = get_art_dimensions(pad, x, y, card_border)
    top = y + (w//2) - 1
    left = x - (h//2) - 1
    draw_on_game_centered(pad, x, y, card_border)
    draw_on_game(pad, left + 1, top - 1, card_art)


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
    global FULL_LENGTH
    global FULL_WIDTH
    pad = curses.newpad(layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH,
                        layout.MAIN_SCREEN_W + OUT_OF_SCREEN_LENGTH)

    FULL_LENGTH, FULL_WIDTH = layout.MAIN_SCREEN_H + 2*OUT_OF_SCREEN_LENGTH, \
        layout.MAIN_SCREEN_W + 2*OUT_OF_SCREEN_LENGTH

    for i in range(100):
        pad.addch((i % 26) + ord("a"))

    pad.noutrefresh(OUT_OF_SCREEN_LENGTH, OUT_OF_SCREEN_LENGTH,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad


def draw_cartesian_plane(pad):
    for i in range(-(layout.MAIN_SCREEN_W + OUT_OF_SCREEN_LENGTH)//2, (layout.MAIN_SCREEN_W + OUT_OF_SCREEN_LENGTH)//2):
        try:
            if i % 10 == 0:
                draw_on_game(pad, i, 0, "o")
            else:
                draw_on_game(pad, i, 0, "-")
        except:
            pass

    for i in range(-(layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH)//2, (layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH)//2):
        try:
            if i % 5 == 0:
                draw_on_game(pad, 0, i, "o")
            else:
                draw_on_game(pad, 0, i, "│")
        except:
            pass



def draw_start_screen(pad):
    global count
    global card_border

    pad.border()

    # Forbidden Graphing Calculator Code
    xs = range(
        -(FULL_WIDTH) // 2,
        (FULL_WIDTH) // 2
    )

    points = [int(5 * math.sin(x / 10)) for x in xs]

    for x, y in zip(xs, points):
        if y in range(-(layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH)//2,
                      (layout.MAIN_SCREEN_H + OUT_OF_SCREEN_LENGTH)//2):
            try:
                draw_on_game_centered(pad, x, y, "X")
            except:
                pass

    center = FULL_WIDTH // 2

    def random_card():
        values = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
        suits = ["h", "d", "s", "c"]
        return random.choice(values), random.choice(suits)

    cards = [
        ("a", "h", 100, 0),
        ("k", "s", 150, 20),
        ("5", "d", 200, -40),
        ("j", "c", 300, 60),
        ("3", "h", 120, -10),
        ("q", "d", 250, 40),
        ("7", "s", 180, -55),
        ("9", "c", 350, 70),
        ("2", "h", 160, 15),
        ("10", "d", 220, -25),
        ("4", "s", 280, 50),
        ("6", "c", 320, -65),
        ("8", "h", 190, 35),
        ("k", "d", 260, -50),
        ("a", "s", 300, 55),
        ("j", "h", 330, -20),
        ("5", "c", 210, 45),
        ("q", "s", 240, -35),
        ("9", "d", 270, 65),
        ("2", "c", 310, -60),
        ("10", "h", 340, 10),
        ("3", "s", 130, -30),
        ("k", "c", 290, 25),
        ("a", "d", 370, -45),
        ("7", "h", 180, 55),
        ("q", "c", 260, -20),
        ("4", "d", 150, 50),
        ("6", "h", 310, -70),
        ("9", "s", 200, 65),
        ("5", "h", 280, -35),
        ("j", "d", 230, 40),
        ("8", "s", 190, -60),
        ("10", "c", 330, 75),
        ("2", "d", 170, -50),
        ("a", "c", 220, 35),
        ("q", "h", 250, -45),
        ("7", "d", 300, 55),
        ("3", "c", 140, -25),
        ("9", "h", 270, 65),
        ("k", "h", 240, -40),
        ("5", "s", 310, 50),
        ("j", "s", 280, -60),
        ("4", "c", 160, 30),
        ("10", "s", 350, -70),
        ("8", "c", 200, 45),
        ("a", "h", 230, -55),
        ("q", "d", 270, 60),
        ("6", "s", 180, -30),
        ("2", "h", 320, 70),
        ("k", "s", 260, -65),
    ]

    for i, (val, suit, speed, offset) in enumerate(cards):
        try:
            x_pos = (((count // speed) + offset) % FULL_WIDTH) - center
            list_index = x_pos + center

            if i == 25:
                draw_on_game_centered(pad, 0, 0, start_screen)

            draw_card(pad, val, suit, x_pos, points[list_index])
        except Exception:
            pass

    if count % 1000 >= 500:
        draw_on_game_centered(pad, 0, -8, "Type \"START\" to play")



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

    #Debug Lines
    draw_on_screen(pad, 0, 0, "Test Debug String")
    draw_cartesian_plane(pad)

    pad.noutrefresh(OUT_OF_SCREEN_LENGTH//2, OUT_OF_SCREEN_LENGTH//2,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

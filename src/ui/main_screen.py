import curses
import ui.layout as layout
from pathlib import Path
import interpreter.parser as p
from poker_game.state import State
from poker_game.card import Card
import math
import random
import copy
ART = Path(__file__).parent / "art"

OUT_OF_SCREEN_LENGTH = 40

FULL_WIDTH = 0
FULL_LENGTH = 0

card_border = None
special_card_border = None
card_back = None

start_screen = None

count = 0

cards = {}

def load_art():
    global card_border
    global special_card_border
    global start_screen
    global card_back
    content = (ART/"borders.txt").read_text(encoding="utf-8")

    parts = content.split('#')

    card_border = parts[0]
    special_card_border = parts[1]

    base_card_full = (ART/"faces.txt").read_text(encoding="utf-8")
    base_card_art = base_card_full.split('#')

    suit_map = {
            "d": "♦",
            "h": "♥",
            "s": "♠",
            "c": "♣",
            }

    for suit in ["d", "h", "s", "c"]:
        card_value = {}
        for i, value in enumerate(["a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k"]):
            suited = copy.deepcopy(base_card_art[i])
            suited = suited.replace("X", suit_map[suit])
            card_value[value] = suited 
        cards[suit] = card_value

    start_screen = (ART/"start_screen.txt").read_text(encoding="utf-8")
    card_back = parts[2]


def random_display_card():
    values = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
    suits = ["h", "d", "s", "c"]
    speed = range(100, 200)
    offset = range(-50, 50)

    return random.choice(values), random.choice(suits), random.choice(speed), random.choice(offset)


display_cards = [random_display_card() for x in range(50)]


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
    bottom = y - (w//2)
    right = x + (h//2) + 1
    draw_on_game_centered(pad, x, y, card_border)
    draw_on_game(pad, left+1, top-1, card_art)


def draw_special_card(pad, value, suit, x, y, special_type):
    global special_card_border
    global cards
    card_art = cards[suit][value]
    w, h = get_art_dimensions(pad, x, y, special_card_border)
    top = y + (w//2) - 1
    left = x - (h//2) - 1
    bottom = y - (w//2)
    right = x + (h//2) + 1
    draw_on_game_centered(pad, x, y, special_card_border)
    draw_on_game(pad, left+1, top-1, card_art)
    draw_on_game(pad, left, top, special_type[0].upper())

def draw_unrevealed_card(pad, x, y):
    global card_border
    global cards
    global card_back
    w, h = get_art_dimensions(pad, x, y, card_border)
    draw_on_game_centered(pad, x, y, card_border)
    draw_on_game_centered(pad, x, y, card_back)


def get_and_draw_card(pad, card: Card, x, y):
    if card.revealed:
        if not card.special:
            draw_card(pad, card.value, card.suit, x, y)
        else:
            draw_special_card(pad, card.value, card.suit, x, y, card.special)
    else:
        draw_unrevealed_card(pad, x, y)




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

    center = FULL_WIDTH // 2
    for i, (val, suit, speed, offset) in enumerate(display_cards):
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


def draw_game_screen(pad, state: State):
    #community cards
    community_card_positions = [
            (-10, 0),
            (0, 0),
            (10, 0),
            ]

    next_player_card_pos = -layout.MAIN_SCREEN_W//2 + 8
    next_enemy_card_pos = layout.MAIN_SCREEN_W//2 - 8

    player_hand_height = -layout.MAIN_SCREEN_H//2 + 2
    enemy_hand_height = layout.MAIN_SCREEN_H//2 - 2

    for i, card in enumerate(state.community_cards):
        get_and_draw_card(pad, card,
                          community_card_positions[i][0],
                          community_card_positions[i][1])

    for i, card in enumerate(state.player_hand):
        get_and_draw_card(pad, card, next_player_card_pos, player_hand_height)
        next_player_card_pos += 10

    for i, card in enumerate(state.enemy_hand):
        get_and_draw_card(pad, card, next_enemy_card_pos, enemy_hand_height)
        next_enemy_card_pos -= 10

    # HUD

    draw_on_screen(pad, 0, layout.MAIN_SCREEN_H//2-2, f"Health: {state.player_health}".ljust(15))
    draw_on_screen(pad, 0, layout.MAIN_SCREEN_H//2-1, f"Chips: {state.player_chips}".ljust(15))
    draw_on_screen(pad, 0, layout.MAIN_SCREEN_H//2, f"Current Bet: {state.player_last_bet}".ljust(15))

    draw_on_screen(pad, layout.MAIN_SCREEN_W - 19, layout.MAIN_SCREEN_H//2-2,
                   f"Health: {state.enemy_health}".rjust(15))
    draw_on_screen(pad, layout.MAIN_SCREEN_W - 19, layout.MAIN_SCREEN_H//2-1,
                   f"Chips: {state.enemy_chips}".rjust(15))
    draw_on_screen(pad, layout.MAIN_SCREEN_W - 19, layout.MAIN_SCREEN_H//2,
                   f"Enemy Bet: {state.enemy_last_bet}".rjust(15))

    pot_center = len(str(f"Pot: {state.enemy_last_bet + state.player_last_bet}"))//2
    draw_on_screen(pad, layout.MAIN_SCREEN_W//2 - pot_center, 3,
                   f"Pot: {state.enemy_last_bet + state.player_last_bet}")



def update_screen_pad(pad, state: State):
    global count
    global card_border
    count += 1
    pad.erase()


    if not state.started:
        draw_start_screen(pad)
    else:
        # dito na irerender yung in game stuff
        draw_game_screen(pad, state)
        pass

    # Debug Lines
    # draw_cartesian_plane(pad)

    pad.noutrefresh(OUT_OF_SCREEN_LENGTH//2, OUT_OF_SCREEN_LENGTH//2,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

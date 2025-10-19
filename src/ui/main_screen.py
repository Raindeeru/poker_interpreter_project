import curses
import ui.layout as layout
from pathlib import Path

ART = Path(__file__).parent / "art"

card_border = None
special_card_border = None

count = 0


def load_art():
    global card_border
    global special_card_border
    content = (ART/"borders.txt").read_text(encoding="utf-8")

    parts = content.split('#')

    card_border = parts[0]
    special_card_border = parts[1]


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


def update_screen_pad(pad):
    global count
    global card_border
    count += 1
    pad.erase()

    draw_art(pad, 0, layout.MAIN_SCREEN_W - ((count//1000) % layout.MAIN_SCREEN_W), card_border)
    draw_art(pad, 5, (count//1000) % layout.MAIN_SCREEN_W, special_card_border)

    pad.noutrefresh(0, 0,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

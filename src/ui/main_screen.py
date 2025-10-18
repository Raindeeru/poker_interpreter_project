import curses
import ui.layout as layout

count = 0

def draw_screen_pad():
    pad = curses.newpad(100, 100)


    for i in range(100):
        pad.addch((i % 26) + ord("a"))

    pad.noutrefresh(0, 0,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

def update_screen_pad(pad):
    global count
    count += 1
    pad.erase()

    for i in range(100*99):
        pad.addch((i % 26) + ord("a"))

    pad.noutrefresh((count//100) % 100, 0,
                    1, 1,
                    layout.MAIN_SCREEN_H-2, layout.MAIN_SCREEN_W-2)

    return pad

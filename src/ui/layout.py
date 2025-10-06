# main screen 60 x 60
import curses

MAIN_SCREEN_W, MAIN_SCREEN_H = 100, 20
TERMINAL_W, TERMINAL_H = 100, 10
SIDEBAR_W, SIDEBAR_H = 20, (MAIN_SCREEN_H + TERMINAL_H)

TOTAL_W = MAIN_SCREEN_W + SIDEBAR_W
TOTAL_H = MAIN_SCREEN_H + TERMINAL_H

MAIN_SCREEN_X, MAIN_SCREEN_Y = 0, 0
TERMINAL_X, TERMINAL_Y = 0, MAIN_SCREEN_H
SIDEBAR_X, SIDEBAR_Y = MAIN_SCREEN_W, 0


class Screen:
    def __init__(self):
        self.main_screen = create_main_screen()
        self.terminal = create_terminal()
        self.sidebar = create_sidebar()


def update_screen(stdscr, screen: Screen):
    width, height = stdscr.getmaxyx()[1], stdscr.getmaxyx()[0]
    if width <= 100 or height <= 30:
        stdscr.erase()
        stdscr.attron(curses.color_pair(1))
        stdscr.box()
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(height//2, 1, "Beh and liit masyado ng screen mo ayusin mo naman")
        stdscr.noutrefresh()
        curses.doupdate()
        return

    stdscr.erase()
    stdscr.noutrefresh()

    update_window_box(screen.main_screen)
    update_window_box(screen.terminal)
    update_window_box(screen.sidebar)

    info = f"""
MAIN_SCREEN_W, MAIN_SCREEN_H = {MAIN_SCREEN_W}, {MAIN_SCREEN_H}
TERMINAL_W, TERMINAL_H       = {TERMINAL_W}, {TERMINAL_H}
SIDEBAR_W, SIDEBAR_H         = {SIDEBAR_W}, {SIDEBAR_H}

TOTAL_W, TOTAL_H             = {TOTAL_W}, {TOTAL_H}

MAIN_SCREEN_X, MAIN_SCREEN_Y = {MAIN_SCREEN_X}, {MAIN_SCREEN_Y}
TERMINAL_X, TERMINAL_Y       = {TERMINAL_X}, {TERMINAL_Y}
SIDEBAR_X, SIDEBAR_Y         = {SIDEBAR_X}, {SIDEBAR_Y}
"""

    for i, line in enumerate(info.strip().splitlines()):
        screen.main_screen.addstr(1 + i, 1, line)  # safely inside box
    screen.main_screen.noutrefresh()
    curses.doupdate()



def create_main_screen():
    screen = curses.newwin(MAIN_SCREEN_H,
                           MAIN_SCREEN_W,
                           MAIN_SCREEN_Y,
                           MAIN_SCREEN_X)

    screen.attron(curses.color_pair(1))
    screen.box()
    screen.attroff(curses.color_pair(1))

    return screen

def create_terminal():
    screen = curses.newwin(TERMINAL_H,
                           TERMINAL_W,
                           TERMINAL_Y,
                           TERMINAL_X)

    screen.attron(curses.color_pair(1))
    screen.box()
    screen.attroff(curses.color_pair(1))

    return screen

def create_sidebar():
    screen = curses.newwin(SIDEBAR_H,
                           SIDEBAR_W,
                           SIDEBAR_Y,
                           SIDEBAR_X)

    screen.attron(curses.color_pair(1))
    screen.box()
    screen.attroff(curses.color_pair(1))

    return screen

def update_window_box(window):
    window.erase()
    window.attron(curses.color_pair(1))
    window.box()
    window.attroff(curses.color_pair(1))
    window.noutrefresh()

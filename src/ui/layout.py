import curses
import ui.terminal as term
import ui.input as input

MAIN_SCREEN_W, MAIN_SCREEN_H = 85, 20
TERMINAL_W, TERMINAL_H = 85, 10
SIDEBAR_W, SIDEBAR_H = 35, (MAIN_SCREEN_H + TERMINAL_H)

TOTAL_W = MAIN_SCREEN_W + SIDEBAR_W
TOTAL_H = MAIN_SCREEN_H + TERMINAL_H

MAIN_SCREEN_X, MAIN_SCREEN_Y = 0, 0
TERMINAL_X, TERMINAL_Y = 0, MAIN_SCREEN_H
SIDEBAR_X, SIDEBAR_Y = MAIN_SCREEN_W, 0

SMALL_SCREEN_MESSAGE = "Screen too Small! Resize terminal please"

TEST_SCREEN = \
'''
                                                     │{`-√-`}│ │{`-√-`}│ │{`-√-`}│
 Health:                                             │{,-o-,}│ │{,-o-,}│ │{,-o-,}│
 Chips :                                             │{│≤│≥│}│ │{│≤│≥│}│ │{│≤│≥│}│
                                                     │Θ`-√-`Θ│ │Θ`-√-`Θ│ │Θ`-√-`Θ│
                                                     └───────┘ └───────┘ └───────┘
                                                                                  
                           ┌───────┐ ╔═══════╗ ┌───────┐                          
                           │10     │ ║10   +2║ │Θ,-o-,Θ│                          
                           │ Ω   Ω │ ║ Ω   Ω ║ │{│≤│≥│}│                          
                           │ Ω Ω Ω │ ║ Ω Ω Ω ║ │{`-√-`}│                          
                           │ Ω   Ω │ ║ Ω Ω Ω ║ │{,-o-,}│                          
                           │ Ω   Ω │ ║ Ω   Ω ║ │{│≤│≥│}│                          
                           │     10│ ║     10║ │Θ`-√-`Θ│                          
                           └───────┘ ╚═══════╝ └───────┘                          
┌───────┐ ╔═══════╗ ┌───────┐                                                     
│10     │ ║10   +2║ │Θ,-o-,Θ│                                                     
│ Ω   Ω │ ║ Ω   Ω ║ │{│≤│≥│}│                                                     
│ Ω Ω Ω │ ║ Ω Ω Ω ║ │{`-√-`}│                                                     
'''


class Screen:
    def __init__(self):
        self.main_screen = create_main_screen()
        self.terminal = create_terminal()
        self.sidebar = create_sidebar()


def update_screen(stdscr, screen: Screen):
    width, height = stdscr.getmaxyx()[1], stdscr.getmaxyx()[0]

    if width < TOTAL_W or height < TOTAL_H + 1:
        stdscr.erase()
        stdscr.attron(curses.color_pair(1))
        stdscr.box()
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(height//2, 1, SMALL_SCREEN_MESSAGE)
        stdscr.noutrefresh()
        curses.doupdate()
        return Screen()

    stdscr.erase()
    stdscr.noutrefresh()

    update_window_box(screen.main_screen)
    update_window_box(screen.sidebar)
    update_window_box(screen.terminal)

    # Dito natin iuupdate yung ui based sa game state
    # I display yung cards
    # output ng last commands sa screen, sa terminal, sa sidebar
    # mga ganun

    for i, line in enumerate(TEST_SCREEN.splitlines()):
        screen.main_screen.addstr(i, 1, line)

    screen.main_screen.noutrefresh()

    show_terminal_output(screen.terminal)
    show_terminal_input(screen.terminal)

    screen.terminal.noutrefresh()

    return screen


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


def show_terminal_output(terminal):
    for i, line in enumerate(term.terminal_history):
        terminal.move(i + 1, 1)
        terminal.addstr(line)


def show_terminal_input(terminal):
    terminal.hline(TERMINAL_H - 3, 1, ord("-"), TERMINAL_W-2)
    terminal.move(TERMINAL_H - 2, 1)
    terminal.addstr(f"> {input.input_str}")

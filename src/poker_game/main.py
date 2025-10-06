import curses
from curses import wrapper
import ui.layout as layout
import ui.input as input

# mga shit dito imomove dapat sa ibang files, tinetesting ko lang
# basta yung main file dapat esentially magstart lang magrun
# tas yung input, yung program loop, dapat mga separate yan
# para mas organized
# gagawa tayo gamestate class, sa init mag iinit tayo ng object nun


def run(stdscr):
    screen = layout.Screen()

    while True:
        layout.update_screen(stdscr, screen)

        try:
            key = stdscr.getkey()
            if key == "q":
                break
        except curses.error:
            pass


def init(stdscr):
    # Para kay Derven 'to na line kasi transparent yung
    # background ng terminal niya hahaha
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.nodelay(True)

    run(stdscr)


def main():
    wrapper(init)


if __name__ == "__main__":
    main()

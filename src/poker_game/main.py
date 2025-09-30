import curses
from curses import wrapper

# mga shit dito imomove dapat sa ibang files, tinetesting ko lang
# basta yung main file dapat esentially magstart lang magrun
# tas yung input, yung program loop, dapat mga separate yan
# para mas organized


def run(stdscr):
    win = curses.newwin(20, 20, 2, 2)
    stdscr.nodelay(True)  # don't block on getkey

    while True:
        win.erase()
        win.attron(curses.color_pair(1))
        win.box()
        win.attroff(curses.color_pair(1))

        width, height = stdscr.getmaxyx()[1], stdscr.getmaxyx()[0]
        size = width * height
        win.addstr(1, 1, f"Width: {width}, Height: {height}, Size: {size}")

        win.noutrefresh()
        curses.doupdate()

        try:
            key = stdscr.getkey()
            if key == "q":
                break
        except curses.error:
            # no input this frame
            pass


def init(stdscr):
    # Para kay Derven 'to na line kasi transparent yung
    # background ng terminal niya hahaha
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    run(stdscr)


def main():
    wrapper(init)


if __name__ == "__main__":
    main()

import curses


def handle_input(key, terminal):
    terminal.move(0, 0)
    terminal.addstr(key)
    terminal.noutrefresh
    curses.doupdate()

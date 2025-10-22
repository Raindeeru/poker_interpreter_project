import curses
from curses import wrapper
import ui.layout as layout
import ui.input as input
import poker_game.state
import poker_game.game_handler as g

# gagawa tayo gamestate class, sa init mag iinit tayo ng object nun

game_state = poker_game.state.State()


def run(stdscr):
    screen = layout.Screen()

    while True:
        try:
            key = stdscr.getkey()
            if key == "q":
                break
            input.handle_input(key, screen.terminal, game_state)
        except curses.error:
            pass
        
        g.update_enemy(state)

        g.update_round(state)

        g.update_game(state)


        screen = layout.update_screen(stdscr, screen, game_state)
        curses.doupdate()


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

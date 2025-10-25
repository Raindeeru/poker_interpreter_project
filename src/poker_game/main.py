import curses
from curses import wrapper
import ui.layout as layout
import ui.input as input
import poker_game.state
import poker_game.game_handler as g
from poker_game.enemy import Enemy

# gagawa tayo gamestate class, sa init mag iinit tayo ng object nun

game_state = poker_game.state.State()


def run(stdscr):
    screen = layout.Screen()

    while True:
        # handle player input
        command_success = False
        try:
            key = stdscr.getkey()
            command_success = input.handle_input(key, screen.terminal, game_state)
            if game_state.exited:
                break
        except curses.error:
            pass

        if command_success and game_state.has_bet:
            # update enemy and game
            game_state.enemy.decide_next_move(game_state)

        screen = layout.update_screen(stdscr, screen, game_state)
        curses.doupdate()


def init(stdscr):
    # Para kay Derven 'to na line kasi transparent yung
    # background ng terminal niya hahaha
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.nodelay(True)
    game_state.enemy = Enemy(name="Jeremy")

    run(stdscr)


def main():
    wrapper(init)


if __name__ == "__main__":
    main()

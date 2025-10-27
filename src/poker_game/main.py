import curses
from curses import wrapper
import ui.layout as layout
import ui.input as input
import poker_game.state
import poker_game.game_handler as g
from poker_game.enemy import LoadJeremy
from poker_game.shop import populate_shop
from ui.terminal import add_terminal_output

# gagawa tayo gamestate class, sa init mag iinit tayo ng object nun

game_state = poker_game.state.State()


def run(stdscr):
    global game_state
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
            #check round state if its viable to change
            check_update = g.update_round(game_state)
            if check_update[1]:
                game_state = check_update[0]
            else:
                # update enemy and game
                game_state.enemy.decide_next_move(game_state)
                check_update = g.update_round(game_state)
                
                if check_update[1]:
                    game_state = check_update[0]
            
        if game_state.round_state == 3 and \
            (game_state.folded > 0 or (game_state.player_all_in and game_state.enemy_all_in)):
            g.handle_skip_to_round_3(game_state)

        if game_state.win_check_available:
            pattern_out, damage_out, indiv_out = g.check_win(game_state)
            add_terminal_output(pattern_out)
            add_terminal_output(damage_out)
            add_terminal_output(indiv_out)
            
        if game_state.game_finish_check_available:
            check_final_win = g.check_if_game_finished(game_state)
            if game_state.started and check_final_win[1] == "won":
                add_terminal_output(str(check_final_win[2]))
                game_state.win_count += 1
                if game_state.win_count < 3:
                    game_state.in_shop = True
                    game_state.in_game = False
                    populate_shop(game_state)
            elif game_state.started and check_final_win[1] == "lost":
                add_terminal_output(str(check_final_win[2]))
                game_state.in_game = False
                game_state.game_lost = True
            else:
                pass
            
            game_state.game_finish_check_available = False

        screen = layout.update_screen(stdscr, screen, game_state)
        curses.doupdate()


def init(stdscr):
    # Para kay Derven 'to na line kasi transparent yung
    # background ng terminal niya hahaha
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.nodelay(True)

    LoadJeremy(game_state)
    run(stdscr)


def main():
    wrapper(init)


if __name__ == "__main__":
    main()

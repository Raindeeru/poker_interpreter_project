from poker_game.state import State
from pathlib import Path
ART = Path(__file__).parent / "art"


def draw_art(sidebar, x, y, art):
    for i, line in enumerate(art.splitlines()):
        sidebar.addstr(y + i, x, line)


def draw_hello(sidebar, state: State):
    hello = (ART/"hello.txt").read_text(encoding="utf-8")
    draw_art(sidebar, 1, 1, hello)

def draw_inspect(sidebar, state: State):
    draw_art(sidebar, 1, 1, "ispect")
    pass


def draw_enemy(sidebar, state: State):
    enemy_text = f'''
    Enemy: {state.win_count + 1}: {state.enemy.name}
    '''
    draw_art(sidebar, 1, 1, enemy_text)
    pass


def draw_last_win(sidebar, state: State):
    draw_art(sidebar, 1, 1, "last win")
    pass


def update_sidebar(sidebar, state: State):
    to_view = state.view_prio
    match to_view:
        case 'hello':
            draw_hello(sidebar, state)
        case 'inspect':
            draw_inspect(sidebar, state)
        case 'enemy':
            draw_enemy(sidebar, state)
        case 'last_win':
            draw_last_win(sidebar, state)
    sidebar.noutrefresh()
    return sidebar

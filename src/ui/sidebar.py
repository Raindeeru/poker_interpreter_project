from poker_game.state import State
from pathlib import Path
import ui.layout as layout
ART = Path(__file__).parent / "art"


suit_map = {
        "d": "♦",
        "h": "♥",
        "s": "♠",
        "c": "♣",
        }

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
    enemy_text = f'''Enemy {state.win_count + 1}: {state.enemy.name}
---------------------------------
Health = {state.enemy_health} / 1000 HP
Chips = {state.enemy_chips}
Last Bet = {state.enemy_last_bet}
Aggressiveness = {'Low' if state.enemy.base_aggressiveness < 120
        else 'High' if state.enemy.base_aggressiveness > 150
        else 'Normal'}
'''
    draw_art(sidebar, 1, 1, enemy_text)

def get_hand_str(hand):
    hand_str = ""
    for card in hand:
        hand_str += f"{str(card.value).upper()}{suit_map[card.suit]} "
    return hand_str

def draw_last_win(sidebar, state: State):
    line = "-----Last-Win--------------------"
    draw_art(sidebar, 1, layout.SIDEBAR_H//2, line)
    if state.last_winner == 0:
        return
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 1, f"{'You' if state.last_winner == 1 else state.enemy.name}")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 2 ,f"{get_hand_str(state.last_winning_hand)}")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 3, "------")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 4 ,f"Player Hand: {get_hand_str(state.last_player_hand)}")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 5 ,f"{state.last_player_pattern}")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 6 ,f"Enemy Hand: {get_hand_str(state.last_enemy_hand)}")
    draw_art(sidebar, 1, layout.SIDEBAR_H//2 + 7 ,f"{state.last_enemy_pattern}")


def update_sidebar(sidebar, state: State):
    to_view = state.view_prio
    match to_view:
        case 'hello':
            draw_hello(sidebar, state)
        case 'inspect':
            draw_inspect(sidebar, state)
        case 'enemy':
            draw_enemy(sidebar, state)

    if to_view != 'hello':
        draw_last_win(sidebar, state)
    sidebar.noutrefresh()
    return sidebar

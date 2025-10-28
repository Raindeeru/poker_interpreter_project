import curses
import string
from interpreter.core import interpret_command
from ui.terminal import add_terminal_output
from poker_game.state import State

alphabet = list(string.ascii_letters + string.digits + " ")

max_str_len = 80
input_str = ""

input_history = []
input_hist_position = 0

cursor_pos = 0


def handle_input(key, terminal, state: State):
    global input_str
    global input_hist_position
    global cursor_pos

    if key in ('KEY_BACKSPACE', '\b', '\x7f'):
        if len(input_str) > 0 and abs(cursor_pos) <= len(input_str):
            if cursor_pos == 0:
                input_str = input_str[:-1]
            else:
                idx = len(input_str) + cursor_pos
                input_str = input_str[:idx-1] + input_str[idx:]
        input_hist_position = 0
        return False

    if key in ('KEY_UP'):
        if input_history:
            if input_hist_position < len(input_history):
                input_hist_position += 1
                input_str = input_history[-input_hist_position]

    if key in ('KEY_DOWN'):
        if input_history:
            if input_hist_position > 1:
                input_hist_position -= 1
                input_str = input_history[-input_hist_position]
            else:
                input_hist_position = 0
                input_str = ""

    if key in ('KEY_LEFT'):
        if cursor_pos <= 0 and abs(cursor_pos) <= len(input_str):
            cursor_pos -= 1
        return False

    if key in ('KEY_RIGHT'):
        if cursor_pos < 0:
            cursor_pos += 1
        return False

    if key == "\n":
        if not input_str:
            return False
        input_hist_position = 0
        cursor_pos = 0
        # dito na magsesend ng string sa interpreter
        # interpreter.interpret(input_str) or something like that
        is_success, out = interpret_command(input_str, state)
        add_terminal_output(out)
        input_history.append(input_str)
        input_str = ""
        return is_success

    if key not in alphabet:
        return False

    # dapat hinahandle niya ng maayos mga input
    if len(input_str) < max_str_len:
        if cursor_pos == 0:
            input_str += key
        else:
            idx = len(input_str) + cursor_pos  # convert relative cursor position
            input_str = input_str[:idx] + key + input_str[idx:]

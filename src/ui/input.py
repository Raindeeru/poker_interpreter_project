import curses
import string
from interpreter.core import interpret_command
from ui.terminal import add_terminal_output

alphabet = list(string.ascii_letters + string.digits + " ")

max_str_len = 80
input_str = ""

def handle_input(key, terminal):
    global input_str

    if key in ('KEY_BACKSPACE', '\b', '\x7f'):
        input_str = input_str[:-1]

    if key == "\n":
        # dito na magsesend ng string sa interpreter
        # interpreter.interpret(input_str) or something like that
        out = interpret_command(input_str, None)
        add_terminal_output(out)
        input_str = ""

    if key not in alphabet:
        return

    # dapat hinahandle niya ng maayos mga input
    if len(input_str) >= max_str_len:
        return
    input_str += key

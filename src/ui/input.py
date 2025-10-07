import curses

input_str = ""


def handle_input(key, terminal):
    global input_str
    input_str += key

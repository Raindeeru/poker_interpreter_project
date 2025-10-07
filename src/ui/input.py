import curses

input_str = ""


def handle_input(key, terminal):
    global input_str

    # dapat hinahandle niya ng maayos mga input
    input_str += key

terminal_history = []

def add_terminal_output(str):
    terminal_history.append(str)
    if len(terminal_history) >= 7:
        terminal_history.pop(0)

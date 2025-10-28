terminal_history = []

def add_terminal_output(str):
    for line in str.splitlines():
        if not line:
            continue
        terminal_history.append(line.strip())
    if len(terminal_history) >= 7:
        terminal_history.pop(0)

import interpreter.parser as p


def check_bet_valid(target):
    if target is p.Number:
        return True
    else:
        return (False, "Wrong Target on the Bet Command!")


def check_quit_valid(target):
    if target is None:
        return True
    else:
        return (False, "Quit has targets!")

def check_use_valid(target):
    if isinstance(target, p.SpecialCardCommand):
        return True
    else:
        return (False, "Use command must target valid card")


def valid_semantics(ast):
    if ast.command == "bet":
        return check_bet_valid(ast.target)
    
    if ast.command == "use":
        return check_use_valid(ast.target)
    

    pass


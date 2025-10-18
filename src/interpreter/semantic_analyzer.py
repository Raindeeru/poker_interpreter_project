import interpreter.parser as p


def check_bet_valid(target):
    if isinstance(target, p.Number):
        return (True, "Valid bet command")
    else:
        return (False, "Wrong target on the bet command! Must be a number.")


def check_quit_valid(target):
    if target is None:
        return True
    else:
        return (False, "Quit has targets!")

def check_action_valid(action):
    if not isinstance(action, p.Action):
        return (False, "Invalid Action structure")
    if action.action != "change":
        return (False, f"Unsupported Action: '{action.action}'")
    return (True, "Valid action")


#CHANGE
def check_change_valid(change: p.ChangeTarget):
    valid_keys = ["suit"]
    if change.change_key not in valid_keys:
        return (False, f"Invalid key '{change.change_key}'. Must be 'suit'.")
    if not isinstance(change.card_id, p.CardID):
        return (False, "Invalid target card ID in change command.")
    if change.change_value != 'random':
        if not isinstance(change.change_value, (p.Suit, p.AlphabetValue, p.Number)):
            return (False, f"Invalid change value: {change.change_value}.")
    return (True, "Valid change target")


#USE
def check_use_valid(target):
    if not isinstance(target, p.SpecialCardCommand):
        return (False, "Use command must target valid card")

    result = check_action_valid(target.action)
    if result is not True:
        return result

    result = check_change_valid(target.action.target)
    if result[0] is False:
        return result

    return (True, "Valid use command")


def valid_semantics(ast):
    if ast.command == "bet":
        return check_bet_valid(ast.target)
    
    if ast.command == "use":
        return check_use_valid(ast.target)
    

    pass


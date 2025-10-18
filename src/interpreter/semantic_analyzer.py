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


def check_value_change(value):
    valid_suit = ['h', 'd', 'c', 's']
    
    if not isinstance(value, p.Suit):
        return (False, "Invalid suit used in change action")
    if value.value not in valid_suit:
        return (False, f"Invalid suit '{value.value}' used in change action")
    else:
        return (True, "Valid command")

def check_card_id_valid(target):
    if not isinstance(target.card_id, p.CardID):
        return (False, "Invalid CardID used in change action")
    else:
        return check_value_change(target.change_value)
        
        
def check_change_valid(target):
    valid_keys = ["suit"]
    
    if not isinstance(target, p.ChangeTarget):
        return (False, "Invalid target for change action")
    
    if target.change_key not in valid_keys:
        return (False, f"Invalid key '{target.change_key}'. Must be 'suit'.")
    else:
        return check_card_id_valid(target)
   


def check_action_valid(action):
    if not isinstance(action, p.Action):
        return (False, "Invalid Action Used")
    
    if action.action == "change":
        return check_change_valid(action.target)
    
    return (False, f"Invalid action '{action.action}' used in special card command")


def check_use_valid(target):
    if not isinstance(target, p.SpecialCardCommand):
        return (False, "Use command must target valid card")
    elif not isinstance(target.special_card, p.CardID):
        return (False, "Special card must be a valid CardID")
    else:
        return check_action_valid(target.action)


def valid_semantics(ast):
    if ast.command == "bet":
        return check_bet_valid(ast.target)
    
    if ast.command == "use":
        return check_use_valid(ast.target)
    

    pass


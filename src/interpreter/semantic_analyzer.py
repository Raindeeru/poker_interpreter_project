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

#####################################################################################################################
#Error checks for the commands
#use [card identifier] to change suit of [card identifier] to [{random} | specific suit(H,D,S,C)]
#use [card identifier] to change values of  [card identifier] to [{random} | int(1-10) | value(J,Q,K,A)]
#use [card identifier] to reveal int(0-4)


def check_card_id_valid(target):
    if not isinstance(target.card_id, p.CardID):
        return (False, "Invalid CardID used in change action")
    else:
        return (True, "Command is Valid!")
        

def check_change_valid(target):
    valid_keys = ["suit","value"]
    valid_suits = ['h', 'd', 'c', 's']
    valid_values = ['a', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'j', 'q', 'k']
    
    if not isinstance(target, p.ChangeTarget):
        return (False, "Invalid target for change action")
    
    if target.change_key not in valid_keys:
        return (False, f"Invalid key '{target.change_key}'. Must be 'suit'.")
    
    if target.change_value == "random":
        return True
    
    match target.change_key:
        case "suit":
            if target.change_value.value not in valid_suits:
                return (False, f"Invalid suit '{target.change_value.value}' used in change action")
            
            return check_card_id_valid(target)
        case "value":
            if target.change_value.num not in valid_values:
                return (False, f"Invalid value used in change action")
            
            return check_card_id_valid(target)
        case _:
            return (False, "Invalid change key used in change action")


def check_reveal_valid(target):
    if not isinstance(target, p.Number):
        return (False, "Invalid target for reveal action")
    elif target.num not in [0, 1, 2, 3, 4]:
        return (False, "Reveal target must be an integer between 0 and 4") 
    else:  
        return (True, "Reveal Command is Valid!")
    

def check_action_valid(action):
    if not isinstance(action, p.Action):
        return (False, "Invalid Action Used")
    
    if action.action == "change":
        return check_change_valid(action.target)
    elif action.action == "exchange":
        return None
    elif action.action == "reveal":
        return check_reveal_valid(action.target)
    else:
        return (False, f"Invalid action '{action.action}' used in special card command")


def check_use_valid(target):
    if not isinstance(target, p.SpecialCardCommand):
        return (False, "Use command must target valid card")
    elif not isinstance(target.special_card, p.CardID):
        return (False, "Special card must be a valid CardID")
    else:
        return check_action_valid(target.action)
    
######################################################################################################################


def valid_semantics(ast):
    if ast.command == "bet":
        return check_bet_valid(ast.target)
    
    if ast.command == "use":
        return check_use_valid(ast.target)
    

    pass


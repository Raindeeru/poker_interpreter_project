import interpreter.parser as p


def check_bet_valid(target):
    if isinstance(target, p.Number):
        return (True, "Valid bet command")
    else:
        return (False, "Wrong target on the bet command! Must be a number.")


def check_quit_valid(target):
    if target is None:
        return (True, "Quitted")
    else:
        return (False, "Quit has targets!")


def check_start_valid(target):
    if target is None:
        return (True, "Game started!")
    else:
        return (False, "Invalid start command!")


def check_fold_valid(target):
    if target is None:
        return (True, "valid command")
    else:
        return (False, "Invalid fold command!")


def check_all_valid(target):
    if target is None:
        return (True, "valid command")
    else:
        return (False, "Invalid all command!")


def check_call_valid(target):
    if isinstance(target, p.Number):
        return (True, "Valid call command")
    else:
        return (False, "Invalid call command")
    
def check_buy_valid(target):
    if isinstance(target, p.ItemID):
        return (True, "Valid buy command")
    else:
        return (False, "Invalid buy command")
    
def check_raise_valid(target):
    if isinstance(target, p.Number):
        return (True, "Valid raise command")
    else:
        return (False, "Invalid raise command")

def check_play_valid(target):
    if isinstance(target, list) and len(target) == 2:
        if isinstance(target[0], p.CardID) and isinstance(target[1], p.CardID):
            return (True, "Command is Valid!")
        else:
            return (False, "Invalid Play Command")
    else: 
        return (False, "Invalid Play Command! you must input 2 Cards")
    
def check_inspect_valid(target):
    if isinstance(target, p.CardID):
        return (True, "Valid inspect Commad!")
    else:
        return (False, "Invalid inspect Command!")

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
            if not isinstance(target.change_value, p.AlphabetValue):
                if target.change_value.num not in valid_values:
                    return (False, f"Invalid value used in change action")
            else:
                if target.change_value.value not in valid_values:
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
    
def check_exchange_valid(target):
    if not isinstance(target, p.ExchangeTarget):
        return (False, "Not a valid target!")
    elif isinstance(target.target1, p.Number ) and isinstance(target.target2, p.CardID):
        if target.target1.num not in [0, 1, 2, 3, 4]:
            return (False, "Exchange target must be an integer between 0 and 4") 
        return (True, "Exchange command is Valid!")
    
    elif isinstance(target.target1, p.CardID ) and isinstance(target.target2, p.Number):
        if target.target2.num not in [0, 1, 2, 3, 4]:
            return (False, "Exchange target must be an integer between 0 and 4") 
        return (True, "Exchange command is Valid!")
    else:
        return (False, "Not a valid target!")


def check_action_valid(action):
    if not isinstance(action, p.Action):
        return (False, "Invalid Action Used")
    
    if action.action == "change":
        return check_change_valid(action.target)
    elif action.action == "exchange":
        return check_exchange_valid(action.target)
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
    elif ast.command == "use":
        return check_use_valid(ast.target)
    elif ast.command == "play":
        return check_play_valid(ast.target)
    elif ast.command == "inspect":
        return check_inspect_valid(ast.target)
    elif ast.command == "buy":
        return check_buy_valid(ast.target)
    elif ast.command == "raise":
        return check_raise_valid(ast.target)
    elif ast.command == "call":
        return check_call_valid(ast.target)
    elif ast.command == "fold":
        return check_fold_valid(ast.target) 
    elif ast.command == "all":
        return check_all_valid(ast.target)
    elif ast.command == "start":
        return check_start_valid(ast.target)
    elif ast.command == "quit":
        return check_quit_valid(ast.target)
    else:
        return (False, "Not a Valid Command")


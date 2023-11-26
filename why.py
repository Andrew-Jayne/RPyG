from interaction.interaction import Interaction

def sanitize(input_string:str):
    #exit if string is longer that 128 Chars
    if len(input_string) > 128:
            print("Input Length Exceeds Expected Parameters: Exiting!")
            exit()
    #Set unwanted chars
    chars_to_remove = '!#*.[]{}\\|":;/<>\\\()\''
    control_chars = ''.join(map(chr, range(0, 32)))+ chr(127)
    literal_control_strings = ['\\n', '\\t', '\\r', '\\x0c', '\\x0b']  # Literal string representations of control chars
    #Remove unwanted chars
    limited_string = input_string[:32] # Limit the input to 32 characters first
    for literal in literal_control_strings:
        limited_string = limited_string.replace(literal, '')
    cleaned_string = ''.join(char for char in limited_string if char not in chars_to_remove and char not in control_chars)

    return cleaned_string

def validate_input(choice_list:list, prompt_message:str):
        chosen_action = None
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = sanitize(input(prompt_message).upper())
            if chosen_action not in choice_list:
                dumb_check += 1
                print("Invalid Choice Try Again")
                if dumb_check == 10:
                    print("Look it's not hard, just enter a valid choice....", end="\n\n")
                    exit()
            
        return chosen_action



def welcome():
    print("Welcome to RPyG, a text based RPG in Python", end="\n\n")

    mode_choices = ["AUTO", "MANUAL"]
    mode_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----


Please Select your Game mode:
Options are : Manual & Auto


Note: All Prompts in this game are case insensitive


"""
    game_mode = Interaction.validate_input(mode_choices, mode_message)
    print(f"returned game mode is {game_mode}")
    Interaction.global_game_mode = game_mode
    print(f"Global Game Mode is: {Interaction.global_game_mode}")
    


welcome()
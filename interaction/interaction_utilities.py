
def sanitize(input_string:str, max_length = 32) -> str:
    """
    This function Sanitizes strings passed into it and returns up to the max length chars (Default is 32)
    With most escape sequences and control chars removed

    Will Exit if a string Exceeding 512 chars is passed
    """
    #exit if string is longer that 128 Chars
    if len(input_string) > 512:
            raise ValueError("Input Length Exceeds Expected Parameters: Exiting!")
            exit()
    #Set unwanted chars
    chars_to_remove = '!#*.[]{}\\|":;/<>\\\()\''
    control_chars = ''.join(map(chr, range(0, 32)))+ chr(127)
    literal_control_strings = ['\\n', '\\t', '\\r', '\\x0c', '\\x0b']  # Literal string representations of control chars
    #Remove unwanted chars
    limited_string = input_string[:max_length] # Limit the input to the desired lenght
    for literal in literal_control_strings:
        limited_string = limited_string.replace(literal, '')
    cleaned_string = ''.join(char for char in limited_string if char not in chars_to_remove and char not in control_chars)

    return cleaned_string


def validate_input(choice_list:list[str], prompt_message:str) -> str:
        """
        Checks that the string input by the user is in the allowed list of responses
        Sanizites the input then returns up to the max length specified
        """

        chosen_action = ""
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = sanitize(input(prompt_message).upper())
            if chosen_action not in choice_list:
                dumb_check += 1
                if dumb_check == 10:
                    raise FileNotFoundError("Look it's not hard, just enter a valid choice...., Brain not Found")
        return chosen_action

def custom_text_entry(input_message:str, max_length:int) -> str:
    return sanitize(input(input_message)[:max_length])


    
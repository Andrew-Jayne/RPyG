## ChatGPT idea dump, needs processing

import curses
from curses import window  # Importing the window type for type hinting

def text_input_prompt(win: window, prompt: str) -> str:
    """
    Prompts the user for input, displaying the prompt at the top line and
    echoing their input on the line below.

    :param win: A curses window object.
    :param prompt: The prompt string to display.
    :return: The string entered by the user.
    """
    win.addstr(0, 0, prompt)
    curses.echo(False)  # Disable automatic echoing
    win.move(1, 0)  # Move the cursor to the line below the prompt

    input_str: str = ""
    while True:
        key = win.getch()
        if key in (curses.KEY_ENTER, 10, 13):  # Handle Enter key
            break
        elif key in (curses.KEY_BACKSPACE, 127) and input_str:
            input_str = input_str[:-1]
            win.addstr(1, max(len(input_str), 0), " ")
            win.move(1, len(input_str))
        else:
            try:
                char = chr(key)
                input_str += char
                win.addstr(1, len(input_str) - 1, char)  # Manually echo the character
            except ValueError:
                # Ignore non-printable characters
                continue

    curses.echo(True)  # Re-enable automatic echoing
    return input_str

def main(stdscr: window) -> None:
    """
    The main function for the curses application.

    :param stdscr: The standard screen object provided by curses.wrapper().
    """
    stdscr.clear()
    user_input = text_input_prompt(stdscr, "Enter something: ")
    stdscr.clear()
    stdscr.addstr(0, 0, f"You entered: {user_input}")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)





def prompt_user(win, prompt):
    """Prompt the user with a question, accept 'yes' or 'no' as input strings."""
    win.addstr(3, 0, prompt)
    win.clrtoeol()  # Clear to the end of the line in case there's any text
    win.refresh()

    # Initialize an empty string to collect input
    input_str = ""
    win.keypad(True)  # Enable keypad mode to capture special keys like ENTER

    while True:
        key = win.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:  # Enter key (KEY_ENTER, 10 LF, 13 CR)
            if input_str.lower() in ["yes", "no"]:  # Check if the input is valid
                break  # Exit the loop if valid input is received
            else:
                win.addstr(4, 0, "Please type 'yes' or 'no'.")
                win.clrtoeol()
                win.move(3, len(prompt))  # Move cursor back to the end of the prompt
                input_str = ""  # Reset input_str to collect input again
                continue
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Handle backspace for input correction
            input_str = input_str[:-1]  # Remove the last character in input_str
            win.addstr(3, len(prompt), input_str + " ")  # Update the display with the current input_str
            win.move(3, len(prompt) + len(input_str))  # Move cursor to the correct position
        else:
            input_str += chr(key)  # Append the pressed key to input_str
            win.addstr(3, len(prompt), input_str)  # Display the current input_str
            win.refresh()

    win.clrtoeol()  # Clear line after final input is accepted
    win.keypad(False)  # Turn off keypad mode
    return input_str.lower() == "yes"  # Return True if 'yes', False otherwise



def prompt_user(win, prompt):
    """Display a yes/no prompt, show the user's input, and return True for 'y' or False for 'n'."""
    win.addstr(3, 0, prompt)  # Adjust the position as needed
    win.refresh()
    while True:
        key = win.getch()
        if key in [ord('y'), ord('Y'), ord('n'), ord('N')]:
            # Echo the user's choice back to the screen
            win.addstr(chr(key).lower())  # Display the key; converting to lowercase for consistency
            win.refresh()
            time.sleep(1)  # Give the user a moment to see the entered key
            return key in [ord('y'), ord('Y')]
        else:
            # Optional: Notify the user of invalid input
            win.addstr(4, 0, "Invalid input. Please press 'y' or 'n'.")
            win.clrtoeol()  # Clear to the end of the line
            win.move(3, len(prompt))  # Move the cursor back to the end of the prompt
            win.refresh()



import curses
import time

def prompt_user(win, prompt):
    """Display a yes/no prompt and return True for 'y' or False for 'n'."""
    while True:
        win.addstr(3, 0, prompt)  # Adjust the position as needed
        win.refresh()
        key = win.getch()
        if key in [ord('y'), ord('Y')]:
            return True
        elif key in [ord('n'), ord('N')]:
            return False

def curses_main(win):
    curses.curs_set(0)  # Hide cursor
    win.clear()  # Clear the window

    my_message = "You have Died, try again"
    my_message_list = ["sucks to suck", "just try harder 4head", "you're better than this"]

    while True:
        # Display the initial message
        win.addstr(0, 0, my_message)
        win.refresh()
        time.sleep(2)  # Display the initial message for 2 seconds

        # Display messages from the list, one by one
        for message in my_message_list:
            win.clear()  # Clear the previous message
            win.addstr(0, 0, my_message)  # Re-display the initial message at the top
            win.addstr(1, 0, message)  # Display the next message from the list
            win.refresh()
            time.sleep(2)  # Pause to read the message

        # After displaying all messages, prompt the user
        win.clear()
        if not prompt_user(win, "Would you like to try again? (y/n): "):
            break  # Exit the loop (and the program) if the user responds with 'n'

# Initialize curses
curses.wrapper(curses_main)




import curses
import time

# Function to initialize and manipulate the curses window
def curses_main(win):
    # Initial setup
    curses.curs_set(0)  # Hide cursor
    win.nodelay(True)  # Make getch() non-blocking
    win.clear()  # Clear the window

    my_message = "You have Died, try again"
    my_message_list = ["sucks to suck", "just try harder 4head", "you're better than this"]

    # Display the initial message
    win.addstr(0, 0, my_message)
    win.refresh()
    time.sleep(2)  # Display the initial message for 2 seconds

    # Display messages from the list, one by one
    for message in my_message_list:
        win.clear()  # Clear the previous message
        win.addstr(0, 0, my_message)  # Re-display the initial message at the top
        win.addstr(1, 0, message)  # Display the next message from the list
        win.refresh()
        time.sleep(2)  # Pause to read the message

    win.nodelay(False)  # Wait for user input
    win.getch()  # Wait for a key press before exiting

# Initialize curses
curses.wrapper(curses_main)

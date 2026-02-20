import RPyG
from interfaces import BasicTerminalInterface


def main():
    RPyG.launch_game(interface=BasicTerminalInterface())


# Main Function Wrapper to Accept and Pass Args (well... when we have them lol)
if __name__ == "__main__":
    main()

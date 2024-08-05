import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Options in a 2x2 grid
    options = [["attack", "evade"], ["special", "heal"]]
    rows, cols = len(options), len(options[0])
    
    # Initial cursor position
    current_row, current_col = 0, 0
    
    while True:
        stdscr.clear()
        
        # Display options
        for i in range(rows):
            for j in range(cols):
                if i == current_row and j == current_col:
                    stdscr.addstr(i, j*10, options[i][j], curses.A_REVERSE)  # Highlight the current selection
                else:
                    stdscr.addstr(i, j*10, options[i][j])
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            current_row = (current_row - 1) % rows
        elif key == curses.KEY_DOWN:
            current_row = (current_row + 1) % rows
        elif key == curses.KEY_LEFT:
            current_col = (current_col - 1) % cols
        elif key == curses.KEY_RIGHT:
            current_col = (current_col + 1) % cols
        elif key == ord('\n'):
            return options[current_row][current_col]
        
        stdscr.refresh()

def get_user_selection():
    return curses.wrapper(main)

# Example usage:
if __name__ == "__main__":
    selection = get_user_selection()
    print(f"You selected: {selection}")

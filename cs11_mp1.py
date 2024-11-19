import time
import os
import subprocess
import sys
from movement_testing import movement 

'''Notes:
Current Status: 
    - Can read from input file
        - Can take an input level file in terminal
        - Has a default level
        - Initializes Values: rows, moves, grid (Comments at function)
    - Displays the basic UI
        - Grid, Past moves, remaining moves, points
        - Allows input of moves (With validation and can't go under 0 moves)
    - Allow restarting after the game
    - Main Menu
        - Can start the game from the main menu
        - Allows direct to level playing, if stated in terminal
        - Can now access rules (that still need to be written)
        - Added other stuff in main menu but no functionality yet
        - Repeats main menu call if invalid input
    - Can Clear Screen
    - Allow time delays 
    - Movement is done and has been implemented already

TODO:
    - Points system
    - Count how many eggs there still are
        - So when there are 0 eggs, the game ends
    - Make separate files for game tech for a cleaner main file.
    - Make _test versions of functions
    - Add more detailed docs
    - Properly make the text/non-game files 
        - README file
        - Rules
        - Developer
        - Leaderboard (If we do this)
        - etc. 
    - Add features for plus points
'''



def get_rules(): #For Style
    with open('rules.txt', encoding = 'utf-8') as f:
        rules = f.readlines()
        print(rules)

def main_menu(): #For Style
    print("Welcome to the Egg Roll Challenge!")
    print("Insert Cool Preable I can't be asked to make rn")
    print("Man it's 11:30. This just a preview\n")
    print("[Play]\n[Rules]\n[Level Select]\n[Leaderboard]\n[Developers]\netc.")
    

    #This part need optimizing. make a while loop to condition to continue
    #asking if
    choice = input("What do you wish to do?: ")
    clear_screen()
    if choice == 'Play':
        game()
    elif choice == "Rules":
        get_rules()
    elif choice == 'Level Select':
        print("Not 100% Sure how just yet")
    elif choice == 'Leaderboard':
        print("Not yet sure if we will")
    elif choice == 'Developers':
        print("Under Construction")
    else:
        print("Invalid Input. Try Again\n")
        main_menu()


def initialize(level = 'level1.in'):    #For Game Req
    if len(sys.argv) < 2: #Default Level
        with open(level, encoding = 'utf-8') as f:
            rows = int(f.readline().strip())
            moves = int(f.readline().strip())
            grid = list(f.readline().strip()
                for i in range(rows)
                )
        return tuple((rows, moves, grid))

    #Specific Level: If level called in Terminal
    with open(sys.argv[1], encoding = 'utf-8') as f:
        rows = int(f.readline().strip())
        moves = int(f.readline().strip())
        grid = list(f.readline().strip()
            for i in range(rows)
            )
    return tuple((rows, moves, grid))

def valid_input(input_str, max_moves): #For Game Req
    return list(value
        for value in input_str
        if value.upper() in 'LRFB'
        )[:max_moves] #limit max length to remaining amount of moves


def print_grid(grid): #For Game Req
    for line in grid:
        print(line) 

def get_pastmoves(moves): #For Game Req
    result = ""
    for move in moves:
        if move.lower() == 'l':
            result += "← "
        elif move.lower() == 'r':
            result += "→ "
        elif move.lower() == 'f':
            result += "↑ "
        elif move.lower() == 'b':
            result += "↓ "
    return result

def clear_screen(): #For Game Req
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])

def game(): #Playing the Game & For Game Req
    '''
    Can add the initializing of the variables to initialize 
    functions. They're just here for now for easyness
    '''
    rows = 0
    moves = 0
    points = 0
    grid = []
    past_moves = []
    (rows, moves, grid) = initialize() 

    while moves > 0 : #and there are still eggs
        clear_screen()
        print_grid(grid)
        print("Previous Moves:", get_pastmoves(past_moves))
        print(f"Remaining Moves: {moves}")
        print(f"Points: {points}")
        move = valid_input(input("Enter Move/s: "), moves)
        past_moves += move

        for move_input in move:
            movement(grid, move_input)
         
        moves -= len(move)

    '''
    Final Screen: Post Game
    [This is where we could add level system or play again, or both]
    (This could be its own function too)
    '''
    print_grid(grid)
    print("Previous Moves:", get_pastmoves(past_moves))
    print(f"Remaining Moves: {moves}")
    print(f"Points: {points}\n")

    #Post - game (Only a very vague idea)
    print("Congrats!")
    continue_game = input("Do you want to play again? [Y/N]: ")
    if continue_game == 'Y':
        clear_screen()
        continue_game = input("Do you want to restart level or go to the next level? [Restart/Next]: ")
        if continue_game == 'Restart':
            game()


def main(): #Main Game
    if len(sys.argv) < 2:
        main_menu()
    else:
        game()

#Call Game
main()

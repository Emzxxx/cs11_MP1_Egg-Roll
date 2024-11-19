import os
import subprocess
import sys
import time



def print_grid(grid): #For Game Req
    for line in grid:
        print(line) 
def clear_screen(): #For Game Req
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])



egg = '\U0001F95A'
wall = '\U0001F9F1'
pan = '\U0001F373'
grass = '\U0001F7E9'
empty_nest = '\U0001FAB9' 
full_nest = '\U0001FABA'

temp_grid = [
    '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱',
    '🧱🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🧱',
    '🧱🟩🟩🟩🍳🪹🥚🟩🟩🟩🟩🧱',
    '🧱🟩🟩🟩🟩🟩🟩🟩🍳🟩🟩🧱',
    '🧱🟩🟩🟩🟩🥚🪹🟩🟩🥚🥚🧱',
    '🧱🥚🥚🟩🥚🟩🟩🟩🥚🟩🟩🧱',
    '🧱🟩🟩🟩🥚🍳🟩🟩🟩🟩🟩🧱',
    '🧱🟩🟩🟩🟩🟩🥚🥚🟩🟩🟩🧱',
    '🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱'
]

def movement(grid, direction):
    if direction.lower() == 'l':
        move_left(grid)
    elif direction.lower() == 'r':
        move_right(grid)
    elif direction.lower() == 'f':
        move_up(grid)
    elif direction.lower() == 'b':
        move_down(grid)

'''
up down are fine na, left right still a bit scuffed in the extra_actions() function
'''



def move_up(grid): #needs optimization, separate printing and mutating grid i think
    clear_screen()
    postmove_grid = grid
    while True:
        print_grid(postmove_grid)   
        premove_grid = [line for line in postmove_grid]
        postmove_grid = move_up_once(postmove_grid)

        if premove_grid == postmove_grid:
            #If no changes to the grid aka no more movement possible
            return postmove_grid
        
        
        
        time.sleep(0.5)
        clear_screen()
        
def move_down(grid): #Incomplete pa
    clear_screen()
    postmove_grid = grid
    while True:   
        print_grid(postmove_grid)
        premove_grid = [line for line in postmove_grid]
        postmove_grid = move_down_once(postmove_grid)

        if premove_grid == postmove_grid:
            return postmove_grid
        
        time.sleep(0.5)
        clear_screen()

def move_left(grid):
    clear_screen()
    while True:
        print_grid(grid)

        oldgrid = [line for line in grid] 
        move_left_once(grid)
        
        if oldgrid == grid:
            break

        time.sleep(0.5)
        clear_screen()  

def move_right(grid):
    clear_screen() 
    while True:
        print_grid(grid)

        oldgrid = [line for line in grid] 
        move_right_once(grid)

        if oldgrid == grid:
            break
        
        time.sleep(0.5)
        clear_screen()  

def move_up_once(grid):
    for row in range(1, len(grid)):
        for column in range(1, len(grid[0])-1):
            if grid[row][column] == egg:
                #Will need to add a condition to check what is the next tile
                #If special tile, do smthn else
                #make a special function for other relationships
                if grid[row-1][column] == grass:
                    row_curr = list(grid[row])
                    #In this case it means the row above the current row
                    row_next = list(grid[row-1])

                    row_curr[column] = grass
                    row_next[column] = egg

                    grid[row] = "".join(row_curr)
                    grid[row-1] = "".join(row_next)

                #If the next thing is a Pan
                else:
                    movement_specialAction(grid, row, column, grid[row-1][column])
    return grid

def move_down_once(grid):
    #First reverse the input grid
    grid.reverse()

    #Next, with the reversed grid reuse move up once function since moving down is just moving up from the other side of the board
    moved_grid = move_up_once(grid)

    #then reverse it again to get the proper orientation
    moved_grid.reverse()
    return moved_grid

def move_left_once(grid):
    for column in range(2, len(grid[0])-1):
        for row in range(1, len(grid)-1):
            if grid[row][column] == egg:
                #get the row
                if grid[row][column-1] == grass:
                    currrow = list(grid[row])
                    #current column
                    currrow[column] = grass
                
                    #column-1 or colunch just to the left
                    currrow[column-1] = egg
                    grid[row] = "".join(currrow)
                else:
                    movement_specialAction(grid, row, column, grid[row][column-1])
                    
def move_right_once(grid):
    for column in range(len(grid[0])-2, 0, -1):
        for row in range(len(grid)-1, 0, -1):
            if grid[row][column] == egg:
                #get the row
                if grid[row][column+1] == grass:
                    currrow = list(grid[row])
                    #current column
                    currrow[column] = grass
                
                    #column-1 or colunch just to the left
                    currrow[column+1] = egg
                    grid[row] = "".join(currrow)
                else:
                    movement_specialAction(grid, row, column, grid[row][column+1])


def movement_specialAction(grid, row, column, next_tile):
    #Accepts the current tile (egg tile) and accepts the next tile that isnt grass (empty/full nest and pan)
    row_curr = list(grid[row])
    #In this case it means the row above the current row
    row_next = list(grid[row-1])

    if next_tile == pan:
        row_curr[column] = grass #New tile of the current tile index
        row_next[column] = pan #New tile of the next tile index
    elif next_tile == empty_nest:
        row_curr[column] = grass #New tile of the current tile index
        row_next[column] = full_nest #New tile of the next tile index
    elif next_tile == full_nest:
        row_curr[column] = egg #New tile of the current tile index
        row_next[column] = full_nest #New tile of the next tile index

    grid[row] = "".join(row_curr)
    grid[row-1] = "".join(row_next)



move_up(temp_grid)
move_down(temp_grid)
move_left(temp_grid)
move_right(temp_grid)

"""This file contains a function, solve_sudoku, that will take a manually inputted 9x9 sudoku board and return a solution
The solution is implemented using recursive backtracking
"""
import copy

#type in a game of sudoku here
sudoku_board = [
        [5,3,0,   0,7,0,   0,0,0],
        [6,0,0,   1,9,5,   0,0,0],
        [0,9,8,   0,0,0,   0,6,0],

        [8,0,0,   0,6,0,   0,0,3],
        [4,0,0,   8,0,3,   0,0,1],
        [7,0,0,   0,2,0,   0,0,6],
        
        [0,6,0,   0,0,0,   2,8,0],
        [0,0,0,   4,1,9,   0,0,5],
        [0,0,0,   0,8,0,   0,7,9]
]


def main() -> None:
    #create a copy of the original board before it mutates
    original_board = copy.deepcopy(sudoku_board)
    
    print(f"The original board is:\n{create_ASCII_board(original_board)}")

    if solve_sudoku(sudoku_board):
        print(f"The solved board is:\n{create_ASCII_board(sudoku_board)}")
    else:
        print("This board is not solvable")


def solve_sudoku(board: list[list[int]]) -> bool:
    """Takes in a 9x9 sudoku board and returns True if it has modified it to a solution and False if a solution does not exist"""
    #find the first empty cell
    row, column = find_next_empty_cell(board)

    #check if the sudoku is solved
    if row == -1 and column == -1:
        return True 
    
    #input a guess into the empty cell
    for guess in range (1,10):
        #check if the guess is valid
        if is_valid_guess(board, guess, row, column):
            #if the guess is valid, insert the guess into the board
            board[row][column] = guess

            #recursively call the function again
            if solve_sudoku(board):
                return True

        #if this stage is reached, the guess is not valid or the previous guesses did not result in a valid solution
        #in this case, reset the guess
        board[row][column] = 0
    
    #if this step is reached, the input board is unsolvable
    return False


def find_next_empty_cell(board: list[list[int]]) -> tuple[int, int]:
    """given an input board, returns the row and column index of the first empty cell or (-1, -1) if no empty cells are found"""
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)
            
    return (-1, -1)


def is_valid_guess(board: list[list[int]], guess: int, row: int, column: int) -> bool:
    """given an input guess, returns True if it is valid through the rules of Sudoku and False otherwise"""
    #check 1: the same int can not appear in the same row
    for i in range(9):
        if board[row][i] == guess:
            return False

    #check 2: the same int can not appear in the same column
    for i in range(9):
        if board[i][column] == guess:
            return False
    
    #check 3: the same int can not appear in the same box
    #first find which box the guess is in 
    box_row = row // 3
    box_column = column // 3

    #knowing what box the guess is in, interate through that box
    starting_row = box_row * 3
    starting_column = box_column * 3

    for i in range(3):
        for j in range(3):
            if board[starting_row + i][starting_column + j] == guess:
                return False
    
    #if all other checks pass, the guess is valid
    return True


def create_ASCII_board(board: list[list[int]]) -> str:
    """converts the board into an ASCII representation for clarity"""
    output_string = ""
    
    for i in range(9):
        #print a horizontal line for every 3 rows, but not before the first 3 rows
        if i % 3 == 0 and i != 0:
            output_string += "- - - - - - - - - - -\n"

        for j in range(9):
            #print a vertical line after every 3 numbers, but not before the first 3 numbers
            if j % 3 == 0 and j != 0:
                output_string += "| "
            
            #print numbers, going to a new line if the number is the last one in a row
            if j == 8:
                output_string += f"{board[i][j]}\n"
            else: 
                output_string += f"{board[i][j]} "

    return output_string


if __name__ == "__main__":
    main()
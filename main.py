"""This file presents an interactive sudoku game that a user can play
If desired, the user can utilize the sudoku backtracking algorithm to solve the sudoku for them
"""
from __future__ import annotations #used to typehint a class that isn't defined yet (see SudokuBoard.deselect_cell())
from Sudoku_Solver import is_valid_guess, find_next_empty_cell
import pygame
import os


#constants
BACKGROUND_COLOR = (255, 255, 255)
GRIDLINE_COLOR = (0, 0, 0)
CELL_FONT_COLOR = (0,0, 0)
GUESS_FONT_COLOR = (128, 128, 128)
SELECT_BORDER_COLOR = (255, 0, 0)
FOOTER_MESSAGE_COLOR = (0, 0, 0)

CELL_SIDE_LENGTH = 60
BOARD_WIDTH, BOARD_HEIGHT = CELL_SIDE_LENGTH * 9, CELL_SIDE_LENGTH * 9
FOOTER_HEIGHT = CELL_SIDE_LENGTH
WINDOW_WIDTH, WINDOW_HEIGHT = BOARD_WIDTH, BOARD_HEIGHT + FOOTER_HEIGHT

THIN_LINE_WIDTH = 1
THICK_LINE_WIDTH = 3

CELL_FONT_SIZE = CELL_SIDE_LENGTH // 2
GUESS_FONT_SIZE = CELL_FONT_SIZE // 2
FOOTER_FONT_SIZE = FOOTER_HEIGHT // 2

FONT_FILE_PATH = os.path.join(os.path.dirname(__file__), "CourierPrimeSans.ttf")

ANIMATION_SPEED = 1


class SudokuBoard:
    """This class manages the sudoku board state and draws it onto the window
    
    Attributes:
        window: the pygame window
        cells (list[list[Cell]]): contains the 81 cells accesible by row and column
        board (list[list[int]]): a matrix representation of the current state of the board
        currently_selected_cell (tuple(int, int)): the row and column index of the currently selected cell
        footer_message (str): the message that is to be displayed on the footer, based on the board state
    """
    def __init__(self, window: pygame.Surface) -> None:
        """Initializes the sudoku board and its cells"""
        self.window = window
        self.board = [
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
        self.cells = [[SudokuCell(self.board[i][j], i, j) for j in range(9)] for i in range(9)]
        self.currently_selected_cell = None
        self.footer_message = None

  
    def draw_board(self) -> None:
        """Draws the sudoku board with a background, gridlines, and cells"""
        #draw background
        self.window.fill(BACKGROUND_COLOR)

        #draw horizontal gridlines
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.window, GRIDLINE_COLOR, (0, CELL_SIDE_LENGTH * i), (BOARD_WIDTH, CELL_SIDE_LENGTH * i), THICK_LINE_WIDTH)
            else:
                pygame.draw.line(self.window, GRIDLINE_COLOR, (0, CELL_SIDE_LENGTH * i), (BOARD_WIDTH, CELL_SIDE_LENGTH * i), THIN_LINE_WIDTH)
        
        #draw vertical gridlines
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.window, GRIDLINE_COLOR, (CELL_SIDE_LENGTH * i, 0), (CELL_SIDE_LENGTH * i, BOARD_HEIGHT), THICK_LINE_WIDTH)
            else:
                pygame.draw.line(self.window, GRIDLINE_COLOR, (CELL_SIDE_LENGTH * i, 0), (CELL_SIDE_LENGTH * i, BOARD_HEIGHT), THIN_LINE_WIDTH)
        
        #draw cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw_cell(self.window)
        
        #draw footer message
        if self.footer_message is not None:
            self.display_footer_message(self.footer_message)
    
    
    def select_cell(self, mouse_x: int, mouse_y: int) -> None:
        """Selects a cell to interact with it
        
        Arguments:
            mouse_x: the x position of the mouse on mouseclick
            mouse_y: the y position of the mouse on mouseclick
        """
        #make every cell not selected
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False
        
        #only look at clicks on the board
        if mouse_x > BOARD_WIDTH or mouse_y > BOARD_HEIGHT:
            return

        #find the cell the coordinates are pointing to
        cell_x, cell_y = mouse_x // CELL_SIDE_LENGTH, mouse_y // CELL_SIDE_LENGTH

        #set the correct cell to selected
        cell = self.cells[cell_y][cell_x]
        cell.is_selected = True

        #record the index of which cell is selected
        self.currently_selected_cell = (cell_y, cell_x)


    def deselect_cell(self, cell: SudokuCell) -> None:
        """Deselects a selected cell"""
        cell.is_selected = False
        self.currently_selected_cell = None

    
    def display_guess(self, input_number: int) -> None:
        """Adds a temporary guess on a selected cell and then deselects it
        Arguments:
            input_number: a keyboard input number that is the temporary guess
        """
        row, column = self.currently_selected_cell
        cell = self.cells[row][column]
        if cell.is_editable:
            cell.guess = input_number
    

    def clear_cell(self) -> None:
        """Clears a selected cell of placed values or temporary guesses and then deselects it"""
        row, column = self.currently_selected_cell
        cell = self.cells[row][column]
        if cell.is_editable:
            cell.value = 0
            cell.guess = 0
            self.board[row][column] = 0 #update board state
        self.deselect_cell(cell)


    def lock_in_guess(self) -> None:
        """"Locks in" the temporary guess and deselects the cell"""
        row, column = self.currently_selected_cell
        cell = self.cells[row][column]

        if cell.guess == 0:
            self.deselect_cell(cell)
            return

        if cell.is_editable == False:
            self.deselect_cell
            return

        #turn guess into value 
        if is_valid_guess(self.board, cell.guess, row, column):
            cell.value = cell.guess
            cell.guess = 0
            self.board[row][column] = cell.value #update board state
            self.footer_message = None
            self.deselect_cell(cell)
        
        else: 
            cell.guess = 0
            self.footer_message = "Invalid Guess"
            self.deselect_cell(cell)
        
        if self.is_solved(self.board):
            #remove the user's ability to edit the board
            self.freeze_board()
            self.footer_message = "Congratulations!"


    def is_solved(self, board: list[list[int]]) -> bool:
        """Returns True if the board is solved and False if not"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                  return False
        return True
    

    def freeze_board(self) -> None:
        """Makes the board unable to be edited further"""
        for i in range(9):
                for j in range(9):
                    self.cells[i][j].is_editable = False


    def display_footer_message(self, message: str) -> None:
        """Displays an input message onto the footer"""
        footer_font = pygame.font.Font(FONT_FILE_PATH, FOOTER_FONT_SIZE)
        footer_text = footer_font.render(message, True, FOOTER_MESSAGE_COLOR)

        footer_text_height = footer_text.get_height()
        footer_text_width = footer_text.get_width()
    
        self.window.blit(footer_text, (BOARD_WIDTH // 2 - footer_text_width // 2, BOARD_HEIGHT + FOOTER_HEIGHT // 2 - footer_text_height // 2))
    

    def auto_solve(self) -> bool:
        """Visualizes the sudoku backtracking algorithm as it solves the board for the user
        
        Returns:
            bool: used for recursion
        """
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False

        #find first empty cell; if none, the board is solved
        row, column = find_next_empty_cell(self.board)

        if row == -1 or column == -1:
            return True

        #try guesses and recursively call function
        #edit both the game window and the board state
        for guess in range (1,10):
            self.cells[row][column].is_selected = True #creates visual effect

            if is_valid_guess(self.board, guess, row, column):
                self.cells[row][column].value = guess
                self.board[row][column] = guess

                #update the window
                self.draw_board()
                pygame.display.update()
                pygame.time.delay(ANIMATION_SPEED)

                if self.auto_solve():
                    return True

            #if a guess doesn't result in a solved board, reset the guess
            self.cells[row][column].value = 0
            self.board[row][column] = 0

        #return False if the input board did not result in a solution
        return False
            

class SudokuCell:
    """This class represents models the 81 cells of sudoku
    
    Attributes:
        value: the number in the cell
        row: the row index of the cell
        column: the column index of the cell
        guess: the temporary guess that a user inputs before committing to a guess
        is_selected (bool): True if a cell is clicked on and False otherwise
        is_editable (bool): True if a cell can be edited and False otherwise
    """
    def __init__(self, value: int, row: int, column: int) -> None:
        """Initializes the cell"""
        self.value = value
        self.row = row
        self.column = column
        self.guess = 0
        self.is_selected = False

        #if a cell has a value upon creation its value is not changeable
        if self.value:
            self.is_editable = False
        else:
            self.is_editable = True
    

    def draw_cell(self, window: pygame.Surface) -> None:
        """Draws a cell of the sudoku board onto the pygame window
        
        Arguments:
            window: the pygame window
        """
        #refer to correct cell by pixels pointing to top-left corner of cell
        cell_x = CELL_SIDE_LENGTH * self.column 
        cell_y = CELL_SIDE_LENGTH * self.row 
       
        #display non-zero cells
        if self.value:
            value_text_font = pygame.font.Font(FONT_FILE_PATH, CELL_FONT_SIZE)
            value_text = value_text_font.render(str(self.value), True, CELL_FONT_COLOR)

            value_text_width = value_text.get_width()
            value_text_height = value_text.get_height()

            window.blit(value_text, (cell_x + CELL_SIDE_LENGTH // 2 - value_text_width // 2, cell_y + CELL_SIDE_LENGTH // 2 - value_text_height // 2))
        
        #display guess if one exists
        if self.guess:
            guess_font = pygame.font.Font(FONT_FILE_PATH, GUESS_FONT_SIZE)
            guess_text = guess_font.render(str(self.guess), True, GUESS_FONT_COLOR)

            window.blit(guess_text, (cell_x + GUESS_FONT_SIZE // 2, cell_y + GUESS_FONT_SIZE // 2))

        #if a cell is selected, add a border around it
        if self.is_selected:
            select_border = pygame.Rect(cell_x, cell_y, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH)
            pygame.draw.rect(window, SELECT_BORDER_COLOR, select_border, THICK_LINE_WIDTH)


def main() -> None:
    """The main function of the program
    Creates a pygame window that displays a sudoku board
    The user can input guesses and play sudoku
    Additionally, the user can press the spacebar to solve the board using a backtracking algorithm
    """
    #initializations
    input_number = None

    #create window 
    GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku")

    #create board
    board = SudokuBoard(GAME_WINDOW)

    #start loop
    run = True
    while run:
        for event in pygame.event.get():
            #end loop on close
            if event.type == pygame.QUIT:
                run = False
            
            #select cells on mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board.select_cell(mouse_x, mouse_y)
            
            #take in inputs from keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    input_number = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    input_number = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    input_number = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    input_number = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    input_number = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    input_number = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    input_number = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    input_number = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    input_number = 9
                
                #autosolve
                if event.key == pygame.K_SPACE:
                    if board.auto_solve():
                        board.freeze_board()
                        board.footer_message = "Congratulations!"
                    else:
                        board.freeze_board()
                        board.footer_message = "Unsolvable Board :("
                
                #for selected cells there are 3 actions
                if board.currently_selected_cell is not None:
                    #display temporary guess
                    if input_number:
                        board.display_guess(input_number)
                        input_number = None
                    
                    #clear selected cells
                    if (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.key == pygame.K_CLEAR):
                        board.clear_cell()
                    
                    #"lock in" temporary guess on selected cells
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                        board.lock_in_guess()

        board.draw_board()
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
# Sudoku_Solver_GUI

This project allows users to interact with the game of Sudoku in two ways. In Sudoku_Solver.py, you can input a board and get a solved version of the board back. In main.py, you can play a game of Sudoku or watch the Sudoku backtracking algorithm solve the board in real time.

## Installation Steps

### 1\. Clone the repository
```bash
git clone https://github.com/RudraPatel2003/Sudoku_Solver_GUI.git
```   
### 2\. Change the working directory
```bash
cd Sudoku_Solver_GUI
```
### 3\. Install dependencies   

Windows:
```bash
py -m pip install -r requirements.txt
```
Unix/macOS:
```bash
python -m pip install -r requirements.txt
```

## Usage

### Sudoku_Solver.py
Type in a Sudoku board into the "sudoku_board" variable. Run the program to be printed the original board and the solved version of the board, if one exists.

### main.py

Run the program to launch the Sudoku game. 

Click on a cell to select it. 

All cells that contain numbers when the game is started are uneditable. 

If an editable cell is selected, there are 3 options:
1. Type in a number to mark a guess
2. Press ENTER or RETURN to lock in a guess
3. Press DELETE or CLEAR or BACKSPACE to clear a cell of any guesses or locked-in values.

Press SPACEBAR to watch the Sudoku backtracking algorithm solve the board for you.

## Contributing
Pull requests are welcome.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# SudokuPython
By Mike Rosinsky

## Description
This project uses a backtracking algorithm to solve a game of sudoku. The project is coded in Python (3.x) and uses the pygame module to create the GUI.


## Start-Up Instructions
1) Install pygame for python3
```
python3 -m pip install -U pygame --user
```
2) Run sudoku.py
```
python3 sudoku.py
```

## Using the Program
- Left click to select a block
- Press a number (1-9) to enter a number into the selected block
- Press Backspace to clear the selected box
- Press Space to reset the board
- Press Enter to start the solving algorithm

- Note: The sudoku puzzle is hardcoded into the program. For now, you'll have to go into the program and change the board directly if you want a new sudoku board.
- If you've entered incorrect numbers into the puzzle and start the algorithm, it will not find a solution

- There is also an animate flag hardcoded into the program. By default it is set to 'True' so you can see the process it uses, but it can be set to 'False' for instant solves

## Screenshots

![img](https://imgur.com/eJMHSrU)

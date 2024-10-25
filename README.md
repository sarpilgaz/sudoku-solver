# Sudoku Solver

A simple Sudoku solver, created from the framework provided by my university.

## Sudoku Format

Sudokus are stored and read from a directory in the root called `Sudokus`. The format is as follows:

- 9x9 board
- Unset fields are represented by `0`
- Each row ends with a newline character, except the last row

Refer to the `sudokus` folder for examples.

## Algorithm

The solver uses the AC-3 constraint satisfaction algorithm initially. If AC-3 alone doesn't solve the puzzle, it continues with backtracking DFS. 

Optional heuristics for AC-3 are available to order the arcs. These heuristics include:
- **MRV (Minimum Remaining Values)**: Prioritizes variables with the fewest legal values left.
- **Set Fields First**: Prefers working with already set fields.

## Possible Further Improvements & To-Do

1. **Extend user interface**
   Extend the user interface and functionality of selecting a sudoku so that more than the 5 available sudokus are available to be solved.

2. **Create GUI**
   Probably never, but might as well write it here. 
   

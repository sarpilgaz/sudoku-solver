# Sudoku Solver

A simple Sudoku solver, created from the framework provided by my university.
Run simply by:
```bash
Python3 App.py
```

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
- As It stands, these heuristics make 0 FUCKING difference, I have no clue why. I suspect it is related to how I handle AC-3 and thhe eventual need to visit all arcs anyway, but idk.

## Benchmarking

Benchmarking is available for the number of arc revisions made for each sudoku, and each heuristic. CSV files will be created in a folder
named Benchmarks.
```bash
Python3 Benchmarker.py
```

## Possible Further Improvements & To-Do

1. **Make Heuristics Actually Matter**
   Make heuristics actually make a difference, I suspect this is tied to the AC-3 implementation and not the method in which heuristics are calculated.

2. **Create GUI**
   Probably never, but might as well write it here. 
   

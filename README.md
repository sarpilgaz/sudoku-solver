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

1. **Optimize the Backtracker with Forward Planning**  
   Forward planning can reduce the domains of neighboring variables when a field is set. This approach offers the following benefits:
   - **Early Pruning**: If a domain becomes empty, we can immediately prune, avoiding a dead-end track.
   - **Fewer Backtracking Steps**: Reducing domain sizes decreases the number of steps and recursions required to reach a solution.

2. **Extend Functionality**  
   Allow the solver to handle more than 5 different Sudoku options.

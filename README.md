A simple sudoku solver, created from the framework my university provided.

Sudokus are stored & read from a directory in the root, called sudokus, which follow this format:

9x9 board, unset fields are 0, and one newline character at the end of each row, excluding the last, for example:
000006080
009105372
080700016
000000034
000351000
730000000
610008020
823904600
070600000

The algorithm uses AC-3 constraint satisfaction first, and continues with backtracking DFS if AC-3 didn't manage to solve it.
Optional heuristics for the AC-3 algorithm are present, which are used to order the arcs. These are MRV and set fields first.


Possible Further improvements, and todo:
    1) optimize the backtracker with forward planning, which aims to reduce the domains of neighbours when a field is set. This can have the following benefits:
        -> Early pruning. If a domain is emptied, we can be sure we are on a dead end track, and prune.
        -> Reduction in backtrack steps. The algorithm considers all values present in a variables domain. Reduction in said domains can result in less steps and less recursion required to reach a solution.
    2)extend the functionality to allow for more than 5 different sudoku options
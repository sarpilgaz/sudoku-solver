from Field import Field


class Sudoku:
    def __init__(self, filename):
        self.NO_ROWS: int = 9
        self.NO_COLS: int = 9
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid
    
    def add_neighbours_of_a_field(self, grid: Field[[]], row_index: int, col_index: int):
        """
        Adds the neighbours of a given field f, f is given as its indices in the grid.
        Neighbors include cells in the same row, column, and 3x3 block.
        """
        n = []

        # Add neighbors in the same row
        for col in range(self.NO_COLS):
            if col != col_index:  # Exclude  itself
                n.append(grid[row_index][col])

        # Add neighbors in the same column
        for row in range(self.NO_ROWS):
            if row != row_index:  # Exclude itself
                n.append(grid[row][col_index])

        # Add neighbors in the same 3x3 block
        block_row_start = (row_index // 3) * 3
        block_col_start = (col_index // 3) * 3
        for i in range(block_row_start, block_row_start + 3):
            for j in range(block_col_start, block_col_start + 3):
                if i != row_index or j != col_index:  # Exclude itself
                    n.append(grid[i][j])

        grid[row_index][col_index].set_neighbours(n)


    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """
        for row in range(0,9):
            for col in range(0,9):
                Sudoku.add_neighbours_of_a_field(grid, row, col)

    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board

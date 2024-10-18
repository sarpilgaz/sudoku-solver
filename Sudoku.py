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

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """
        for row in range(0,9):
            for col in range(0,9):
                n = []
                # Add neighbors in the same row
                for col_i in range(9):
                    if col_i != col:  # Exclude  itself
                        n.append(grid[row][col_i])

                # Add neighbors in the same column
                for row_i in range(9):
                    if row_i != row:  # Exclude itself
                        n.append(grid[row_i][col])

                # Add neighbors in the same 3x3 block
                block_row_start = (row // 3) * 3
                block_col_start = (col // 3) * 3
                for i in range(block_row_start, block_row_start + 3):
                    for j in range(block_col_start, block_col_start + 3):
                        if i != row or j != col:  # Exclude itself
                            n.append(grid[i][j])
                    
                grid[row][col].set_neighbours(n)

    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board

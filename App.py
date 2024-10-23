import os
import sys
from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")

class App:


    @staticmethod
    def solve_sudoku(sudoku_file, h_type, solver_type):
        game = Game(Sudoku(sudoku_file), h_type)
        game.show_sudoku()
        if solver_type == 1:
            if (game.full_solver() and game.valid_solution()):
                print("Solved!")
            else:
                print("Could not solve this sudoku :(")
        else:
            if (game.AC_3() and game.valid_solution()):
                if (game.full_solver() and game.valid_solution()):
                    print("Solved!")
            else:
                print("Could not solve this sudoku :(")

    @staticmethod
    def start():
        while True:
            file_num = input("Enter Sudoku file (1-5): ")

            file = None
            for filename in os.listdir(sudoku_folder):
                if file_num in filename:
                    file = filename
            if file is not None:
                print("There are optional heuristics available for the AC-3 part of the solver, pick the number presented with the heuristic if you wish to use one:")
                print("-1 for no heuristic, \n 0 for MRV, \n 1 for finalized fields first, \n 2 for both MRV and finalized fields")
                print("After that, please indicate if you want to only use AC-3, or utilize the full solver, which does backtracking after AC-3 if necessary")
                print("0 for only AC-3, 1 for full solving")
                h_type = int(input())
                solver_type = int(input())
                
                if h_type < -1 and h_type > 2:
                    print("invalid heuristic choice, defaulting to no heuristic, you naughty boy >:(")
                    h_type = -1
                if not (solver_type == 0 or solver_type == 1):
                    print("invalid choice for solver selection, defaulting to the full solver.")
                    solver_type = 1
                App.solve_sudoku(os.path.join(sudoku_folder, file), h_type, solver_type)
            else:
                print("Invalid choice")

            continue_input = input("Continue? (yes/no): ")
            if continue_input.lower() != 'yes':
                break


if __name__ == "__main__":
    App.start()


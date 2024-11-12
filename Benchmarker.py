import os
import csv
from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")
benchmark_folder = os.path.join(os.path.dirname(__file__), "Benchmarks")
nr_of_heuristics = 3  # number of heuristics, not including no heuristic (-1)

# Create the benchmark folder if it does not exist
os.makedirs(benchmark_folder, exist_ok=True)

def solve_sudoku(sudoku_file, h_type) -> bool:
    """Solves a Sudoku using a specified heuristic."""
    game = Game(Sudoku(sudoku_file), h_type, True)
    if game.AC_3() and game.valid_solution():
        return True, game.arc_revisions
    else:
        return False, game.arc_revisions

def benchmark() -> None:
    """Benchmark different heuristics on multiple Sudoku puzzles and save results to CSV files in a separate folder."""
    # Retrieve the list of files and sort them numerically
    files = sorted(os.listdir(sudoku_folder), key=lambda f: int(f.replace("Sudoku", "").replace(".txt", "")))
    
    # Loop through each Sudoku file
    sudoku_number = 1
    for filename in files:
        sudoku_path = os.path.join(sudoku_folder, filename)
        
        # Create a CSV file for each Sudoku in the Benchmarks folder
        csv_filename = f"benchmark_{filename.replace('.txt', '')}.csv"
        csv_filepath = os.path.join(benchmark_folder, csv_filename)
        
        # Open the CSV file for writing
        with open(csv_filepath, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header row
            writer.writerow(["Sudoku Number", "Solved?", "Heuristic ID", "Revisions"])
            
            # Loop from -1 to nr_of_heuristics to test each heuristic
            for heuristic in range(-1, nr_of_heuristics):
                solved, revisions = solve_sudoku(sudoku_path, heuristic)
                
                # Write benchmark results to the CSV
                writer.writerow([sudoku_number, int(solved), heuristic, revisions])
        
        print(f"Benchmark results written to {csv_filepath}")
        sudoku_number += 1

if __name__ == "__main__":
    benchmark()

from queue import Queue
from Sudoku import Sudoku

class Game:

    def __init__(self, sudoku):
        self.arc_queue = Queue()
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def init_queue(self):
        """
        Init the arc queue with the tuples
        """
        for row in range (0,9):
            for col in range (0,9):
                field = self.sudoku.board[row][col]
                neighbours = field.get_neighbours()
                for n in neighbours:
                    self.arc_queue.put((field, n))

    def revise(self, arc):
        """
        Revises the domain of the first field in the given arc.
        Removes values from the domain of the first field that do not satisfy the constraint.
        The constraint is that the values of two fields in an arc cannot be the same.
        
        :param arc: A tuple of two Fields, (field1, field2), where field1 is being revised.
        :return: True if the domain of the first field was revised, False otherwise.
        """
        revised = False
        domain_of_first = arc[0].get_domain().copy() 
        domain_of_second = arc[1].get_domain()

        #if the domain of second is empty, this means the field was already set in the first place.
        if len(domain_of_second) == 0:
            second_value = arc[1].get_value()
            for value in domain_of_first:
            # If the value of the first field is equal to the fixed value of the second field,
            # remove it from the first field's domain (constraint violation)
                if value == second_value:
                    arc[0].remove_from_domain(value)
                    revised = True
            return revised
        
        for value_1 in domain_of_first:
            diff_value = False
            # Check if there is any value in the second domain that satisfies the constraint
            #if a different value is found in the second domain, this satisfies the constraint
            for value_2 in domain_of_second:
                if (value_1 != value_2):
                    diff_value = True
                    break
            if not diff_value:
                arc[0].remove_from_domain(value_1)
                revised = True

        return revised

    def put_neighbours_in_queue(self, field):
        """
        Function puts all neighbours of a field into the arc_queue as the tuple (neighbour, field)
        """
        neighbours = field.get_neighbours()
        for n in neighbours:
            self.arc_queue.put((n, field))

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        self.init_queue()

        while not self.arc_queue.empty():
            current_arc = self.arc_queue.get()

            if self.revise(current_arc):
                if current_arc[0].get_domain_size() == 0:
                    print("unsolveable sudoku detected, last state is as follows:")
                    self.show_sudoku()
                    return False #no solution is possible
                self.put_neighbours_in_queue(current_arc[0])

        return True #freedom!


    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution.
        A valid solution satisfies:
        - Each row contains unique numbers from 1 to 9.
        - Each column contains unique numbers from 1 to 9.
        - Each 3x3 block contains unique numbers from 1 to 9.
        @return: True if the sudoku solution is correct, False otherwise
        """
        
        # Check every row:
        for i in range(9):
            s = set()
            for j in range(9):
                value = self.sudoku.board[i][j].get_value()
                if value in s or value == 0:
                    if value == 0:
                        print(f"Unset field found on row {i+1}, AC-3 algorithm must have failed. Displaying the last state:")
                    else:
                        print(f"The value {value} was detected twice in row {i+1}. Displaying the state:")
                    self.show_sudoku() 
                    return False  # Counterexample found
                s.add(value)

        # Check every column:
        for i in range(9):
            s = set()
            for j in range(9):
                value = self.sudoku.board[j][i].get_value()
                if value in s or value == 0:
                    if value == 0:
                        print(f"Unset field found on row {i+1}, AC-3 algorithm must have failed. Displaying the last state:")
                    else:
                        print(f"The value {value} was detected twice in column {i+1}. Displaying the state:")
                    self.show_sudoku() 
                    return False  # Counterexample found
                s.add(value)

        # Check every 3x3 subgrid:
        for row_block in range(0, 9, 3): 
            for col_block in range(0, 9, 3):
                s = set()
                for i in range(3):
                    for j in range(3):
                        value = self.sudoku.board[row_block + i][col_block + j].get_value()
                        if value in s or value == 0:
                            if value == 0:
                                print(f"Unset field found on row {i+1}, AC-3 algorithm must have failed. Displaying the last state:")
                            else:
                                print(f"The value {value} was detected twice in 3x3 grid {i+1}, {j+1}. Displaying the state:")
                            self.show_sudoku() 
                            return False  # Counterexample found
                        s.add(value)

        #no counter example found, sudoku is solved correctly
        self.show_sudoku()
        return True


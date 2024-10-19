from queue import Queue
import heapq
from Sudoku import Sudoku

class Game:

    def __init__(self, sudoku):
        self.arc_queue = Queue()
        self.arc_pqueue = [] # prio queue in case heuristics are used. This will be a list of type tuple (priority, arc).
        self.h_type = -1 # use -1 if you want no heuristic
        self.sudoku = sudoku

    def set_heuristic_type(self, h):
        self.h_type = h

    def get_heuristic_type(self):
        return self.h_type

    def show_sudoku(self):
        print(self.sudoku)

    def heuristic_picker(self, arc):
        heuristic_id = self.h_type
        field1, field2 = arc
        domain1_size = field1.get_domain_size()
        domain2_size = field2.get_domain_size()

        if heuristic_id == 0: #MRV only
            return min(domain1_size, domain2_size)
        
        elif heuristic_id == 1: #finalized fields first only
            if domain1_size == 1 or domain2_size == 1:
                return 1 #top prio

        elif heuristic_id == 2: #both
            if domain1_size == 1 or domain2_size == 1:
                return 1 #top prio
            else: return min(domain1_size, domain2_size)
        
        return 0 #default to 0


    def init_queue(self):
        """
        Init the arc queue with the tuples
        """
        for row in range (0,9):
            for col in range (0,9):
                field = self.sudoku.board[row][col]
                neighbours = field.get_neighbours()
                for n in neighbours:
                    arc = (field, n)
                    if self.h_type == -1: # ne heuristic requested
                        self.arc_queue.put(arc)
                    else:
                        prio = self.heuristic_picker(arc)
                        heapq.heappush(self.arc_pqueue, (prio, arc))

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
        currently puts duplicate arcs in queue
        """
        neighbours = field.get_neighbours()
        for n in neighbours:
            arc = (n, field)
            if self.h_type == -1: # no heuristic requested
                self.arc_queue.put(arc)
            else:
                priority = self.heuristic_picker(arc)
                heapq.heappush(self.arc_pqueue, (priority, arc))

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        self.init_queue()

        while True:
            current_arc = ()
            if self.h_type == -1: #no heuristic requested
                if self.arc_queue.empty():
                    break
                current_arc = self.arc_queue.get()
            else:
                if not self.arc_pqueue:
                    break
                priority, current_arc = heapq.heappop(self.arc_pqueue)

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


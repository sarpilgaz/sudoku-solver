from queue import Queue
import heapq
from Sudoku import Sudoku

class Game:

    def __init__(self, sudoku, h_type, benchmarking_mode):
        self.arc_queue = Queue()
        self.arc_pqueue = [] # prio queue in case heuristics are used. This will be a list of type tuple (priority, arc).
        self.h_type = h_type
        self.sudoku = sudoku
        self.arc_revisions = 0
        self.benchmark_mode = benchmarking_mode

    def set_heuristic_type(self, h):
        self.h_type = h

    def get_heuristic_type(self):
        return self.h_type

    def show_sudoku(self):
        print(self.sudoku)

    #functions for AC-3:

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
        
        return 1 #default to 1


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
                    self.arc_revisions += 1
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
                self.arc_revisions += 1 

        return revised

    def put_neighbours_in_queue(self, arc):
        """
        Function puts all neighbours of a field into the arc_queue as the tuple (neighbour, field)
        We need to put back a arc back in the queue even if it may already be present, because after a revision, because:

        The reason is that even if an arc is already in the queue, a revision of the domain can potentially make it necessary to revise the same arc again. 
        For example, reducing the domain of a neighboring variable might require rechecking all arcs involving that variable, even if those arcs are already in the queue.
        If you skip adding an arc back, you risk missing necessary domain reductions, leading to an incomplete or incorrect arc consistency check.
        """
        neighbours = arc[0].get_other_neighbours(arc[1])
        for n in neighbours:
            n_arc = (n, arc[0])
            if self.h_type == -1: # no heuristic requested
                self.arc_queue.put(n_arc)
            else:
                priority = self.heuristic_picker(n_arc)
                heapq.heappush(self.arc_pqueue, (priority, n_arc))

    def AC_3(self) -> bool:
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
            else: #some heuristic requested
                if not self.arc_pqueue:
                    break
                #we dont need priority anymore
                priority, current_arc = heapq.heappop(self.arc_pqueue)

            if self.revise(current_arc):
                if current_arc[0].get_domain_size() == 0:
                    if not self.benchmark_mode:
                        print("unsolveable sudoku detected, last state is as follows:")
                        self.show_sudoku()
                    return False #no solution is possible
                self.put_neighbours_in_queue(current_arc)
        if self.benchmark_mode:
            print(self.arc_revisions)
        return True #freedom!

    #functions for backtracking search:

    def pick_unset_field(self):
        """Function to pick an unset field for the next field to assign a value to.
        Uses MRV to select the most constrained field.
        Degree heuristic was tried, but proved to slow down the overall solving, and thus MRV is the only heuristic used.
        """
        len_of_most_constrained = float('inf')  # Initialize to a high value

        for i in range(9):
            for j in range(9):
                field = self.sudoku.board[i][j]
                domain_size = field.get_domain_size()

                # Find the most constrained field
                if domain_size < len_of_most_constrained and field.get_value() == 0:
                    len_of_most_constrained = domain_size
                    most_constrained_field = field

        return most_constrained_field

    def check_neighbours(self, field):
        """function to check the neighbours of a given field to see if it doesn't violate constraints
        returns true is no constraint is violated, false otherwise
        """
        for n in field.get_neighbours():
            if field.get_value() == n.get_value():
                return False #big no no !
        return True
    
    def forward_check(self, field, value, changes):
        """function applies a forward checking heuristic to the backtracker.
        for all the neighbours of the given "field", we remove the value that was assigned to it from their domains. The value is in parameter "value".
        all the changes to domains are remembered in list "changes" which is a tuple (field, <value removed from domain>)
        if, as the result of the domain reduction, a domain is size 0, then this assignment "value" to "field" must be incorrect, therefore a dead end.
            in this case, the "value" is removed from "field" and a function to restore domains using list "changes" is called.
            finally, we return False in this case.
        if not, we return true.
        """
        for n in field.get_neighbours():
            len_of_n_domain_before = n.get_domain_size()
            if value in n.get_domain():
                n.remove_from_domain_no_assign(value)
                changes.append((n, value))
            
            if n.get_domain_size() == 0 and len_of_n_domain_before != 0: #It is only a const. violation if the RESULT of the reduction reduces the domain to 0. 
                self.undo_changes(changes)
                field.remove_value()
                return False
        return True

    def undo_changes(self, changes):
        """simply loops over the list and restores "value" to the domain of "curr_field" """
        for curr_field, value in changes:
            curr_field.add_to_domain(value) 
    
    def backtracker(self):
        """
        Solves the Sudoku board using backtracking search with forward checking 
        to reduce domains and enforce constraints.

        Steps:
        1. If the board is fully solved, fills in the
        board values with `fill_board()` and terminates successfully.
        2. else, Selects the next unset field using `pick_unset_field()`.
        3. Iterates over possible values in the field's domain:
        - Tentatively assigns a value to the field.
        - Validates the assignment against neighboring fields with `check_neighbours()`.
        - Applies `forward_check()` to reduce domains of neighboring fields,
            recording any changes in list `changes` for rollback.
        - Recursively continues the search if forward checking succeeds.
        4. If the assignment leads to a dead end, calls `undo_changes()` to rollback
        domain reductions and proceeds with the next value.

        Returns:
            True if the board is successfully solved, False otherwise.
        """
        if self.is_solved():
            self.fill_board()
            return True
        
        curr_field = self.pick_unset_field()

        for v in curr_field.get_domain():
            curr_field.set_value(v)
            if self.check_neighbours(curr_field):
                changes = []
                if self.forward_check(curr_field, v, changes):
                    if self.backtracker():
                        return True
                
                self.undo_changes(changes)

        return False
    
    def is_solved(self):
        """function checks if the sudoku board is "filled" or not.
        a board is "filled" iff all fields have a domain smaller than 1, including.
        this is because the backtracker doesn't assign values to fields as soon as their domain reaches zero. 
        """
        for i in range(0, 9):
            for j in range(0,9):
                if self.sudoku.board[i][j].get_domain_size() > 1:
                    return False
        return True
    
    def fill_board(self):
        """function simply loops over the board and assigns for fields which have a domain of 1 the value in their domain"""
        for i in range(0, 9):
            for j in range(0,9):
                if self.sudoku.board[i][j].get_domain_size() == 1:
                    self.sudoku.board[i][j].set_value(self.sudoku.board[i][j].get_domain()[0])

    
    #solver and verifier:
    
    def full_solver(self):
        """A full solver function that does backtracking after AC-3, if necessary.
        Even though the backtracker is called everytime regardless of the success of AC-3, the function immediately terminates if the
        state of the sudoku is filled.
        """
        return self.AC_3() and self.backtracker()
    

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution.
        A valid solution satisfies:
        - Each row contains unique numbers from 1 to 9.
        - Each column contains unique numbers from 1 to 9.
        - Each 3x3 block contains unique numbers from 1 to 9.
        @return: True if the sudoku solution is correct, False otherwise
        """
        # Check rows
        for i in range(9):
            if not self.check_and_report(
                (self.sudoku.board[i][j].get_value() for j in range(9)),
                f"row {i+1}"
            ):
                return False

        # Check columns
        for i in range(9):
            if not self.check_and_report(
                (self.sudoku.board[j][i].get_value() for j in range(9)),
                f"column {i+1}"
            ):
                return False

        # Check 3x3 subgrids
        for row_block in range(0, 9, 3):
            for col_block in range(0, 9, 3):
                if not self.check_and_report(
                    (self.sudoku.board[row_block + i][col_block + j].get_value()
                    for i in range(3) for j in range(3)),
                    f"3x3 block starting at ({row_block+1},{col_block+1})"
                ):
                    return False

        # If no counterexample was found, the sudoku is solved correctly
        if not self.benchmark_mode:
            self.show_sudoku()
        return True

    def check_and_report(self, values, context) -> bool:
        """
        Checks a sequence of values for duplicates or unset fields.
        Reports any issues found if not in benchmark mode.
        
        :param values: An iterable of values to check.
        :param context: A string indicating the context (e.g., "row 1", "column 3").
        :return: False if an error is found, True otherwise.
        """
        seen = set()
        for value in values:
            if value in seen or value == 0:
                self.report_error(value, context)
                return False
            seen.add(value)
        return True

    def report_error(self, value, context):
        """
        Reports an error based on the value and context, unless in benchmark mode.
        
        :param value: The problematic value.
        :param context: A string indicating where the error was found.
        """
        if self.benchmark_mode:
            return

        if value == 0:
            print(f"Unset field found in {context}, AC-3 algorithm must have failed. Displaying the last state:")
        else:
            print(f"The value {value} was detected twice in {context}. Displaying the state:")
        self.show_sudoku()

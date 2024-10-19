class Field:
    # region constructors

    def __init__(self, *args):

        self.value = 0
        self.domain = []
        # A list of all the fields that this field is constrained by
        self.neighbours = []
        self.priority = -1 #used in case heuristics are requested during the AC-3 algorithm


        # Constructor in case the field is unknown
        if len(args) == 0:
            for i in range(1, 10):
                self.domain.append(i)

        # Constructor in case the field is known, i.e., it contains a value
        if len(args) == 1:
            self.value = args[0]
            self.domain = []

    # endregion

    # region overloaded comparison operators, used in case of heuristics during AC-3

    # explanation on why this is needed:
    # during heuristic comparison, heapq has a tuple of priority and arc (prio, arc)
    # if priority values are the same, python will try to compare arcs, which is a tuple of fields (field, field)
    # in the same fashion, this will lead to python comparing two fields, which does not make sense in the context of sudoku, and these particular heuristics
    # therefore I introduced a dummy field priority and overloaded the equals operator, now all fields are "equal"
    # This means that the two tuples of (priority, arc) are always equal if priority is equal, because arcs are always "equal"
    # This is the exact behaviour we want, and it is always deterministic.

    def __lt__(self, other):
        return self.priority == other.priority
    
    #endregion

    # region value functions

    def is_finalized(self):
        """
        Has this field been set to a non-zero value? If so then it is finalized.
        :return: Boolean indicating if the field is finalized.
        """
        return self.value != 0

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    # endregion

    # region neighbor functions

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def get_other_neighbours(self, b):
        """
        Return all neighbours of this field except neighbour b
        @param b:
        @return: All neighbors of this Field except b
        """
        new_neighbours = self.neighbours
        new_neighbours.remove(b)
        return new_neighbours

    # endregion

    # region domain functions

    def get_domain(self):
        return self.domain

    def get_domain_size(self):
        return len(self.domain)

    def remove_from_domain(self, value):
        """
        Removes the given value from the domain, and possibly assigns the last value to the field
        :param value: value to remove
        :return: true if the value was removed
        """
        value_removed = self.domain.remove(value)
        if len(self.domain) == 1:
            self.set_value(self.domain[0])
        return value_removed

    # endregion

    # region Misc Functions

    def __str__(self):
        """
        Displays non-finalized fields with a period, otherwise displays the finalized value
        :return:
        """
        return "." if self.value == 0 else str(self.value)

    # endregion

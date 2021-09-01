# NOTE: You may change the way actions and the payoff matrix are represented.
#  However if you do so, you'll have to update the __repr__ method accordingly.
#  Also FixedMatrixSuite will have to be updated to reflect your changes, which can be quite a bit of work.
#
# You may not change the actions and payoffs of the matrix games in FixedMatrixSuite, only their representation.

import abc
import random
from typing import List, Tuple, Dict

# Define custom types for actions and payoffs.
Payoff = float
Action = int


class MatrixSuite(metaclass=abc.ABCMeta):
    """Abstract representation of a suite of matrix games.

    Class attributes:
        *name*: Name of the matrix suite.
                If it only generates one type of matrix,
                it can also be the name of that matrix type. (i.e. Constant Sum)

        *row_actions*: List of actions that the row player has in the current matrix.

        *col_actions*: List of actions that the column player has in the current matrix.

        *payoff_matrix*: A 2D list containing tuples with the payoffs of the row and column players.

        Indices of the outer list are row actions.

        Indices of the inner list are column actions.

        The first item of the tuple is the row player payoff,
        the second item is the column player payoff.
    """
    name: str
    row_actions: List[Action]
    col_actions: List[Action]
    payoff_matrix: List[List[Tuple[Payoff, Payoff]]]

    @abc.abstractmethod
    def generate_new_payoff_matrix(self) -> None:
        """Generate a new payoff matrix and update the row and column actions accordingly."""
        pass

    def __repr__(self) -> str:
        """Prettified string representation of the matrix, useful for testing.
        This will show if you use **print()** on an instance of this class."""
        out: str = ""
        for ra in self.row_actions:
            for ca in self.col_actions:
                out += self.payoff_matrix[ra][ca].__repr__() + " "
            out += "\n"
        return out

    # Here you can add more methods to make implementing strategies easier,
    # for example a method that returns a given players actions.
    def get_actions(self, player: str) -> List[Action]:
        """Return the actions of the given player.
        :param player: A string of either 'row' or 'col',
        representing which player the strategy is currently playing as.
        """
        if player == "row":
            return self.row_actions
        elif player == "col":
            return self.col_actions
        else:
            raise Exception("ERROR: *player* should be either 'row' of 'col', not '" + player + "'!")


class FixedMatrixSuite(MatrixSuite):
    """Predetermined suite of matrices, don't use with more than 9 restarts, because it will run out of matrices.

    Class attributes:
        *matrices*: A dictionary of the matrices and their attributes.

        Structured like this,

        key: index, to be matched with *k*

        value: List containing the number of row actions,
        the number of column actions and
        the payoff matrix in that order.

        *k*: Number of the matrix that is currently active.
    """
    matrices: Dict[int, Tuple[int, int, List[List[Tuple[Payoff, Payoff]]]]]
    k: int

    def __init__(self) -> None:
        """Initialize the suite and 'generate' the first payoff matrix."""
        self.name = "Fixed Matrix Suite"
        self.k = 0

        self.matrices = {
            1: (2, 2, [[(2, 2), (6, 0)], [(0, 6), (4, 4)]]),
            2: (2, 2, [[(9, 2), (2, 8)], [(8, 0), (1, 7)]]),
            3: (2, 2, [[(1, 8), (1, 1)], [(2, 1), (2, 9)]]),
            4: (3, 3, [[(1, 8), (9, 0), (6, 3)], [(9, 0), (0, 9), (0, 9)], [(9, 0), (2, 7), (9, 0)]]),
            5: (3, 3, [[(3, 3), (4, 4), (9, 9)], [(2, 2), (0, 0), (6, 6)], [(1, 1), (5, 5), (8, 8)]]),
            6: (3, 3, [[(9, 1), (0, 2), (10, 1)], [(8, 2), (8, 2), (8, 0)], [(0, 1), (1, 1), (1, 9)]]),
            7: (3, 3, [[(2, 8), (1, 8), (7, 1)], [(7, 0), (1, 7), (8, 2)], [(7, 2), (7, 2), (8, 0)]]),
            8: (3, 3, [[(2, 2), (4, 1), (6, 0)], [(1, 4), (3, 3), (5, 2)], [(0, 6), (2, 5), (4, 4)]]),
            9: (4, 4,
                [[(5, 9), (0, 10), (9, 6), (3, 2)], [(7, 7), (1, 1), (4, 1), (1, 7)], [(3, 0), (4, 0), (9, 3), (5, 9)],
                 [(2, 1), (2, 7), (0, 10), (0, 9)]]),
            10: (4, 4, [[(10, 0), (4, 6), (5, 5), (8, 2)], [(8, 2), (5, 5), (6, 4), (10, 0)],
                        [(5, 5), (8, 2), (0, 10), (8, 2)], [(1, 9), (4, 6), (7, 3), (6, 4)]])
        }

        self.generate_new_payoff_matrix()

    def __repr__(self) -> str:
        """Add some extra information to the print of this class."""
        out = self.name + ": Matrix " + self.k.__repr__() + "\n"
        out += super().__repr__()  # Add the representation of the superclass ( GameSuite.__repr__() ).
        return out

    def generate_new_payoff_matrix(self) -> None:
        """Not so much generate as just getting the next matrix out of the dictionary."""
        self.k += 1
        try:
            v = self.matrices[self.k]
        except KeyError:
            raise Exception("Key is not in matrix dictionary, you probably did too many restarts.")
        self.row_actions = list(range(v[0]))
        self.col_actions = list(range(v[1]))
        self.payoff_matrix = v[2]


# Add the other game suites below


class RandomIntMatrixSuite(MatrixSuite):
    def __init__(self) -> None:
        """Initialize the suite and 'generate' the first payoff matrix."""
        self.name = "Random Int Matrix Suite"
        self.k = 0
        self.generate_new_payoff_matrix()

    def __repr__(self) -> str:
        """Add some extra information to the print of this class."""
        out = self.name + ": Matrix " + self.k.__repr__() + "\n"
        out += super().__repr__()  # Add the representation of the superclass ( GameSuite.__repr__() ).
        return out

    def generate_new_payoff_matrix(self) -> None:
        self.k += 1
        # Randomly choose the number of row actions from [2, 5]
        self.row_actions = list(range(random.randint(2, 5)))
        # Randomly choose the number of col actions from [2, 5]
        self.col_actions = list(range(random.randint(2, 5)))
        # Randomly generate the payoff matrix with the payoff from [1, 3]
        self.payoff_matrix = []
        for row_action in self.row_actions:
            row = []
            for col_action in self.col_actions:
                payoff_tuple = (random.randint(1, 3), random.randint(1, 3))
                row.append(payoff_tuple)
            self.payoff_matrix.append(row)


class RandomFloatMatrixSuite(MatrixSuite):
    def __init__(self) -> None:
        """Initialize the suite and 'generate' the first payoff matrix."""
        self.name = "Random Float Matrix Suite"
        self.k = 0
        self.generate_new_payoff_matrix()

    def __repr__(self) -> str:
        """Add some extra information to the print of this class."""
        out = self.name + ": Matrix " + self.k.__repr__() + "\n"
        out += super().__repr__()  # Add the representation of the superclass ( GameSuite.__repr__() ).
        return out

    def generate_new_payoff_matrix(self) -> None:
        self.k += 1
        # Randomly choose the number of row actions from [2, 5]
        self.row_actions = list(range(random.randint(2, 5)))
        # Randomly choose the number of col actions from [2, 5]
        self.col_actions = list(range(random.randint(2, 5)))
        # Randomly generate the payoff matrix with the payoff from [1, 3]
        self.payoff_matrix = []
        for row_action in self.row_actions:
            row = []
            for col_action in self.col_actions:
                payoff_tuple = (random.uniform(0.0, 3.0), random.uniform(0.0, 3.0))
                row.append(payoff_tuple)
            self.payoff_matrix.append(row)
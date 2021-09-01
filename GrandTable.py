# NOTE: This is a suggestion of how you could begin implementing the Grand Table,
# feel free to come up with your own way. You may change almost everything of this class,
# it just has to calculate the grand table on a matrix suite,
#  given a list of strategies, restarts and rounds per restart.
import copy
from statistics import mean

from typing import List

import MatrixSuite
from Game import Game
from Strategies import Strategy


class GrandTable:
    """Calculate the grand table on a MatrixSuite for the given strategies, restarts and rounds per restart.

    Class attributes:
        *matrix_suite*: The MatrixSuite that the game is played on,
        should generate a new payoff matrix after each restart.

        *row_strategies*: List of N instances of Strategy subclasses, which should be included in the Grand Table.

        *col_strategies*: List of N instances of Strategy subclasses, which should be included in the Grand Table.

        Either row or col strategies should be a deepcopy of strategies so they don't refer to the same instances.
        Credit: Thanks Vincent and Wiebe for noticing that this is necessary.

        *restarts*: Number of restarts that should occur during the calculation of the Grand Table.

        *rounds*: Number of rounds that should be played for each restart.

        *games*: Instance of Game for every combination of *strategies*, so N x N.
        The outer list are row players and the inner list are column players.

        *grand_table*: Same 2D list as *games* but only contains the resulting score.
    """
    matrix_suite: MatrixSuite
    row_strategies: List[Strategy]
    col_strategies: List[Strategy]
    restarts: int
    rounds: int
    games: List[List[Game]]
    grand_table: List[List[float]]

    def __init__(self, matrix_suite: MatrixSuite, strategies: List[Strategy],
                 nr_of_restarts: int, rounds_per_restart: int) -> None:
        self.row_strategies = strategies
        self.col_strategies = copy.deepcopy(strategies)
        self.matrix_suite = matrix_suite
        self.games = [[Game(self.matrix_suite, row_player, col_player)
                       for col_player in self.col_strategies]
                      for row_player in self.row_strategies]
        self.grand_table = [[0
                             for _ in self.col_strategies]
                            for _ in self.row_strategies]
        self.restarts = nr_of_restarts
        self.rounds = rounds_per_restart

    def __repr__(self) -> str:
        out: str = ""
        # Determine format string with enough padding for the longest strategy name.
        # padding = max(map(lambda s: len(s.name), self.strategies))
        # You know what, to make it easier, just make everything 7 characters at most.
        padding = "7"
        # If you want to know how this works, look up Pythons format method on google.
        name_format_row = '{:>' + padding + "." + padding + '}'
        name_format_col = '{:^' + padding + "." + padding + '}'
        score_format = '{:^' + padding + '.2f}'

        # Create the table header
        header = name_format_row.format("") + "||"
        for strat in self.col_strategies:
            header += name_format_col.format(strat.name) + "|"
        header += "|" + name_format_col.format("MEAN") + "|"
        hline = "=" * len(header)
        out = out + hline + "\n" + header + "\n"

        # Now create each row of the table
        for i, row in enumerate(self.grand_table):
            # Add the name of the strategy to the row.
            out += name_format_row.format(self.row_strategies[i].name) + "||"
            for score in row:
                out += score_format.format(score) + "|"
            out += "|" + score_format.format(mean(row)) + "|"
            out += "\n"

        # Add one last horizontal line
        out = out + hline + "\n"
        return out

    # Methods to play all games for the specified number of rounds and handle the restarts, can go here.
    def play(self):

        # Iterate through the number of restarts that should occur during the calculation of the Grand Table
        for curr_restart in range(self.restarts + 1):
            print(self.matrix_suite)

            # Iterate through the number of rounds that should be played for each restart
            for curr_round in range(self.rounds):
                # Iterate through every combination of strategies (every game), so N x N
                for curr_row_of_games in self.games:
                    for curr_game in curr_row_of_games:
                        # Play one combination of strategies once
                        curr_game.play()

            # Calculate the average payoff for every combination of strategies for the row player before restart
            for i, row_of_games in enumerate(self.games):
                for j, game in enumerate(row_of_games):
                    row_player_avg_payoff = mean(game.row_player_payoffs)
                    # Record the sum of the average payoff by every restart in the Grand Table
                    self.grand_table[i][j] += row_player_avg_payoff

            if curr_restart < self.restarts:
                # Generate the new matrix suite (game)
                self.matrix_suite.generate_new_payoff_matrix()

            for i, row_of_games in enumerate(self.games):
                for j, game in enumerate(row_of_games):
                    # Play the new matrix suite (game)
                    game.initialize(self.matrix_suite)

        # Calculate the score in the Grand Table
        for i, row in enumerate(self.grand_table):
            for j, score in enumerate(row):
                self.grand_table[i][j] = score / (self.restarts + 1)
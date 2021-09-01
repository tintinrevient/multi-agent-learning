# Note: You may not change methods in the Strategy class, nor their input parameters.
# Information about the entire game is given in the *initialize* method, as it gets the entire MatrixSuite.
# During play the payoff matrix doesn't change so if your strategy needs that information,
#  you can save it to Class attributes of your strategy. (like the *actions* attribute of Aselect)

import abc
import random
import numpy as np
import math
from typing import List

import MatrixSuite
from MatrixSuite import Action, Payoff
import Utils


class Strategy(metaclass=abc.ABCMeta):
    """Abstract representation of a what a Strategy should minimally implement.

    Class attributes:
        name: A string representing the name of the strategy.
    """
    name: str

    def __repr__(self) -> str:
        """The string representation of a strategy is just it's name.
        So it you call **print()** it will output the name.
        """
        return self.name

    @abc.abstractmethod
    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Initialize/reset the strategy with a new game.
        :param matrix_suite: The current MatrixSuite,
        so the strategy can extract the information it needs from the payoff matrix.
        :param player: A string of either 'row' or 'col',
        representing which player the strategy is currently playing as.
        """
        pass

    @abc.abstractmethod
    def get_action(self, round_: int) -> Action:
        """Calculate the action for this round.
        :param round_: The current round number.
        """
        pass

    @abc.abstractmethod
    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        """Update the strategy with the result of this round.
        :param round_: The current round number.
        :param action: The action this strategy played this round.
        :param payoff: The payoff this strategy received this round.
        :param opp_action: The action the opposing strategy played this round.
        """
        pass


# As an example we have implemented the first strategy for you.


class Aselect(Strategy):
    """Implements the Aselect (random play) algorithm."""
    actions: List[Action]

    def __init__(self):
        """The __init__ method will be called when you create an object.
        This should set the name of the strategy and handle any additional parameters.

        Example:
            To create an object of the Aselect class you use, "Aselect()"

            If you want to pass it parameters on creation, e.g. "Aselect(0.1)",

            you need to modify "__init__(self)" to "__init__(self, x: float)",
            and you probably also want to save "x", or whatever you name it,
            to a class attribute, so you can use it in other methods.
            """
        self.name = "Aselect"

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

    def get_action(self, round_: int) -> Action:
        """Pick the next action randomly from the possible actions."""
        return random.choice(self.actions)

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        """Aselect has no update mechanic."""
        pass


# Add the other strategies below


class EpsilonGreedy(Strategy):
    """Implements the Epsilon-Greedy algorithm."""
    actions: List[Action]

    def __init__(self, epsilon: float):
        self.name = "EGreedy"
        # Initialize the exploration probability epsilon
        self.epsilon = epsilon

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        self.action_payoff_list = [0.0 for _ in self.actions]
        self.action_num_list = [1 for _ in self.actions] # To avoid being divided by zero

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        if self.round_ == 0:
            action = random.choice(self.actions)
        else:
            # Calculate the action value for each action
            self.action_value_list = list(map(lambda x, y: x/y, self.action_payoff_list, self.action_num_list))
            # Choose the actions with the highest action value (the highest-action-value actions can be more than one)
            optimal_actions = [i for i, value in enumerate(self.action_value_list) if value == max(self.action_value_list)]

            # The random action resulting from the epsilon-probability of exploration
            random_action = random.choice(self.actions)

            # The final possible actions -> actions with larger probability are multiplied proportionally
            optimal_actions_str = list(map(str, optimal_actions))
            random_action_str = [str(random_action)]
            actions_str = optimal_actions_str * (int((1 - self.epsilon) * 100 / len(optimal_actions_str))) + random_action_str * (int(self.epsilon * 100))
            actions = list(map(int, actions_str))

            # Pick the next action randomly from the possible actions with equal probability
            action = random.choice(actions)

        return action


    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        self.action_payoff_list[action] += payoff
        self.action_num_list[action] += 1


class UCB(Strategy):
    """Implements the Upper-Confidence-Bound (UCB) algorithm."""
    actions: List[Action]

    def __init__(self, confidence_level: float):
        self.name = "UCB"
        # Initialize the confidence level
        self.confidence_level = confidence_level

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        self.action_payoff_list = [0.0 for _ in self.actions]
        self.action_num_list = [1 for _ in self.actions]  # To avoid being divided by zero

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        if self.round_ == 0:
            action = random.choice(self.actions)
        else:
            # Calculate the action value for each action
            self.action_value_list = list(map(lambda x, y: x / y, self.action_payoff_list, self.action_num_list))

            # Add the confidence level and an uncertainty measure
            self.adjusted_action_value_list = list(map(lambda x, y: x + y, self.action_value_list, [self.confidence_level * np.sqrt((np.log(self.round_)/z)) for z in self.action_num_list]))

            # Choose the actions with the highest action value (the highest-action-value actions can be more than one)
            optimal_actions = [i for i, value in enumerate(self.adjusted_action_value_list) if
                               value == max(self.adjusted_action_value_list)]

            # Pick the next action randomly from the possible optimal actions with equal probability
            action = random.choice(optimal_actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        self.action_payoff_list[action] += payoff
        self.action_num_list[action] += 1


class SatisficingPlay(Strategy):
    """Implements the Satisficing Play algorithm."""
    actions: List[Action]

    def __init__(self, persistence_rate: float, initial_aspiration_level: float):
        self.name = "SatisficingPlay"

        # Initialize the persistence rate
        self.persistence_rate = persistence_rate
        # Initialize the initial aspiration level
        self.initial_aspiration_level = initial_aspiration_level

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        self.previous_aspiration_level = self.initial_aspiration_level
        self.previous_action = 0
        self.previous_payoff = 0.0

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        if self.round_ == 0:
            action = random.choice(self.actions)
        else:
            if self.previous_payoff >= self.previous_aspiration_level:
                action = self.previous_action
            else:
                action = random.choice(self.actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        self.previous_action = action
        self.previous_payoff = payoff

        # Update the aspiration level
        self.previous_aspiration_level = self.persistence_rate * self.previous_aspiration_level + (1 - self.persistence_rate) * self.previous_payoff


class Bully(Strategy):
    """Implements the Bully algorithm."""
    actions: List[Action]

    def __init__(self):
        self.name = "Bully"

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        # Get the action with a highest security value from the payoff matrix
        actions_by_security_values = []
        if player == "row":
            self.payoff_matrix = matrix_suite.payoff_matrix
            for row in self.payoff_matrix:
                security_value = min([x for (x, y) in row if y == max(row, key=lambda x: x[1])[1]])
                actions_by_security_values.append(security_value)
        if player == "col":
            self.payoff_matrix = Utils.transpose(matrix_suite.payoff_matrix)
            for row in self.payoff_matrix:
                security_value = min([y for (x, y) in row if x == max(row, key=lambda x: x[0])[0]])
                actions_by_security_values.append(security_value)

        self.action = actions_by_security_values.index(max(actions_by_security_values))

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        return self.action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_


class FictitiousPlay(Strategy):
    """Implements the Fictitious Play algorithm."""
    actions: List[Action]

    def __init__(self):
        self.name = "FictitiousPlay"

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        self.player = player
        self.beliefs = [0 for _ in self.actions]
        if player == "row":
            self.payoff_matrix = matrix_suite.payoff_matrix
        if player == "col":
            self.payoff_matrix = Utils.transpose(matrix_suite.payoff_matrix)

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        # There might exist multiple possible actions with the same maximum belief value
        actions = [i for i, value in enumerate(self.beliefs) if value == max(self.beliefs)]
        # Pick the next action randomly from the multiple optimal actions
        action = random.choice(actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        if self.player == "row":
            action_potential_payoffs = [row[opp_action][0] for row in self.payoff_matrix]
        if self.player == "col":
            action_potential_payoffs = [row[opp_action][1] for row in self.payoff_matrix]

        # Get the potential optimal actions
        action_potential_optimal = [i for i, value in enumerate(action_potential_payoffs) if value == max(action_potential_payoffs)]

        # Update the beliefs
        self.beliefs = [value + 1 if i in action_potential_optimal else value for i, value in enumerate(self.beliefs)]


class RegretMatching(Strategy):
    """Implements the Proportional Regret Matching algorithm."""
    actions: List[Action]

    def __init__(self):
        self.name = "RegretMatching"

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        self.player = player
        if player == "row":
            self.payoff_matrix = matrix_suite.payoff_matrix
        if player == "col":
            self.payoff_matrix = Utils.transpose(matrix_suite.payoff_matrix)
        self.cumulative_actual_payoff = 0.0
        self.cumulative_expected_payoffs = [0.0 for _ in self.actions]
        self.regret_matching = [0.0 for _ in self.actions]

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        if sum(self.regret_matching) > 0:
            # There might exist multiple possible actions with the same maximum regret value
            actions = [i for i, value in enumerate(self.regret_matching) if value == max(self.regret_matching)]
            # Pick the next action randomly from the multiple optimal actions
            action = random.choice(actions)
        else:
            action = random.choice(self.actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        # Update the cumulative actual payoff
        self.cumulative_actual_payoff += payoff
        # Update the cumulative expected payoff
        if self.player == "row":
            potential_payoffs = [self.payoff_matrix[x][opp_action][0] for x in self.actions]
        if self.player == "col":
            potential_payoffs = [self.payoff_matrix[x][opp_action][1] for x in self.actions]

        self.cumulative_expected_payoffs = list(map(lambda x, y: x + y, self.cumulative_expected_payoffs, potential_payoffs))

        # Update the average regrets
        average_regrets_ = [(x - self.cumulative_actual_payoff) / round_ for x in self.cumulative_expected_payoffs]
        average_regrets = [0.0 if x <= 0.0 else x for x in average_regrets_] # For values <= 0, adjust them to 0

        # Update the regret matching if the sum is greater than 0
        if sum(average_regrets) > 0:
            self.regret_matching = [x / sum(average_regrets) for x in average_regrets]
        else:
            self.regret_matching = [0.0 for _ in self.actions]


class Softmax(Strategy):
    """Implements the Softmax algorithm."""
    actions: List[Action]

    def __init__(self, initial_q_value: float, learning_rate: float, temperature: float):
        self.name = "Softmax"
        self.initial_q_value = initial_q_value
        self.learning_rate = learning_rate
        self.temperature = temperature

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        if player == "row":
            self.payoff_matrix = matrix_suite.payoff_matrix
            # Initialize the geometric averages by (max+min)/2 of all the payoffs a player can get
            payoffs = [tuple[0] for row in self.payoff_matrix for tuple in row]
        if player == "col":
            self.payoff_matrix = Utils.transpose(matrix_suite.payoff_matrix)
            # Initialize the geometric averages by (max+min)/2 of all the payoffs a player can get
            payoffs = [tuple[1] for row in self.payoff_matrix for tuple in row]

        min_payoff = min(payoffs)
        max_payoff = max(payoffs)
        initial_value = (min_payoff + max_payoff) / 2
        self.geometric_averages = [initial_value for _ in self.actions]
        self.q_values = [self.initial_q_value for _ in self.actions]

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        # Pick the actions with the maximum payoff average
        actions = [i for i, value in enumerate(self.geometric_averages) if value == max(self.geometric_averages)]
        # If there are multiple optimal actions, randomly pick one
        action = random.choice(actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        # Update the Q-value
        self.q_values[action] = (1 - self.learning_rate) * self.q_values[action] + self.learning_rate * payoff

        # Update the geometric averages
        geometric_averages_ = [math.e**(x / self.temperature) for x in self.q_values]
        sum_of_geometric_averages_ = sum(geometric_averages_)
        self.geometric_averages = [x / sum_of_geometric_averages_ for x in geometric_averages_]


class MutualBenefit(Strategy):
    """Implements the Mutual Benefit algorithm."""
    actions: List[Action]

    def __init__(self):
        self.name = "MutualBenefit"

    def initialize(self, matrix_suite: MatrixSuite, player: str) -> None:
        """Just save the actions as that's the only thing we need."""
        self.actions = matrix_suite.get_actions(player)

        self.round_ = 0
        if player == "row":
            self.payoff_matrix = matrix_suite.payoff_matrix
            # Initialize the geometric averages by (max+min)/2 of all the payoffs a player can get
            payoffs = [tuple[0] for row in self.payoff_matrix for tuple in row]
        if player == "col":
            self.payoff_matrix = Utils.transpose(matrix_suite.payoff_matrix)
            # Initialize the geometric averages by (max+min)/2 of all the payoffs a player can get
            payoffs = [tuple[1] for row in self.payoff_matrix for tuple in row]

        min_payoff = min(payoffs)
        max_payoff = max(payoffs)
        self.initial_value = (min_payoff + max_payoff) / 2

        self.action_payoff_list = [self.initial_value for _ in self.actions] # the initial total payoff for the row player and col player
        self.action_num_list = [1 for _ in self.actions] # To avoid being divided by zero

    def get_action(self, round_: int) -> Action:
        """Pick the next action."""
        action_avg_payoff_list = list(map(lambda x, y: (x / y), self.action_payoff_list, self.action_num_list))
        optimal_actions = [i for i, value in enumerate(action_avg_payoff_list) if value == max(action_avg_payoff_list)]

        # If there are multiple optimal actions, randomly pick up one action
        action = random.choice(optimal_actions)

        return action

    def update(self, round_: int, action: Action, payoff: Payoff, opp_action: Action, opp_payoff: Payoff) -> None:
        self.round_ = round_
        self.action_payoff_list[action] += payoff + opp_payoff
        self.action_num_list[action] += 1

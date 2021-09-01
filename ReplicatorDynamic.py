# NOTE: Execute the replicator dynamic on the grand table also visualize it as a graph.
# You may change everything in this file.

from typing import List
import numpy as np
import matplotlib.pyplot as plt

from GrandTable import GrandTable


# Proportions you will have to use:
uniform_with_own_strat = [1/9] * 9
uniform_without_own_strat = [1/8] * 8
non_uniform_with_own_strat = [0.12, 0.08, 0.06, 0.15, 0.05, 0.21, 0.06, 0.09, 0.18]
non_uniform_without_own_strat = [0.22, 0.19, 0.04, 0.06, 0.13, 0.10, 0.05, 0.21]


class ReplicatorDynamic:
    def __init__(self, start_proportions: List[float], grand_table: GrandTable):
        self.old_proportions = start_proportions
        self.grand_table = grand_table
        self.step = 0
        self.history = []
        self.history.append(self.old_proportions)

    def step(self):
        temp_score = np.matmul(self.grand_table.grand_table, self.old_proportions)
        updated_score = np.multiply(self.old_proportions, temp_score)
        sum_of_score = sum(updated_score)
        self.new_proportions = [x / sum_of_score for x in updated_score]

        # Update the history
        self.history.append(self.new_proportions)

    def evolve(self):
        while True:
            self.step += 1
            ReplicatorDynamic.step(self)
            # Euclidean distance between two proportions
            self.distance = np.sqrt(sum(list(map(lambda x, y: (x - y)**2, self.old_proportions, self.new_proportions))))

            if self.distance  < 0.001: # Less than a very small value 0.001
                break
            else:
                self.old_proportions = self.new_proportions

    def to_graph(self):
        """Visualize the evolution of proportions."""
        plt.plot(list(range(len(self.history))), self.history)
        plt.gca().legend(('Random', 'E-Greedy', 'UCB', 'Satisficing Play', 'Bully', 'Fictitious Play', 'Regret Matching', 'Softmax', 'Mutual Benefit'), loc='upper left')
        plt.xlabel('Step')
        plt.ylabel('Proportion')
        plt.title('Replicator dynamics')
        plt.show()

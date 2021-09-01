# Note: From this script the program can be run.
# You may change everything about this file.

import MatrixSuite
import Strategies
import Game
from GrandTable import GrandTable
import ReplicatorDynamic
import Nash
from typing import List

eight_strategies = [Strategies.Aselect(), Strategies.EpsilonGreedy(0.1), Strategies.UCB(1.0),
                    Strategies.SatisficingPlay(0.1, 2.0), Strategies.Bully(), Strategies.FictitiousPlay(),
                    Strategies.RegretMatching(), Strategies.Softmax(5.0, 0.1, 1.0)]

nine_strategies = [Strategies.Aselect(), Strategies.EpsilonGreedy(0.1), Strategies.UCB(1.0),
                   Strategies.SatisficingPlay(0.1, 2.0), Strategies.Bully(), Strategies.FictitiousPlay(),
                   Strategies.RegretMatching(), Strategies.Softmax(5.0, 0.1, 1.0), Strategies.MutualBenefit()]

fixed_matrix_suite = MatrixSuite.FixedMatrixSuite()
random_int_matrix_suite = MatrixSuite.RandomIntMatrixSuite()
random_float_matrix_suite = MatrixSuite.RandomFloatMatrixSuite()

def generate_grand_table(matrix_suite: MatrixSuite, strategies: List[Strategies.Strategy], restarts: int):
     matrix_suite = matrix_suite
     strategies = strategies
     print("Strategies:", strategies)

     grand_table = GrandTable(matrix_suite, strategies, restarts, 1000)
     grand_table.play()
     print(grand_table)

     return grand_table


# # Example of how to test a strategy:
# matrix_suite = FixedMatrixSuite()  # Create a matrix suite
#
# strat = Strategies.Bully() # Create the strategy you want to test.
#
# strat.initialize(matrix_suite, "row")  # Initialise it with the game suite and as either "row" or "col" player.
#
# action = strat.get_action(1)  # Get the next action
# print("Strategy plays action:" + action.__repr__())
#
# strat.update(1, action, 1.5, 1, 2)  # Update the strategy with a fake payoff and opponent action.
# # Now you might want to look at the class attributes of the strategy,
# # which you can call the same as functions, just without any parentheses.
# print("Bully actions:")
# print(strat.actions)
# print()


if __name__ == "__main__":

     # Change your options
     option = 3

     options = {
          1: ("fixed", 8, True),
          2: ("fixed", 8, False),
          3: ("fixed", 9, True),
          4: ("fixed", 9, False),
          5: ("rand_int", 8, True),
          6: ("rand_int", 8, False),
          7: ("rand_int", 9, True),
          8: ("rand_int", 9, False),
          9: ("rand_float", 8, True),
          10: ("rand_float", 8, False),
          11: ("rand_float", 9, True),
          12: ("rand_float", 9, False)
     }

     if option == 1:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[1])

          # Grand table
          grand_table = generate_grand_table(fixed_matrix_suite, eight_strategies, 9)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 2:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[2])

          # Grand table
          grand_table = generate_grand_table(fixed_matrix_suite, eight_strategies, 9)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 3:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[3])

          # Grand table
          grand_table = generate_grand_table(fixed_matrix_suite, nine_strategies, 9)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)

     if option == 4:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[4])

          # Grand table
          grand_table = generate_grand_table(fixed_matrix_suite, nine_strategies, 9)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)

     if option == 5:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[5])

          # Grand table
          grand_table = generate_grand_table(random_int_matrix_suite, eight_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 6:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[6])

          # Grand table
          grand_table = generate_grand_table(random_int_matrix_suite, eight_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 7:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[7])

          # Grand table
          grand_table = generate_grand_table(random_int_matrix_suite, nine_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)

     if option == 8:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[8])

          # Grand table
          grand_table = generate_grand_table(random_int_matrix_suite, nine_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)

     if option == 9:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[9])

          # Grand table
          grand_table = generate_grand_table(random_float_matrix_suite, eight_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 10:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[10])

          # Grand table
          grand_table = generate_grand_table(random_float_matrix_suite, eight_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_without_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(eight_strategies, grand_table)

     if option == 11:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[11])

          # Grand table
          grand_table = generate_grand_table(random_float_matrix_suite, nine_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)

     if option == 12:
          print("(Matrix Suite, Number of Strategies, Uniform?) ->", options[12])

          # Grand table
          grand_table = generate_grand_table(random_float_matrix_suite, nine_strategies, 19)

          # Replicator dynamics
          replicator_dynamic = ReplicatorDynamic.ReplicatorDynamic(ReplicatorDynamic.non_uniform_with_own_strat,
                                                                   grand_table)
          replicator_dynamic.evolve()
          replicator_dynamic.to_graph()

          # Nash equilibrium
          Nash.nash_equilibria(nine_strategies, grand_table)
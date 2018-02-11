# coding: utf-8
import numpy as np
from Dynamic_calculation_of_children import LeducGame
from cfr import cfr
from cfr_game import CFRGame
from example_strategy import constant_action, random_strategy, uniformly_random_strategy
from best_response import best_response, compute_exploitability

if __name__ == "__main__":
    game = LeducNode.create_game(3)
    #game.print_tree(only_leaves=True)

    # The strategy that always folds.
    strategy_folds = constant_action(game, 1, 0)
    strategy_folds.update(constant_action(game, 2, 0))
    exploitability_folds = compute_exploitability(game, strategy_folds)
    print("Exploitability of always folding: {}".format(exploitability_folds))

    # The strategy that always calls
    strategy_calls = constant_action(game, 1, 1)
    strategy_calls.update(constant_action(game, 2, 1))
    exploitability_calls = compute_exploitability(game, strategy_calls)
    print("Exploitability of always calling: {}".format(exploitability_calls))

    # The strategy that always raises.
    strategy_raises = constant_action(game, 1, 2)
    strategy_raises.update(constant_action(game, 2, 2))
    exploitability_raises = compute_exploitability(game, strategy_raises)
    print("Exploitability of always raising: {}".format(exploitability_raises))

    # A randomly chosen strategy
    strategy_random = random_strategy(game, 1)
    strategy_random.update(random_strategy(game, 2))
    exploitability_random = compute_exploitability(game, strategy_random)
    print("Exploitability of the random strategy: {}".format(exploitability_random))

    # A strategy that chooses actions uniformly at random.
    strategy_uniformly_random = uniformly_random_strategy(game, 1)
    strategy_uniformly_random.update(uniformly_random_strategy(game, 2))
    exploitability_uniformly_random = compute_exploitability(game, strategy_uniformly_random)
    print("Exploitability of the uniformly random strategy: {}".format(exploitability_uniformly_random))

    # Use CFR on Leduc
    print("Now running CFR")
    cfr(CFRGame(game))

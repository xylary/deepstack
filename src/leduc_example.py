# coding: utf-8
import numpy as np
from leduc import Leduc
from cfr import cfr
from cfr_game import CFRGame
from example_strategy import constant_action, random_strategy, uniformly_random_strategy
from best_response import best_response, compute_exploitability

if __name__ == "__main__":
    game = Leduc.create_game(3)
    #game.print_tree(only_leaves=True)

    print("Consider the strategy that always folds")
    strategy_folds = constant_action(game, 1, 0)
    strategy_folds.update(constant_action(game, 2, 0))
    exploitability_folds = compute_exploitability(game, strategy_folds)
    print("Exploitability of always folding: {}".format(exploitability_folds))

    print("Consider the strategy that always calls")
    strategy_calls = constant_action(game, 1, 1)
    strategy_calls.update(constant_action(game, 2, 1))
    exploitability_calls = compute_exploitability(game, strategy_calls)
    print("Exploitability of always calling: {}".format(exploitability_calls))

    print("Consider the strategy that always raises")
    strategy_raises = constant_action(game, 1, 2)
    strategy_raises.update(constant_action(game, 2, 2))
    exploitability_raises = compute_exploitability(game, strategy_raises)
    print("Exploitability of always raising: {}".format(exploitability_raises))

    print("Consider a randomly chosen strategy")
    strategy_random = random_strategy(game, 1)
    strategy_random.update(random_strategy(game, 2))
    exploitability_random = compute_exploitability(game, strategy_random)
    print("Exploitability of the random strategy: {}".format(exploitability_random))

    print("Consider a uniformly random strategy")
    strategy_uniformly_random = uniformly_random_strategy(game, 1)
    strategy_uniformly_random.update(uniformly_random_strategy(game, 2))
    exploitability_uniformly_random = compute_exploitability(game, strategy_uniformly_random)
    print("Exploitability of the uniformly random strategy: {}".format(exploitability_uniformly_random))

    # Use CFR on Leduc
    print("Now running CFR")
    cfr(CFRGame(game))

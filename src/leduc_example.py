# coding: utf-8
import numpy as np
from leduc import Leduc
from cfr import cfr
from cfr_game import CFRGame
from example_strategy import constant_action
from best_response import best_response

if __name__ == "__main__":
    game = Leduc.create_game(3)
    #game.print_tree(only_leaves=True)

    # Use CFR on Leduc
    cfr(CFRGame(game))
    

    n = 10000
#    print("We compute a random strategy for player 2")
#    strategy_2 = random_strategy(game, 2)
#    #print(strategy_2)
#    exploitability_2, br_against_2 = best_response(game, strategy_2, 1)
#    print("The best response against this random strategy has value: {}".format(exploitability_2))
#    #print("The best response strategy is")
#    #print(br_against_2)

#    results = game.expected_value(br_against_2, strategy_2, n)
#    print("We now run {} games of this strategy against the best response, and \
#    find the mean value for player 1 is {} with standard error {}".format(n,
#    np.mean(results), np.std(results) / np.sqrt(n)))


    print("Now consider the strategy where player 2 always folds.")
    strategy_2_0 = constant_action(game, 2, 0)
    print(strategy_2_0)
    exploitability_2_0, br_against_2_0 = best_response(game, strategy_2_0, 1)
    print("The best response against this strategy has value: \
    {}".format(exploitability_2_0))
    #print("The best response strategy is")
    #print(br_against_2_0)
    results = game.expected_value(br_against_2_0, strategy_2_0, n)
    print("We now run {} games of this strategy against the best response, and \
    find the mean value for player 1 is {} with standard error {}".format(n,
    np.mean(results), np.std(results) / np.sqrt(n)))

    print("Now consider the strategy where player 1 always folds.")
    strategy_1_0 = constant_action(game, 1, 0)
    exploitability_1_0, br_against_1_0 = best_response(game, strategy_1_0, 2)
    print("The best response against this strategy has value: \
    {}".format(exploitability_1_0))
    #print("The best response strategy is")
    #print(br_against_1_0)
    results = game.expected_value(strategy_1_0, br_against_1_0, n)
    print("We now run {} games of this strategy against the best response, and \
    find the mean value for player 1 is {} with standard error {}".format(n,
    np.mean(results), np.std(results) / np.sqrt(n)))

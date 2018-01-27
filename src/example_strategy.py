# coding: utf-8
import numpy as np

def random_distribution(n_items):
    """ Returns a random probability distribution over n items. Formally, we
    choose a point uniformly at random from the n-1 simplex.
    """
    return np.random.dirichlet([1.0 for i in range(n_items)])

def random_strategy(game, player):
    # We return a dictionary from information set identifiers to probabilities
    # over actions for the given player.
    # - game is an ExtensiveGame instance.
    info_sets = game.build_information_sets(player)

    # Restrict to information sets where the given player has to take an action.
    player_info_sets = {k: v for k, v in info_sets.items() if k.player == player}

    # Now randomly generate player 1's strategy and player 2's strategy. Define
    # a strategy as being a dictionary from information set identifiers to
    # probabilities over actions available in that information set.
    strategy = {}
    for node, identifier in player_info_sets.items():
        actions = node.children.keys()
        # Only need to add to the strategy for nodes whose information set has
        # not been included already.
        if not identifier in strategy:
            # Sample actions uniformly at random. Can change this later.
            probs = random_distribution(len(actions))
            strategy[identifier] = {a: p for a, p in zip(actions, probs)}

    return strategy

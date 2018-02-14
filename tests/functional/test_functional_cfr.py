import numpy as np
import pytest

from deepstack import cfr
from deepstack import leduc
from deepstack import cfr_game
from deepstack import example_strategy
from deepstack import best_response


def test_strategy_always_folds_on_leduc():
    game = leduc.Leduc.create_game(3)

    # The strategy that always folds.
    strategy_folds = example_strategy.constant_action(game, 1, 0)
    strategy_folds.update(example_strategy.constant_action(game, 2, 0))
    exploitability_folds = best_response.compute_exploitability(
        game, strategy_folds)

    # This is just expected because it is consistently computed
    expected_exploitability = 2.6
    eps = 1e-10
    assert abs(exploitability_folds - expected_exploitability) < eps


def test_strategy_always_calls_on_leduc():
    game = leduc.Leduc.create_game(3)

    # The strategy that always calls.
    strategy_calls = example_strategy.constant_action(game, 1, 1)
    strategy_calls.update(example_strategy.constant_action(game, 2, 1))
    exploitability_calls = best_response.compute_exploitability(
        game, strategy_calls)

    # This is just expected because it is consistently computed
    expected_exploitability = 4.266666666666
    eps = 1e-10
    assert abs(exploitability_calls - expected_exploitability) < eps


def test_strategy_always_raises_on_leduc():
    game = leduc.Leduc.create_game(3)

    # The strategy that always raises.
    strategy_raises = example_strategy.constant_action(game, 1, 2)
    strategy_raises.update(example_strategy.constant_action(game, 2, 2))
    exploitability_raises = best_response.compute_exploitability(
        game, strategy_raises)

    # This is just expected because it is consistently computed
    expected_exploitability = 11.5999999999
    eps = 1e-10
    assert abs(exploitability_raises - expected_exploitability) < eps


def test_strategy_random_on_leduc():
    game = leduc.Leduc.create_game(3)

    # Set the seed.
    seed = 2
    np.random.seed(seed)

    # The strategy that always raises
    strategy_random = example_strategy.random_strategy(game, 1)
    strategy_random.update(example_strategy.random_strategy(game, 2))
    exploitability_random = best_response.compute_exploitability(
        game, strategy_random)

    # This is just expected because it is consistently computed
    expected_exploitability = 5.297170632756803
    eps = 1e-10
    assert abs(exploitability_random - expected_exploitability) < eps


def test_strategy_uniformly_random_on_leduc():
    game = leduc.Leduc.create_game(3)

    # Set the seed.
    seed = 2
    np.random.seed(seed)

    # The strategy that always raises
    strategy_uniformly_random = example_strategy.uniformly_random_strategy(
        game, 1)
    strategy_uniformly_random.update(example_strategy.uniformly_random_strategy(
        game, 2))
    exploitability_uniformly_random = best_response.compute_exploitability(
        game, strategy_uniformly_random)

    # This is just expected because it is consistently computed
    expected_exploitability = 4.611111111111111
    eps = 1e-10
    assert abs(exploitability_uniformly_random - expected_exploitability) < eps


def test_cfr_on_leduc():
    # Set the seed.
    seed = 2
    np.random.seed(seed)

    # Test the cfr function on Leduc. This doesn't actually test anything, but
    # just checks that it runs.
    game = leduc.Leduc.create_game(3)
    cfr.cfr(cfr_game.CFRGame(game), num_iters=100)

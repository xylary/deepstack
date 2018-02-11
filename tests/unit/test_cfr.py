import numpy as np
import pytest

from deepstack import cfr

def test_cfr_compute_average_strategy():
    action_counts = {1: {1: 3, 2: 5}, 2: {2: 5, 3: 7}}
    expected = {1: {1: 3.0/8.0, 2: 5.0/8.0}, 2: {2: 5.0/12.0, 3: 7.0/12.0}}
    computed = cfr.compute_average_strategy(action_counts)
    assert expected == computed

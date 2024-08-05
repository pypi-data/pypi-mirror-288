from typing import ClassVar

from mergr.merger import Merger, Strategies

from .merge_funcs import add, multiply


def test_exact_strategy_picking():
    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {
            int: multiply,
        }

    merger = MyMerger({str: add})

    assert merger.pick_strategy(1) == multiply
    assert merger.pick_strategy("a") == add


def test_tuple_strategy_picking():
    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {
            (int, float): multiply,
        }

    merger = MyMerger({str: add})

    assert merger.pick_strategy(1) == multiply
    assert merger.pick_strategy(1.0) == multiply
    assert merger.pick_strategy("a") == add


def test_exact_strategy_over_tuple_strategy():
    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {
            (int, float, str): add,
            int: multiply,
        }

    merger = MyMerger({str: add})

    assert merger.pick_strategy(1) == multiply
    assert merger.pick_strategy(1.0) == add
    assert merger.pick_strategy("a") == add


def test_fallback_to_default_strategy():
    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {
            (int, float, str): add,
            int: multiply,
        }

    merger = MyMerger({str: add})

    assert merger.pick_strategy(1.0) == add
    assert merger.pick_strategy("a") == add
    assert merger.pick_strategy([1, 2, 3]) == merger.default_strategy

from typing import ClassVar

from mergr.merger import Merger, Strategies

from .merge_funcs import add, multiply


def test_default():
    merger = Merger()

    assert not hasattr(merger, "strategies")
    assert merger._strategies == {}
    assert merger.default_strategy(1, 2) == 1


def test_passing_default_strategy():
    merger = Merger(default_strategy=add)

    assert merger.default_strategy == add


def test_class_strategies():
    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {int: add}

    merger = MyMerger()

    assert len(merger.strategies) == 1
    assert merger.strategies[int] == add

    assert len(merger._strategies) == 1
    assert merger._strategies[int] == add


def test_initialization_with_strategies():
    merger = Merger(strategies={int: multiply})

    assert not hasattr(merger, "strategies")

    assert len(merger._strategies) == 1
    assert merger._strategies[int] == multiply


def test_strategies_merging():
    def multiply(a, b):
        return a * b

    class MyMerger(Merger):
        strategies: ClassVar[Strategies] = {int: add, str: add}

    merger = MyMerger({int: multiply, float: multiply})

    assert len(merger.strategies) == 2
    assert merger.strategies[int] == add
    assert merger.strategies[str] == add

    assert len(merger._strategies) == 3
    assert merger._strategies[int] == multiply
    assert merger._strategies[str] == add
    assert merger._strategies[float] == multiply

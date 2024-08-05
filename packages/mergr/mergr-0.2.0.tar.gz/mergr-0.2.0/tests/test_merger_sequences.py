import pytest

from mergr.merger import Merger

from .merge_funcs import add, multiply
from .mergers import SequenceDeepMerger


def test_sequences_extended():
    merge = Merger()

    assert merge((), [1]) == [1]
    assert merge(([],), [1]) == [[], 1]
    assert merge([1, 2], [3, 4]) == [1, 2, 3, 4]


def test_does_not_mutate_input_sequences():
    merge = Merger()

    a = (1, 2)
    b = [3, 4]

    assert merge(a, b) == [1, 2, 3, 4]

    assert a == (1, 2)
    assert b == [3, 4]


def test_fallback_to_default_if_b_is_not_sequence():
    merge = Merger()

    assert merge(None, [1, 2]) is None
    assert merge([1, 2], None) == [1, 2]
    assert merge([1, 2], 2) == [1, 2]
    assert merge([1, 2], "2") == [1, 2, "2"]
    assert merge([1, 2], {1: [2]}) == [1, 2]


def test_process_str_and_bytes_by_pick_strategy():
    merge = Merger({str: add})

    assert merge("a", "b") == "ab"
    assert merge(b"a", "b") == b"a"

    with pytest.raises(TypeError):
        merge("a", b"b")


def test_custom_sequences_merging_method():
    merge = SequenceDeepMerger({int: multiply})

    assert merge((1, 2), [3, 4, 5]) == [3, 8, 5]
    assert merge((1, 2, 3, 4), [2, 2]) == [2, 4, 3, 4]

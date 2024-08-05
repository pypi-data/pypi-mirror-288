from .mergers import NoneReplacer


def test_none_replacement():
    merger = NoneReplacer()

    assert merger.merge(None, 1) == 1
    assert merger.merge(1, None) == 1


def test_merger_object_call():
    merge = NoneReplacer()

    assert merge(1, 2) == 1
    assert merge([1, 2, 3], True) == [1, 2, 3]

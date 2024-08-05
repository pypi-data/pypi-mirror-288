from dataclasses import dataclass

from mergr.merger import Merger

from .merge_funcs import add, multiply
from .mergers import NoneReplacer


@dataclass(frozen=True)
class Nested1:
    nested1_prop_str: str
    nested1_prop_int: int


@dataclass(frozen=True)
class Nested2:
    nested2_prop_str: str
    nested2_prop_int: int


@dataclass(frozen=True)
class Root:
    prop_str: str
    prop_int: int

    nested1: Nested1
    nested2: Nested2 | None = None


dataobj1 = Root(
    prop_str="foo",
    prop_int=42,
    nested1=Nested1(nested1_prop_str="bar", nested1_prop_int=24),
    nested2=None,
)

dataobj2 = Root(
    prop_str="bar",
    prop_int=24,
    nested1=Nested1(nested1_prop_str="bar", nested1_prop_int=24),
    nested2=Nested2(nested2_prop_str="baz", nested2_prop_int=12),
)


def test_dataclasses_merged():
    merger = NoneReplacer(
        strategies={
            int: multiply,
            str: add,
        },
    )

    dataobj_merged = merger.merge(dataobj1, dataobj2)

    assert dataobj_merged.prop_str == "foobar"
    assert dataobj_merged.prop_int == 1008

    assert dataobj_merged.nested1.nested1_prop_str == "barbar"
    assert dataobj_merged.nested1.nested1_prop_int == 576

    assert dataobj_merged.nested2.nested2_prop_str == "baz"
    assert dataobj_merged.nested2.nested2_prop_int == 12


def test_dataclasses_not_merged_if_no_common_props():
    merger = Merger()

    dataobj1 = Nested1(nested1_prop_str="bar", nested1_prop_int=24)
    dataobj2 = Nested2(nested2_prop_str="baz", nested2_prop_int=12)

    assert merger.merge(dataobj1, dataobj2) == dataobj1


def test_fallback_to_default_if_b_is_not_dataclass():
    merger = Merger()

    assert merger.merge(dataobj1, 2) == dataobj1

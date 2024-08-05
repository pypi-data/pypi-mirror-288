from types import NoneType
from typing import TYPE_CHECKING, ClassVar

from mergr.merger import Merger, Strategies

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


class NoneReplacer(Merger):
    strategies: ClassVar[Strategies] = {
        NoneType: lambda _, b: b,
    }


class MappingDeepMerger(Merger):
    def merge_mappings(self, a: "Mapping", b: "Mapping") -> dict:
        return {
            k: self.merge(a[k], b[k])
            if k in a and k in b
            else a.get(k, b.get(k))
            for k in {*a.keys(), *b.keys()}
        }


class SequenceDeepMerger(Merger):
    def merge_sequences(self, a: "Sequence", b: "Sequence") -> list:
        a_len = len(a)
        b_len = len(b)
        if a_len == b_len:
            tail: Sequence = []
        elif a_len > b_len:
            tail = a[b_len:]
        else:
            tail = b[a_len:]
        return [
            *[self.merge(x[0], x[1]) for x in zip(a, b, strict=False)],
            *tail,
        ]

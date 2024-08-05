from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from typing import Any, ClassVar, Protocol, TypeAlias, runtime_checkable

MergeFn: TypeAlias = Callable[[Any, Any], Any]
Strategies: TypeAlias = dict[type | tuple[type, ...], MergeFn]


@runtime_checkable
class Dataclass(Protocol):
    __dataclass_fields__: dict[str, Any]


class Merger:
    strategies: ClassVar[Strategies]
    default_strategy: MergeFn

    _strategies: Strategies

    def __init__(
        self,
        strategies: Strategies | None = None,
        default_strategy: MergeFn = lambda a, _: a,
    ) -> None:
        if hasattr(self.__class__, "strategies"):
            _strategies = dict(self.__class__.strategies)
        else:
            _strategies = {}

        if strategies:
            _strategies.update(strategies)

        self._strategies = _strategies
        self.default_strategy = default_strategy

    def __call__(self, a: Any, b: Any) -> Any:
        return self.merge(a, b)

    def pick_strategy(self, a: Any) -> MergeFn:
        exact_type_strategy = self._strategies.get(type(a))

        if exact_type_strategy:
            return exact_type_strategy
        else:
            for types, strategy in self._strategies.items():
                if type(types) is tuple and type(a) in types:
                    return strategy

        return self.default_strategy

    def pick_and_merge(self, a: Any, b: Any) -> Any:
        return self.pick_strategy(a)(a, b)

    def merge_mappings(self, a: Mapping, b: Mapping) -> dict:
        return {**a, **b}

    def merge_sequences(self, a: Sequence, b: Sequence) -> list:
        return [*a, *b]

    def merge_dataclasses(self, a: Dataclass, b: Dataclass) -> Dataclass:
        updates = {}
        for field in a.__dataclass_fields__.values():
            if hasattr(b, field.name):
                value_a = getattr(a, field.name)
                value_b = getattr(b, field.name)
                updates[field.name] = self.merge(value_a, value_b)
        if len(updates):
            return replace(a, **updates)  # type: ignore[type-var]
        return a

    def merge(self, a: Any, b: Any) -> Any:
        if type(a) is str or type(a) is bytes:
            return self.pick_and_merge(a, b)

        if isinstance(a, Mapping) and isinstance(b, Mapping):
            return self.merge_mappings(a, b)

        if isinstance(a, Sequence) and isinstance(b, Sequence):
            return self.merge_sequences(a, b)

        if isinstance(a, Dataclass) and isinstance(b, Dataclass):
            return self.merge_dataclasses(a, b)

        return self.pick_and_merge(a, b)

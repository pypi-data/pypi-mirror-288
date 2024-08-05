from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar

T = TypeVar("T")
K = TypeVar("K")

# def first(collection: List[Any], default=None) -> Any:
#     if collection:
#         return collection[0]
#     return default


def first(iterable: Iterable[Any], default: Any = None) -> Any:
    return next(iter(iterable), default)


def groupby(
    elements: Iterable[T],
    key: Callable[[T], K],
    result: Optional[Dict[K, List[T]]] = None,
) -> Dict[K, List[T]]:
    _result: Dict[K, List[T]] = {} if result is None else result
    for e in elements:
        k = key(e)
        g = _result.setdefault(k, [])
        g.append(e)
    return _result


def uniqueby(elements: Iterable[T], key: Callable[[T], K]) -> List[Any]:
    result: Dict[K, T] = {}
    for e in elements:
        k = key(e)
        result.setdefault(k, e)
    return list(result.values())


__all__ = [
    "first",
    "groupby",
    "uniqueby",
]

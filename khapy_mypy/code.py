import abc
from typing import List, Union, Callable, Optional, TypeVar, Type, Tuple


# class X:
#     pass


# class Y(X):
#     pass


# def f1(data: List[X]) -> None:
#     pass


# data = []  # type: List[Y]
# f1(data)          # FAILS
# f1([Y(), Y()])    # OK


# T1 = Union[str, int]
# T2 = Union[T1, float]


# def f2(val: T2) -> None:
#     pass


# f2("s")


# t = []  # type: List[Callable[[str], None]]
# t.append(f2)


# d = {}  # type: Dict[int, int]
# for a in d:  # types: int
#     pass


# def f3(x: Optional[str]) -> str:
#     if x is not None:
#         return x
#     return "1"


# def f4(x: Optional[str]) -> str:
#     if x is None:
#         x = "1"
#     return x


# T1 = TypeVar('T1', Callable)


# def deco(func: T1) -> T1:
#     return func


# @deco
# def m():
#     pass


# class X:
#     def __init__(self) -> None:
#         pass


# def x() -> None:
#     pass


# def y() -> None:
#     return x()


# def t(x: Tuple[int, ...]) -> None:
#     pass


# t((1,))
# t((1, 2))


def f(x, y):
    r = x + y
    return r


def f1(x: int, y: int) -> int:
    r = x + y  # type: int
    return r


f(1, "2")
f1(1, "2")

d = {1: 2, 3: 4}
for key, val in d:
    pass

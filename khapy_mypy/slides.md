!SLIDE
## Типизация в питоне

### Данилов Константин, Mirantis
### http://koder-ua.blogspot.com/
### https://github.com/koder-ua/

!SLIDE
### Настоящие пацаны на английском
Dec 2016 BayPiggies Talk at LinkedIn: Introducing Type Annotations for Python - https://www.youtube.com/watch?v=ZP_QV4ccFHQ

!SLIDE
### Проблемы

~~~~{python}
    def do_something(data, size, operations, dim=12):
        .....
~~~~

!SLIDE
    * Подавляющее большинство кода типизировано (pypy/psyco)
    * Особенно библиотеки

!SLIDE
### Способы решение
    * докстринги - не фонтан
    * Type inference - RPython, pypy, nuitka, etc
    * typechecker - не совсем то

!SLIDE
### python 3000
    * function annotation
    * cython, pychecker, etc
~~~~{python}
    def f(x: 3, y: int) -> "something"
        pass
~~~~

!SLIDE
### mypy
    * mypy-lang.org
    * typing модуль в 3.5+
    * типизация переменных в 3.6

!SLIDE
### Как работает - базовые типы
~~~~{bash}
    $ pip install mypy-lang
    $ mypy PYTHON_FILES
~~~~

~~~~{make}
    ALL_FILES=$(shell find wally/ -type f -name '*.py')
    STUBS="stubs:.env/lib/python3.5/site-packages"
    ACTIVATE=cd ~/workspace/wally; source .env/bin/activate

    mypy:
            bash -c "${ACTIVATE}; MYPYPATH=${STUBS} python3 -m mypy -s ${ALL_FILES}"
~~~~

!SLIDE
### mypy in action

~~~~{python}
def f(x, y):
    r = x + y
    return r

def f1(x: int, y: int) -> int:
    # mypy и сам это умеет
    r = x + y  # type: int
    return r

f(1, 2)
f(1, "2")
f1(1, "2")  # code.py:98: error: Argument 2 to "f1" has
            # incompatible type "str"; expected "int"
~~~~


!SLIDE
### mypy in action
~~~~{python}
    d = {1: 2, 3: 4}
    for key, val in d:
        pass

    # code.py:101: error: 'builtins.int*' object is not iterable
~~~~

!SLIDE
### Как работает - контейнеры
~~~~{python}
from typing import List, Dict, Tuple, Optional, Callable

T = List[int]
Y = Dict[str, T]
M = Optional[str]
C = Callable[[str, str], int]
C1 = Callable[[], int]
~~~~

!SLIDE
### Как работает - более сложные случаи
~~~~{python}
from typing import TypeOf

T1 = TypeVar('T1', Callable)
def extract_func(data: Tuple[int, T1]) -> T1:
    return data[1]

#---------------------------------------------------

MyType = TypeVar('MyType')
def factory(c: TypeOf[MyType], *args, **kwargs) -> MyType:
    return c(*args, **kwargs)

class D:
    pass

x = factory(D)  # type: D

~~~~

!SLIDE
### Типизация в комментариях

~~~~{python}
def f1(x, y):
    # type: (int, int) -> int
    r = x + y  # type: int
    return r
~~~~

!SLIDE
### Типизация в pyi файлах
    * Именно там лежат стабы для stdlib 
    * Называете файл как модуль, но c расширением pyi
    * Поместить в папку, где его найдет mypy

~~~~{python}
    def f1(x: int, y: int) -> int :...
~~~~

!SLIDE
### Forward reference
~~~~{python}
    class X:
        def copy(self) -> 'X':
            ...
~~~~

!SLIDE
### Что меняется
    * Циклические зависимости - интерфейсы
    * Тут вам не Go. Наследовать интерфейся нужно явно

!SLIDE
### Проблемы c Optional
    * --strict-optional - cool!

!SLIDE
### Проблемы - поддержка
    * pycharm  - 3 from 5

!SLIDE
### Проблемы - баги
    * 534 открытых тикета в трекере. БОльшая часть баги.
~~~~{python}
    # fails in pycharm
    def f() -> Iterable[int]:
        yield 1
~~~~

!SLIDE
### Проблемы - баги. На коротких примерах не воспроизводится
~~~~{python}
    class Storage():
        def append(self, header: List[str], value: numpy.array, *path: str) -> None:
            ...

    class ResultStorage(IResultStorage):
        storage = None  # type: Storage
        ....
        def append_sensor(self, data: numpy.array, node_id: str, metrics_fqn: str) -> None:
            ...
            return self.storage.append([node_id, metrics_fqn, "unknown"], data, path)

    # wally/hlstorage.py: note: In member "append_sensor" of class "ResultStorage":
    # wally/hlstorage.py:165: error: No return value expected
~~~~

!SLIDE
### Проблемы
    * Документация
    * Сообщество

!SLIDE
### Сторонние библиотеки
    * Тут картинка с Траволтой
    * Для FP библиотек особенно сложно все

!SLIDE
### Kовариантность и контравариантность

~~~~{python}
    class X: pass
    class Y(X): pass

    def f1(data: List[X]) -> None:
        pass

    data = []  # type: List[Y]

    f1(data)
    # FAIL - Argument 1 to "f1" has incompatible type List[Y]; expected List[X]

    f1([Y(), Y()])    # OK
~~~~

!SLIDE
### Нехватка функциональности
    * Копирование типов
~~~~{python}
    def mydec(func: Callable[????]) -> Callable[????]:
        def closure(p1: int, *args, **kwargs):
            print(p1)
            return func(*args, **kwargs)
        return closure 

    X = TypeVar('X')
    def add1(x: X) -> typeof(X + int):
        return x + 1
~~~~


!SLIDE
### __XXX__

~~~~{python}
    class X:
        def __init__(self):
            pass

    # code.py: note: In member "__init__" of class "X":
    # code.py:66: error: Function is missing a type annotation


    class X:
        def __init__(self) -> None:
            pass
    # OK
~~~~

!SLIDE
### __XXX__

~~~~{python}
    class X:
        def __add__(self, o: 'X') -> 'X':
            pass

    # code.py: note: In member "__init__" of class "X":
    # code.py:66: error: Function is missing a type annotation


    class X:
        def __init__(self) -> None:
            pass
    # OK
~~~~


!SLIDE
### Появляются плохо читаемы описания типов
    * Callable[[A, Dict[B, T], List[M]], C]  == (A, {B:T}, [M]) -> C

!SLIDE
### Без cast пока никуда
~~~~{python}
    # OK
    auth_url = cast(str, openrc['os_auth_url'])

    # NOT OK
    RequestMethod = Callable[[str], Callable]
    PUT = cast(RequestMethod, partial(make_call, 'put'))  # type: RequestMethod
~~~~

!SLIDE
### Держите себя в руках


!SLIDE
### Итоги

### Вопросы и помидоры








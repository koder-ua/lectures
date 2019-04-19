Что такое типизация
Зачем она питону
Как это работает

Проблемы:

Желание остаться в рамках стандартного синтаксиса делает код весьма громоздким
    Callable[[int, int], int] == (int, int) -> int

Документация
Фичи
Баги (отдельно в mypy отдельно в pycharm, остальные еще не успели подтянуться. всего-то 3 года прошло)
Поддержка библиотек
Только проверка типов пока и не видно подвижек(cython/typechek - ауууу)

Функциональность:
    отсутствие const
    ковариантность и контравариантность
    Кросс-зависимости
    Нехватка функциональности - Tuple[int...]
    __XXX__ требуют лишних описаний типов
    нельзя скопировать тип функции или объекта, нету RET_TYPE(F), etc
    нельзя получить тип выражения, например TYPEOF(a+b)
    Сколь-нить сложные типы имеют ОЧЕНЬ сложные и нечитаемые описания
    без cast никуда
    Проверка на None таки сильно не всегда помогает (хотя strict nullable это круто)


    class A: pass
    class B(A): pass

    def r(t: List[A]) -> None:
        pass

    x = [B(), B()]  # type: List[B]
    r(x)


Наследование:

    class A:
        def copy(self) -> 'A':
            return self


    class B1(A):
        def copy(self) -> 'A':
            return self


    class B2(A):
        def copy(self) -> 'B':
            return self


    class B3(A):
        def copy(self) -> 'A':
            return cast(A, self)



class A:
    @classmethod
    def x(self) -> None:
        pass


ObjClass = TypeVar('ObjClass', bound=A)
ObjClass.x()



Links:
https://www.reddit.com/r/Python/comments/5nb0si/why_optional_type_hinting_in_python_is_not_that/
Dec 2016 BayPiggies Talk at LinkedIn: Introducing Type Annotations for Python - https://www.youtube.com/watch?v=ZP_QV4ccFHQ
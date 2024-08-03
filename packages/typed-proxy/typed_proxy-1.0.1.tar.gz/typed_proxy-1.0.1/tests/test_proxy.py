from proxy import Proxy


class Foo:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def f1(self) -> int:
        return self.a

    def f2(self) -> int:
        return self.b


class Bar(Foo, metaclass=Proxy):
    __proxied__: Foo

    def f2(self) -> int:
        return 1

    def f3(self) -> int:
        return self.__proxied__.b

    def f4(self) -> int:
        return self.f1()

    def f5(self) -> int:
        return self.__proxied__.f1()


class Baz(Foo, metaclass=Proxy):
    __proxied__: Foo

    def __init__(self, a: int, b: int, c: int) -> None:
        self.b = a
        self.c = b
        self.d = c

    def f2(self) -> int:
        return self.a + self.b

    def f3(self) -> int:
        return self.c

    def f4(self) -> int:
        return self.f1()

    def f5(self) -> int:
        return self.__proxied__.f1()


def test_proxy1() -> None:
    foo = Foo(1, 2)
    assert foo.f1() == 1
    assert foo.f2() == 2


def test_proxy2() -> None:
    bar = Bar.proxy(Foo(3, 4))
    assert bar.f1() == 3
    assert bar.f2() == 1
    assert bar.f3() == 4
    assert bar.f4() == 3
    assert bar.f5() == 3


def test_proxy3() -> None:
    baz = Baz.proxy(Foo(5, 6), 7, 8, 9)
    assert baz.f1() == 5
    assert baz.f2() == 12
    assert baz.f3() == 8
    assert baz.f4() == 5
    assert baz.f5() == 5

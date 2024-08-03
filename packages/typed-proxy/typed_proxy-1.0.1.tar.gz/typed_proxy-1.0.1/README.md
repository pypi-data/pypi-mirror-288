# typed-proxy
![Build status](https://github.com/jonghwanhyeon/typed-proxy/actions/workflows/publish.yml/badge.svg)

A Python package that provides a metaclass for creating proxy classes with type annotations.

## Help
See [documentation](https://typed-proxy.readthedocs.io) for more details

## Install
To install **typed-proxy**, simply use pip:

```console
$ pip install typed-proxy
```

## Examples
### Basic Usage
You can simply create a proxy class using the `Proxy` metaclass. The following example shows how to define a class `Bar` that proxies the class `Foo`.

```python
from proxy import Proxy


class Foo:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def f1(self) -> None:
        print(f"Foo(a={self.a}, b={self.b}).f1()")

    def f2(self) -> None:
        print(f"Foo(a={self.a}, b={self.b}).f2()")

    def f3(self) -> None:
        print(f"Foo(a={self.a}, b={self.b}).f3()")


class Bar(Foo, metaclass=Proxy):
    def f2(self) -> None:
        print(f"Bar(a={self.a}, b={self.b}).f2()")


bar = Bar.proxy(Foo(1, 2))
bar.f1() # Foo(a=1, b=2).f1()
bar.f2() # Bar(a=1, b=2).f2()
bar.f3() # Foo(a=1, b=2).f3()
```

### Accessing the Proxied Object
You can access the proxied object via the `__proxied__` attribute in the proxy class.

```python
class Bar(Foo, metaclass=Proxy):
    def f2(self) -> None:
        print(f"Bar(a={self.a}, b={self.b}).f2()")
        self.__proxied__.f2()


bar = Bar.proxy(Foo(1, 2))
bar.f1()  # Foo(a=1, b=2).f1()
bar.f2()  # Bar(a=1, b=2).f2() / Foo(a=1, b=2).f2()
bar.f3()  # Foo(a=1, b=2).f3()
```

### Explicitly Defining `__proxied__`
Since type checkers cannot statically resolve `__proxied__`, they might raise an issue such as `error: "Bar" has no attribute "__proxied__"`.
To resolve this, you can explicitly define the `__proxied__` attribute as follows.

```python
class Bar(Foo, metaclass=Proxy):
    __proxied__: Foo

    def f2(self) -> None:
        print(f"Bar(a={self.a}, b={self.b}).f2()")
        self.__proxied__.f2()


bar = Bar.proxy(Foo(1, 2))
bar.f1()  # Foo(a=1, b=2).f1()
bar.f2()  # Bar(a=1, b=2).f2() / Foo(a=1, b=2).f2()
bar.f3()  # Foo(a=1, b=2).f3()
```

### Custom `__init__()` for Proxy Class
You can define a custom `__init__()` method in the proxy class and provide arguments using the `proxy()` method with `*args` and `**kwargs`.

```python
class Bar(Foo, metaclass=Proxy):
    def __init__(self, a: int, b: int, c: int):
        self.b = a
        self.c = b
        self.d = c

    def f3(self) -> None:
        print(f"Bar(a={self.a}, b={self.b}, c={self.c}, d={self.d}).f3()")


bar = Bar.proxy(Foo(1, 2), 3, 4, 5)
bar.f1()  # Foo(a=1, b=2).f1()
bar.f2()  # Foo(a=1, b=2).f2()
bar.f3()  # Bar(a=1, b=3, c=4, d=5).f3()
```
from __future__ import annotations

from abc import ABCMeta
from contextlib import suppress
from typing import Any, TypeVar

T = TypeVar("T")


def _should_intercept(self: object, name: str) -> bool:
    names = set()

    with suppress(AttributeError):
        names.update(object.__getattribute__(self, "__slots__"))

    with suppress(AttributeError):
        names.update(object.__getattribute__(self, "__dict__").keys())

    with suppress(AttributeError):
        names.update(object.__getattribute__(type(self), "__slots__"))

    with suppress(AttributeError):
        names.update(object.__getattribute__(type(self), "__dict__").keys())

    return name in names


class Proxied(type):
    """A metaclass that proxies attribute access to another object."""

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Any:
        """Create a new class with proxied attribute access."""
        if "__init__" not in namespace:
            namespace["__init__"] = cls.__proxied_init__

        namespace["__getattribute__"] = cls.__proxied_getattribute__
        namespace["__repr__"] = cls.__proxied_repr__

        return super().__new__(cls, name, bases, namespace)

    def proxy(cls: type[T], target: Any, *args: Any, **kwargs: Any) -> T:
        """Create a proxy instance for the given `target`.

        The given `target` can be accessed via `__proxied__` attribute.
        If a proxy class defines its own `__init__()` method, you can provide arguments using `*args` and `**kwargs`.

        Args:
            cls: The class of the proxy.
            target: The target object to be proxied.
            *args: Additional arguments for `__init__()` method of the proxy class.
            **kwargs: Additional keyword arguments for `__init__()` method of the proxy class.

        Returns:
            A proxy instance for the target object.
        """
        instance = cls(*args, **kwargs)
        setattr(instance, "__proxied__", target)
        return instance

    def __proxied_init__(self: object) -> None:  # noqa: D105
        pass

    def __proxied_getattribute__(self: object, name: str) -> Any:  # noqa: D105
        if _should_intercept(self, name):
            return object.__getattribute__(self, name)

        proxied = object.__getattribute__(self, "__proxied__")
        return object.__getattribute__(proxied, name)

    def __proxied_repr__(self: object) -> str:  # noqa: D105
        proxied = object.__getattribute__(self, "__proxied__")
        return f"{type(self).__name__}({proxied})"


class Proxy(Proxied, type):
    """A metaclass that combines [`Proxied`][proxy.Proxied] and [`type`][type]."""


class ABCProxy(Proxied, ABCMeta):
    """A metaclass that combines [`Proxied`][proxy.Proxied] and [`ABCMeta`][abc.ABCMeta]."""

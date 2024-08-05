import functools
from typing import Callable, Any, Optional
from inspect import isfunction
import builtins


@functools.lru_cache()
def builtin_attributes():
    attributes = set()

    for typ in builtins.__dict__.values():
        if isinstance(typ, type):
            attributes |= {*dir(typ)}

    return set([key for key in attributes if key.startswith('_')])


def is_builtin(typ: type) -> bool:
    return Proxy(typ).__name__ in dir(builtins)


class Proxy:
    def __init__(self, obj):
        self._source = obj

    def __getattribute__(self, item):
        source = object.__getattribute__(self, '_source')
        is_source_type = issubclass(
            object.__getattribute__(source, '__class__'), type
        )

        result = (type if is_source_type else object).__getattribute__(source, item)

        if hasattr(result, '__get__') and not isfunction(result):
            result = result.__get__(
                None if is_source_type else source,
                object.__getattribute__(source, '__class__')
            )

        return result


class Descriptor:
    def __init__(self, obj):
        self._source = obj

    @property
    def __annotations__(self):
        proxy = Proxy(self._source)

        if isinstance(self._source, type):
            own_annotations = {}

            for base in [proxy.__class__, *reversed(proxy.__bases__)]:
                if is_builtin(base):
                    continue

                own_annotations.update(Descriptor(base).__annotations__)

            own_annotations.update(proxy.__dict__.get('__annotations__') or {})

            return own_annotations
        else:
            return Descriptor(proxy.__class__).__annotations__

    def __dir__(self):
        proxy = Proxy(self._source)

        if isinstance(self._source, type):
            own_keys = set()

            for base in [proxy.__class__, *reversed(proxy.__bases__)]:
                if is_builtin(base):
                    continue

                own_keys |= set(dir(Descriptor(base)))

            own_keys |= (
                    {*proxy.__dict__.keys(), *self.__annotations__.keys()} -
                    {'__doc__', '__weakref__', '__module__', '__annotations__', '__dict__'}
            )

            return list(own_keys)
        else:
            return list({*proxy.__dict__.keys(), *dir(Descriptor(proxy.__class__))})

    @property
    def __dict__(self) -> dict[str, tuple[Optional[type], Any]]:
        proxy = Proxy(self._source)
        dct = {}

        for key in dir(self):
            typ, value = self.__annotations__.get(key), None

            try:
                value = getattr(proxy, key)
            except AttributeError:
                pass

            dct[key] = (typ, value)

        return dct

    def filter(self, predicate: Callable[[str, type, Any], bool]):
        return {
            key: (typ, value)
            for key, (typ, value) in self.__dict__.items()
            if predicate(key, typ, value)
        }

    def tree(self):
        checked_entries = []

        if isinstance(self._source, type):
            for base in [self._source.__class__, *reversed(self._source.__bases__)]:
                if is_builtin(base):
                    continue

                for leaf in Descriptor(base).tree():
                    if leaf in checked_entries:
                        continue
                    else:
                        yield leaf
                        checked_entries.append(leaf)

            yield self._source
        else:
            raise TypeError()


class SharedMethod:
    def __init__(self, func: Callable):
        self._callback = func

    def __get__(self, instance, owner):
        def call(*args, **kwargs):
            return self._callback(instance or owner, *args, **kwargs)

        return call


class DualMeta(type):
    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        typ_instance = super().__new__(cls, name, bases, dct)

        for key in dct.keys():
            if key in builtin_attributes():
                continue

            value = getattr(Proxy(typ_instance), key)

            if (
                isfunction(value)
                and not hasattr(value, '__isabstractmethod__')
            ):
                setattr(typ_instance, key, SharedMethod(value))

        for key, (_, value) in Descriptor(cls).filter(
            lambda k, t, v: (
                k not in {'__new__', '__init__', '__call__'}
                and not hasattr(v, '__isabstractmethod__')
                and isfunction(v)
            )
        ).items():
            if key in builtin_attributes():
                setattr(typ_instance, key, value)
            else:
                setattr(typ_instance, key, SharedMethod(value))

        return typ_instance


class ModelType(type):
    def __call__(cls, **kwargs):
        instance = object.__new__(cls)

        for key, (_, value) in Descriptor(cls).filter(
            lambda k, t, v: not isfunction(v)
        ).items():
            if key in kwargs:
                setattr(instance, key, kwargs.pop(key))
            else:
                setattr(instance, key, value)

        if len(kwargs.keys()) > 0:
            raise AttributeError([key for key in kwargs])

        return instance

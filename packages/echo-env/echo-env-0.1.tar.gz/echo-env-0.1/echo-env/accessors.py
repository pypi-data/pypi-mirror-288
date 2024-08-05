from inspect import isfunction
from os import environ
from abc import abstractmethod
from wrappers import Proxy, Descriptor, DualMeta, ModelType


class NodeType(DualMeta, ModelType):
    def __new__(cls, *args, **kwargs):
        typ_instance = super().__new__(cls, *args, **kwargs)

        for key, (typ, value) in Descriptor(typ_instance).filter(
            lambda k, t, v: not isfunction(v) and not k.startswith('_')
        ).items():
            if isinstance(typ, NodeType) and value is None:
                default_value = typ()

                if hasattr(default_value, '__set_name__'):
                    default_value.__set_name__(typ_instance, key)

                setattr(typ_instance, key, default_value)

        return typ_instance

    @abstractmethod
    def _path(self) -> list[str]:
        pass

    def __getattribute__(self, item):
        desc = Descriptor(self)
        proxy = Proxy(self)

        if item.startswith('_'):
            return getattr(proxy, item)

        try:
            (typ, value) = desc.__dict__[item]

            if (
                isfunction(value) or (
                    isinstance(value, NodeType)
                    or isinstance(Proxy(value).__class__, NodeType)
                )
            ):
                return value

            env_name = '_'.join([*proxy._path(), item]).upper()

            env_variable = environ.get(env_name)

            if env_variable is None:
                return value
            else:
                if typ is not None:
                    env_variable = typ(env_variable)

                return env_variable
        except KeyError:
            raise AttributeError(f'{item}')


class Node(metaclass=NodeType):
    _root = None

    @abstractmethod
    def __set_name__(self, owner, name):
        pass


class Branch(Node):
    __alias__: str

    def __set_name__(self, owner, name):
        self.__alias__ = name
        self._root = owner

    def _path(self):
        nodes = []

        if self._root is not None:
            nodes.extend(self._root._path())

        nodes.append(self.__alias__)

        return nodes


class Bundle(Node):
    def __set_name__(self, owner, name):
        self._root = owner

    def _path(self):
        return (
            [] if self._root is None
            else self._root._path()
        )

# Copyright (c) OpenMMLab. All rights reserved.
import copy
from collections import OrderedDict
from typing import Any, Optional

from addict import Dict

from .lazy import LazyObject

BASE_KEY = '_base_'
DELETE_KEY = '_delete_'


def _lazy2string(cfg_dict, dict_type=None):
    if isinstance(cfg_dict, dict):
        dict_type = dict_type or type(cfg_dict)
        return dict_type({k: _lazy2string(v) for k, v in dict.items(cfg_dict)})
    elif isinstance(cfg_dict, (tuple, list)):
        return type(cfg_dict)(_lazy2string(v) for v in cfg_dict)
    elif isinstance(cfg_dict, LazyObject):
        return cfg_dict.dump_str
    else:
        return cfg_dict


class ConfigDict(Dict):
    """A dictionary for config which has the same interface as python's built-
    in dictionary and can be used as a normal dictionary.

    The Config class would transform the nested fields (dictionary-like fields)
    in config file into ``ConfigDict``.

    If the class attribute ``lazy``  is ``False``, users will get the
    object built by ``LazyObject`` or ``LazyAttr``, otherwise users will get
    the ``LazyObject`` or ``LazyAttr`` itself.

    The ``lazy`` should be set to ``True`` to avoid building the imported
    object during configuration parsing, and it should be set to False outside
    the Config to ensure that users do not experience the ``LazyObject``.
    """
    lazy = False

    def __init__(__self, *args, **kwargs):
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)
        for arg in args:
            if not arg:
                continue
            # Since ConfigDict.items will convert LazyObject to real object
            # automatically, we need to call super().items() to make sure
            # the LazyObject will not be converted.
            if isinstance(arg, ConfigDict):
                for key, val in dict.items(arg):
                    __self[key] = __self._hook(val)
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in dict.items(kwargs):
            __self[key] = __self._hook(val)

    def __missing__(self, name):
        raise KeyError(name)

    def __getattr__(self, name):
        try:
            value = super().__getattr__(name)
            if isinstance(value, LazyObject) and not self.lazy:
                value = value.build()
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no "
                                 f"attribute '{name}'")
        except Exception as e:
            raise e
        else:
            return value

    @classmethod
    def _hook(cls, item):
        # avoid to convert user defined dict to ConfigDict.
        if type(item) in (dict, OrderedDict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __setattr__(self, name, value):
        value = self._hook(value)
        return super().__setattr__(name, value)

    def __setitem__(self, name, value):
        value = self._hook(value)
        return super().__setitem__(name, value)

    def __getitem__(self, key):
        return self.build_lazy(super().__getitem__(key))

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in super().items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def __copy__(self):
        other = self.__class__()
        for key, value in super().items():
            other[key] = value
        return other

    copy = __copy__

    def __iter__(self):
        # Implement `__iter__` to overwrite the unpacking operator `**cfg_dict`
        # to get the built lazy object
        return iter(self.keys())

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get the value of the key. If class attribute ``lazy`` is True, the
        LazyObject will be built and returned.

        Args:
            key (str): The key.
            default (any, optional): The default value. Defaults to None.

        Returns:
            Any: The value of the key.
        """
        return self.build_lazy(super().get(key, default))

    def pop(self, key, default=None):
        """Pop the value of the key. If class attribute ``lazy`` is True, the
        LazyObject will be built and returned.

        Args:
            key (str): The key.
            default (any, optional): The default value. Defaults to None.

        Returns:
            Any: The value of the key.
        """
        return self.build_lazy(super().pop(key, default))

    def update(self, *args, **kwargs) -> None:
        """Override this method to make sure the LazyObject will not be built
        during updating."""
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError('update only accept one positional argument')
            # Avoid to used self.items to build LazyObject
            for key, value in dict.items(args[0]):
                other[key] = value

        for key, value in dict(kwargs).items():
            other[key] = value
        for k, v in other.items():
            if ((k not in self) or (not isinstance(self[k], dict))
                    or (not isinstance(v, dict))):
                self[k] = self._hook(v)
            else:
                self[k].update(v)

    def build_lazy(self, value: Any) -> Any:
        """If class attribute ``lazy`` is False, the LazyObject will be built
        and returned.

        Args:
            value (Any): The value to be built.

        Returns:
            Any: The built value.
        """
        if isinstance(value, LazyObject) and not self.lazy:
            value = value.build()
        return value

    def values(self):
        """Yield the values of the dictionary.

        If class attribute ``lazy`` is False, the value of ``LazyObject`` or
        ``LazyAttr`` will be built and returned.
        """
        values = []
        for value in super().values():
            values.append(self.build_lazy(value))
        return values

    def items(self):
        """Yield the keys and values of the dictionary.

        If class attribute ``lazy`` is False, the value of ``LazyObject`` or
        ``LazyAttr`` will be built and returned.
        """
        items = []
        for key, value in super().items():
            items.append((key, self.build_lazy(value)))
        return items

    def merge(self, other: dict):
        """Merge another dictionary into current dictionary.

        Args:
            other (dict): Another dictionary.
        """
        default = object()

        def _merge_a_into_b(a, b):
            if isinstance(a, dict):
                if not isinstance(b, dict):
                    a.pop(DELETE_KEY, None)
                    return a
                if a.pop(DELETE_KEY, False):
                    b.clear()
                all_keys = list(b.keys()) + list(a.keys())
                return {
                    key: _merge_a_into_b(a.get(key, default), b.get(key, default))
                    for key in all_keys if key != DELETE_KEY
                }
            else:
                return a if a is not default else b

        merged = _merge_a_into_b(copy.deepcopy(other), copy.deepcopy(self))
        self.clear()
        for key, value in merged.items():
            self[key] = value

    def __reduce_ex__(self, proto):
        # Override __reduce_ex__ to avoid `self.items` will be
        # called by CPython interpreter during pickling. See more details in
        # https://github.com/python/cpython/blob/8d61a71f9c81619e34d4a30b625922ebc83c561b/Objects/typeobject.c#L6196  # noqa: E501
        return (self.__class__, ({
            k: v
            for k, v in super().items()
        }, ), None, None, None, None)

    def __eq__(self, other):
        if isinstance(other, ConfigDict):
            return other.to_dict() == self.to_dict()
        elif isinstance(other, dict):
            return {k: v for k, v in self.items()} == other
        else:
            return False

    def _to_lazy_dict(self):
        """Convert the ConfigDict to a normal dictionary recursively, and keep
        the ``LazyObject`` or ``LazyAttr`` object not built."""

        def _to_dict(data):
            if isinstance(data, ConfigDict):
                return {key: _to_dict(value) for key, value in Dict.items(data)}
            elif isinstance(data, dict):
                return {key: _to_dict(value) for key, value in data.items()}
            elif isinstance(data, (list, tuple)):
                return type(data)(_to_dict(item) for item in data)
            else:
                return data

        return _to_dict(self)

    def to_dict(self):
        """Convert the ConfigDict to a normal dictionary recursively, and
        convert the ``LazyObject`` or ``LazyAttr`` to string."""
        return _lazy2string(self, dict_type=dict)

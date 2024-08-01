# Copyright (c) OpenMMLab. All rights reserved.
import builtins
import copy
import importlib
import inspect
import os
import platform
import sys
import tempfile
import uuid
from argparse import ArgumentParser
from importlib.machinery import PathFinder
from itertools import chain
from pathlib import Path
from types import BuiltinFunctionType, FunctionType, ModuleType
from typing import Any, Iterable, Optional, Tuple, Union
from warnings import warn

from .config_dict import ConfigDict
from .lazy import LazyImportContext, LazyObject, recover_lazy_field

BASE_KEY = '_base_'
DELETE_KEY = '_delete_'

if platform.system() == 'Windows':
    import regex as re
else:
    import re  # type: ignore


def format_inpsect(obj):
    file = inspect.getsourcefile(obj)
    lines, lineno = inspect.getsourcelines(obj)
    msg = f'File "{file}", line {lineno}\n--> {lines[0]}'
    return msg


def dump_extra_type(value):
    if isinstance(value, LazyObject):
        return value.dump_str
    if isinstance(value, (type, FunctionType, BuiltinFunctionType)):
        return LazyObject(value.__name__, value.__module__).dump_str
    if isinstance(value, ModuleType):
        return LazyObject(value.__name__).dump_str

    typename = type(value).__module__ + '.' + type(value).__name__
    if typename == 'torch.dtype':
        return LazyObject(str(value)).dump_str

    return None


def filter_imports(item):
    k, v = item
    # If the name is the same as the function/type name,
    # It should come from import instead of a field
    if v is BaseImportContext:
        # Avoid to make `read_base` a field.
        return False
    elif isinstance(v, (FunctionType, type)):
        return v.__name__ != k
    elif isinstance(v, LazyObject):
        return v.name != k
    elif isinstance(v, ModuleType):
        return False
    return True


def add_args(parser: ArgumentParser, cfg: dict, prefix: str = '') -> ArgumentParser:
    """Add config fields into argument parser.

    Args:
        parser (ArgumentParser): Argument parser.
        cfg (dict): Config dictionary.
        prefix (str, optional): Prefix of parser argument.
            Defaults to ''.

    Returns:
        ArgumentParser: Argument parser containing config fields.
    """
    for k, v in cfg.items():
        if isinstance(v, str):
            parser.add_argument('--' + prefix + k)
        elif isinstance(v, bool):
            parser.add_argument('--' + prefix + k, action='store_true')
        elif isinstance(v, int):
            parser.add_argument('--' + prefix + k, type=int)
        elif isinstance(v, float):
            parser.add_argument('--' + prefix + k, type=float)
        elif isinstance(v, dict):
            add_args(parser, v, prefix + k + '.')
        elif isinstance(v, Iterable):
            parser.add_argument('--' + prefix + k, type=type(next(iter(v))), nargs='+')
        else:
            warn(f'cannot parse key {prefix + k} of type {type(v)}')
    return parser


class Config:
    """A facility for config and config files.

    It supports common file formats as configs: python/json/yaml.
    ``Config.fromfile`` can parse a dictionary from a config file, then
    build a ``Config`` instance with the dictionary.
    The interface is the same as a dict object and also allows access config
    values as attributes.

    Args:
        cfg_dict (dict, optional): A config dictionary. Defaults to None.
        cfg_text (str, optional): Text of config. Defaults to None.
        filename (str or Path, optional): Name of config file.
            Defaults to None.

    Here is a simple example:

    Examples:
        >>> from mmcfg import Config
        >>> cfg = Config(dict(a=1, b=dict(b1=[0, 1])))
        >>> cfg.a
        1
        >>> cfg.b
        {'b1': [0, 1]}
        >>> cfg.b.b1
        [0, 1]
        >>> cfg = Config.fromfile('tests/data/py_config/base1.py')
        >>> cfg.item4
        'test'
        >>> cfg
        "Config [path: /home/username/projects/mmcfg/tests/data/py_config/base1.py]
        :"
        "{'item1': [1, 2], 'item2': {'a': 0}, 'item3': True, 'item4': 'test'}"

    You can find more advance usage in the `config tutorial`_.

    .. _config tutorial: https://mmengine.readthedocs.io/en/latest/advanced_tutorials/config.html
    """  # noqa: E501
    _pkg_prefix = '_mmcfg'

    def __init__(self,
                 cfg_dict: Optional[dict] = None,
                 cfg_text: Optional[str] = None,
                 filename: Optional[Union[str, Path]] = None):
        filename = str(filename) if isinstance(filename, Path) else filename
        if cfg_dict is None:
            cfg_dict = dict()
        elif not isinstance(cfg_dict, dict):
            raise TypeError('cfg_dict must be a dict, but '
                            f'got {type(cfg_dict)}')

        if not isinstance(cfg_dict, ConfigDict):
            cfg_dict = ConfigDict(cfg_dict)
        # Recover dumped lazy object like '<torch.nn.Linear>' from string
        cfg_dict = recover_lazy_field(cfg_dict)

        super(Config, self).__setattr__('_cfg_dict', cfg_dict)
        super(Config, self).__setattr__('_filename', filename)
        if cfg_text:
            text = cfg_text
        elif filename:
            with open(filename, encoding='utf-8') as f:
                text = f.read()
        else:
            text = ''

        super(Config, self).__setattr__('_text', text)

        self._sanity_check(self._to_lazy_dict())

    @staticmethod
    def _sanity_check(cfg):
        if isinstance(cfg, dict):
            for v in cfg.values():
                Config._sanity_check(v)
        elif isinstance(cfg, (tuple, list, set)):
            for v in cfg:
                Config._sanity_check(v)
        elif isinstance(cfg, (type, FunctionType)):
            if (Config._pkg_prefix in cfg.__module__ or '__main__' in cfg.__module__):
                msg = ('You cannot use temporary functions '
                       'as the value of a field.\n\n')
                msg += format_inpsect(cfg)
                raise ValueError(msg)

    @staticmethod
    def fromstring(cfg_str: str, file_format: str) -> 'Config':
        """Build a Config instance from config text.

        Args:
            cfg_str (str): Config text.
            file_format (str): Config file format corresponding to the
               config str. Only py/yml/yaml/json type are supported now!

        Returns:
            Config: Config object generated from ``cfg_str``.
        """
        if file_format not in ['.py', '.json', '.yaml', '.yml']:
            raise OSError('Only py/yml/yaml/json type are supported now!')

        # A temporary file can not be opened a second time on Windows.
        # See https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile for more details. # noqa
        # `temp_file` is opened first in `tempfile.NamedTemporaryFile` and
        #  second in `Config.from_file`.
        # In addition, a named temporary file will be removed after closed.
        # As a workaround we set `delete=False` and close the temporary file
        # before opening again.

        with tempfile.NamedTemporaryFile(
                'w', encoding='utf-8', suffix=file_format, delete=False) as temp_file:
            temp_file.write(cfg_str)

        cfg = Config.fromfile(temp_file.name)
        os.remove(temp_file.name)  # manually delete the temporary file
        return cfg

    @staticmethod
    def fromfile(filename: Union[str, Path], keep_imported: bool = False) -> 'Config':
        """Build a Config instance from config file.

        Args:
            filename (str or Path): Name of config file.
            use_predefined_variables (bool, optional): Whether to use
                predefined variables. Defaults to True.
            import_custom_modules (bool, optional): Whether to support
                importing custom modules in config. Defaults to None.
            lazy_import (bool): Whether to load config in `lazy_import` mode.
                If it is `None`, it will be deduced by the content of the
                config file. Defaults to None.

        Returns:
            Config: Config instance built from config file.
        """
        # Enable lazy import when parsing the config.
        # Using try-except to make sure ``ConfigDict.lazy`` will be reset
        # to False. See more details about lazy in the docstring of
        # ConfigDict
        filename = Path(filename).expanduser().resolve()
        ConfigDict.lazy = True
        try:
            module = Config._get_config_module(filename)
            module_dict = {
                k: getattr(module, k)
                for k in dir(module) if not k.startswith('__')
            }
            if not keep_imported:
                module_dict = dict(filter(filter_imports, module_dict.items()))

            cfg_dict = ConfigDict(module_dict)

            cfg = Config(cfg_dict, filename=filename)
        finally:
            ConfigDict.lazy = False
            for mod in list(sys.modules):
                if mod.startswith(Config._pkg_prefix):
                    del sys.modules[mod]

        return cfg

    @staticmethod
    def _merge_a_into_b(a: dict, b: dict, allow_list_keys: bool = False) -> dict:
        """Merge dict ``a`` into dict ``b`` (non-inplace).

        Values in ``a`` will overwrite ``b``. ``b`` is copied first to avoid
        in-place modifications.

        Args:
            a (dict): The source dict to be merged into ``b``.
            b (dict): The origin dict to be fetch keys from ``a``.
            allow_list_keys (bool): If True, int string keys (e.g. '0', '1')
              are allowed in source ``a`` and will replace the element of the
              corresponding index in b if b is a list. Defaults to False.

        Returns:
            dict: The modified dict of ``b`` using ``a``.

        Examples:
            # Normally merge a into b.
            >>> Config._merge_a_into_b(
            ...     dict(obj=dict(a=2)), dict(obj=dict(a=1)))
            {'obj': {'a': 2}}

            # Delete b first and merge a into b.
            >>> Config._merge_a_into_b(
            ...     dict(obj=dict(_delete_=True, a=2)), dict(obj=dict(a=1)))
            {'obj': {'a': 2}}

            # b is a list
            >>> Config._merge_a_into_b(
            ...     {'0': dict(a=2)}, [dict(a=1), dict(b=2)], True)
            [{'a': 2}, {'b': 2}]
        """
        b = b.copy()
        for k, v in a.items():
            if allow_list_keys and k.isdigit() and isinstance(b, list):
                k = int(k)
                if len(b) <= k:
                    raise KeyError(f'Index {k} exceeds the length of list {b}')
                b[k] = Config._merge_a_into_b(v, b[k], allow_list_keys)
            elif isinstance(v, dict):
                if k in b and not v.pop(DELETE_KEY, False):
                    allowed_types: Union[Tuple,
                                         type] = (dict,
                                                  list) if allow_list_keys else dict
                    if not isinstance(b[k], allowed_types):
                        raise TypeError(
                            f'{k}={v} in child config cannot inherit from '
                            f'base because {k} is a dict in the child config '
                            f'but is of type {type(b[k])} in base config. '
                            f'You may set `{DELETE_KEY}=True` to ignore the '
                            f'base config.')
                    b[k] = Config._merge_a_into_b(v, b[k], allow_list_keys)
                else:
                    b[k] = ConfigDict(v)
            else:
                b[k] = v
        return b

    @staticmethod
    def get_argparser(description=None):
        """Generate argparser from config file automatically (experimental)"""
        partial_parser = ArgumentParser(description=description)
        partial_parser.add_argument('config', help='config file path')
        cfg_file = partial_parser.parse_known_args()[0].config
        cfg = Config.fromfile(cfg_file)
        parser = ArgumentParser(description=description)
        parser.add_argument('config', help='config file path')
        add_args(parser, cfg)
        return parser, cfg

    @staticmethod
    def _get_config_module(filename: Union[str, Path]):
        file = Path(filename).absolute()
        module_name = re.sub(r'\W|^(?=\d)', '_', file.stem)
        # Build a unique module name to avoid conflict.
        _CFG_UID = uuid.uuid4().hex[:8]
        fullname = f'{Config._pkg_prefix}{_CFG_UID}_{module_name}'

        # import config file as a module
        with LazyImportContext():
            spec = importlib.util.spec_from_file_location(fullname, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
            sys.modules[fullname] = module

        return module

    @staticmethod
    def _dict_to_config_dict_lazy(cfg: Union[dict, tuple, list, Any]):
        """Recursively converts ``dict`` to :obj:`ConfigDict`. The only
        difference between ``_dict_to_config_dict_lazy`` and
        ``_dict_to_config_dict_lazy`` is that the former one does not consider
        the scope, and will not trigger the building of ``LazyObject``.

        Args:
            cfg (dict): Config dict.

        Returns:
            ConfigDict: Converted dict.
        """
        # Only the outer dict with key `type` should have the key `_scope_`.
        if isinstance(cfg, dict):
            cfg_dict = ConfigDict()
            for key, value in cfg.items():
                cfg_dict[key] = Config._dict_to_config_dict_lazy(value)
            return cfg_dict
        if isinstance(cfg, (tuple, list)):
            return type(cfg)(Config._dict_to_config_dict_lazy(_cfg) for _cfg in cfg)
        return cfg

    def get_pretty_text(self) -> str:
        """Get formatted python config text."""

        def _format_dict(input_dict):
            use_mapping = not all(str(k).isidentifier() for k in input_dict)

            if use_mapping:
                item_tmpl = '{k}: {v}'
            else:
                item_tmpl = '{k}={v}'

            items = []
            for k, v in input_dict.items():
                v_str = _format_basic_types(v)
                k_str = _format_basic_types(k) if use_mapping else k
                items.append(item_tmpl.format(k=k_str, v=v_str))
            items = ','.join(items)

            if use_mapping:
                return '{' + items + '}'
            else:
                return f'dict({items})'

        def _format_list_tuple_set(input_container):
            items = []

            for item in input_container:
                items.append(_format_basic_types(item))

            if isinstance(input_container, tuple):
                items = items + [''] if len(items) == 1 else items
                return '(' + ','.join(items) + ')'
            elif isinstance(input_container, list):
                return '[' + ','.join(items) + ']'
            elif isinstance(input_container, set):
                return '{' + ','.join(items) + '}'

        def _format_basic_types(input_):
            if isinstance(input_, str):
                return repr(input_)
            elif isinstance(input_, dict):
                return _format_dict(input_)
            elif isinstance(input_, (list, set, tuple)):
                return _format_list_tuple_set(input_)
            else:
                dump_str = dump_extra_type(input_)
                if dump_str is not None:
                    return repr(dump_str)
                else:
                    return str(input_)

        cfg_dict = self._to_lazy_dict()

        items = []
        for k, v in cfg_dict.items():
            items.append(f'{k} = {_format_basic_types(v)}')

        text = '\n'.join(items)

        return text

    def __repr__(self):
        return f'Config (path: {self._filename}): {self._cfg_dict.__repr__()}'

    def __len__(self):
        return len(self._cfg_dict)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._cfg_dict, name)

    def __getitem__(self, name):
        return self._cfg_dict.__getitem__(name)

    def __setattr__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setattr__(name, value)

    def __setitem__(self, name, value):
        if isinstance(value, dict):
            value = ConfigDict(value)
        self._cfg_dict.__setitem__(name, value)

    def __iter__(self):
        return iter(self._cfg_dict)

    def __getstate__(
            self) -> Tuple[dict, Optional[str], Optional[str], bool]:  # type: ignore
        return (self._cfg_dict, self._filename, self._text)

    def __setstate__(  # type: ignore
            self,
            state: Tuple[dict, Optional[str], Optional[str], bool],
    ):
        super(Config, self).__setattr__('_cfg_dict', state[0])
        super(Config, self).__setattr__('_filename', state[1])
        super(Config, self).__setattr__('_text', state[2])

    def __deepcopy__(self, memo):
        cls = self.__class__
        other = cls.__new__(cls)
        memo[id(self)] = other

        for key, value in self.__dict__.items():
            super(Config, other).__setattr__(key, copy.deepcopy(value, memo))

        return other

    def __copy__(self):
        cls = self.__class__
        other = cls.__new__(cls)
        other.__dict__.update(self.__dict__)
        super(Config, other).__setattr__('_cfg_dict', self._cfg_dict.copy())

        return other

    copy = __copy__

    def __dir__(self) -> Iterable[str]:
        # Used for IPython completion
        return chain(super().__dir__(), self._cfg_dict.keys())

    def _to_lazy_dict(self, keep_imported: bool = False) -> dict:
        """Convert config object to dictionary and filter the imported
        object."""
        res = self._cfg_dict._to_lazy_dict()

        if keep_imported:
            return res
        else:
            return dict(filter(filter_imports, res.items()))

    def dump(self, file: Optional[Union[str, Path]] = None) -> str:
        """Dump config to file or return config text.

        Args:
            file (str or Path, optional): If not specified, then the object
            is dumped to a str, otherwise to a file specified by the filename.
            Defaults to None.

        Returns:
            str or None: Config text.
        """
        cfg_dict = self.to_dict()
        if file is None:
            return self.get_pretty_text

        file = Path(file).expanduser().resolve()
        if file.suffix == '.py':
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.get_pretty_text)
        elif file.suffix == '.json':
            import json
            with open(file, 'w') as f:
                json.dump(cfg_dict, f)
        elif file.suffix in ['.yml', '.yaml']:
            import yaml
            from yaml import SafeDumper
            with open(file, 'w') as f:
                yaml.dump(cfg_dict, Dumper=SafeDumper)
        else:
            raise ValueError('Unsupported dump file type.')

    def to_dict(self, keep_imported: bool = False):
        """Convert all data in the config to a builtin ``dict``.

        Args:
            keep_imported (bool): Whether to keep the imported field.
                Defaults to False

        If you import third-party objects in the config file, all imported
        objects will be converted to a string like ``torch.optim.SGD``
        """
        _cfg_dict = self._to_lazy_dict(keep_imported=keep_imported)

        def lazy2string(cfg_dict):
            if isinstance(cfg_dict, dict):
                return type(cfg_dict)({k: lazy2string(v) for k, v in cfg_dict.items()})
            elif isinstance(cfg_dict, (tuple, list)):
                return type(cfg_dict)(lazy2string(v) for v in cfg_dict)
            else:
                dump_str = dump_extra_type(cfg_dict)
                return dump_str if dump_str is not None else cfg_dict

        return lazy2string(_cfg_dict)


class BaseImportContext():

    def __enter__(self):
        # Disable enabled lazy loader during parsing base
        self.lazy_importers = []
        for p in sys.meta_path:
            if isinstance(p, LazyImportContext) and p.enable:
                self.lazy_importers.append(p)
                p.enable = False

        old_import = builtins.__import__

        def new_import(name, globals=None, locals=None, fromlist=(), level=0):
            # For relative import, the new import allows import from files
            # which are not in a package.
            # For absolute import, the new import will try to find the python
            # file according to the module name literally, it's used to handle
            # importing from installed packages, like
            # `mmpretrain.configs.resnet.resnet18_8xb32_in1k`.

            cur_file = None

            # Try to import the base config source file
            if level != 0 and globals is not None:
                # For relative import path
                if '__file__' in globals:
                    loc = Path(globals['__file__']).parent
                else:
                    loc = Path(os.getcwd())
                cur_file = self.find_relative_file(loc, name, level - 1)
                if not cur_file.exists():
                    raise ImportError(f'Cannot find the base config "{name}" from '
                                      f'{loc}: {cur_file} does not exist.')
            elif level == 0:
                # For absolute import path
                pkg, _, mod = name.partition('.')
                pkg = PathFinder.find_spec(pkg)
                if mod and pkg.submodule_search_locations:
                    loc = Path(pkg.submodule_search_locations[0])
                    cur_file = self.find_relative_file(loc, mod)
                    if not cur_file.exists():
                        raise ImportError(f'Cannot find the base config "{name}": '
                                          f'{cur_file} does not exist.')

            # Recover the original import during handle the base config file.
            builtins.__import__ = old_import

            if cur_file is not None:
                mod = Config._get_config_module(cur_file)

                for k in dir(mod):
                    mod.__dict__[k] = Config._dict_to_config_dict_lazy(getattr(mod, k))
            else:
                mod = old_import(name, globals, locals, fromlist=fromlist, level=level)

            builtins.__import__ = new_import

            return mod

        self.old_import = old_import
        builtins.__import__ = new_import

    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.__import__ = self.old_import
        for p in self.lazy_importers:
            p.enable = True

    @staticmethod
    def find_relative_file(loc: Path, relative_import_path, level=0):
        if level > 0:
            loc = loc.parents[level - 1]
        names = relative_import_path.lstrip('.').split('.')

        for name in names:
            loc = loc / name

        return loc.with_suffix('.py')


read_base = BaseImportContext

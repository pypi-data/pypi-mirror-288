# Copyright (c) OpenMMLab. All rights reserved.
import copy
import difflib
import os.path as osp
import sys
from argparse import Action, ArgumentParser, Namespace
from typing import TYPE_CHECKING, Any, Sequence, Union

if TYPE_CHECKING:
    from mmcfg.config import Config

PYTHON_ROOT_DIR = osp.dirname(osp.dirname(sys.executable))


class ConfigParsingError(RuntimeError):
    """Raise error when failed to parse pure Python style config files."""


def diff(cfg1: Union[str, 'Config'], cfg2: Union[str, 'Config']) -> str:
    from mmcfg.config import Config
    if isinstance(cfg1, str):
        cfg1 = Config.fromfile(cfg1)

    if isinstance(cfg2, str):
        cfg2 = Config.fromfile(cfg2)

    res = difflib.unified_diff(cfg1.get_pretty_text.split('\n'),
                               cfg2.get_pretty_text.split('\n'))

    try:
        import rich.console
        import rich.text
    except ImportError:
        rich = None

    if rich is None:
        return '\n'.join(res)

    # Convert into rich format for better visualization
    console = rich.console.Console()
    text = rich.text.Text()
    for line in res:
        if line.startswith('+'):
            color = 'bright_green'
        elif line.startswith('-'):
            color = 'bright_red'
        else:
            color = 'bright_white'
        _text = rich.text.Text(line + '\n')
        _text.stylize(color)
        text.append(_text)

    with console.capture() as capture:
        console.print(text)

    return capture.get()


class DictAction(Action):
    """Argparse action to split an argument into KEY=VALUE form on the first =
    and append to a dictionary.

    List options can be passed as comma separated values, i.e 'KEY=V1,V2,V3',
    or with explicit brackets, i.e. 'KEY=[V1,V2,V3]'. It also support nested
    brackets to build list/tuple values. e.g. 'KEY=[(V1,V2),(V3,V4)]'
    """

    @staticmethod
    def _parse_int_float_bool(val: str) -> Union[int, float, bool, Any]:
        """Parse int/float/bool value in the string."""
        try:
            return int(val)
        except ValueError:
            pass
        try:
            return float(val)
        except ValueError:
            pass
        if val.lower() in ['true', 'false']:
            return True if val.lower() == 'true' else False
        if val == 'None':
            return None
        return val

    @staticmethod
    def _parse_iterable(val: str) -> Union[list, tuple, Any]:
        """Parse iterable values in the string.

        All elements inside '()' or '[]' are treated as iterable values.

        Args:
            val (str): Value string.

        Returns:
            list | tuple | Any: The expanded list or tuple from the string,
            or single value if no iterable values are found.

        Examples:
            >>> DictAction._parse_iterable('1,2,3')
            [1, 2, 3]
            >>> DictAction._parse_iterable('[a, b, c]')
            ['a', 'b', 'c']
            >>> DictAction._parse_iterable('[(1, 2, 3), [a, b], c]')
            [(1, 2, 3), ['a', 'b'], 'c']
        """

        def find_next_comma(string):
            """Find the position of next comma in the string.

            If no ',' is found in the string, return the string length. All
            chars inside '()' and '[]' are treated as one element and thus ','
            inside these brackets are ignored.
            """
            assert (string.count('(') == string.count(')')) and (
                    string.count('[') == string.count(']')), \
                f'Imbalanced brackets exist in {string}'
            end = len(string)
            for idx, char in enumerate(string):
                pre = string[:idx]
                # The string before this ',' is balanced
                if ((char == ',') and (pre.count('(') == pre.count(')'))
                        and (pre.count('[') == pre.count(']'))):
                    end = idx
                    break
            return end

        # Strip ' and " characters and replace whitespace.
        val = val.strip('\'\"').replace(' ', '')
        is_tuple = False
        if val.startswith('(') and val.endswith(')'):
            is_tuple = True
            val = val[1:-1]
        elif val.startswith('[') and val.endswith(']'):
            val = val[1:-1]
        elif ',' not in val:
            # val is a single value
            return DictAction._parse_int_float_bool(val)

        values = []
        while len(val) > 0:
            comma_idx = find_next_comma(val)
            element = DictAction._parse_iterable(val[:comma_idx])
            values.append(element)
            val = val[comma_idx + 1:]

        if is_tuple:
            return tuple(values)

        return values

    def __call__(self,
                 parser: ArgumentParser,
                 namespace: Namespace,
                 values: Union[str, Sequence[Any], None],
                 option_string: str = None):
        """Parse Variables in string and add them into argparser.

        Args:
            parser (ArgumentParser): Argument parser.
            namespace (Namespace): Argument namespace.
            values (Union[str, Sequence[Any], None]): Argument string.
            option_string (list[str], optional): Option string.
                Defaults to None.
        """
        # Copied behavior from `argparse._ExtendAction`.
        options = copy.copy(getattr(namespace, self.dest, None) or {})
        if values is not None:
            for kv in values:
                key, val = kv.split('=', maxsplit=1)
                options[key] = self._parse_iterable(val)
        setattr(namespace, self.dest, options)

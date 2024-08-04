from typing import Callable
import sys


XEET_GREEN = '\033[92m'
XEET_RED = '\033[91m'
XEET_YELLOW = '\033[93m'
XEET_WHITE = '\u001b[37;1m'
XEET_RESET = '\033[0m'
XEET_ORANGE = '\033[38;5;208m'

_colored_print = True


def xeet_color_enabled() -> bool:
    return _colored_print


def set_no_color_print() -> None:
    global _colored_print
    _colored_print = False


def _gen_print_func(color: str, dflt_file=None) -> Callable:
    def _print(*args, **kwargs) -> None:
        if "file" not in kwargs:
            kwargs["file"] = dflt_file
        if not _colored_print:
            print(*args, **kwargs)
            return
        print(color, end='', file=kwargs["file"])
        print(*args, **kwargs)
        print(XEET_RESET, end='', flush=True, file=kwargs["file"])
    return _print


pr_ok = _gen_print_func(XEET_GREEN)
pr_err = _gen_print_func(XEET_RED, dflt_file=sys.stderr)
pr_warn = _gen_print_func(XEET_YELLOW, dflt_file=sys.stderr)
pr_info = print
pr_verbose = print
pr_bright = _gen_print_func(XEET_WHITE)
pr_orange = _gen_print_func(XEET_ORANGE)

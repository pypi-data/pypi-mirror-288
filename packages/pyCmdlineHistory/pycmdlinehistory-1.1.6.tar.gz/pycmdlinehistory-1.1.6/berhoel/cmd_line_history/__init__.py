"""Save command line history and provide a command line completer for python."""

from __future__ import annotations

import atexit
from readline import set_pre_input_hook, write_history_file
from typing import TYPE_CHECKING

from .history import HISTORY_PATH, History

if TYPE_CHECKING:
    from pathlib import Path

__date__ = "2024/08/05 23:15:09 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = """Copyright © 2006 by Sunjoong LEE
Copyright © 2020, 2022, 2024 Berthold Höllmann"""
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


def save_history(history_path: Path | None = None) -> None:
    """Save command history at program exit."""
    if history_path is None:
        history_path = HISTORY_PATH
    write_history_file(history_path)


atexit.register(save_history)


def hook() -> None:
    """Clean up before rl completer is executed."""
    set_pre_input_hook()
    del locals()["History"]
    del locals()["__file__"]


set_pre_input_hook(hook)

locals()["__builtins__"]["history"] = History()

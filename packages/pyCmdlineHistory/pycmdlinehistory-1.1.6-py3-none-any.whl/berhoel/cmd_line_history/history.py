"""Handle command line history."""

from __future__ import annotations

from itertools import count as icount
from pathlib import Path
from readline import (
    clear_history,
    get_completer_delims,
    get_current_history_length,
    get_history_item,
    parse_and_bind,
    read_history_file,
    set_completer,
    set_completer_delims,
    set_history_length,
    write_history_file,
)
import sys
from tempfile import mkstemp

# Local library imports.
from .irl_completer import IrlCompleter

__date__ = "2024/08/05 23:45:50 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = """Copyright © 2006 by Sunjoong LEE
Copyright © 2020, 2022, 2024 Berthold Höllmann"""
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

HISTORY_PATH = Path.home() / f".pyhistory{sys.version_info.major}"
HISTORY_LENGTH = 100


class History:
    """Manage command history."""

    def __init__(self) -> None:
        """Intialize class instance."""
        self.recall()
        set_history_length(HISTORY_LENGTH)

        parse_and_bind("tab: complete")
        delims = get_completer_delims()
        set_completer_delims(delims)
        set_completer(IrlCompleter().complete)

    def __repr__(self) -> str:
        """Print out current history information."""
        length = get_current_history_length()
        if length > 1:
            try:
                return "\n".join(get_history_item(i) for i in range(1, length))
            except UnicodeDecodeError:
                return b"\n".join(
                    get_history_item(i).encode() for i in range(1, length)
                ).decode()

        else:
            return ""

    def __call__(self) -> None:
        """Print out current history information with line number."""
        length = get_current_history_length()
        if length > 1:
            kount = icount(1)
            try:
                for command in [get_history_item(i) for i in range(1, length)]:
                    print(f"{next(kount)}\t{command}")  # noqa:T201
            except UnicodeDecodeError:
                print(b"{next(kount)}\t{command}")  # noqa:T201

    @staticmethod
    def save(filename: Path, pos: int | None = None, end: int | None = None) -> None:
        """Write history number from pos to end into filename file."""
        length = get_current_history_length()
        if length > 1:
            if not pos:
                pos = 1
            elif pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end or end >= length:
                end = length
            end = length + end if end < 0 else end + 1

            with filename.open("w") as f_p:
                if pos < end:
                    for i in range(pos, end):
                        f_p.write(f"{get_history_item(i)}\n")
                else:
                    f_p.write(f"{get_history_item(pos)}\n")

    @staticmethod
    def clear() -> None:
        """Save the current history and clear it."""
        write_history_file(HISTORY_PATH)
        clear_history()

    @staticmethod
    def recall(history_path: Path = HISTORY_PATH) -> None:
        """Clear the current history and recall it from saved."""
        clear_history()
        if history_path.exists():
            read_history_file(history_path)

    @staticmethod
    def execute(pos: int, end: int | None = None) -> None:
        """Execute history number from pos to end."""
        length = get_current_history_length()
        if length > 1:
            if pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end:
                end = pos + 1
            elif end >= length:
                end = length
            end = length + end if end < 0 else end + 1

            filename = Path(mkstemp()[1])
            with filename.open("w") as f_p:
                for i in range(pos, end):
                    f_p.write(f"{get_history_item(i)}\n")
            try:
                with filename.open("rb") as f_p:
                    # exec previously saved commands
                    exec(compile(f_p.read(), filename, "exec"), locals())  # noqa:S102
                read_history_file(filename)
            except Exception:  # noqa:BLE001,S110 (ignore all errors)
                pass
            filename.unlink()

"""Command line comleter helper for python."""

from __future__ import annotations

from os import listdir
from os.path import split
from pathlib import Path
from pwd import getpwall
from rlcompleter import Completer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


__date__ = "2024/08/05 23:41:18 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = """Copyright © 2006 by Sunjoong LEE
Copyright © 2020, 2022, 2024 by Berthold Höllmann"""
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class IrlCompleter(Completer):
    """Commandline completer."""

    def __init__(self, namespace: dict[str, Any] | None = None) -> None:
        """Intialize class instance."""
        super().__init__(namespace=namespace)
        self.matches = [""]

    def complete(self, text: str, state: int) -> str | None:
        """Complete current command."""
        if text == "":
            # you could replace '    ' to \t if you indent via tab
            return ["    ", None][state]
        if text.count("'") == 1:
            if not state:
                self.file_matches(text, "'")
            try:
                return self.matches[state]
            except IndexError:
                return None
        if text.count('"') == 1:
            if not state:
                self.file_matches(text, '"')
            try:
                return self.matches[state]
            except IndexError:
                return None
        else:
            return Completer.complete(self, text, state)

    def file_matches(self, text: str, mark: str) -> None:
        """Check if input matche a file."""
        if "~" in text:
            if "/" in text:
                text = f'{mark}{Path(text[text.find("~"):]).expanduser()}'
            else:
                self.user_matches(text, mark)
                return

        text1 = text[1:]
        delim = "/"

        if not text1:
            directory = ""
        elif text1 == ".":
            directory = "."
        elif text1 == "..":
            directory = ".."
        elif text1 == "/":
            directory = "/"
            delim = ""
        elif text1.endswith("/"):
            directory = text1[:-1]
            delim = text1[len(directory) :]
        else:
            directory, partial = split(text1)
            delim = text1[len(directory) :][: -len(partial)]

        if directory:
            listing = [f"{mark}{directory}{delim}{x}" for x in listdir(directory)]
        else:
            listing = [f"{mark}{x}" for x in listdir(".")]

        n = len(text)
        self.matches = [x for x in listing if x[:n] == text]

    def user_matches(self, text: str, mark: str) -> None:
        """Upate `self.matches` according to input."""
        self.matches = [
            f"{mark}~{x.pw_name}" for x in getpwall() if x.pw_name.startswith(text)
        ]

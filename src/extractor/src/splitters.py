from .register import registry

import shlex
import re

from .base import Splitter, CharSplitter


@registry.add_splitter("character")
class Character(CharSplitter):
    def __init__(self, char):
        self.char = char
        super(Character, self).__init__(char)


@registry.add_splitter("space")
class Space(CharSplitter):
    char = " "


@registry.add_splitter("shlex")
class Shlex(Splitter):
    def split(self, message):
        return shlex.split(message, posix=True)


@registry.add_splitter("regex")
class Regex(Splitter):
    def __init__(self, regex):
        self.regex = regex
        super(Regex, self).__init__(regex)

    def split(self, message):
        return re.split(self.regex, message)


@registry.add_splitter("nothing")
class DoNothing(Splitter):
    def split(self, message):
        return message,  # Return a tuple containing only the message
import shlex
import re

from .base import Splitter, CharSplitter


class Character(CharSplitter):
    def __init__(self, char):
        self.char = char
        super(Character, self).__init__(char)


class Space(CharSplitter):
    char = " "


class Shlex(Splitter):
    def split(self, message):
        return shlex.split(message)


class Regex(Splitter):
    def __init__(self, regex):
        self.regex = regex
        super(Regex, self).__init__(regex)

    def split(self, message):
        return re.split(self.regex, message)


class DoNothing(Splitter):
    def split(self, message):
        return message,  # Return a tuple containing only the message
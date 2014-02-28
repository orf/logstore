from .base import Separator
import shlex


class RegexSeparator(Separator):
    def __init__(self, regex):
        self.regex = regex

    def separate(self, message):
        return self.regex.split(message)


class ShlexSeparator(Separator):
    def separate(self, message):
        return shlex.split(message)


class CharacterSeparator(Separator):
    def __init__(self, char):
        self.char = char

    def separate(self, message):
        return message.split(self.char)
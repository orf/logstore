from .base import Splitter
import shlex
import re


class Character(Splitter):
    def __init__(self, char):
        self.char = char
        super(Character, self).__init__(char)

    def separate(self, message):
        return message.split(self.char)


class Shlex(Splitter):
    def separate(self, message):
        return shlex.split(message)


class Regex(Splitter):
    def __init__(self, regex):
        self.regex = regex
        super(Regex, self).__init__(regex)

    def separate(self, message):
        return re.split(self.regex, message)


class DoNothing(Splitter):
    def separate(self, message):
        return message,  # Return a tuple containing only the message
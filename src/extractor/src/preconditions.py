from .base import Precondition


class StartsWithPrecondition(Precondition):
    def __init__(self, string):
        self.string = string

    def should_use(self, message):
        return message.startswith(self.string)


class RegexPrecondition(Precondition):
    def __init__(self, regex):
        self.regex = regex

    def should_use(self, message):
        return self.regex.match(message)


class ContainsPrecondition(Precondition):
    def __init__(self, string):
        self.string = string

    def should_use(self, message):
        return self.string in message
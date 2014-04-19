from .register import registry
from .base import Transformer
from datetime import datetime
import shlex


class Remove(Transformer):
    def transform(self, value):
        characters = self.args.get_arg("characters", slice=slice(0, None))
        limit = int(self.args.get_arg("limit", None, -1))
        for character in characters:
            value = value.replace(character, "", limit)

        return value, None


class Replace(Transformer):
    def transform(self, value):
        target = self.args.get_arg("target", 0)
        replace_with = self.args.get_arg("replace_with", 1)
        limit = int(self.args.get_arg("limit", None, -1))

        return value.replace(target, replace_with, limit), None


class LowerCase(Transformer):
    def transform(self, value):
        return value.lower(), None


class UpperCase(Transformer):
    def transform(self, value):
        return value.upper(), None


class TimeFormat(Transformer):
    def transform(self, value):
        pattern = self.args.get_arg("pattern", 0)
        return datetime.strptime(value, pattern)


registry.add("transformer", "remove", Remove)
registry.add("transformer", "time format", TimeFormat)
registry.add("transformer", "upper case", UpperCase)
registry.add("transformer", "lower case", LowerCase)
registry.add("transformer", "replace", Replace)
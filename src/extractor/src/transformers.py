from .register import registry
from .base import Transformer
from datetime import datetime
import shlex


@registry.add_transformer("remove")
class Remove(Transformer):
    def transform(self, value):
        characters = self.args.get_arg("characters", slice=slice(0, None))
        limit = int(self.args.get_arg("limit", None, -1))
        for character in characters:
            value = value.replace(character, "", limit)

        return value, None


@registry.add_transformer("replace")
class Replace(Transformer):
    def transform(self, value):
        target = self.args.get_arg("target", 0)
        replace_with = self.args.get_arg("replace_with", 1)
        limit = int(self.args.get_arg("limit", None, -1))

        return value.replace(target, replace_with, limit), None


@registry.add_transformer("lower case")
class LowerCase(Transformer):
    def transform(self, value):
        return value.lower(), None


@registry.add_transformer("upper case")
class UpperCase(Transformer):
    def transform(self, value):
        return value.upper(), None


@registry.add_transformer("time format")
class TimeFormat(Transformer):
    def transform(self, value):
        pattern = self.args.get_arg("pattern", 0)
        return datetime.strptime(value, pattern)
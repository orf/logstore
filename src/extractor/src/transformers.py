from .register import registry
from .base import Transformer
from datetime import datetime
import shlex


@registry.add_transformer("remove")
class RemoveTransformer(Transformer):
    def transform(self, value):
        characters = self.get_arg("characters", 0)
        limit = self.get_arg("limit", None)
        for character in shlex.split(characters):
            value = value.replace(character, "", limit or -1)

        return value, None


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
        pattern = self.get_arg("pattern", 0)
        return datetime.strptime(value, pattern)
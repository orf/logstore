from .register import registry
from .base import Transformer


@registry.add_transformer("remove")
class RemoveTransformer(Transformer):
    def __init__(self, characters):
        self.characters = characters

    def transform(self, value):
        for character in self.characters:
            value = value.replace(character, "")

        return value, None


@registry.add_transformer("lower case")
class LowerCase(Transformer):
    def transform(self, value):
        return value.lower(), None


@registry.add_transformer("upper case")
class UpperCase(Transformer):
    def transform(self, value):
        return value.upper(), None
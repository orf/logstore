from .base import Transformer


class RemoveTransformer(Transformer):
    def __init__(self, characters):
        self.characters = characters

    def transform(self, value):
        for character in self.characters:
            value = value.replace(character, "")

        return value, None


class LowerCase(Transformer):
    def transform(self, value):
        return value.lower(), None


class UpperCase(Transformer):
    def transform(self, value):
        return value.upper(), None
from .base import Transformer


class StripTransformer(Transformer):
    def __init__(self, characters):
        self.characters = characters

    def transform(self, value):
        return value.strip(self.characters), None
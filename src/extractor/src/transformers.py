from .base import Transformer


class StripTransformer(Transformer):
    def __init__(self, characters):
        self.characters = characters

    def transform(self, message):
        return message.strip(self.characters)
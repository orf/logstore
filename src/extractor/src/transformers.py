from .base import Transformer


class StipTransformer(Transformer):
    def __init__(self, characters):
        self.characters = characters

    def transform(self, message):
        return message.strip(self.characters)
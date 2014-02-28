from .base import Token


class TypedToken(Token):
    def __init__(self, *args, **kwargs):
        self.token_type = kwargs.pop("token_type")
        super(TypedToken, self).__init__(*args, **kwargs)

    def get_value(self):
        return {self.name: self.token_type(self.token)}
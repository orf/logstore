from .register import registry


@registry.add_type("int", display_name="Integer")
class Integer(int):
    pass


@registry.add_type("string")
class String(unicode):
    pass
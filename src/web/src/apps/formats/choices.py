from django_choice_object import Choice


class SplitterChoice(Choice):
    NONE = 0
    CHARACTER = 1
    SPACE = 2
    SHLEX = 3
    REGEX = 4


class TypeChoice(Choice):
    INTEGER = 1
    DATETIME = 2
    IP_ADDRESS = 3, "IP Address"


class TransformChoice(Choice):
    REMOVE = 1
    IP_LOOKUP = 2, "IP Country Lookup"
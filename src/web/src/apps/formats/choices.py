from django_choice_object import Choice


class SplitterChoice(Choice):
    NONE = 0
    CHARACTER = 1
    SHLEX = 2
    REGEX = 3


class TypeChoice(Choice):
    INTEGER = 1
    DATETIME = 2


class TransformChoice(Choice):
    SPLIT = 1
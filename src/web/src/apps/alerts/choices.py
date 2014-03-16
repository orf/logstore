from django_choice_object import Choice


class StatisticalChoice(Choice):
    MIN = "min"
    MAX = "max"
    STANDARD_DEVIATION = "std_deviation"
    VARIANCE = "variance"
    TOTAL = "total"
    MEAN = "mean"


class TimeSpanChoice(Choice):
    MINUTES = 0
    HOURS = 1
    DAYS = 2
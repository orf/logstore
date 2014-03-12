from django_choice_object import Choice


class TimeSpanChoice(Choice):
    MINUTES = 0
    HOURS = 1
    DAYS = 2
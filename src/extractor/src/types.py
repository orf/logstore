from .register import registry
from dateutil import parser
from datetime import datetime, date, time


def generic_datetime_type(value, type):
    if isinstance(value, basestring):
        return parser.parse(value, fuzzy=True)
    elif not isinstance(value, type):
        raise ValueError("Value %s is not a %s" % (value, type.__name__))
    return value


def get_datetime(value):
    return generic_datetime_type(value, datetime)


def get_date(value):
    return generic_datetime_type(value, date)


def get_time(value):
    return generic_datetime_type(value, time)


registry.add("type", "int", int, display_name="Integer")
registry.add("type", "string", str)
registry.add("type", "float", float)
registry.add("type", "datetime", get_datetime)
registry.add("type", "date", get_date)
registry.add("type", "time", get_time)
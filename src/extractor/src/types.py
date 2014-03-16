from .register import registry
from dateutil import parser
from datetime import datetime, date, time


@registry.add_type("int", display_name="Integer")
class Integer(int):
    pass


@registry.add_type("string")
class String(unicode):
    pass


def generic_datetime_type(value, type):
    if isinstance(value, basestring):
        return parser.parse(value)
    elif not isinstance(value, type):
        raise ValueError("Value %s is not a %s" % (value, type.__name__))
    return value


@registry.add_type("datetime")
def get_datetime(value):
    return generic_datetime_type(value, datetime)


@registry.add_type("date")
def get_date(value):
    return generic_datetime_type(value, date)


@registry.add_type("time")
def get_time(value):
    return generic_datetime_type(value, time)
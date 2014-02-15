import re
from twisted.python import usage
from logstore.conductor import conductor

# Stolen from Django
web_validator = re.compile(
        r'^http(s)?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def verify_addr(val):
    if not web_validator.match(val):
        raise ValueError("Please enter a valid HTTP(s) URL")
    return val.rstrip("/")


class Options(usage.Options):
    optParameters = [
        ("web_addr", "w", None, "The web address the master is running on", verify_addr)
    ]


def makeService(config):
    return conductor.make_service(config)
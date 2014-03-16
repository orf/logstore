import shlex
import re


def parse_arguments(args):
    returner = {}

    for i, arg in enumerate(shlex.split(args)):
        returner[i] = arg
        match = re.match('(?P<name>[a-zA-Z]+):(?P<value>.*)', arg)
        if match:
            groupdict = match.groupdict()
            returner[groupdict["name"]] = groupdict["value"]

    return returner
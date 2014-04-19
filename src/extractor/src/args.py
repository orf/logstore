import shlex
import re
from collections import OrderedDict


class Arguments(object):
    def __init__(self, args):
        self.args = parse_arguments(args)

    def get_arg(self, name, position=None, default=None, slice=None):
        if slice is not None:
            key_slice = [key for key in self.args.keys()[slice] if isinstance(key, int)]
            return [self.args[key] for key in key_slice]
        else:
            return self.args.get(name, self.args.get(position, default) if position is not None else default)


def parse_arguments(args):
    returner = OrderedDict()

    for i, arg in enumerate(shlex.split(args or "")):
        returner[i] = arg
        match = re.match('(?P<name>[a-zA-Z]+):(?P<value>.*)', arg)
        if match:
            groupdict = match.groupdict()
            returner[groupdict["name"]] = groupdict["value"]

    return returner
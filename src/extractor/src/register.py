from collections import namedtuple


RegistryEntry = namedtuple("RegistryEntry", "name cls")


class Registry(object):
    def __init__(self):
        self.splitter = {}
        self.transformer = {}
        self.type = {}

    def add(self, type, name, cls, display_name=None):
        getattr(self, type)[name] = RegistryEntry(display_name or name.capitalize(), cls)

    def decorate(self, type, name, display_name=None):
        def _register(cls):
            self.add(type, name, cls, display_name)
            return cls
        return _register

    def get_choices(self, type):
        return [(name, item.name) for name, item in getattr(self, type).items()]

    def get_by_name(self, type, name):
        return getattr(self, type)[name].cls

registry = Registry()
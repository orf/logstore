from collections import namedtuple


RegistryEntry = namedtuple("RegistryEntry", "name cls")


class Registry(object):
    def __init__(self):
        self.splitters = {}
        self.transformers = {}
        self.types = {}

    def add_splitter(self, name, display_name=None):
        def _register(cls):
            self.splitters[name] = RegistryEntry(display_name or name.capitalize(), cls)
            return cls
        return _register

    def add_transformer(self, name, display_name=None):
        def _register(cls):
            self.transformers[name] = RegistryEntry(display_name or name, cls)
            return cls
        return _register

    def add_type(self, name, display_name=None):
        def _register(cls):
            self.types[name] = RegistryEntry(display_name or name, cls)
            return cls
        return _register

    def get_transformer_choices(self):
        return [(name, item.name) for name, item in self.transformers.items()]

    def get_splitter_choices(self):
        return [(name, item.name) for name, item in self.transformers.items()]

    def get_type_choices(self):
        return [(name, item.name) for name, item in self.transformers.items()]

    def get_splitter_by_name(self, name):
        return self.splitters[name].cls

    def get_transformer_by_name(self, name):
        return self.transformers[name].cls

    def get_type_by_name(self, name):
        return self.types[name].cls


registry = Registry()
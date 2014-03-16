from string import Template
from . import args


class Format(object):
    def __init__(self, splitter, fields):
        self.splitter = splitter
        self.fields = fields

    def process(self, message):
        tokens = self.splitter.split(message)
        results = {}
        map(results.update, (f.process(tokens) for f in self.fields))
        return results


class Splitter(object):
    def __init__(self, _):
        pass

    def split(self, message):
        raise NotImplementedError()


class CharSplitter(Splitter):
    char = None

    def split(self, message):
        return message.split(self.char)


class Field(object):
    def __init__(self, name, source, transformers, type=None):
        self.name = name
        self.source = source
        self.transformers = transformers
        self.type = type

    def process(self, tokens, get_transform_list=False):
        token = self.source.get_token(tokens)
        path = self.name
        returner = {self.name: token}

        if get_transform_list:
            transform_list = []

        for transformer in self.transformers:
            try:
                new_token, new_path = transformer.transform(token)
            except Exception, e:
                transform_list.append((e, token))
                break

            if get_transform_list:
                transform_list.append(new_token)

            # Add new_token to path
            returner = self.set_from_path(returner, path, new_token)

            if new_path is not None:
                path = "%s.%s" % (path, new_path)
                token = self.get_from_path(returner, path)
            else:
                token = new_token

        if get_transform_list:
            return transform_list

        # Update the type
        if self.type:
            self.set_from_path(
                returner,
                path,
                self.type(self.get_from_path(returner, path))
            )

        return returner
        #return {self.name: token.get_data(type=self.type)}  #self.type(token) if self.type else token}

    def set_from_path(self, dictionary, path, new_value):
        split_path = path.split(".")
        path_traverse, path_end = split_path[0:-1], split_path[-1]

        r = dictionary
        for key_name in path_traverse:
            r = r[key_name]

        r[path_end] = new_value
        return dictionary

    def get_from_path(self, dictionary, path):
        r = dictionary
        for key_name in path.split("."):
            r = r[key_name]
        return r


class SourceTemplate(Template):
    idpattern = "[0-9]*" # Only numbers


class FieldSource(object):
    def __init__(self, expr):
        if expr.isdigit():  # It supports just specifying a index
            expr = "$" + expr
        self.template = SourceTemplate(expr)

    def get_token(self, tokens):
        return self.template.safe_substitute(**{str(idx): token for idx, token in enumerate(tokens)})


class Transformer(object):
    def __init__(self, arguments):
        self.args = args.parse_arguments(arguments)

    def get_arg(self, name, position):
        return self.args.get(name, self.args.get(position, None) if position is not None else None)

    def transform(self, value):
        raise NotImplementedError()


class Precondition(object):
    def should_use(self, message):
        raise NotImplementedError()
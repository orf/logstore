
"""
Example Data:
-----------------------------------------------------------------
Pinging google.com [83.100.221.240] with 32 bytes of data:
Request timed out.
Reply from 83.100.221.240: bytes=32 time=289ms TTL=60
Reply from 83.100.221.240: bytes=32 time=35ms TTL=60
64.242.88.10 - - [07/Mar/2004:16:05:49 -0800] "GET /twiki/bin/edit/Main/Double_bounce_sender?topicparent=Main.ConfigurationVariables HTTP/1.1" 401 12846
"""


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

    def process(self, tokens):
        token = self.source.get_token(tokens)

        for transformer in self.transformers:
            token = transformer.transform(token)

        return {self.name: self.type(token) if self.type else token}


class FieldSource(object):
    def __init__(self, source):
        self.source = source

    def get_token(self, tokens):
        sources = self.source.split(",")
        return "".join([tokens[int(i.strip())] for i in sources])


class Transformer(object):
    def transform(self, message):
        raise NotImplementedError()


class Precondition(object):
    def should_use(self, message):
        raise NotImplementedError()
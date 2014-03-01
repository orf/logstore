
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
    def __init__(self, separator):
        self.separator = separator
        self.tokens = []

    def process(self, message):
        self.tokens = self.separator.separate(message)


class Splitter(object):
    def __init__(self, _):
        pass

    def separate(self, message):
        raise NotImplementedError()


class Token(object):
    def __init__(self, token, name):
        self.token = token
        self.name = name

    def get_value(self):
        return {self.name: self.token}


class Precondition(object):
    def should_use(self, message):
        raise NotImplementedError()


class Transformer(object):
    def transform(self, message):
        raise NotImplementedError()
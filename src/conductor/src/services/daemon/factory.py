from thrift.transport import TTwisted
from .protocol import AuthenticatingThriftProtocol
from collections import namedtuple

ClientReference = namedtuple("ClientReference", "name instance")


class AuthenticatingThriftServerFactory(TTwisted.ThriftServerFactory):
    protocol = AuthenticatingThriftProtocol

    def __init__(self, *args, **kwargs):
        self.clients = {}
        self.frontend = kwargs.pop("frontend")
        self.queue = kwargs.pop("queue")
        self.websockets = kwargs.pop("websockets")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)
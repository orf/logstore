from collections import namedtuple, defaultdict

from thrift.transport import TTwisted

from .protocol import AuthenticatingThriftProtocol


ClientReference = namedtuple("ClientReference", "name instance")


class AuthenticatingThriftServerFactory(TTwisted.ThriftServerFactory):
    protocol = AuthenticatingThriftProtocol

    def __init__(self, *args, **kwargs):
        self.clients = defaultdict(list)
        self.frontend = kwargs.pop("frontend")
        self.queue = kwargs.pop("queue")
        self.stats = kwargs.pop("stats")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)

    def add_handler(self, handler):
        self.clients[handler.server_id].append(handler)

    def remove_handler(self, handler):
        if handler in self.clients[handler.server_id]:
            self.clients[handler.server_id].remove(handler)

    def terminate_connections(self, server_id):
        for handler in self.clients[server_id]:
            handler.transport.loseConnection()
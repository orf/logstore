from thrift.transport import TTwisted

from .protocol import InternalServiceProtocol


class InternalServiceFactory(TTwisted.ThriftServerFactory):
    protocol = InternalServiceProtocol

    def __init__(self, *args, **kwargs):
        self.websocket_component = kwargs.pop("websocket_component")
        self.stats = kwargs.pop("stats")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)
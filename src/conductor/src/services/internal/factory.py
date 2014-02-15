from thrift.transport import TTwisted
from .protocol import InternalServiceProtocol


class InternalServiceFactory(TTwisted.ThriftServerFactory):
    protocol = InternalServiceProtocol

    def __init__(self, *args, **kwargs):
        self.websocket_factory = kwargs.pop("websocket_factory")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)
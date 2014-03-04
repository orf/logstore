from thrift.transport import TTwisted

from .protocol import InternalServiceProtocol


class InternalServiceFactory(TTwisted.ThriftServerFactory):
    protocol = InternalServiceProtocol

    def __init__(self, *args, **kwargs):
        self.websocket_factory = kwargs.pop("websocket_factory")
        self.daemon_service_factory = kwargs.pop("daemon_service_factory")
        self.frontend = kwargs.pop("frontend")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)
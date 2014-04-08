from thrift.transport import TTwisted

from .protocol import InternalServiceProtocol


class InternalServiceFactory(TTwisted.ThriftServerFactory):
    protocol = InternalServiceProtocol

    def __init__(self, *args, **kwargs):
        self.websocket_component = kwargs.pop("websocket_component")
        self.daemon_service_factory = kwargs.pop("daemon_service_factory")
        self.queue_factory = kwargs.pop("queue_factory")
        self.stats = kwargs.pop("stats")
        TTwisted.ThriftServerFactory.__init__(self, *args, **kwargs)
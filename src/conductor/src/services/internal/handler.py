from logstore.thrift_protocol.twisted.protocol import InternalConductorService
from zope.interface import implements
from twisted.internet import defer


class InternalServiceHandler():
    implements(InternalConductorService.Iface)

    def __init__(self, factory):
        self.factory = factory

    @defer.inlineCallbacks
    def percolator_hit(self, logline, time, server_name, file_name, hits):
        yield self.factory.websocket_factory.got_percolator_hit(logline, time, server_name, file_name, hits)
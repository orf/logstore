from logstore.thrift_protocol.twisted.protocol import InternalConductorService
from zope.interface import implements
from twisted.internet import defer
from twisted.python import log


class InternalServiceHandler():
    implements(InternalConductorService.Iface)

    def __init__(self, factory):
        self.factory = factory

    @defer.inlineCallbacks
    def percolator_hit(self, logline, time, server_name, file_name, hits, search_id):
        for hit in hits:
            if hit.startswith("lu:"):
                self.factory.websocket_factory.got_percolator_hit(logline, time, server_name, file_name, hit, search_id)
            elif hit.startswith("ev:"):
                self.factory.frontend.got_event_hit(logline, time, server_name, file_name, hit, search_id)

    def remove_server(self, server_id):
        log.msg("Terminating all connections from %s" % server_id)
        self.factory.daemon_service_factory.terminate_connections(server_id)
        return True
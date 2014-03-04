from logstore.thrift_protocol.twisted.protocol import InternalConductorService
from zope.interface import implements
from twisted.internet import defer
from twisted.python import log


class InternalServiceHandler():
    implements(InternalConductorService.Iface)

    def __init__(self, factory):
        self.factory = factory

    @defer.inlineCallbacks
    def percolator_hit(self, *args, **kwargs):
        try:
            r = yield self._percolator_hit(*args, **kwargs)
            defer.returnValue(r)
        except Exception, e:
            print e

    @defer.inlineCallbacks
    def _percolator_hit(self, logline, time, server_name, file_name, hits, search_id):
        for hit in hits:
            if hit.startswith("lu:"):
                self.factory.websocket_factory.got_percolator_hit(logline, time, server_name, file_name, hit, search_id)
            elif hit.startswith("ev:"):
                self.factory.frontend.got_percolator_hit(logline, time, server_name, file_name, hit, search_id)
        yield True

    def remove_server(self, server_id):
        log.msg("Terminating all connections from %s" % server_id)
        self.factory.daemon_service_factory.terminate_connections(server_id)
        return True

    @defer.inlineCallbacks
    def create_event(self, event):
        print "Creating event percolator for %s" % event
        percolate_id = yield self.factory.websocket_factory.add_event_query(event.query)
        defer.returnValue(percolate_id)

    @defer.inlineCallbacks
    def remove_event(self, percolate_id):
        print "Removing percolator %s" % percolate_id
        yield self.factory.websocket_factory.remove_percolator(percolate_id)
        defer.returnValue(True)
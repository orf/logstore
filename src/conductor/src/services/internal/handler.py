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

        update_hits = [hit for hit in hits if hit.startswith("lu.")]
        #event_hits = [hit for hit in hits if hit.startswith("ev:")]

        for update in update_hits:
            yield self.factory.websocket_component.got_percolator_hit(logline, time, server_name, file_name,
                                                                    update, search_id)

        self.factory.stats.increment_stat("got_percolator_hit")

    def increment_stat(self, stat_name):
        self.factory.stats.increment_stat(stat_name)

    def remove_server(self, server_id):
        log.msg("Terminating all connections from %s" % server_id)
        self.factory.websocket_component.terminate_connections(server_id)
        return True

    @defer.inlineCallbacks
    def create_event(self, event):
        print "Creating event percolator for %s" % event
        percolate_id = yield self.factory.websocket_component.add_event_query(event.query)
        defer.returnValue(percolate_id)

    @defer.inlineCallbacks
    def remove_event(self, percolate_id):
        print "Removing percolator %s" % percolate_id
        try:
            yield self.factory.websocket_component.remove_percolator(percolate_id)
        except Exception, e:
            print "Error removing percolator: %s" % e
        defer.returnValue(True)
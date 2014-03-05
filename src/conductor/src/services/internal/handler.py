from logstore.thrift_protocol.twisted.protocol import InternalConductorService
from zope.interface import implements
from twisted.internet import defer
from twisted.python import log

import json


class InternalServiceHandler():
    implements(InternalConductorService.Iface)

    def __init__(self, factory):
        self.factory = factory


    @defer.inlineCallbacks
    def percolator_hit(self, logline, time, server_name, file_name, hits, search_id):

        update_hits = [hit for hit in hits if hit.startswith("lu:")]
        event_hits = [hit for hit in hits if hit.startswith("ev:")]

        for update in update_hits:
            yield self.factory.websocket_factory.got_percolator_hit(logline, time, server_name, file_name,
                                                                    update, search_id)

        if event_hits:
            pass  # Do nothing for now
            """self.factory.queue_factory.queue_analyse(json.dumps({"logline": logline,
                                                                 "time": time,
                                                                 "server_name": server_name,
                                                                 "file_name": file_name,
                                                                 "hits": event_hits,
                                                                 "search_id": search_id}))"""

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
        try:
            yield self.factory.websocket_factory.remove_percolator(percolate_id)
        except Exception, e:
            print "Error removing percolator: %s" % e
        defer.returnValue(True)
from autobahn.wamp1.protocol import WampServerProtocol, exportRpc
from twisted.internet import defer


class LiveUpdateProtocol(WampServerProtocol):
    def __init__(self):
        self.query_hash = None
        self.watched_stats = []

    @exportRpc
    @defer.inlineCallbacks
    def subscribe(self, query):
        self.query_hash = yield self.factory.add_live_update_query(query)
        self.registerForPubSub("logbook/live/%s" % self.query_hash, pubsub=self.SUBSCRIBE)
        defer.returnValue(self.query_hash)

    @exportRpc
    @defer.inlineCallbacks
    def change_subscription(self, query):
        if self.query_hash is not None:
            yield self.factory.remove_client(self.query_hash)
            self.query_hash = yield self.factory.add_live_update_query(query)
            defer.returnValue(self.query_hash)

    def onSessionOpen(self):
        print "Session open"
        self.registerForRpc(self, "logbook/update#")
        self.registerForPubSub("logbook/stat/", prefixMatch=True, pubsub=self.SUBSCRIBE)

    @defer.inlineCallbacks
    def connectionLost(self, reason):
        WampServerProtocol.connectionLost(self, reason)

        if self.query_hash is not None:
            yield self.factory.remove_client(self.query_hash)


from autobahn.wamp.protocol import ApplicationSession
from autobahn.twisted.wamp import FutureMixin
from collections import defaultdict

import json
import hashlib

from zope.interface import implements
from twisted.web.iweb import IBodyProducer
from twisted.internet import defer, reactor
from twisted.web.client import Agent, HTTPConnectionPool, readBody, Headers


http_pool = HTTPConnectionPool(reactor)
http_pool.maxPersistentPerHost = 10
web_agent = Agent(reactor, pool=http_pool)


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class LiveUpdateComponent(FutureMixin, ApplicationSession):
    def __init__(self, stats):
        self.watched_stats = []
        self.percolators = defaultdict(int)
        self.stat_watchers = defaultdict(int)
        self.stats = stats
        self.stats.global_watch(self.stat_watcher)
        self.clients = []

        ApplicationSession.__init__(self)

    def onConnect(self):
        self.join("realm1")

    @defer.inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.subscribe_to_query, "logbook.update.subscribe")
        yield self.register(self.unregister_query, "logbook.update.unsubscribe")

    @defer.inlineCallbacks
    def subscribe_to_query(self, query):
        query_hash = yield self.add_live_update_query(query_string=query["query_string"],
                                                      streams=query["stream"],
                                                      servers=query["server"])
        #self.registerForPubSub("logbook/live/%s" % self.query_hash, pubsub=self.SUBSCRIBE)
        defer.returnValue(query_hash)

    def stat_watcher(self, name, value):
        self.publish("logbook.stat.%s" % name, value)

    @defer.inlineCallbacks
    def unregister_query(self, query_hash):
        if query_hash in self.percolators:
            self.percolators[query_hash] -= 1

            if self.percolators[query_hash] == 0:
                print "Removing percolator"
                del self.percolators[query_hash]
                # ToDo: Some kind of locking here
                yield self.remove_percolator(query_hash)
                print "Removed percolator %s" % query_hash
        defer.returnValue("")

    @defer.inlineCallbacks
    def remove_percolator(self, query_hash):
        resp = yield web_agent.request(
            "DELETE",
            "http://localhost:9200/logs/.percolator/%s" % str(query_hash),
            Headers(),
        )

        yield readBody(resp)  # ToDo: Check if this this needed

    @defer.inlineCallbacks
    def add_live_update_query(self, query_string, streams=None, servers=None):
        query = "(%s)" % query_string
        if servers or streams:
            # Add servers and streams to the query string
            if servers:
                query += " AND (%s) " % " OR ".join(["server_id:%s" % server for server in servers])
            if streams:
                query += " AND (%s) " % " OR ".join(["stream_name:'%s'" % stream for stream in streams])

        query_hash = self.get_query_hash(query, namespace="lu")
        if query_hash not in self.percolators:
            yield self.create_percolator(query, query_hash)
        self.percolators[query_hash] += 1
        defer.returnValue(query_hash)

    @defer.inlineCallbacks
    def add_event_query(self, query):
        query_hash = self.get_query_hash(query, namespace="ev")
        r = yield self.create_percolator(query, query_hash)
        defer.returnValue(query_hash if r else None)

    def get_query_hash(self, query, namespace):
        return "%s.%s" % (namespace, hashlib.md5(query).hexdigest())

    @defer.inlineCallbacks
    def create_percolator(self, query, percolate_id):
        print "Adding query '%s' -> %s" % (query, percolate_id)

        resp = yield web_agent.request(
            "PUT",
            "http://localhost:9200/logs/.percolator/%s" % percolate_id,
            Headers(),
            StringProducer(json.dumps(
                {
                    "query": {
                        "query_string": {
                            "default_field": "message",
                            "query": query
                        }
                    }
                })
            )
        )

        body = yield readBody(resp)  # Is this needed?
        print "Percolator created: %s" % body

        defer.returnValue(True)

    @defer.inlineCallbacks
    def got_percolator_hit(self, line, time, server_id, file_name, hash, search_id):
        if hash in self.percolators:
            yield self.publish("logbook.live.%s" % hash,
                                {
                                    "_source": {
                                        "message": line,
                                        "data": {"time": time},
                                        "server_id": server_id,
                                        "stream_name": file_name,
                                        "search_id": search_id
                                    }
                                })


from autobahn.wamp1.protocol import WampServerFactory
from.protocol import LiveUpdateProtocol
from collections import defaultdict
from zope.interface import implements
from twisted.web.iweb import IBodyProducer
from twisted.internet import defer, reactor
from twisted.web.client import Agent, HTTPConnectionPool, readBody, Headers
from twisted.python import log
import hashlib
import json


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


class LiveUpdateFactory(WampServerFactory):
    protocol = LiveUpdateProtocol

    def __init__(self, *args, **kwargs):
        self.percolators = defaultdict(int)
        WampServerFactory.__init__(self, *args, **kwargs)

    @defer.inlineCallbacks
    def remove_client(self, query_hash):

        if query_hash in self.percolators:
            self.percolators[query_hash] -= 1

            if self.percolators[query_hash] == 0:
                print "Removing percolator"
                del self.percolators[query_hash]

                resp = yield web_agent.request(
                    "DELETE",
                    "http://localhost:9200/_percolator/logs/%s" % query_hash,
                    Headers(),
                    None
                )

                body = yield readBody(resp)  # ToDo: Check if this this needed


    @defer.inlineCallbacks
    def add_query(self, query):
        query_hash = hashlib.md5(query).hexdigest()
        print "Adding query '%s' -> %s" % (query, query_hash)
        create = query_hash not in self.percolators

        self.percolators[query_hash] += 1
        if create:
            print "Creating percolator..."
            resp = yield web_agent.request(
                "PUT",
                "http://localhost:9200/_percolator/logs/%s" % hashlib.md5(query).hexdigest(),
                Headers(),
                StringProducer(json.dumps(
                    {
                        "query": {
                            "query_string": {
                                "query": query
                            }
                        }
                    }))
            )

            body = yield readBody(resp)  # Is this needed?
            print "Percolator created: %s" % body

        defer.returnValue(query_hash)

    @defer.inlineCallbacks
    def got_percolator_hit(self, line, time, server_name, file_name, hashes):
        for hash in (h for h in hashes if h in self.percolators):
            yield self.dispatch("logbook/live/%s" % hash,
                                {
                                    "line": line,
                                    "time": time,
                                    "server": server_name,
                                    "file": file_name
                                })

    def notify_server_connected(self, token, server_id, server_ip):
        log.msg("Sending notification of server connection. Token: %s ID: %s IP: %s" % (token, server_id, server_ip))
        self.dispatch("logbook/live/install/%s" % token, {"id": server_id, "ip": server_ip})

    #def onClientSubscribed(self, proto, topicUri):
    #    print proto, topicUri
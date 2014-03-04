from collections import defaultdict
import hashlib
import json

from autobahn.wamp1.protocol import WampServerFactory
from zope.interface import implements
from twisted.web.iweb import IBodyProducer
from twisted.internet import defer, reactor
from twisted.web.client import Agent, HTTPConnectionPool, readBody, Headers
from twisted.python import log

from.protocol import LiveUpdateProtocol


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

                # ToDo: Some kind of locking here

                resp = yield web_agent.request(
                    "DELETE",
                    "http://localhost:9200/logs/.percolator/%s" % query_hash,
                    Headers(),
                    None
                )

                body = yield readBody(resp)  # ToDo: Check if this this needed


    @defer.inlineCallbacks
    def add_query(self, query):
        percolator_name = "lu:%s" % hashlib.md5(query).hexdigest()
        print "Adding query '%s' -> %s" % (query, percolator_name)
        create = percolator_name not in self.percolators

        self.percolators[percolator_name] += 1
        if create:
            print "Creating percolator..."
            resp = yield web_agent.request(
                "PUT",
                "http://localhost:9200/logs/.percolator/%s" % percolator_name,
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

        defer.returnValue(percolator_name)

    @defer.inlineCallbacks
    def got_percolator_hit(self, line, time, server_id, file_name, hash, search_id):
        if hash in self.percolators:
            yield self.dispatch("logbook/live/%s" % hash,
                                {
                                    "_source": {
                                        "message": line,
                                        "read_time": time,
                                        "server_id": server_id,
                                        "file_name": file_name,
                                        "search_id": search_id
                                    }
                                })

    def notify_server_connected(self, token, server_id, server_ip):
        log.msg("Sending notification of server connection. Token: %s ID: %s IP: %s" % (token, server_id, server_ip))
        self.dispatch("logbook/live/install/%s" % token, {"id": server_id, "ip": server_ip})

from twisted.internet import defer, reactor
from twisted.web import client
from twisted.web.client import HTTPConnectionPool
import treq

pool = HTTPConnectionPool(reactor, persistent=True)
#pool.maxPersistentPerHost = 4


class FrontendConnector(object):

    def __init__(self, frontend_addr):
        self.frontend_addr = frontend_addr
        self.lock = defer.DeferredLock()
        self.api_path = "%s/api" % self.frontend_addr

    @defer.inlineCallbacks
    def check_ip(self, ip_address):
        response = yield treq.get("%s/server_auth?ip=%s" % (self.api_path, ip_address))

        if response.code != 200:
            defer.returnValue(False)
        body = yield client.readBody(response)
        defer.returnValue(int(body))
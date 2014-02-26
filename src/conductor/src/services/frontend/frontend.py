from twisted.internet import defer, reactor
from twisted.web import client
from twisted.web.client import HTTPConnectionPool
import urllib
import json


pool = HTTPConnectionPool(reactor, persistent=True)
pool.maxPersistentPerHost = 4


class FrontendConnector(object):
    def __init__(self, frontend_addr):
        self.frontend_addr = frontend_addr

    @defer.inlineCallbacks
    def check_ip(self, ip_address):
        response = yield self._send_request("server_auth", {"ip": ip_address})
        if response.code != 200:
            defer.returnValue(False)

        body = yield client.readBody(response)
        defer.returnValue(int(body))

    # Internal methods
    @defer.inlineCallbacks
    def _send_request(self, api_method, args=None):
        """
        Send a request to the API method given and return the response
        """
        agent = client.Agent(reactor, pool=pool)
        path = "%s/api/%s?%s" % (self.frontend_addr, api_method, urllib.urlencode(args or {}))
        print "Requesting %s" % path
        response = yield agent.request(
            "GET",
            path
        )
        defer.returnValue(response)

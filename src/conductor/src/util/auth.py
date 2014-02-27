from twisted.internet import defer
from twisted.python import log


class AuthenticatingMixin(object):
    def __init__(self):
        self.server_id = None

    @defer.inlineCallbacks
    def _authenticate(self, host):
        is_auth = yield self.factory.frontend.check_ip(host.host)
        defer.returnValue(is_auth)

    @defer.inlineCallbacks
    def connectionMade(self):
        host = self.transport.getPeer()
        log.msg("Checking host %s" % host)

        self.transport.pauseProducing()
        try:
            self.server_id = yield self._authenticate(host)
        except Exception, e:
            log.err(_why="Error checking authentication status")

        if self.server_id:
            self.transport.resumeProducing()
            log.msg("Host is authenticated")
            self.auth_success(self.server_id)
        else:
            self.transport.loseConnection()
            log.msg("Host is not authenticated, connection dropped")
from thrift.transport import TTwisted, TTransport
from twisted.internet import defer
from .handler import ConductorServiceHandler
from logstore.thrift_protocol.twisted.protocol import ConductorService
from twisted.python import log


class AuthenticatingThriftProtocol(TTwisted.ThriftServerProtocol):

    def __init__(self):
        self.processor = None
        self.node_info = None

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
            is_authenticated = yield self._authenticate(host)
        except Exception, e:
            log.err(_why="Error checking authentication status")
            is_authenticated = False

        if is_authenticated:
            self.transport.resumeProducing()
            log.msg("Host is authenticated")
        else:
            self.transport.loseConnection()
            log.msg("Host is not authenticated, connection dropped")

    def connectionLost(self, reason=None):
        log.msg("Lost connection: %s" % self.node_info)

    @defer.inlineCallbacks
    def stringReceived(self, frame):
        # HACK HACK HACK HACK HACK
        # Getting at the transport inside a service handler is fucking impossible. So here we
        # create a new ServiceHandler for each call we receive. Horribly inefficient but it will do
        # until a better way is found
        # HACK HACK HACK HACK HACK
        tmi = TTransport.TMemoryBuffer(frame)
        tmo = TTransport.TMemoryBuffer()

        iprot = self.factory.iprot_factory.getProtocol(tmi)
        oprot = self.factory.oprot_factory.getProtocol(tmo)

        if self.processor is None:
            self.transport.pauseProducing()

            self.node_info = yield self.factory.frontend.get_node_info(self.transport.getPeer().host)

            self.factory.websockets.notify_server_connected(self.node_info["token"],
                                                            self.node_info["id"],
                                                            self.transport.getPeer().host)

            self.processor = ConductorService.Processor(
                ConductorServiceHandler(self.node_info, self.factory)
            )

            self.transport.resumeProducing()

        d = self.processor.process(iprot, oprot)
        d.addCallbacks(self.processOk, self.processError,
            callbackArgs=(tmo,))
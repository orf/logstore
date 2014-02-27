from thrift.transport import TTwisted, TTransport
from .handler import ConductorServiceHandler
from ...util.auth import AuthenticatingMixin
from logstore.thrift_protocol.twisted.protocol import ConductorService
from twisted.python import log


class AuthenticatingThriftProtocol(AuthenticatingMixin, TTwisted.ThriftServerProtocol):
    def __init__(self):
        self.processor = None
        super(AuthenticatingThriftProtocol, self).__init__()

    def connectionLost(self, reason=None):
        if self.server_id:
            log.msg("Lost connection: %s" % self.server_id)
            self.factory.remove_handler(self)

    def auth_success(self, server_id):
        self.factory.add_handler(self)

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
            self.processor = ConductorService.Processor(
                ConductorServiceHandler(self.server_id, self.factory)
            )

        d = self.processor.process(iprot, oprot)
        d.addCallbacks(self.processOk, self.processError,
            callbackArgs=(tmo,))
from thrift.transport import TTwisted, TTransport
from logstore.thrift_protocol.twisted.protocol import InternalConductorService

from .handler import InternalServiceHandler


class InternalServiceProtocol(TTwisted.ThriftServerProtocol):
    def __init__(self):
        self.processor = None

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

            self.processor = InternalConductorService.Processor(
                InternalServiceHandler(self.factory)
            )

            self.transport.resumeProducing()

        d = self.processor.process(iprot, oprot)
        d.addCallbacks(self.processOk, self.processError,
            callbackArgs=(tmo,))
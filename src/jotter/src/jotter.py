from logstore.thrift_protocol.twisted.protocol import ConductorService
from logstore.thrift_protocol.twisted.protocol.ttypes import LogLine
from twisted.internet import endpoints, stdio, reactor, defer, interfaces, task
from twisted.python import usage
from twisted.protocols import basic
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from zope.interface import implements
import sys
import datetime
import time


class Options(usage.Options):
     optParameters = [
         ["master", "m", None],
         ["name", "n", None]
     ]


class StandardInputForwarder(basic.LineReceiver):
    implements(interfaces.IHalfCloseableProtocol)
    from os import linesep as delimiter

    def __init__(self, endpoint_deferred, file_name):
        self.endpoint_deferred = endpoint_deferred
        self.file_name = file_name
        self.client = None
        self.stdin_closed = False
        self.start_time = time.time()

        self.queue = []
        self.flush_queue_loop = task.LoopingCall(self.flushQueue)

    @defer.inlineCallbacks
    def flushQueue(self):
        if not self.queue:
            defer.returnValue(None)

        self.pauseProducing()

        try:
            yield self.client.got_log_lines(self.queue)
        except Exception, e:
            print "Error: %s" % e
        else:
            self.queue = []

        self.resumeProducing()

    @defer.inlineCallbacks
    def connectionMade(self):
        self.pauseProducing()

        conn = yield self.endpoint_deferred
        self.client = yield conn.client

        self.resumeProducing()
        self.flush_queue_loop.start(1)

    def lineReceived(self, line):
        self.queue.append(
            LogLine(file_name=self.file_name,
                    read_time=datetime.datetime.now().isoformat(),
                    log_line=line)
        )

        if len(self.queue) == 100:
            self.flushQueue()

    def readConnectionLost(self):
        print "stdin closed"
        self.flushQueue()
        if self.flush_queue_loop.running:
            self.flush_queue_loop.stop()
        self.stdin_closed = True
        print time.time() - self.start_time


def main():
    options = Options()

    try:
        options.parseOptions(sys.argv[1:])
    except usage.UsageError, errorText:
        print "%s: %s" % (sys.argv[0], errorText)
        print "%s: Try --help for usage details" % sys.argv[0]
        sys.exit(1)

    endpoint = endpoints.clientFromString(reactor, options["master"])

    stdio.StandardIO(
        StandardInputForwarder(
            endpoint.connect(TTwisted.ThriftClientFactory(
                ConductorService.Client, TBinaryProtocol.TBinaryProtocolFactory())
            ),
            options["name"]
        )
    )

    reactor.run()


if __name__ == "__main__":
    main()
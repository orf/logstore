import sys
import datetime
import time

from logstore.thrift_protocol.twisted.protocol import ConductorService
from logstore.thrift_protocol.twisted.protocol.ttypes import LogLine
from twisted.internet import endpoints, stdio, reactor, defer, interfaces, task
from twisted.python import usage
from twisted.protocols import basic
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from zope.interface import implements


class Options(usage.Options):
     optParameters = [
         ["master", "m", None],
         ["name", "n", None],
         ["file", "f", None]
     ]


class StandardInputForwarder(basic.LineReceiver):
    implements(interfaces.IHalfCloseableProtocol)

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
            if self.stdin_closed and not self._buffer:
                reactor.stop()
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
        print "Conn made"
        self.pauseProducing()

        conn = yield self.endpoint_deferred
        self.client = yield conn.client

        self.resumeProducing()
        self.flush_queue_loop.start(1)

    def lineReceived(self, line):
        if line:
            self.queue.append(
                LogLine(file_name=self.file_name,
                        read_time=datetime.datetime.now().isoformat(),
                        log_line=line)
            )

    def readConnectionLost(self):
        print "stdin closed"
        self.stdin_closed = True
        print time.time() - self.start_time


class FileForwarder(object):
    implements(interfaces.IConsumer)

    def __init__(self, protocol):
        self.protocol = protocol
        self.producer = None
        self.disconnecting = False

    def registerProducer(self, producer, streaming):
        self.producer = producer
        self.producer.resumeProducing()

    def unregisterProducer(self):
        self.producer = None

    def write(self, data):
        self.protocol.dataReceived(data)


class ConnectionFactory(TTwisted.ThriftClientFactory):

    def clientConnectionLost(self, connector, reason):
        print "Connection lost: %s" % reason

    def clientConnectionFailed(self, connector, reason):
        print "Failed"

    def startedConnecting(self, connector):
        print "Started connecting"


@defer.inlineCallbacks
def send_file(file_path, forwarder):
    with open(file_path, "rb") as fd:
        file_producer = basic.FileSender()
        file_producer.disconnecting = False

        forwarder.makeConnection(file_producer)
        yield file_producer.beginFileTransfer(fd, FileForwarder(forwarder))
        forwarder.readConnectionLost()


def main():
    options = Options()

    try:
        options.parseOptions(sys.argv[1:])
    except usage.UsageError, errorText:
        print "%s: %s" % (sys.argv[0], errorText)
        print "%s: Try --help for usage details" % sys.argv[0]
        sys.exit(1)

    if options["file"] and not options["name"]:
        import os
        options["name"] = os.path.basename(options["file"])

    endpoint = endpoints.clientFromString(reactor, options["master"])
    forwarder = StandardInputForwarder(
        endpoint.connect(
            ConnectionFactory(
                ConductorService.Client, TBinaryProtocol.TBinaryProtocolFactory())
            ), options["name"]
        )

    if options["file"]:
        send_file(options["file"], forwarder)
    else:
        stdio.StandardIO(forwarder)

    reactor.run()


if __name__ == "__main__":
    main()
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet import endpoints
from logstore.thrift_protocol.twisted.protocol import ConductorService

import thrift
from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol
from twisted.python import usage
import sys


class Options(usage.Options):
     optParameters = [
         ["master", "m", None],
         ["name", "n", None]
     ]


def main():
    print "Got that shit"


if __name__ == "__main__":
    options = Options()

    try:
        options.parseOptions(sys.argv[1:])
    except usage.UsageError, errorText:
        print "%s: %s" % (sys.argv[0], errorText)
        print "%s: Try --help for usage details" % sys.argv[0]
        sys.exit(1)

    endpoint = endpoints.clientFromString(reactor, options["master"])
    d = endpoint.connect(TTwisted.ThriftClientFactory(
        ConductorService.Client, TBinaryProtocol.TBinaryProtocolFactory())
    )
    d.addCallback(lambda conn: conn.client)
    d.addCallback(main)
    reactor.run()


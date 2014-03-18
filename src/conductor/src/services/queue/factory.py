from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.defer import DeferredQueue, inlineCallbacks
from twisted.internet import reactor
import pika

from .protocol import RabbitMQConnectionProtocol


@inlineCallbacks
def rabbitmq_reconnector(client, factory, backoff=1):
    print "Attempting to connect to rabbitmq"
    try:
        yield client.connect(factory)
    except Exception, e:
        backoff = min(backoff * 2, 10)
        print "Backing off for %s" % backoff
        reactor.callLater(backoff, rabbitmq_reconnector, client, factory, backoff=backoff)


class RabbitMQConnectionFactory(ReconnectingClientFactory):
    maxDelay = 60
    protocol = RabbitMQConnectionProtocol

    def __init__(self):
        self.parse_queue = DeferredQueue()
        self.event_queue = DeferredQueue()

    def queue_message(self, message):
        self.parse_queue.put(message)

    #def queue_analyse(self, message):
    #    self.event_queue.put(message)

    def buildProtocol(self, addr):
        p = self.protocol(pika.ConnectionParameters(), input_queues={"parse": self.parse_queue})
        p.factory = self
        print "Built proto"
        return p

    def clientConnectionFailed(self, connector, reason):
        pass
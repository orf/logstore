from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.defer import DeferredQueue
import pika

from .protocol import RabbitMQConnectionProtocol


class RabbitMQConnectionFactory(ReconnectingClientFactory):
    maxDelay = 60
    protocol = RabbitMQConnectionProtocol

    def __init__(self):
        self.parse_queue = DeferredQueue()
        self.analyse_queue = DeferredQueue()

    def queue_message(self, message):
        self.parse_queue.put(message)

    def queue_analyse(self, message):
        self.analyse_queue.put(message)

    def buildProtocol(self, addr):
        p = self.protocol(pika.ConnectionParameters(), input_queues={"parse": self.parse_queue,
                                                                     "analyse": self.analyse_queue})
        p.factory = self
        return p
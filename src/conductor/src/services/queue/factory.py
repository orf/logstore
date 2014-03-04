from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.defer import DeferredQueue
import pika

from .protocol import RabbitMQConnectionProtocol


class RabbitMQConnectionFactory(ReconnectingClientFactory):
    maxDelay = 60
    protocol = RabbitMQConnectionProtocol

    def __init__(self):
        self.queue = DeferredQueue()

    def queue_message(self, message):
        self.queue.put(message)

    def buildProtocol(self, addr):
        p = self.protocol(pika.ConnectionParameters(), input_queue=self.queue)
        p.factory = self
        return p
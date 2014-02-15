from pika.adapters import twisted_connection
from twisted.internet import defer
from twisted.python import log

import pika


class RabbitMQConnectionProtocol(twisted_connection.TwistedProtocolConnection):
    def __init__(self, parameters, input_queue):
        self.__input_queue = input_queue
        super(RabbitMQConnectionProtocol, self).__init__(parameters)
        self._pump_messages()

    @defer.inlineCallbacks
    def _pump_messages(self):
        connection = yield self.ready
        channel = yield connection.channel()
        exchange = yield channel.exchange_declare(exchange="to_parse", type="fanout")
        queue = yield channel.queue_declare(queue="parse_queue", auto_delete=False, durable=True)
        yield channel.queue_bind(exchange="to_parse", queue="parse_queue")

        while True:
            message = yield self.__input_queue.get()

            try:
                if not connection.transport.connected:
                    raise Exception("Not connected to RabbitMQ!")
                yield channel.basic_publish(exchange="to_parse", body=message, routing_key="",
                                            properties=pika.BasicProperties(delivery_mode=2))
            except Exception, e:
                log.err(e, _why="Error sending message, terminating")
                self.__input_queue.put(message)
                defer.returnValue(None)

    def connectionLost(self, reason):
        self._set_connection_state(self.CONNECTION_CLOSED)  # Seems to be a bug or something, this isn't set.
        super(RabbitMQConnectionProtocol, self).connectionLost(reason)

    def connectionMade(self):
        self.factory.resetDelay()
        super(RabbitMQConnectionProtocol, self).connectionMade()
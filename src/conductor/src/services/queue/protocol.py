from pika.adapters import twisted_connection
from twisted.internet import defer
from twisted.python import log

import pika


# ToDo: Fix all of this. It doesn't handle rabbitmq reconnection *at all* :(


class RabbitMQConnectionProtocol(twisted_connection.TwistedProtocolConnection):
    def __init__(self, parameters, input_queues):
        super(RabbitMQConnectionProtocol, self).__init__(parameters)
        self.pump(input_queues)

    @defer.inlineCallbacks
    def pump(self, queues):
        connection = yield self.ready
        for name, queue in queues.items():
            self._pump_messages(connection, queue, name, name)

    @defer.inlineCallbacks
    def _pump_messages(self, connection, input_queue, exchange_name, queue_name):
        channel = yield connection.channel()
        exchange = yield channel.exchange_declare(exchange=exchange_name, type="fanout")
        queue = yield channel.queue_declare(queue=queue_name, auto_delete=False, durable=True)
        yield channel.queue_bind(exchange=exchange_name, queue=queue_name)

        while True:
            message = yield input_queue.get()
            try:
                if not connection.transport.connected:
                    raise Exception("Not connected to RabbitMQ!")
                yield channel.basic_publish(exchange=exchange_name, body=message, routing_key="",
                                            properties=pika.BasicProperties(delivery_mode=2))
            except Exception, e:
                log.err(e, _why="Error sending message, terminating")
                input_queue.put(message)
                defer.returnValue(None)

    def connectionLost(self, reason):
        #self._set_connection_state(self.CONNECTION_CLOSED)  # Seems to be a bug or something, this isn't set
        print "Lost RabbitMQ connection"
        super(RabbitMQConnectionProtocol, self).connectionLost(reason)

    def connectionMade(self):
        self.factory.resetDelay()
        super(RabbitMQConnectionProtocol, self).connectionMade()
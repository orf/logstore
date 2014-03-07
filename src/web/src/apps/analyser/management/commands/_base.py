from django.core.management.base import BaseCommand

import json

from elasticsearch import Elasticsearch
from logstore.thrift_protocol.plain.protocol import InternalConductorService
from thrift.transport import TSocket
from thrift.transport.TTransport import TFramedTransport, TBufferedTransport, TTransportException
from thrift.protocol import TBinaryProtocol
import pika
import time

FORMAT_CACHE = {}


class QueueProcessCommand(BaseCommand):
    args = ""
    help = ""
    name = ""

    queue_name = ""

    def get_thrift_client(self):
        transport = TBufferedTransport(
            TFramedTransport(
                TSocket.TSocket("localhost", 6061)
            ))

        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = InternalConductorService.Client(protocol)
        client.transport = transport

        wait = 1
        while True:
            try:
                transport.open()
                return client
            except TTransportException, e:
                wait = min(wait * 2, 15)
                print "Error connecting to conductor: %s. Backing off %s" % (e, wait)
                time.sleep(wait)

    def handle(self, *args, **options):
        self.es = Elasticsearch('http://localhost:9200/')

        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_qos(prefetch_count=20)

        self.client = self.get_thrift_client()

        self.stdout.write("Started %s on queue %s" % (self.name, self.queue_name))

        # Get ten messages and break out
        for method_frame, properties, body in channel.consume(self.queue_name):
            # We get a message in the following format:
            # ANALYZE|node_id|file_id|read_time|log_line...
            self.got_message(json.loads(body))
            channel.basic_ack(method_frame.delivery_tag)

        # Cancel the consumer and return any pending messages
        requeued_messages = channel.cancel()
        print 'Requeued %i messages' % requeued_messages

        # Close the channel and the connection
        channel.close()
        connection.close()

    def send_to_conductor(self, method_name, *args, **kwargs):
        wait = 1

        while True:
            try:
                return getattr(self.client, method_name)(*args, **kwargs)
            except Exception, e:
                wait = min(wait * 2, 10)
                print "Error from conductor (s:%s): %s" % (wait, e)
                self.client.transport.close()
                time.sleep(wait)
                self.client = self.get_thrift_client()

    def got_message(self, message):
        raise NotImplementedError()

    def create_mappings(self):
        self.es.indices.create("logs", body={
                "mappings": {
                    {"line": {
                        "properties": {
                            "message": {"type": "string"},
                            "read_time": {"type": "date"},

                            "data": {
                                "type": "object"
                            },

                            "server_id": {
                                "type": "integer",
                            },

                            "file_name": {
                                "type": "string"
                            }
                        }
                    }}
                }
            }
        )
import time

from logstore.thrift_protocol.plain.protocol import InternalConductorService
from logstore.thrift_protocol.plain.protocol.ttypes import Event
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from elasticsearch import Elasticsearch
from django.conf import settings
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from .models import EventQuery


es = Elasticsearch(settings.ELASTICSEARCH_URL)


@receiver(post_delete, sender=EventQuery)
def handle_event_query_deletion(sender, **kwargs):
    # Gotta disconnect the server from the conductor
    transport = TTransport.TFramedTransport(
        TSocket.TSocket("localhost", settings.CONDUCTOR_PORT))

    proto = TBinaryProtocol.TBinaryProtocol(transport)
    client = InternalConductorService.Client(proto)
    transport.open()
    client.remove_event(kwargs["instance"].percolate_hash)
    transport.close()


@receiver(post_save, sender=EventQuery)
def handle_event_query_creation(sender, **kwargs):
    print "Creating query"
    if kwargs["created"]:
        inst = kwargs["instance"]
        # Start a new percolator
        transport = TTransport.TFramedTransport(
        TSocket.TSocket("localhost", settings.CONDUCTOR_PORT))

        proto = TBinaryProtocol.TBinaryProtocol(transport)
        client = InternalConductorService.Client(proto)
        transport.open()
        hash_result = client.create_event(
            Event(id=inst.id,
                  name=inst.name,
                  query=inst.query)
        )
        transport.close()
        print "Hash: %s" % hash_result
        inst.percolate_hash = hash_result
        inst.save()
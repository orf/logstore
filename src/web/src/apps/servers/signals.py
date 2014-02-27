from logstore.thrift_protocol.plain.protocol import InternalConductorService
from django.db.models.signals import post_delete
from django.dispatch import receiver
from elasticsearch import Elasticsearch
from django.conf import settings
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from .models import Server
import time

es = Elasticsearch(settings.ELASTICSEARCH_URL)


@receiver(post_delete, sender=Server)
def handle_server_deletion(sender, **kwargs):
    # Gotta disconnect the server from the conductor
    transport = TTransport.TFramedTransport(
        TSocket.TSocket("localhost", settings.CONDUCTOR_PORT))

    proto = TBinaryProtocol.TBinaryProtocol(transport)
    client = InternalConductorService.Client(proto)
    transport.open()
    client.remove_server(kwargs["instance"].id)
    transport.close()


    t1 = time.time()
    es.delete_by_query("logs", "line", q="server_id:%s" % kwargs["instance"].id)
    t2 = time.time()
    print "Delete took %s" % str(t2-t1)

from dateutil.parser import parse
from elasticsearch import Elasticsearch
from logstore.thrift_protocol.plain.protocol import InternalConductorService
from thrift.transport import TSocket
from thrift.transport.TTransport import TFramedTransport, TBufferedTransport
from thrift.protocol import TBinaryProtocol
import json
import sys
import pika


def main():
    es = Elasticsearch('http://localhost:9200/')
    try:
        es.indices.create("logs", body={
            "mappings": {
                {"line": {
                    "properties": {
                        "message": {"type": "string"},
                        "read_time": {"type": "date"},

                        "data": {
                            "type": "object",
                            "dynamic": True,
                            "properties": {
                                "ip": {"type": "ip"}
                            }
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
        })
    except Exception:
        pass

    print "Index and mapping created"

    connection = pika.BlockingConnection()
    channel = connection.channel()

    transport = TBufferedTransport(
        TFramedTransport(
            TSocket.TSocket("localhost", 6061)
        ))

    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = InternalConductorService.Client(protocol)
    transport.open()

    # Get ten messages and break out
    for method_frame, properties, body in channel.consume('parse_queue'):
        # We get a message in the following format:
        # ANALYZE|node_id|file_id|read_time|log_line...
        message = json.loads(body)

        if message["method"] == "ANALYZE":
            message = message["data"]

            read_time = parse(message["read_time"])
            doc = {
                "message": message["log_message"],
                "read_time": read_time,
                "server_id": message["server_id"],
                "file_name": message["file_name"],
                "data": {
                    "omg": 10
                }
            }

            result = es.index(index="logs", doc_type="line", body=doc)
            percolate_result = es.percolate(index="logs", doc_type="line", id=result["_id"])
            if percolate_result["matches"]:
                client.percolator_hit(doc["message"],
                                      read_time.isoformat(),
                                      doc["server_id"],
                                      doc["file_name"],
                                      set((m["_id"] for m in percolate_result["matches"])))
            sys.stdout.write(".")

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)


    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    print 'Requeued %i messages' % requeued_messages

    # Close the channel and the connection
    channel.close()
    connection.close()
    transport.close()


if __name__ == "__main__":
    main()
from zope.interface import implements
from logstore.thrift_protocol.twisted.protocol import ConductorService
from twisted.python import log
import json


class ConductorServiceHandler(object):
    implements(ConductorService.Iface)

    def __init__(self, node_info, factory):
        self.node_info = node_info
        self.factory = factory
        log.msg("ConductorServiceHandler started for node %s" % node_info)

    def got_log_line(self, line):
        """
        Log a message from a watched LogFile
        """
        self.factory.queue.queue_message(
            json.dumps(
                {
                    "method": "ANALYZE",
                    "server_info": {"id": self.node_info["id"], "name": self.node_info["name"]},
                    "file_name": line.file_name,
                    "read_time": line.read_time,
                    "log_message": line.log_line
                }
            )
        )

        return True

    # Batch operations:
    def got_log_lines(self, lines):
        for line in lines:
            self.got_log_line(line)

        return True

    def hello_world(self):
        return True
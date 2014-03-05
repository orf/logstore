import json

from zope.interface import implements
from logstore.thrift_protocol.twisted.protocol import ConductorService
from twisted.python import log


class ConductorServiceHandler(object):
    implements(ConductorService.Iface)

    def __init__(self, server_id, factory):
        self.server_id = server_id
        self.factory = factory
        log.msg("ConductorServiceHandler started for server #%s" % server_id)

    def got_log_line(self, line):
        """
        Log a message from a watched LogFile
        """
        self.factory.queue.queue_message(
            json.dumps(
                {
                    "server_id": self.server_id,
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
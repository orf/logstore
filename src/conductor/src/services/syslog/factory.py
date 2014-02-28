from twisted.internet.protocol import ServerFactory
from .protocol import SysLogProtocol


class SysLogFactory(ServerFactory):
    protocol = SysLogProtocol

    def __init__(self, frontend, queue):
        self.frontend = frontend
        self.queue = queue
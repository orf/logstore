from twisted.internet.protocol import ServerFactory
from .protocol import SysLogProtocol


class SysLogFactory(ServerFactory):
    protocol = SysLogProtocol

    def __init__(self, frontend):
        self.frontend = frontend
from twisted.internet.protocol import ServerFactory
from .protocol import SysLogProtocol


class SysLogFactory(ServerFactory):
    protocol = SysLogProtocol
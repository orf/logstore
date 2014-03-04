from thrift.protocol import TBinaryProtocol
from twisted.application import internet, service

from .services.frontend.frontend import FrontendConnector
from .services.daemon.factory import AuthenticatingThriftServerFactory
from .services.internal.factory import InternalServiceFactory
from .services.queue.factory import RabbitMQConnectionFactory
from .services.live_update.factory import LiveUpdateFactory
from .services.syslog.factory import SysLogFactory


def make_daemon_server_factory(frontend, queue, ws):
    return AuthenticatingThriftServerFactory(None, TBinaryProtocol.TBinaryProtocolFactory(),
                                             frontend=frontend, queue=queue, websockets=ws)


def make_internal_server_factory(ws_factory, daemon_service_factory, frontend):
    return InternalServiceFactory(None, TBinaryProtocol.TBinaryProtocolFactory(),
                                  websocket_factory=ws_factory,
                                  daemon_service_factory=daemon_service_factory,
                                  frontend=frontend)


def make_service(config):
    queue_factory = RabbitMQConnectionFactory()
    frontend = FrontendConnector(config["web_addr"])

    ws_factory = LiveUpdateFactory("ws://localhost:6062")
    conductor_service = service.MultiService()
    daemon_service_factory = make_daemon_server_factory(frontend, queue_factory, ws_factory)
    internal_service_factory = make_internal_server_factory(ws_factory, daemon_service_factory, frontend)
    syslog_factory = SysLogFactory(frontend, queue_factory)

    internet.TCPClient("localhost", 5672, queue_factory).setServiceParent(conductor_service)
    internet.TCPServer(6060, daemon_service_factory).setServiceParent(conductor_service)
    internet.TCPServer(6061, internal_service_factory, interface="127.0.0.1").setServiceParent(conductor_service)
    internet.TCPServer(6062, ws_factory).setServiceParent(conductor_service)
    internet.TCPServer(6063, syslog_factory).setServiceParent(conductor_service)
    return conductor_service


def run():
    from twisted.python import usage, log
    from twisted.internet import reactor
    from .tap import Options
    import sys

    log.startLogging(sys.stdout)

    options = Options()
    try:
        options.parseOptions(sys.argv[1:])
    except usage.UsageError, e:
        print "Error: %s" % e
        #sys.exit(1)

    service = make_service(options)
    service.startService()
    reactor.run()
    print service
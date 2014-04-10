from thrift.protocol import TBinaryProtocol
from twisted.application import internet, service
from twisted.internet.endpoints import clientFromString
from twisted.internet import reactor
from autobahn.wamp.router import RouterFactory
from autobahn.twisted.wamp import RouterSessionFactory
from autobahn.twisted.websocket import WampWebSocketServerFactory

from .services.frontend.frontend import FrontendConnector
from .services.daemon.factory import AuthenticatingThriftServerFactory
from .services.internal.factory import InternalServiceFactory
from .services.queue.factory import RabbitMQConnectionFactory, rabbitmq_reconnector
from .services.live_update.component import LiveUpdateComponent
from .services.syslog.factory import SysLogFactory
from .services.stats.stats import Stats




def make_daemon_server_factory(frontend, queue, ws, stats):
    return AuthenticatingThriftServerFactory(None, TBinaryProtocol.TBinaryProtocolFactory(),
                                             frontend=frontend, queue=queue, websockets=ws, stats=stats)


def make_internal_server_factory(ws, daemon_service_factory, queue_factory, stats):
    return InternalServiceFactory(None, TBinaryProtocol.TBinaryProtocolFactory(),
                                  websocket_component=ws,
                                  daemon_service_factory=daemon_service_factory,
                                  queue_factory=queue_factory, stats=stats)


def make_websocket_factory(stats):
    session_factory = RouterSessionFactory(RouterFactory())
    component = LiveUpdateComponent(stats)
    session_factory.add(component)
    factory = WampWebSocketServerFactory(session_factory, debug=False)
    return component, factory


def make_service(config):
    queue_factory = RabbitMQConnectionFactory()
    frontend = FrontendConnector(config["web_addr"])
    stats = Stats()

    ws_component, ws_factory = make_websocket_factory(stats)
    conductor_service = service.MultiService()
    daemon_service_factory = make_daemon_server_factory(frontend, queue_factory, ws_component, stats)
    internal_service_factory = make_internal_server_factory(ws_component, daemon_service_factory, queue_factory, stats)
    syslog_factory = SysLogFactory(frontend, queue_factory, stats)

    #internet.UDPClient("192.168.137.79", 8125, graphite).setServiceParent(conductor_service)
    #clientFromString(reactor, config["statsd_addr"]).connect(graphite)
    rabbitmq_reconnector(clientFromString(reactor, config["queue_addr"]), queue_factory)
    #internet.TCPClient("localhost", 5672, queue_factory).setServiceParent(conductor_service)
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
from twisted.protocols.basic import LineReceiver


class SysLogProtocol(LineReceiver):
    # https://gist.github.com/gleicon/749857
    delimiter = "\n"

    def lineReceived(self, line):
        print "Got syslog line: %s" % line
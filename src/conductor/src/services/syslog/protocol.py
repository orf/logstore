from twisted.protocols.basic import LineReceiver
from ...util.auth import AuthenticatingMixin
import re
import math
import json
import datetime

severity = ('emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug')
facility = ('kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news',
            'uucp', 'cron', 'authpriv', 'ftp', 'ntp', 'audit', 'alert', 'at', 'local0',
            'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7')

fs_match = re.compile("<(.+)>(.*)", re.I)


class SysLogProtocol(AuthenticatingMixin, LineReceiver):
    # https://gist.github.com/gleicon/749857
    delimiter = "\n"

    def auth_success(self, server_id):
        pass

    def lineReceived(self, line):
        line = line.strip()
        print self._calc_lvl(line), line

        self.factory.queue.queue_message(
            json.dumps(
                {
                    "method": "ANALYZE",
                    "data": {
                        "server_id": self.server_id,
                        "file_name": "syslog",
                        "read_time": datetime.datetime.now().isoformat(),
                        "log_message": line
                    }
                }
            )
        )

    def _calc_lvl(self, line):
        lvl = fs_match.split(line)
        if lvl and len(lvl) > 1:
            i = int(lvl[1])
            fac = int(math.floor(i / 8))
            sev = i - (fac * 8)
            return (facility[fac], severity[sev])
        return (None, None)

#192.168.137.1
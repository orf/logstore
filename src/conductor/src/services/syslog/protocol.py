import re
import math
import json
import datetime

from twisted.protocols.basic import LineReceiver

from ...util.auth import AuthenticatingMixin


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
        severity, facility = self._calc_lvl(line)

        self.factory.queue.queue_message(
            json.dumps({"data": {"severity": severity, "facility": facility},
                        "server_id": self.server_id,
                        "file_name": "syslog",
                        "read_time": datetime.datetime.now().isoformat(),
                        "log_message": line
                    })
        )

        self.factory.stats.increment_stat("got_log_line")

    def _calc_lvl(self, line):
        lvl = fs_match.split(line)
        if lvl and len(lvl) > 1:
            i = int(lvl[1])
            fac = int(math.floor(i / 8))
            sev = i - (fac * 8)
            return (facility[fac], severity[sev])
        return (None, None)

#192.168.137.1
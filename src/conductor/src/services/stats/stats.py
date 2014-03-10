from collections import defaultdict
import itertools

from twisted.internet import task


class Stats(object):
    def __init__(self):
        _default_stat = lambda: {"count": 0, "avg": 0, "watchers": []}
        self.stats = defaultdict(_default_stat)
        self.global_watchers = []
        self.avg_loop = task.LoopingCall(self.sum_averages)
        self.avg_loop.start(1)

        self.stats["got_log_line"] = _default_stat()
        self.stats["got_event_hit"] = _default_stat()
        self.stats["processed_message"] = _default_stat()

    def sum_averages(self):
        for name in self.stats:
            stat = self.stats[name]
            stat["avg"] = stat["count"]
            stat["count"] = 0

            for watcher in itertools.chain(stat["watchers"], self.global_watchers):
                watcher(name, stat["avg"])

    def global_watch(self, func):
        self.global_watchers.append(func)

    def global_unwatch(self, func):
        if func in self.global_watchers:
            self.global_watchers.remove(func)

    def watch_stat(self, name, func):
        self.stats[name]["watchers"].append(func)

    def unwatch_stat(self, name, func):
        if func in self.stats[name]["watchers"]:
            self.stats[name]["watchers"].remove(func)

    def increment_stat(self, name):
        self.stats[name]["count"] += 1

    def get_average_stat(self, name):
        return self.stats[name]["avg"]
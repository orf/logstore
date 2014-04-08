from logstore.web.apps.formats.models import Format
from logstore.web.apps.events.models import EventQuery
from dateutil.parser import parse

from ._base import QueueProcessCommand


class Command(QueueProcessCommand):
    queue_name = "parse"
    name = "Analyser"

    def __init__(self):
        self.format_cache = {}
        self.event_cache = {}
        super(Command, self).__init__()

    def got_message(self, message):
        if "read_time" not in message:
            return

        read_time = parse(message["read_time"])

        data = message.get("data", {})
        data.update({"time": read_time})
        formats = self.get_formats(message["file_name"])

        for format in formats:
            try:
                extracted_data = format.process(message["log_message"])
            except Exception, e:
                print e
                pass
            else:
                if "field_errors" in extracted_data:
                    #print "Field errors: %s" % extracted_data["field_errors"]
                    data.setdefault("field_errors", []).append(extracted_data["field_errors"])
                else:
                    data.update(extracted_data)

        doc = {
            "message": message["log_message"],
            "server_id": message["server_id"],
            "stream_name": message["file_name"],
            "events": [],
            "failed_formats": [],
            "data": data
        }

        result = self.es.index(index="logs", doc_type="line", body=doc)
        self.send_to_conductor("increment_stat", "processed_message")
        percolate_result = self.es.percolate(index="logs", doc_type="line", id=result["_id"])

        # ToDo: Refactor this to handle events first, then handle live updates.

        if percolate_result["matches"]:
            live_update_matches = [m["_id"] for m in percolate_result["matches"] if m["_id"].startswith("lu.")]

            if live_update_matches:
                self.notify_live_update(doc, live_update_matches, result["_id"], read_time)

            event_ids = [m["_id"] for m in percolate_result["matches"] if m["_id"].startswith("ev.")]
            if event_ids:
                search_id = result["_id"]

                queries = self.get_events(event_ids)
                if not queries:
                    self.stdout.write("!", ending="")
                    return

                new_names = [query.name for query in queries if query.name not in doc["events"]]
                if new_names:
                    doc["events"].extend(new_names)
                    updated_result = self.es.index("logs", "line", doc, id=search_id)
                    self.send_to_conductor("increment_stat", "got_event_hit")

                    # Check to see if it matches any new percolators
                    new_percolate_result = self.es.percolate(index="logs", doc_type="line", id=search_id)
                    if new_percolate_result["matches"]:
                        new_live_update_matches = [m["_id"] for m in new_percolate_result["matches"]
                                                   if m["_id"].startswith("lu.")]
                        to_notify = set(new_live_update_matches) - set(live_update_matches)
                        if to_notify:
                            self.notify_live_update(doc, to_notify, updated_result["_id"], read_time)
                    self.stdout.write("#", ending="")

            self.stdout.write("", ending="")
        self.stdout.write(".", ending="")

    def notify_live_update(self, doc, matches, result_id, read_time):
        self.send_to_conductor("percolator_hit",
                               doc["message"],
                               read_time.isoformat(),
                               doc["server_id"],
                               doc["stream_name"],
                               matches,
                               result_id)

    def get_formats(self, stream_name):
        if stream_name not in self.format_cache:
            self.format_cache[stream_name] = [f.create_format()
                                              for f in Format.objects.filter(streams__name=stream_name).all()]
        return self.format_cache[stream_name]

    def get_events(self, ids):
        for id in ids:
            if not id in self.event_cache:
                try:
                    # ToDo: Support multiple events with the same query hash
                    self.event_cache[id] = EventQuery.objects.get(percolate_hash=id)
                except EventQuery.DoesNotExist:
                    return None #self.event_cache[id] = None

        return [self.event_cache[id]
                for id in ids
                if self.event_cache[id] is not None]

# Acknowledge the message

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=250)
    count = models.BigIntegerField(default=0)


class EventFile(models.Model):
    name = models.CharField(max_length=250)
    event = models.ForeignKey("events.Event", related_name="files")


class EventQuery(models.Model):
    name = models.CharField(max_length=250)
    weight = models.IntegerField()
    query = models.CharField(max_length=1024)
    percolate_hash = models.TextField(default="")

    event = models.ForeignKey("events.Event", related_name="queries")

    def __unicode__(self):
        return '%s  Weight: %s  Query: "%s"' % (self.name, self.weight, self.query)

    def get_file_name_query(self, postfix=""):
        names = self.event.files.values_list("name")
        if not names:
            return ""
        return " OR ".join('(file_name:"%s")' % name for name in names) + postfix

    def get_query(self):
        prefix = self.get_file_name_query(postfix=" AND ")
        return "%s(%s)" % (prefix, self.query)
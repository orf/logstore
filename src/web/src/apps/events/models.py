import hashlib

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
    percolate_hash = models.TextField()

    event = models.ForeignKey("events.Event", related_name="queries")

    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.query).hexdigest()
        return super(EventQuery, self).save(*args, **kwargs)
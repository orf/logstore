import hashlib

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=250)
    count = models.BigIntegerField()


class EventFile(models.Model):
    name = models.CharField(max_length=250)
    event = models.ForeignKey("formats.Format", related_name="files")


class EventQuery(models.Model):
    name = models.CharField(max_length=250)
    weight = models.IntegerField()
    query = models.CharField(max_length=1024)
    hash = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(self.query).hexdigest()
        return super(EventQuery, self).save(*args, **kwargs)
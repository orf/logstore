import datetime

from django.db import models
from django.utils import timezone


def get_snapshot_datetime():
    d = datetime.datetime.now()
    return datetime.datetime(year=d.year, month=d.month,
                             day=d.day, hour=d.hour, minute=d.minute,
                             tzinfo=timezone.get_current_timezone())


def get_latest_snapshot():
    try:
        return Snapshot.objects.latest("time")
    except Snapshot.DoesNotExist:
        return None


class Snapshot(models.Model):
    time = models.DateTimeField(primary_key=True, default=get_snapshot_datetime)
    total_count = models.BigIntegerField()

    store_size = models.BigIntegerField()
    avg_fetch_time = models.IntegerField()
    total_queries = models.BigIntegerField()

import datetime

from django.db import models
from model_utils.fields import MonitorField


class Server(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ip = models.IPAddressField(unique=True)

    #total_lines = models.BigIntegerField(default=0)
    #total_lines_changed = MonitorField(monitor="total_lines", default=lambda: datetime.datetime.now())



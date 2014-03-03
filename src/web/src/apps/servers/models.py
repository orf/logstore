from django.db import models
from model_utils.fields import MonitorField

import datetime


class Server(models.Model):
    name = models.CharField(max_length=250, unique=True)
    ip = models.IPAddressField(unique=True)

    total_lines = models.BigIntegerField(default=0)
    total_lines_changed = MonitorField(monitor="total_lines", default=lambda: datetime.datetime.now())



from django.db import models
from model_utils.managers import InheritanceManager


class Alert(models.Model):
    name = models.CharField(max_length=255)


class AlertContact(models.Model):
    alert = models.ForeignKey("alerts.Alert", related_name="contacts")
    objects = InheritanceManager()


class EmailContact(AlertContact):
    email_address = models.EmailField()


class TextContact(AlertContact):
    phone_number = models.CharField(max_length=255)


class PushBulletContact(AlertContact):
    device_id = models.CharField(max_length=255)


class AlertCondition(models.Model):
    alert = models.ForeignKey("alerts.Alert", related_name="conditions")
    objects = InheritanceManager()


class EventCountCondition(AlertContact):
    pass
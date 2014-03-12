from __future__ import division

import datetime

from django.db import models
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from model_utils.managers import InheritanceManager
from django.conf import settings
import pushbullet

from .choices import TimeSpanChoice


class SelectSubclassManager(InheritanceManager):
    def get_queryset(self):
        return super(SelectSubclassManager, self).get_queryset().select_related().select_subclasses()


class Alert(models.Model):
    name = models.CharField(max_length=255)

    def notify(self, current_value, condition):
        for contact in self.contacts.all():
            contact.notify(current_value, condition)


class AlertContact(models.Model):
    name = None
    alert = models.ForeignKey("alerts.Alert", related_name="contacts")
    objects = SelectSubclassManager()

    def notify(self, current_value, triggered_condition):
        raise NotImplementedError()


class EmailContact(AlertContact):
    name = "Email"
    email_address = models.EmailField()

    contact = lambda s: s.email_address

    def notify(self, current_value, triggered_condition):
        send_mail("Alert %s has been triggered" % self.alert.name,
                  "Logstore event %s has a value of %s" % (self.condition.event.name, current_value),
                  "logstore@local", [self.email_address], fail_silently=True)


class TextContact(AlertContact):
    name = "Text"
    phone_number = models.CharField(max_length=255)

    contact = lambda s: s.phone_number

    def notify(self, current_value, triggered_condition):
        return  # Do nothing for now.


class PushBulletContact(AlertContact):
    name = "PushBullet"
    device_name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)

    contact = lambda s: s.device_name

    def notify(self, current_value, triggered_condition):
        pushbullet.Device(settings.PUSHBULLET_API_KEY, self.device_id)\
            .push_note("Alert %s has been triggered" % self.alert.name,
                       "Logstore event %s has a value of %s" % (self.condition.event.name, current_value))


class AlertCondition(models.Model):
    alert = models.ForeignKey("alerts.Alert", related_name="conditions")
    event_query = models.ForeignKey("events.EventQuery", related_name="alerts")
    time_value = models.PositiveIntegerField()
    time_choice = models.IntegerField(choices=TimeSpanChoice, default=TimeSpanChoice.MINUTES)
    last_triggered = models.DateTimeField(auto_now_add=True)

    objects = SelectSubclassManager()

    def description(self):
        raise NotImplementedError()

    def get_timespan(self):
        # Simplest is sometimes best. This could be done more cleverly.
        if self.time_choice == TimeSpanChoice.MINUTES:
            return datetime.timedelta(minutes=self.time_value)
        elif self.time_choice == TimeSpanChoice.HOURS:
            return datetime.timedelta(hours=self.time_value)
        elif self.time_choice == TimeSpanChoice.DAYS:
            return datetime.timedelta(days=self.time_value)

    def check_triggered(self, started, es):
        current_value = self.get_current_value(started, es)
        trigger_value = self.get_trigger_value(started, es)
        return trigger_value < current_value, trigger_value, current_value

    def get_trigger_value(self, started, es):
        raise NotImplementedError()

    def get_range_query(self, started):
        return {"range": {"read_time": {"lte": started, "gte": started - self.get_timespan()}}}

    def get_query_string(self):
        return {"query_string": {"query": "%sevents:'%s'" % (self.event_query.get_file_name_query(postfix=" AND "),
                                                             self.event_query.name)}}

    def get_query(self, started):
        return {
            "bool": {
                "must": [
                    self.get_query_string(),
                    self.get_range_query(started)
                ]
            }
        }

    def get_current_value(self, started, es):
        return es.count("logs", "line", {"query": self.get_query(started)})["count"]


class EventCountCondition(AlertCondition):
    threshold = models.PositiveIntegerField()

    def get_trigger_value(self, started, es):
        return self.threshold

    def description(self):
        return "More than %s %s events in %s %s" % (self.threshold, self.event_query.name,
                                                    self.time_value, self.get_time_choice_display())


class EventTriggeredCondition(AlertCondition):
    def get_trigger_value(self, started, es):
        return 1

    def description(self):
        return "A single %s event, triggered every %s %s" % (self.event_query.name, self.time_value,
                                                             self.get_time_choice_display())


class EventPercentageCondition(AlertCondition):
    percentage = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])

    def get_trigger_value(self, started, es):
        # The default get_current_value returns the current count of the
        return self.percentage

    def check_triggered(self, started, es):
        current_value = self.get_current_value(started, es)
        trigger_value = self.get_trigger_value(started, es)
        return (current_value / trigger_value * 100) >= trigger_value, trigger_value, current_value



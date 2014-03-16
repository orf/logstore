from __future__ import division

import datetime

from django.db import models
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from model_utils.managers import InheritanceManager
from django.conf import settings
import pushbullet

from .choices import TimeSpanChoice, StatisticalChoice


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
                       "Logstore event %s has a value of %s" % (triggered_condition.event_query.name, current_value))


class AlertCondition(models.Model):
    alert = models.ForeignKey("alerts.Alert", related_name="conditions")
    event_query = models.ForeignKey("events.EventQuery", related_name="alerts", null=True)
    format_field = models.ForeignKey("formats.Field", related_name="alerts", null=True)
    time_value = models.PositiveIntegerField()
    time_choice = models.IntegerField(choices=TimeSpanChoice, default=TimeSpanChoice.MINUTES)
    next_trigger = models.DateTimeField(auto_now_add=True)

    objects = SelectSubclassManager()

    def name(self):
        return self.event_query.name

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

    def get_file_filter(self, postfix=""):
        if self.event_query_id:
            return self.event_query.get_file_name_query(postfix)
        else:
            return self.format_field.format.get_file_name_query(postfix)

    def get_query(self, started, filter_by_event=True):
        qs = self.get_file_filter(postfix=" AND " if filter_by_event else "")
        if filter_by_event:
            qs += "events:'%s'" % self.event_query.name

        return {
            "query": {
                "bool": {
                    "must": [
                        {"query_string": {"query": qs}},
                        {"range": {"read_time": {"lte": started, "gte": started - self.get_timespan()}}}
                    ]
                }
            }
        }

    def get_current_value(self, started, es, query=None, key=""):
        return es.count("logs", "line", self.get_query(started) if query is None else query)["count"]


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


class StatisticalValueCondition(AlertCondition):
    statistic = models.CharField(choices=StatisticalChoice, max_length=255)
    value = models.IntegerField()

    def get_trigger_value(self, started, es):
        return self.value

    def get_query(self, started, filter_by_event=False):
        query = super(StatisticalValueCondition, self).get_query(started, filter_by_event)
        query["facets"] = {"average": {"statistical": {"field": "data.%s" % self.format_field.name}}}
        return query

    def get_current_value(self, started, es, query=None, key=""):
        return es.search("logs",
                         "line",
                         self.get_query(started) if query is None else query,
                         size=0)["facets"]["average"][self.statistic]

    def description(self):
        return "%s with an %s value above %s every %s %s" % (self.format_field.name, self.get_statistic_display(),
                                                             self.value, self.time_value,
                                                             self.get_time_choice_display())

    def name(self):
        return self.format_field.name


class EventPercentageCondition(AlertCondition):
    percentage = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])

    def get_trigger_value(self, started, es):
        total_lines = self.get_current_value(started, es, query=self.get_query(started, filter_by_event=False))
        return (total_lines / 100) * self.percentage

    def description(self):
        return "More than %s%% of messages are %s" % (self.percentage, self.event_query.name)
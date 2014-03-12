import datetime
import time

from django.utils.timezone import get_current_timezone
import kronos
import elasticsearch

from .models import Alert


@kronos.register("*/1 * * * *")
def test_alerts():
    es = elasticsearch.Elasticsearch()

    started = datetime.datetime.now()

    alerts = Alert.objects.all()

    print "Testing %s alerts..." % alerts.count()
    for alert in alerts:
        print " - Testing alert %s" % alert

        for condition in alert.conditions.all():
            if condition.last_triggered + condition.get_timespan() > datetime.datetime.now(tz=get_current_timezone()):
                print "Condition skipped"
                continue
            print "  - Testing condition for %s" % condition.event_query.name
            condition.check_triggered(started, es)
            triggered, trigger_value, current_value = condition.has_triggered(started, es)
            if triggered:
                print "   - Condition fired - %s" % current_value
                # Update the last triggered time
                condition.last_triggered = datetime.datetime.now(tz=get_current_timezone())
                condition.save()

                alert.notify(current_value, condition)
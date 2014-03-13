import datetime
import time

from django.utils.timezone import get_current_timezone
import kronos
import elasticsearch

from .models import Alert


@kronos.register("*/1 * * * *")
def test_alerts():
    es = elasticsearch.Elasticsearch()

    started = datetime.datetime.now(tz=get_current_timezone())

    alerts = Alert.objects.all()

    print "Testing %s alerts..." % alerts.count()
    for alert in alerts:
        print " - Testing alert %s" % alert.name

        for condition in alert.conditions.filter(next_trigger__lte=started).all():
            print "  - Testing condition for %s" % condition.event_query.name
            triggered, trigger_value, current_value = condition.check_triggered(started, es)
            if triggered:
                print "   - Condition fired - %s" % current_value
                # Update the last triggered time
                condition.next_trigger = started + condition.get_timespan()
                condition.save()

                alert.notify(current_value, condition)
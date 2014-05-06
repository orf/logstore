from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ""
    name = "Run alert server"

    def handle(self, *args, **options):
        from ...cron import test_alerts
        import time

        while True:
            test_alerts()
            time.sleep(60)
# Downloads and extracts

import os
import gzip
import urllib

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Downloads and extracts the GeoIP database"

    def handle(self, *args, **options):
        target_dir = settings.GEOIP_DATABASE_DIR
        download_file = os.path.join(target_dir, "GeoIP.dat.gz")
        extracted_file = os.path.join(target_dir, "GeoIP.dat")

        urllib.urlretrieve("http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz",
                           download_file)
        self.stdout.write("Downloaded GeoIP database, extracting")
        gzip_file = gzip.open(download_file)

        with open(extracted_file, "wb") as extract_fd:
            extract_fd.write(gzip_file.read())
        gzip_file.close()
        self.stdout.write("Extracted to %s" % extracted_file)
        os.remove(download_file)
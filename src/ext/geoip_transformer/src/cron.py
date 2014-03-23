import kronos
import os
import gzip
import urllib
from django.conf import settings


@kronos.register("0 0 * * *")
def download_geoip():
    target_dir = getattr(settings, "GEOIP_DATABASE_DIR", os.path.join(settings.BASE_DIR, ".cache"))

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    download_file = os.path.join(target_dir, "GeoIP.dat.gz")
    extracted_file = os.path.join(target_dir, "GeoIP.dat")
    print "Downloading to %s" % target_dir
    urllib.urlretrieve("http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz", download_file)
    print "Downloaded GeoIP database, extracting"
    gzip_file = gzip.open(download_file)

    with open(extracted_file, "wb") as extract_fd:
        extract_fd.write(gzip_file.read())
    gzip_file.close()
    print "Extracted to %s\n" % extracted_file
    os.remove(download_file)
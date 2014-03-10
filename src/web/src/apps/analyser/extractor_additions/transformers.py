import os

from logstore.extractor.base import Transformer
from pygeoip import GeoIP, MEMORY_CACHE
from django.conf import settings


# Not thread safe, but screw it for now
lookup = GeoIP(os.path.join(settings.GEOIP_DATABASE_DIR, "GeoIP.dat"), MEMORY_CACHE)


class GeoIPLookup(Transformer):
    def __init__(self, args):
        self.args = args

    def transform(self, value):
        country = lookup.country_name_by_addr(value)
        return {"ip": value, "country": country}, "ip"
import os

from logstore.extractor.base import Transformer
from logstore.extractor.register import registry
from pygeoip import GeoIP, MEMORY_CACHE
from django.conf import settings
import warnings

geoip_base_location = getattr(settings, "GEOIP_DATABASE_DIR", os.path.join(settings.BASE_DIR, ".cache"))
geoip_file = os.path.join(geoip_base_location, "GeoIP.dat")

try:
    lookup = GeoIP(geoip_file, MEMORY_CACHE)
except IOError:
    warnings.warn("File %s does not exist, GeoIP lookups will fail. Run the download_geoip task to fix this" % geoip_file)
    lookup = None


@registry.add_transformer("geoip", "GeoIP Lookup")
class GeoIPLookup(Transformer):
    def __init__(self, args):
        self.args = args

    def transform(self, value):
        if lookup is None:
            return value, ""

        country = lookup.country_name_by_addr(value)
        return {"ip": value, "country": country}, "ip"


@registry.add_type("ip", "IP Address")
class IPType(unicode):
    pass
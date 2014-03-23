from logstore.extractor.base import Transformer
from logstore.extractor.register import registry
import httpagentparser


@registry.add_transformer("http_request", "HTTP Request")
class HttpRequestTransformer(Transformer):
    def __init__(self, args):
        self.args = args

    def transform(self, value):
        try:
            command, path, version = value.split()
        except ValueError:
            # Invaid HTTP header I guess
            return {"raw": value}, "raw"

        version_number = version.split("/", 1)[1]

        return {"raw": value, "path": path, "command": command, "version": float(version_number)}, "raw"
from logstore.extractor.base import Transformer
from logstore.extractor.register import registry
import httpagentparser


class UserAgentTransformer(Transformer):
    def __init__(self, args):
        self.args = args

    def transform(self, value):
        if self.args == "simple":
            os, browser = httpagentparser.simple_detect(value)
            parsed = {"os": os, "browser": browser}
        else:
            parsed = httpagentparser.detect(value)
        returner = {"raw": value}
        returner.update(parsed)
        return returner, "raw"

registry.add("transformer", "user_agent", UserAgentTransformer, display_name="User-Agent")
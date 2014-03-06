import unittest

from ..base import Format, Field, FieldSource, Transformer
from ..splitters import Character
from ..transformers import StripTransformer


class DataTransformer(Transformer):
    def transform(self, value):
        return {"new_key": value}, "new_key"


class TransformerTests(unittest.TestCase):
    def TestProcessData(self):
        format = Format(splitter=Character(" "),
                        fields=[
                            Field("IP", FieldSource("2"), [DataTransformer(), StripTransformer(":")])
                        ])
        x = format.process("Reply from 83.100.221.240: bytes=32 time=289ms TTL=60")
        self.assertEqual(x["IP"], {"new_key": "83.100.221.240"})

    def TestProcessDataMultiple(self):
        format = Format(splitter=Character(" "),
                        fields=[
                            Field("IP", FieldSource("2"), [DataTransformer(), DataTransformer(), StripTransformer(":")])
                        ])
        x = format.process("Reply from 83.100.221.240: bytes=32 time=289ms TTL=60")
        self.assertEqual(x["IP"], {"new_key": {"new_key": "83.100.221.240"}})

if __name__ == "__main__":
    unittest.main()
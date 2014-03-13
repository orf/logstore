import unittest

from ..base import Format, Field, FieldSource
from ..splitters import Character
from ..transformers import RemoveTransformer


class FormatTests(unittest.TestCase):
    def TestProcessData(self):
        format = Format(splitter=Character(" "),
                        fields=[
                            Field("IP", FieldSource("2"), [RemoveTransformer(":")]),
                            Field("Time", FieldSource("4"), [RemoveTransformer("time="), RemoveTransformer("ms")])
                        ])
        x = format.process("Reply from 83.100.221.240: bytes=32 time=289ms TTL=60")
        self.assertEqual(x["IP"], "83.100.221.240")
        self.assertEqual(x["Time"], "289")

if __name__ == "__main__":
    unittest.main()
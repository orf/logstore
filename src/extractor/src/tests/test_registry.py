import unittest

from ..base import Transformer
from ..register import Registry


class TestTransformer(Transformer):
    def transform(self, value):
        return {"transformed": True, "value": value}, "value"


class FormatTests(unittest.TestCase):
    def TestRegistry(self):
        r = Registry()
        r.add("transformer", "test", TestTransformer)
        self.assertTrue(r.get_by_name("transformer", "test"))
        self.assertEqual(TestTransformer, r.get_by_name("transformer", "test"))
        self.assertRaises(AttributeError, r.get_by_name, "invalid_type", "test")
        self.assertRaises(KeyError, r.get_by_name, "transformer", "does_not_exist")

if __name__ == "__main__":
    unittest.main()
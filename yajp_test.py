import unittest
from yajp import parse, YajpType, YajpParse


class YajpTest(unittest.TestCase):

    def test_parse_null(self):
        status, v = parse("null")
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.NULL, v.type)

if __name__ == '__main__':
    unittest.main()

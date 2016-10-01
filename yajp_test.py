import unittest
from yajp import parse, YajpValue, YajpType, YajpParse


class YajpTest(unittest.TestCase):

    def test_parse_null(self):
        v = YajpValue(YajpType.FALSE)
        status, v = parse('null')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_expect_value(self):
        v = YajpValue(YajpType.FALSE)
        status, v = parse('')
        self.assertEqual(YajpParse.EXPECT_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

        v = YajpValue(YajpType.FALSE)
        status, v = parse(' ')
        self.assertEqual(YajpParse.EXPECT_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_invalid_value(self):
        v = YajpValue(YajpType.FALSE)
        status, v = parse('nul')
        self.assertEqual(YajpParse.INVALID_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

        v = YajpValue(YajpType.FALSE)
        status, v = parse('?')
        self.assertEqual(YajpParse.INVALID_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_root_not_singular(self):
        v = YajpValue(YajpType.FALSE)
        status, v = parse('null x')
        self.assertEqual(YajpParse.ROOT_NOT_SINGULAR, status)
        self.assertEqual(YajpType.NULL, v.type)


if __name__ == '__main__':
    unittest.main()

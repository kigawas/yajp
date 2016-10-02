import unittest
from yajp import parse, YajpType, YajpParse


class YajpTest(unittest.TestCase):

    def test_parse_null(self):
        status, v = parse('null')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_expect_value(self):
        status, v = parse('')
        self.assertEqual(YajpParse.EXPECT_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

        status, v = parse(' ')
        self.assertEqual(YajpParse.EXPECT_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_invalid_value(self):
        status, v = parse('nul')
        self.assertEqual(YajpParse.INVALID_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

        status, v = parse('?')
        self.assertEqual(YajpParse.INVALID_VALUE, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_root_not_singular(self):
        status, v = parse('null x')
        self.assertEqual(YajpParse.ROOT_NOT_SINGULAR, status)
        self.assertEqual(YajpType.NULL, v.type)

    def test_true(self):
        v = YajpType(YajpType.FALSE)
        status, v = parse('true')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.TRUE, v.type)

    def test_false(self):
        status, v = parse('false')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.FALSE, v.type)


if __name__ == '__main__':
    unittest.main()

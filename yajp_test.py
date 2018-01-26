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

        self.parse_invalid_number(YajpParse.ROOT_NOT_SINGULAR, '0123')
        self.parse_invalid_number(YajpParse.ROOT_NOT_SINGULAR, '0x0')
        self.parse_invalid_number(YajpParse.ROOT_NOT_SINGULAR, '0x123')

    def test_true(self):
        v = YajpType(YajpType.FALSE)
        status, v = parse('true')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.TRUE, v.type)

    def test_false(self):
        status, v = parse('false')
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.FALSE, v.type)

    def parse_valid_number(self, number):
        status, v = parse(number)
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.NUMBER, v.type)
        self.assertEqual(float(number), v.n)

    def parse_invalid_number(self, error, number):
        status, v = parse(number)
        self.assertEqual(error, status)

    def test_number(self):

        self.parse_valid_number('0')
        self.parse_valid_number('-0')
        self.parse_valid_number('-0.0')
        self.parse_valid_number('1')
        self.parse_valid_number('-1')
        self.parse_valid_number('1.5')
        self.parse_valid_number('-1.5')
        self.parse_valid_number('3.1416')
        self.parse_valid_number('1E10')
        self.parse_valid_number('1e10')
        self.parse_valid_number('1E+10')
        self.parse_valid_number('1E-10')
        self.parse_valid_number('-1E10')
        self.parse_valid_number('-1e10')
        self.parse_valid_number('-1E+10')
        self.parse_valid_number('-1E-10')
        self.parse_valid_number('1.234E+10')
        self.parse_valid_number('1.234E-10')
        self.parse_valid_number('1e-10000')  # must underflow
        self.parse_valid_number("1.0000000000000002")  # the smallest number > 1
        self.parse_valid_number("4.9406564584124654e-324")  # minimum denormal
        self.parse_valid_number("-4.9406564584124654e-324")
        self.parse_valid_number("2.2250738585072009e-308")  # Max subnormal double
        self.parse_valid_number("-2.2250738585072009e-308")
        self.parse_valid_number("2.2250738585072014e-308")  # Min normal positive double
        self.parse_valid_number("-2.2250738585072014e-308")
        self.parse_valid_number("1.7976931348623157e+308")  # Max double
        self.parse_valid_number("-1.7976931348623157e+308")

        self.parse_invalid_number(YajpParse.INVALID_VALUE, '+0')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, '+1')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, '.123')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, '1.')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, 'INF')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, 'inf')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, 'NAN')
        self.parse_invalid_number(YajpParse.INVALID_VALUE, 'nan')

        self.parse_invalid_number(YajpParse.NUMBER_TOO_BIG, '1e309')
        self.parse_invalid_number(YajpParse.NUMBER_TOO_BIG, '-1e309')

    def parse_valid_string(self, expect, string):
        status, v = parse(string)
        self.assertEqual(YajpParse.OK, status)
        self.assertEqual(YajpType.STRING, v.type)
        self.assertEqual(expect, v.s)

    def test_string(self):
        self.parse_valid_string('json ', '"json "')
        self.parse_valid_string('', '""')
        # self.parse_valid_string('hello \n world', '"hello \\n world"')
        # self.parse_valid_string('\" \\ / \b \f \n \r \t', '"\\" \\\\ / \\b \\f \\n \\r \\t"')
if __name__ == '__main__':
    unittest.main()

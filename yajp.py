# Yajp: Yet Another Json Parser in Python
import enum


def EXPECT(c, ch):
    '''
    Assert character and move pointer to next (i.e "eat" a character)
    Usage:
    def parse_null(self):
        EXPECT(self, 'n')
        # ...
    '''
    assert isinstance(c, YajpContext)
    assert c.json[0] == ch
    c.json = c.json[1:]


class YajpType(enum.Enum):
    NULL = 0
    FALSE = 1
    TRUE = 2
    NUMBER = 3
    STRING = 4
    ARRAY = 5
    OBJECT = 6


class YajpParse(enum.Enum):
    OK = 0
    EXPECT_VALUE = 1
    INVALID_VALUE = 2
    ROOT_NOT_SINGULAR = 3
    NUMBER_TOO_BIG = 4
    MISS_QUOTATION_MARK = 5


class YajpValue(object):

    def __init__(self, yajp_type, number=0, string=''):
        assert isinstance(yajp_type, YajpType)
        self.type = yajp_type
        self.n = number
        self.s = string

    def __repr__(self):
        return 'YajpValue({}, {})'.format(self.type, self.n)

    @property
    def n(self):
        assert self.type == YajpType.NUMBER
        return self._n

    @n.setter
    def n(self, value):
        self._n = value

    @property
    def s(self):
        assert self.type == YajpType.STRING
        return self._s

    @s.setter
    def s(self, value):
        self._s = value


class YajpContext(object):

    def __init__(self, json):
        self.json = json
        self.stack = []

    def push(self, ch):
        self.stack.append(ch)

    def pop(self, size):
        res = ''.join(self.stack[-size:])
        self.stack = self.stack[:-size]
        return res

    def parse_whitespace(self):
        '''
        One line equivalent:
            self.json = self.json.lstrip()
        '''
        if not self.json:
            return ''

        p = 0
        while self.is_equal_to(p, (' ', '\t', '\n', '\r')):
            p += 1
        self.json = self.json[p:]

    def parse_literal(self, literal, yajp_type):
        EXPECT(self, literal[0])
        if len(self.json) < len(literal) - 1 or self.json[:len(literal) - 1] != literal[1:]:
            return YajpParse.INVALID_VALUE, None
        self.json = self.json[len(literal) - 1:]
        return YajpParse.OK, YajpValue(yajp_type)

    def is_equal_to(self, p, c):
        if isinstance(c, (list, tuple)):
            return p < len(self.json) and self.json[p] in c
        return p < len(self.json) and self.json[p] == c

    def is_digit(self, p):
        return p < len(self.json) and '0' <= self.json[p] <= '9'

    def is_digit_1to9(self, p):
        return p < len(self.json) and '1' <= self.json[p] <= '9'

    def parse_number(self):
        '''
        number = [ - ] int [ frac ] [ exp ]
        Note: int, frac, exp will be expressed by regex beneath
        '''
        p = 0
        if self.is_equal_to(p, '-'):
            p += 1
        if self.is_equal_to(p, '0'):
            '''
            int = 0|[1-9][0-9]*
            '''
            p += 1
        else:
            if not self.is_digit_1to9(p):
                return YajpParse.INVALID_VALUE, None
            p += 1
            while self.is_digit(p):
                p += 1
        if self.is_equal_to(p, '.'):
            '''
            frac = \.[0-9]+
            '''
            p += 1
            if not self.is_digit(p):
                return YajpParse.INVALID_VALUE, None
            p += 1
            while self.is_digit(p):
                p += 1
        if self.is_equal_to(p, ('e', 'E')):
            '''
            exp = (e|E)(\+|-)?[0-9]+
            '''
            p += 1
            if self.is_equal_to(p, ('+', '-')):
                p += 1
            if not self.is_digit(p):
                return YajpParse.INVALID_VALUE, None
            p += 1
            while self.is_digit(p):
                p += 1

        num = float(self.json[:p])

        if num in (float('inf'), float('-inf')):
            return YajpParse.NUMBER_TOO_BIG, None
        self.json = self.json[p:]
        return YajpParse.OK, YajpValue(YajpType.NUMBER, number=num)

    def parse_string(self):
        EXPECT(self, '"')
        for i, ch in enumerate(self.json):
            if ch == '"':
                v = YajpValue(YajpType.STRING, string=self.pop(i))
                self.json = self.json[i + 1:]
                return YajpParse.OK, v
            elif i + 1 == len(self.json):
                return YajpParse.MISS_QUOTATION_MARK, None
            else:
                self.push(ch)

    def parse_value(self):
        head = self.json[0] if len(self.json) else ''
        if head == 'n':
            return self.parse_literal('null', YajpType.NULL)
        elif head == 't':
            return self.parse_literal('true', YajpType.TRUE)
        elif head == 'f':
            return self.parse_literal('false', YajpType.FALSE)
        elif head == '"':
            return self.parse_string()
        elif head == '':
            return YajpParse.EXPECT_VALUE, None
        else:
            return self.parse_number()


def parse(json):
    c = YajpContext(json)
    c.parse_whitespace()
    status, value = c.parse_value()
    assert isinstance(status, YajpParse)
    assert isinstance(value, YajpValue) or value is None
    if value is None:  # fail, set type = NULL
        return status, YajpValue(YajpType.NULL)
    else:
        if status == YajpParse.OK:
            c.parse_whitespace()
            if c.json:
                status = YajpParse.ROOT_NOT_SINGULAR

        return status, value

if __name__ == '__main__':
    v = YajpValue(YajpType.NUMBER)
    v.n = 1
    assert v.n == 1

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


class YajpValue(object):

    def __init__(self, yajp_type):
        assert isinstance(yajp_type, YajpType)
        self.type = yajp_type

    def __repr__(self):
        return 'YajpValue({})'.format(self.type)


class YajpContext(object):

    def __init__(self, json):
        self.json = json

    def parse_whitespace(self):
        '''
        One line equivalent:
            self.json = self.json.lstrip()
        '''
        if not self.json:
            return ''

        p = 0
        while p < len(self.json) and self.json[p] in (' ', '\t', '\n', '\r'):
            p += 1
        self.json = self.json[p:]

    def parse_null(self):
        EXPECT(self, 'n')
        if len(self.json) < 3 or self.json[:3] != 'ull':
            return YajpParse.INVALID_VALUE, None
        self.json = self.json[3:]
        return YajpParse.OK, YajpValue(YajpType.NULL)

    def parse_true(self):
        EXPECT(self, 't')
        if len(self.json) < 3 or self.json[:3] != 'rue':
            return YajpParse.INVALID_VALUE, None
        self.json = self.json[3:]
        return YajpParse.OK, YajpValue(YajpType.TRUE)

    def parse_false(self):
        EXPECT(self, 'f')
        if len(self.json) < 4 or self.json[:4] != 'alse':
            return YajpParse.INVALID_VALUE, None
        self.json = self.json[4:]
        return YajpParse.OK, YajpValue(YajpType.FALSE)

    def parse_value(self):
        head = self.json[0] if len(self.json) else ''
        if head == 'n':
            return self.parse_null()
        elif head == 't':
            return self.parse_true()
        elif head == 'f':
            return self.parse_false()
        elif head == '':
            return YajpParse.EXPECT_VALUE, None
        else:
            return YajpParse.INVALID_VALUE, None


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

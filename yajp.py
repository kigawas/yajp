# Yajp: Yet Another Json Parser in Python
import enum


def EXPECT(c, ch):
    '''
    Assert character and move pointer to next
    Usage:
    def parse_null(self):
        EXPECT(self, 'n')
        # ..
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


class YajpContext(object):

    def __init__(self, json):
        self.json = json

    def parse_whitespace(self):
        p = 0
        for char in self.json:
            if char in (' ', '\t', '\n', '\r'):
                p += 1
        self.json = self.json[p:]

    def parse_null(self):
        EXPECT(self, 'n')
        if self.json[0] != 'u' or self.json[1] != 'l' or self.json[2] != 'l':
            return YajpParse.INVALID_VALUE, None
        self.json = self.json[3:]
        return YajpParse.OK, YajpValue(YajpType.NULL)

    def parse_value(self):
        head = self.json[0]
        if head == 'n':
            return self.parse_null()
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
        return status, value

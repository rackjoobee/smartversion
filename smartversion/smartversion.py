# -*- coding: utf-8 -*-

# TODO missing features (priority order)
# - handle hard cases like distcc, parens
# - timedelta compare
# - i18n
# - support full unicode in name / version / etc

# (see ../TODO and grep TODO)


from __future__ import print_function, unicode_literals

import sys
import os
import string
import re
import datetime
from collections import Counter

PKG_RELEASE_DATA = {}
PKG_SYNONYMS = {}
PKG_DATE_BOUNDARIES = {}
DATA_FILE = 'soft_vers.csv'
DATA_PATH = os.path.join(os.path.dirname(__file__), DATA_FILE)

########
# Constants
########

DIGITS_SET  = set(string.digits)
LETTERS_SET = set(string.ascii_letters)

VERSIONY_CHARS = list(string.digits) + ['.']
VERSIONY_CHARS_SET = set(VERSIONY_CHARS)

WILDCARDS = ['x', 'X', '*']

PURE_VERSION_CHARS = list(string.digits + string.ascii_letters + '._-/') \
                   + WILDCARDS

WORD_TAGS = [
    'dev', 'devel', 'test', 'a', 'alpha', 'b', 'beta',
    'c', 'pre', 'prerelease', 'rc', 'rel', 'post', 'final',
]

DEV_TAGS = ('dev', 'devel')
PRERELEASE_TAGS = ('a', 'alpha', 'b', 'beta', 'c', 'rc', 'pre')

# Package name separators - strings which sep package name
# from the version, e.g. linux[-]2.6.5.
# This should not include '.' since it usually separates
# the version numbers. That case is handled specially.
NAME_SEPS = [
    '-V', '-v', '-R', '-r', '_V', '_v',
    '_R', '_r', ' V', ' v', ' R', ' r',
    '/R', '/r', '/V', '/v', ' ', '-',
    '_', '/'
]
PNS_SET = set(NAME_SEPS)

# Pre-compile our regexes for speed (maybe, but can't hurt,
# and helps readability).
DIGITS_REGEX = re.compile(r'[^0-9]*([0-9]+)')

# Don't mess around with order of thesed
DATE_NUMERIC_REGEXES = [re.compile(x) for x in [
    # Some patterns have empty group for the separator so the
    # indices stay consistent
    r'((?:2\d\d\d|19\d\d))([-._ ])(\d\d)\2(\d\d)',
    r'((?:2\d\d\d|19\d\d))()(\d\d)(\d\d)',
    r'(\d\d)([-._ ])(\d\d)\2((?:2\d\d\d|19\d\d))',
    r'(\d\d)()(\d\d)((?:2\d\d\d|19\d\d))',
]]

DATE_TEXTUAL_REGEXES = [re.compile(x) for x in [
    r'((?:2\d\d\d|19\d\d))([-._ ])([a-zA-Z]{3,})\2(\d\d?)',
    r'((?:2\d\d\d|19\d\d))()([a-zA-Z]{3,})(\d\d?)',
    r'([a-zA-Z]{3,})([-._ ])(\d\d?)[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
    r'(\d\d?)([-._ ])([a-zA-Z]{3,})[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
    r'(\d\d?)()([a-zA-Z]{3,})((?:2\d\d\d|19\d\d|\d\d))',
]]

DURATION_REGEX = re.compile(r'\s*(\d+\s*[a-z]+\,?\s*)\s*(\d+\s*[a-z]+\,?\s*)?\s*(\d+\s*[a-z]+\,?\s*)?')

# TODO i18n and whatnot
MONTHS_SHORT = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
MONTHS_LONG  = ['january', 'february', 'march', 'april', 'june',
                'july', 'august', 'september', 'october', 'november',
                'december']

TMP_PAT = r'{}(?:[-,. _0-9])'       # match on custom boundary
MONTHS_SHORT_REGEX = re.compile(
    '|'.join([TMP_PAT.format(x) for x in MONTHS_SHORT])
)
MONTHS_LONG_REGEX  = re.compile(
    '|'.join([TMP_PAT.format(x) for x in MONTHS_LONG])
)

PROTO_REGEX = re.compile(r'[a-zA-Z]+\d?[dD]')

########
# Helper functions
########

if sys.version_info.major == 2:
    STR_CLASS = str

    def coerce_to_unicode(s):
        return unicode(s)

    def python6_str(s):
        return str(s).encode('utf-8')    # TODO sys.getdefaultencoding?
else:
    STR_CLASS = unicode

    def coerce_to_unicode(s):
        if type(s) is bytes:
            return s.decode('utf-8')
        return str(s)

    def python6_str(s):
        return str(s)

def pluralize(word, n):         # TODO i18n
    assert(isinstance(word, basestring))
    return word + 's' if n == 0 or n > 1 else word

def count_zero_prefixes(s):
    """Return a count of how many zeroes prefix the first non-0 digit char"""
    if not isinstance(s, basestring):
        return 0
    count = 0
    i = 0
    s_len = len(s)
    while i < s_len:
        if s[i] != '0':
            break
        count += 1
        i += 1
    if i > 0 and i == s_len and s[i-1] == '0':
        # Adjust count by one - last zero doesn't count :)~~
        count = count-1 if count > 0 else 0
    return count

def first_digits(s):
    """Return a 2-tuple containing the first group of consecutive digits
       in a string, or None. Tuple: (end_offset, digits_str)"""
    # Note: see below about speed (use first_int() if possible)
    m = re.search(DIGITS_REGEX, s)
    if m:
        return (m.end(1), m.group(1))
    else:
        return None

def first_int(s):
    """Return the first integer in a string, or None"""
    # This technique appears to be faster than the re-based method
    # by almost an order of magnitude. Prefer it
    ret = ''
    for c in s:
        if c in string.digits:
            ret += c
        else:
            break
    if len(ret) > 0:
        return int(ret)
    else:
        return None

def last_int(s):
    """Return the last integer in a string, or None"""
    ret = ''
    for c in reversed(s):
        if c in string.digits:
            ret += c
        else:
            break
    if len(ret) > 0:
        return int(ret[::-1])
    else:
        return None

def any_digits_in_str(s):
    return len(set(s) & DIGITS_SET) > 0

def str_is_all_digits(s):
    return len(s) > 0 and len(set(s) - DIGITS_SET) == 0

def any_letters_in_str(s):
    return len(set(s) & LETTERS_SET) > 0

def next_digit_offset(s, start_offset=0):
    """Given an optional start offset, find the offset of the
       next digit character in string s, or -1.
    """
    s_len = len(s)
    for i in range(start_offset, s_len):
        if s[i] in string.digits:
            return i
    return -1

def next_wildcard_offset(s, start_offset=0):
    s_len = len(s)
    for i in range(start_offset, s_len):
        if s[i] in WILDCARDS:
            return i
    return -1

def any_in_seq(search_vals, seq):
    """Check if any value in search_vals in the sequence seq"""
    for v in search_vals:
        if v in seq:
            return True
    return False

def most_versiony_chars_idx(search_list):
    """Find the index of the list element with the most versiony chars,
       -1 if no elements had VC or list len == 0"""
    if len(search_list) == 0:
        return -1
    max_val = 0
    max_vc_idx = -1
    for i in range(len(search_list)):
        # Can't use a set because it won't count repeated digits
        val = 0
        for c in search_list[i]:
            if c in VERSIONY_CHARS:
                # Actually we're lying. Give periods twice the weight of digits
                val += 2 if c == '.' else 1
        if val > max_val:
            max_val = val
            max_vc_idx = i
    return max_vc_idx

def find_date(s):
    """If possible, find the first string in the line s representing a date,
       and return a 3-tuple: (start, end, datetime.date), or None"""
    s = s.lower()
    # Match strings on custom boundary
    found_b = re.search(MONTHS_SHORT_REGEX, s)
    found_B = re.search(MONTHS_LONG_REGEX, s)
    if found_b and found_B:
        return None
    if not found_b and not found_B:
        m = None
        for pat in DATE_NUMERIC_REGEXES:
            m = re.search(pat, s)
            if m:
                break
        if m:
            groups = m.groups()
            groups_len = len(groups)
            if groups_len == 4:
                x, _, y, z = groups
            else:
                raise Exception("find_date() got bogus number of matched groups (groups={}, groups_len={})".format(groups, groups_len))
            tmp = '{} {} {}'.format(x, y, z)
            if len(x) == 2:
                if int(y) > 12:
                    if int(x) <= 12 and int(y) <= 31 and int(z) >= 1970 \
                            and int(z) <= 2999:
                        return (m.start(),
                            m.end(),
                            datetime.datetime.strptime(tmp, "%m %d %Y").date())
                else:
                    if int(y) <= 12 and int(x) <= 31 and int(z) >= 1970 \
                            and int(z) <= 2999:
                        return (m.start(),
                            m.end(),
                            datetime.datetime.strptime(tmp, "%d %m %Y").date())
            if len(x) == 4:
                if int(y) > 12:
                    if int(x) >= 1970 and int(x) <= 2999 and \
                            int(y) <= 31 and int(z) <= 12:
                        return (m.start(),
                            m.end(),
                            datetime.datetime.strptime(tmp, "%Y %d %m").date())
                else:
                    if int(x) >= 1970 and int(x) <= 2999 and \
                            int(y) <= 12 and int(z) <= 31:
                        return (m.start(),
                            m.end(),
                            datetime.datetime.strptime(tmp, "%Y %m %d").date())
    # If that failed, try textual months
    m = None
    for pat in DATE_TEXTUAL_REGEXES:
        m = re.search(pat, s)
        if m:
            break
    if m:
        groups = m.groups()
        groups_len = len(groups)
        x, _, y, z = groups
        if x[0] not in string.digits:
            # Month first, so swap day and month
            foo = x
            x = y
            y = foo
        if len(x) == 4:
            # Year first, so swap day and year
            foo = x
            x = z
            z = foo
        # Make sure it's a month
        y_tmp = y.lower()
        if y_tmp not in MONTHS_SHORT and y_tmp not in MONTHS_LONG:
            return None
        # Now x is day, y is month, z is year
        fmt = '%d'
        x = '0' + x
        x = x[-2:]
        if len(z) == 2:
            if int(z) > 69:
                z = '19' + z
            else:
                z = '20' + z
            z = z[-4:]
        if len(y) == 3:
            fmt += ' %b'
        else:
            fmt += ' %B'
        fmt += ' %Y'
        #print('fmt = %s' % fmt)
        tmp = '{} {} {}'.format(x, y, z)
        #print('tmp = %s' % tmp)
        return (m.start(),
                m.end(),
                datetime.datetime.strptime(tmp, fmt).date())
    return None

def find_pns(s, start_offset, have_pns):
    """Find a package name separator in a string, or ''"""
    s_len   = len(s)
    sep_len = 1
    # Find first digit
    i = start_offset
    i -= 1
    # Move back one more if v_ersion or r_elease
    if s[i].lower() in ['v', 'r']:
        i -= 1
        sep_len += 1
    # Return string
    sep = s[i:i+sep_len]
    if sep not in NAME_SEPS:
        if have_pns:
            ndo_start = i+sep_len+1
            if ndo_start >= s_len:
                return ''
            ndo = next_digit_offset(s, ndo_start)
            if ndo == -1 or ndo >= s_len:
                return ''
            else:
                return find_pns(s, ndo, have_pns)
        elif sep == '.':
            # Handle case "sendmail.8.14.x". We don't want '.' in NAME_SEPS
            # though - that makes the have_pns check worthless, since '.'
            # is usually version_sep
            return sep
        else:
            # Handle edge case where form is "ProFTPD1.3.3" or so
            return ''
    else:
        return sep

def find_version_sep(s):
    """Given a pure version string, find the character (most often)
       separating version components"""
    i = 0
    s_len = len(s)
    char_count = Counter()
    if s[i] in ['v', 'V', 'r', 'R']:
        i += 1
    if s[i] == '/':
        i += 1
    while i < s_len:
        while i < s_len and s[i] in string.digits:
            i += 1
        if i < s_len:
            char_count[s[i]] += 1
            i += 1
    if len(char_count) > 0:
        most_common = char_count.most_common(1)
        char = most_common[0][0]
        if char in '._':
            return char
    return '.'

def find_pure_version(s):
    """Find a pure version string within a larger string s,
       returning (start offset, end offset, string), or None
    """
    start_offset = next_digit_offset(s)
    if start_offset == -1:
        start_offset = next_wildcard_offset(s)
    if start_offset == -1:
        return None
    # Skip back if we have a 'v' or 'v/' type prefix
    so = start_offset
    if so >= 2 and s[so-2:so].lower() in ('v/', 'r/'):
        so -= 2
    if so >= 1 and s[so-1:so].lower() in ('v', 'r'):
        so -= 1
    # Extract version string
    s_len = len(s)
    i = so
    while i < s_len and s[i] in PURE_VERSION_CHARS:
        i += 1
    return (so, i, s[so:i])


def chunk_part(s):
    chunks = []
    part_len = len(s)
    i = 0
    while i < part_len:
        chunk = ''
        while i < part_len and s[i] in '-._':
            i += 1
        while i < part_len and s[i] in string.digits:
            chunk += s[i]
            i += 1
        if chunk != '':
            if str_is_all_digits(chunk):
                chunk = int(chunk)
            chunks.append(chunk)
            chunk = ''
        while i < part_len and s[i] in string.ascii_letters:
            chunk += s[i]
            i += 1
        if chunk != '':
            chunks.append(chunk)
    return chunks


# Sequence comparison logic
def version_lt_other(vers_a, vers_b):
    """Return True if a version sequence is less than another, False if
       it is greater, or if we can't decide, return two chunks to
       pass to chunk_lt_other (below).
    """
    a = tuple(vers_a.version)
    b = tuple(vers_b.version)
    a_len = len(a)
    b_len = len(b)
    len_diff = abs(a_len - b_len)
    # Extend shorter to length of longer
    if a_len < b_len:
        a = a + ((0,) * len_diff)
    if b_len < a_len:
        b = b + ((0,) * len_diff)
    assert(len(a) == len(b))
    # Find first non-equal
    i = 0
    max_len = len(a)
    while i < max_len:
        if a[i] != b[i]:
            break
    # Compare, handling str vs int
    ai = a[i]
    bi = b[i]
    type_tuple = (type(ai), type(bi))
    if type_tuple == (int, int) or \
       (isinstance(type_tuple[0], basestring) and isinstance(type_tuple[1], basestring)):
        if ai < bi:
            return True
        if ai > bi:
            return False
    # Not enough info, return two chunks, creating fake chunk for
    # the int
    if type_tuple[0] is int:
        chunk_a = [ai]
        chunk_b = vers_b._chunks[i]
    else:
        chunk_a = vers_a.chunks[i]
        chunk_b = [bi]
    return (chunk_a, chunk_b)

def chunk_seq_lt_other(a, b):
    """Compare two chunk sequences and return True if a < b,
       otherwise False. Always return True or False.
    """
    assert(len(a) > 0 and len(b) > 0)
    if type(a[0]) is int and a[0] != 0:
        return False
    if type(b[0]) is int and b[0] != 0:
        return True
    return False # TODO

def human_to_timedelta(s):
    days = 0
    months = 0
    years = 0
    s = s.lower().rstrip().lstrip()
    if str_is_all_digits(s):
        # If only digits, assume number of days
        return datetime.timedelta(int(s))
    m = re.match(DURATION_REGEX, s)
    if m:
        for g in m.groups():
            if g == None:
                break
            clean = g.replace(' ', '')
            n = first_int(clean)
            char_offset = len(str(n))
            duration = clean[char_offset]
            if duration not in 'ymd':
                raise HumanDurationParseError(
                        "Couldn't interpret time spec '{}'".format(g))
            if duration == 'y':
                days += (n * 365)
            if duration == 'm':
                days += (n * 30)
            if duration == 'd':
                days += n
    else:
        raise HumanDurationParseError("invalid duration spec {}".format(s))
    return datetime.timedelta(days)

def timedelta_to_human(delta):
    days = 0
    months = 0
    years = 0
    delta_days = delta.days     # readonly
    if type(delta) is not datetime.timedelta:
        raise TypeError("timedelta_to_human() arg must be datetime.timedelta")
    while delta_days >= 365:
        years += 1
        delta_days -= 365
    while delta_days >= 30:
        months += 1
        delta_days -= 30
    days = delta_days
    assert(days < 30)
    assert(days >= 0)
    s = ''
    if years:
        s += '{} {}'.format(years, pluralize('year', years))
    if months:
        if len(s):
            s += ', '
        s += '{} {}'.format(months, pluralize('month', months))
    if len(s) == 0 or days > 0:
        if len(s):
            s += ', '
        s += '{} {}'.format(days, pluralize('day', days))
    return s


########
# Exception classes
########

class VersionError(Exception):
    pass

class VersionNotComparableError(VersionError):
    """The two versions are not comparable."""

class VersionParseError(VersionError):
    """Failed to parse the version string."""

class VersionInitError(VersionError):
    """Failed to initialize the version instance."""

class HumanDurationParseError(VersionError):
    """Failed to parse the duration string."""

class VersionPartsError(VersionError):
    """Fuckup in VersionParts"""


class VersionPart(unicode):
    """Wrap an int or a string, with convenient comparisons"""
    def __init__(self, str_or_int):
        super(VersionPart, self).__init__(str_or_int)

    def __eq__(self, other):
        if type(other) is int:
            if str_is_all_digits(self):
                return int(self) == other
            other = VersionPart(other)
        return super(VersionPart, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(other) is int:
            if str_is_all_digits(self):
                return int(self) < other
            other = VersionPart(other)
        return super(VersionPart, self).__lt__(other)

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


class VersionParts(list):
    """A list subclass to encapsulate some messy bits. It:
       a) has a set maximum length
       b) allows assigning items at arbitrary indices, up to max len
       c) fills 0 in any unassigned positions up to last assigned position
       d) calculates and stores chunks when assigning items
       e) returns 0 (<max len) instead of raising IndexError
       f) encapsulates logic for comparing version parts (this is
          almost, but not quite, equivalent to comparing versions)
    """

    def __init__(self, *args, **kwargs):
        max_length = kwargs.get('max_length', None)
        if max_length is None or type(max_length) is not int or \
           max_length < 1:
            raise TypeError('must set a max_length (positive int)')
        if len(args) > max_length:
            args = args[:max_length]
        self._max_length = max_length
        self._chunks = [[0]] * max_length
        args = [VersionPart(x) for x in args]
        super(VersionParts, self).__init__(args)
        for i in range(len(args)):
            self._update_chunk(i)

    def __len__(self):
        return super(VersionParts, self).__len__()

    def __getitem__(self, y):
        if y >= self._max_length:
            raise IndexError('list index out of range (>max_length)')
        if y >= len(self):
            return 0
        else:
            return super(VersionParts, self).__getitem__(y)

    def __setitem__(self, i, j):
        if i >= self._max_length:
            raise IndexError('list index out of range (>max_length)')
        self_len = len(self)
        if i >= self_len:
            len_diff = abs(self_len - (i+1))
            self += [0] * len_diff
        j = VersionPart(j)
        super(VersionParts, self).__setitem__(i, j)
        self._update_chunk(i)

    def __delitem__(self, i):
        super(VersionParts, self).__delitem__(i)
        self._chunks[i] = [0]

    def __getslice__(self, i, j):
        if j >= self._max_length:
            raise IndexError('list index out of range (>max_length)')
        return [self[x] for x in range(i, j)]

    def __setslice__(self, i, j, seq):
        if j >= self._max_length:
            raise IndexError('list index out of range (>max_length)')
        seq_vals = [VersionPart(x) for x in seq]
        super(VersionParts, self).__setslice__(i, j, seq_vals)
        for n in range(i, j):
            self._update_chunk(i)

    def append(self, obj):
        self_len = len(self)
        if self_len == self._max_length:
            raise VersionPartsError('parts at max_length already')
        self.__setitem__(self_len, VersionPart(obj))
        self._update_chunk(self_len)

    #TODO others?

    def __eq__(self, other):
        assert(isinstance(other, list) or isinstance(other, tuple))
        max_len = max(len(self), len(other))
        for i in range(max_len):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        assert(isinstance(other, VersionParts))
        if self.__eq__(other):
            return False
        if len(self) == 0:
            return True
        if len(other) == 0:
            return False
        # Find first non-equal element
        self_len = len(self)
        other_len = len(other)
        i = 0
        while i < min(self._max_length, other._max_length):
            if self[i] != other[i]:
                break
            i += 1
        print("i = {}".format(i))
        #print("self[i] = {}".format(self[i]))
        #print("other[i] = {}".format(other[i]))
        # if self_len < other_len:
        #     return True
        # if other_len < self_len:
        #     return False
        # Check chunk lens
        sc = self._chunks[i]
        oc = other._chunks[i]
        print("sc = {}".format(sc))
        print("oc = {}".format(oc))
        sc_len = len(sc)
        oc_len = len(oc)
        # 1. trivial case
        if sc_len == oc_len == 1 and \
           ((type(sc[0]), type(oc[0])) == (int, int) or \
            (isinstance(sc[0], basestring) and isinstance(oc[0], basestring))):
            return self[i] < other[i]
        # Check prerelease
        if sc[0] in PRERELEASE_TAGS and oc[0] not in PRERELEASE_TAGS:
            return True
        if sc[0] not in PRERELEASE_TAGS and oc[0] in PRERELEASE_TAGS:
            return False
        # Otherwise, iterate through chunks
        if sc_len == oc_len:
            i = 0
            while i < min(sc_len, oc_len):
                type_tuple = (type(sc[i]), type(oc[i]))
                if type_tuple == (int, int):
                    return sc[i] < oc[i]
                if isinstance(type_tuple[0], basestring) and isinstance(type_tuple[1], basestring):
                    return sc[i] < oc[i]
                if type_tuple[0] == int and isinstance(type_tuple[1], basestring):
                    return False
                if isinstance(type_tuple[0], basestring) and type_tuple[1] == int:
                    return True
                i += 1
        # Here, one chunk is longer than the other
        if sc_len < oc_len:
            if oc[1] in PRERELEASE_TAGS:
                return False
        if oc_len < sc_len:
            if sc[1] in PRERELEASE_TAGS:
                return True

        raise Exception("should not happen")

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def _update_chunk(self, i):
        j = self[i]
        if str_is_all_digits(j):
            self._chunks[i] = [int(j)]
        else:
            self._chunks[i] = chunk_part(j)

    def is_empty(self):
        return self._chunks == [[0]] * self._max_length


class Version(object):
    name = None
    name_sep = ' '      # default
    version_sep = '.'   # default

    _named_fields  = ('major', 'minor', 'micro', 'nano', 'pico',
                      'femto', 'atto', 'zepto', 'yocto',)
    _max_fields    = len(_named_fields)
    _name_index    = dict(zip(_named_fields, range(_max_fields)))
    _kwargs        = ('release_date', 'eol_date', 'prefix_str', 'suffix_str',
                      'build_meta',)
    _kwargs_defaults = ('name_sep', 'version_sep',)

    # For mocking
    date_class = datetime.date

    # TODO init with list (+kw)

    def __init__(self, *args, **kwargs):
        # Actual storage
        self.parts = VersionParts(max_length=self._max_fields)
        # For round-trip stringify
        self._str_parts = []
        # None before first part
        self._separators = ['']

        # Set defaults = None
        for attr in self._kwargs:
            setattr(self, attr, None)

        if len(args) == 1 and isinstance(args[0], basestring):
            if any_digits_in_str(args[0]):
                # Common case: init with a string to be parsed.
                # Ignores other kwargs.
                Version.parse(args[0], version_obj=self)
                return
            else:
                # Just set name and do other processing
                self.name = args[0]
                args = ()

        # Handle special case
        if 'patch' in kwargs and 'micro' in kwargs:
            raise VersionInitError(
                "Both 'patch' and 'micro' as kwargs -- they are synonyms")

        # Canonical name
        if 'patch' in kwargs:
            kwargs['micro'] = kwargs['patch']
            del kwargs['patch']

        # Process certain kwargs first
        # Custom attrs that shouldn't be None -- leave defaults
        for attr in self._kwargs_defaults:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]

        # Process positional args

        # Got name, and explicit init
        if len(args) > 1 and isinstance(args[0], basestring):
            self.name = args[0]
            args = args[1:]
        if 'name' in kwargs:
            self.name = kwargs['name']
            del kwargs['name']

        # Now process positional args as ordered field values
        if len(args) > self._max_fields:
            args = args[:self._max_fields]
        self.parts = args

        # Process kw-or-positional args
        if len(self.parts) >= 3 and 'patch' in kwargs:
            raise VersionInitError(
                "Specified patch arg as kw but micro positional")

        for attr in self._named_fields:
            if attr in kwargs:
                if getattr(self, attr) != 0:
                    raise VersionInitError(
                        "Specified arg positional and kw ({})".format(attr))
                else:
                    val = int(kwargs[attr])
                    setattr(self, attr, val)
                    del kwargs[attr]

        # Process normal kwargs
        for attr in self._kwargs:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]

        if len(kwargs) > 0:
            raise VersionInitError(
                "Got unexpected kwargs: {}".format(kwargs))

        # TODO set release_date on explicit init


    # Minimal clever encapsulation

    def __getattribute__(self, name):
        if name == 'patch':
            name = 'micro'
        name_index = super(Version, self).__getattribute__('_name_index')
        if name in name_index:
            idx = name_index[name]
            parts = super(Version, self).__getattribute__('parts')
            return parts[idx]
        else:
            return super(Version, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'parts':
            if isinstance(value, VersionParts) or \
               value is None:
                super(Version, self).__setattr__('parts', value)
                return
            if not isinstance(value, list) and \
               not isinstance(value, tuple):
                raise TypeError('tried to assign bad type to .parts')
            args = tuple(value)
            vp = VersionParts(*args, max_length=self._max_fields)
            super(Version, self).__setattr__('parts', vp)
            return
        if name == 'patch':
            name = 'micro'
        name_index = super(Version, self).__getattribute__('_name_index')
        if name in name_index:
            idx = name_index[name]
            parts = super(Version, self).__getattribute__('parts')
            parts[idx] = value
        else:
            super(Version, self).__setattr__(name, value)


    # Comparison methods -- mostly dispatch to VersionParts
    def __eq__(self, other):
        return self.name == other.name and \
               self.parts == other.parts

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.name != other.name:
            raise TypeError("numeric comparing versions with different names")
        return self.parts < other.parts

    def __lte__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__lte__(other)

    def __gte__(self, other):
        return not self.__lt__(other)

    # Other magic

    def __hash__(self):
        if self.name is None:
            name = ''
        else:
            name = self.name + ' '
        return hash(name + python6_str(self.parts))

    def __nonzero__(self):
        return len(self.parts) != 0

    # Stringifying methods

    def get_version_str(self):
        s = ''
        if self.prefix_str:
            s += self.prefix_str
        # Use _str_parts if we parsed
        if self._str_parts:
            use_parts = self._str_parts
        else:
            use_parts = self.parts
        str_vals = [coerce_to_unicode(x) for x in use_parts]
        seps_len = len(self._separators)
        for i, val in enumerate(str_vals):
            if i < seps_len:
                s += self._separators[i]
            else:
                s += self.version_sep
            s += val
        if self.build_meta:
            s += '+' + self.build_meta
        if self.suffix_str:
            s += ' '
            s += self.suffix_str
        return s

    def __unicode__(self):
        # Instead of just keeping the string we gave to parse (if we did),
        # construct manually anyway - more checks for parsing code.
        s = ''
        ns = self.name_sep if self.name_sep else ''
        if self.name:
            s += self.name
            if not self.parts.is_empty():
                s += ns
        s += self.get_version_str()
        return s

    def __str__(self):
        return python6_str(self.__unicode__())

    def __repr__(self):
        # TODO xfixes?
        return "<Version('" + self.__str__() + "')>"


    @classmethod
    def normalize_name(cls, name):
        name = name.strip()
        return re.sub('\s+', ' ', name)


    @classmethod
    def parse_pure(cls, s, version_obj=None):
        """Parse a 'pure' version string, i.e. without any
           package name or extraneous trailing string data.
        """
        if version_obj is None:
            v = Version()
        else:
            v = version_obj

        #print('parse_pure got %s' % s)
        #print('in parse_pure, .name = %s' % v.name)

        s = coerce_to_unicode(s)
        s_len = len(s)
        part_chars = list(string.digits + string.ascii_letters + '-+')

        i = 0
        if s[:2].lower() in ('v/', 'r/'):
            v.prefix_str = s[:2]
            i += 2
        elif s[:1].lower() in ('v', 'r'):
            v.prefix_str = s[:1]
            i += 1
        #print("s = {}".format(s))
        while i < s_len:
            start_offset = i

            # Grab next part if there is one
            while i < s_len and s[i] in part_chars:
                i += 1
            part = s[start_offset:i]

            # SSH special case
            m = re.search('(\d+)(p)(\d+)', part, re.IGNORECASE)
            if m:
                a, b, c = m.group(1), m.group(2), m.group(3)
                v._str_parts.append(a)
                v._str_parts.append(c)
                v.parts.append(a)
                v._separators.append(b)
                v.parts.append(c)
                continue

            # Check for build_meta
            if '+' in part:
                p0, p1 = part.split('+')
                v.build_meta = p1
                part = p0

            if '-' in part and i < s_len:
                space_idx = s.find(' ', i)
                if space_idx != -1:
                    part = part + s[i:space_idx]
                    i = space_idx

            # Save string part for round-trip stringify
            v._str_parts.append(part)

            # Save parts
            if '-' in part and len(v.parts) == 0:
                raise VersionParseError('whut')
            else:
                v.parts.append(part)
            if i < s_len:
                v._separators.append(s[i])
            i += 1

            if i < s_len and s[i-1] == ' ':
                v.suffix_str = s[i:]
                break
            #print("parts  = {}".format(v.parts))
            #print("chunks = {}".format(v.parts._chunks))

        if len(v.parts) > v._max_fields:
            raise VersionParseError("Too many parts")

        if v.name:
            v.release_date = get_release_date(v.name, v.get_version_str())

        return v


    @classmethod
    def parse(cls, s, version_obj=None):
        if version_obj is None:
            v = Version()
        else:
            v = version_obj
        for sep in NAME_SEPS:
            parts = s.split(sep)
            #print('sep = [%s]' % sep)
            #print('parts = %s' % parts)
            name_parts = []
            if len(parts) >= 2 and not any_digits_in_str(parts[0]):
                for i, p in enumerate(parts):
                    if not any_digits_in_str(parts[i]):
                        name_parts.append(p)
                    else:
                        break
                parts = parts[i:]
                vers_parts = sep.join(parts)
                slash_idx = vers_parts.find('/')
                if slash_idx != -1 and next_digit_offset(vers_parts) > slash_idx:
                    continue
                v.name = cls.normalize_name(sep.join(name_parts))
                v.name_sep = sep
                return cls.parse_pure(vers_parts, v)
        return cls.parse_pure(s, v)
        raise VersionParseError("couldn't figure out package name (%s)" % s)


    def get_age(self):
        """Return age in days, or None"""
        if self.release_date is None:
            self.release_date = get_release_date(self.name, self.get_version_str())
        if self.release_date is None:
            # TODO use boundaries?
            return None
        else:
            delta = self.date_class.today() - self.release_date
            return delta.days


# Load release data

with open(DATA_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        if not parts:
            continue
        if len(parts) == 1:
            # a synonym def
            a, b = parts[0].split('=')
            PKG_SYNONYMS[a.lower()] = b.lower()
            PKG_SYNONYMS[b.lower()] = a.lower()
        else:
            pkg_name, vers, release_date_str = parts
            if pkg_name not in PKG_RELEASE_DATA:
                PKG_RELEASE_DATA[pkg_name] = {}
            release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d').date()
            PKG_RELEASE_DATA[pkg_name][vers] = release_date

# Pre-process some things
for pkg_name in PKG_RELEASE_DATA:
    dates = sorted(PKG_RELEASE_DATA[pkg_name].values())
    oldest_date = dates[0]
    newest_date = dates[-1]
    PKG_DATE_BOUNDARIES[pkg_name] = {'oldest': oldest_date, 'newest': newest_date}


def get_release_date(pkg_name, vers):
    pkg_name = pkg_name.lower()
    if pkg_name not in PKG_RELEASE_DATA and pkg_name in PKG_SYNONYMS:
        pkg_name = PKG_SYNONYMS[pkg_name]
    if pkg_name in PKG_RELEASE_DATA:
        if vers in PKG_RELEASE_DATA[pkg_name]:
            return PKG_RELEASE_DATA[pkg_name][vers]
    return None


def get_release_boundaries(pkg_name):
    pkg_name = pkg_name.lower()
    if pkg_name not in PKG_DATE_BOUNDARIES and pkg_name in PKG_SYNONYMS:
        pkg_name = PKG_SYNONYMS[pkg_name]
    if pkg_name in PKG_DATE_BOUNDARIES:
        return PKG_DATE_BOUNDARIES[pkg_name]
    return None

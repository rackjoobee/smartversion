# -*- coding: utf-8 -*-

# TODO missing features (priority order)
# - handle hard cases like distcc, parens

# - coverage
# - pickle / json + restore
# - Sphinx like the click docs
# - timedelta compare
# - i18n
# - support full unicode in name / version / etc

# (see ../TODO and grep TODO)


from __future__ import print_function, unicode_literals

import sys
import string
import re
import datetime
from collections import Counter

########
# Constants
########

STR_TYPES = [str]
if sys.version_info.major == 2:
    STR_TYPES.append(unicode)

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

# Package name separators - strings which sep package name
# from the version, e.g. linux[-]2.6.5. 
# This should not include '.' since it usually separates 
# the version numbers. That case is handled specially.
NAME_SEPS = ['-V', '-v', '-R', '-r', '_V', '_v', '_R', '_r', ' V', ' v', ' R', ' r', '/R', '/r', '/V', '/v', ' ', '-', '_', '/']
PNS_SET = set(NAME_SEPS)

# Pre-compile our regexes for speed (maybe, but can't hurt, 
# and helps readability).
DIGITS_REGEX = re.compile(r'[^0-9]*([0-9]+)')

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
    r'(\d\d?)([-._ ])([a-zA-Z]{3,})[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
    r'([a-zA-Z]{3,})([-._ ])(\d\d?)[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
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
    def coerce_to_unicode(s):
        return unicode(s)

    def python6_str(s):
        return s.encode('utf-8')    # TODO sys.getdefaultencoding?
else:
    def coerce_to_unicode(s):
        if type(s) is bytes:
            return s.decode('utf-8')
        return str(s)

    def python6_str(s):
        return str(s)

def pluralize(word, n):         # TODO i18n
    assert(type(word) in STR_TYPES)
    return word + 's' if n == 0 or n > 1 else word

def count_zero_prefixes(s):
    """Return a count of how many zeroes prefix the first non-0 digit char"""
    if type(s) not in STR_TYPES:
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
        tmp = '{} {} {}'.format(x, y, z)
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
        while i < part_len and s[i] == '-':
            i += 1
        while i < part_len and s[i] in string.digits:
            chunk += s[i]
            i += 1
        if chunk != '':
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
       (type_tuple[0] in STR_TYPES and type_tuple[1] in STR_TYPES):
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


class Version(object):
    name = None
    name_sep = ' '      # default
    version_sep = '.'   # default

    # 'name' is a special case
    _named_fields  = ('major', 'minor', 'micro', 'nano', 'pico',
                      'femto', 'atto', 'zepto', 'yocto',)
    _name_index    = dict(zip(_named_fields, range(len(_named_fields))))
    _kwargs        = ('release_date', 'eol_date', 'prefix_str', 'suffix_str',
                      'build_meta',)
    _kwargs_defaults = ('name_sep', 'version_sep',)

    # For mocking
    date_class = datetime.date

    # TODO init with list / tuple (+kw)

    def __init__(self, *args, **kwargs):
        args_len = len(args)
        self.parts = []             # Actual storage
        self._str_parts = []        # For round-trip stringify
        self._chunks = []           # For comparison
        self._separators = ['']     # None before first part

        # Set defaults = None
        for attr in self._kwargs:
            setattr(self, attr, None)

        if args_len == 1 and type(args[0]) in STR_TYPES:
            if any_digits_in_str(args[0]):
                # Common case: init with a string to be parsed.
                # Ignores other kwargs.
                Version.parse(args[0], version_obj=self)
                return
            else:
                # Just set name and do other processing
                self.name = args[0]
                args = ()
                args_len = 0

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
        if args_len > 1 and type(args[0]) in STR_TYPES:
            self.name = args[0] 
            args = args[1:]
            args_len -= 1

        # Now process positional args as ordered field values
        for i, field_name in enumerate(self._named_fields):
            if i < args_len:
                setattr(self, field_name, args[i])
            else:
                setattr(self, field_name, None)

        # Process kw-or-positional args
        if self.micro is not None and 'patch' in kwargs:
            raise VersionInitError(
                "Specified patch arg as kw but micro positional")

        for attr in self._named_fields + ('name',):
            if attr in kwargs:
                if getattr(self, attr) is not None:
                    raise VersionInitError(
                        "Specified arg positional and kw ({})".format(attr))
                else:
                    setattr(self, attr, kwargs[attr])
                    del kwargs[attr]

        # Process normal kwargs
        for attr in self._kwargs:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
                del kwargs[attr]

        if len(kwargs) > 0:
            raise VersionInitError(
                "Got unexpected kwargs: {}".format(kwargs))

        # Coerce fields to int if appropriate
        for field_name in self._named_fields:
            val = getattr(self, field_name)
            if type(val) in STR_TYPES and \
              str_is_all_digits(val):
                setattr(self, field_name, int(val))


    # Minimal clever encapsulation

    def __getattribute__(self, name):
        if name == 'version':
            vals = []
            named_fields = list(self._named_fields)
            last_idx = len(named_fields) - 1
            include = False
            # Find last value that's not None and include up to that
            for i in range(last_idx, -1, -1):
                val = getattr(self, named_fields[i])
                if val is not None:
                    include = True
                if include:
                    # Intermediate missing values -> 0
                    vals.append(val if val is not None else 0)
            vals.reverse()
            return tuple(vals)
        elif name == 'patch':
            return self.__getattribute__('micro') 
        elif name in self._named_fields:
            return super(Version, self).__getattribute__('_name_index')[name]
        else:
            return super(Version, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'version':
            value_len = len(value)
            for i, field_name in enumerate(self._named_fields):
                if i < value_len:
                    super(Version, self).__setattr__(field_name, value[i])
                else:
                    super(Version, self).__setattr__(field_name, None)
        elif name == 'patch':
            self.__setattr__('micro', value)
        elif name in self._named_fields:
            idx = self._name_index[name]
            self.parts[idx] = value
        else:
            super(Version, self).__setattr__(name, value)
            

    # Comparison methods
    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        # Logic moved to the two seq_lt functions, since a lot of
        # it is repeated
        if self.__eq__(other):
            return False
        ret = version_seq_lt_other(self.version, other.version)
        if type(ret) is bool:
            return ret
        else:
            chunk_a, chunk_b = ret
            return chunk_seq_lt_other(chunk_a, chunk_b)

    def __lte__(self, other):
        if self.__eq__(other):
            return True
        return self.__lt__(other)

    def __gt__(self, other):
        if not self.__eq__(other) and \
           not self.__lt__(other):
            return True
        return False

    def __gte__(self, other):
        if self.__eq__(other):
            return True
        return self.__gt__(other)

    # Other magic

    def __hash__(self):
        return hash(python6_str(self.version))

    def __nonzero__(self):
        return len(self.version) != 0

    # Stringifying methods

    def __unicode__(self):
        # Instead of just keeping the string we gave to parse (if we did),
        # construct manually anyway - more checks for parsing code.
        s = ''
        ns = self.name_sep if self.name_sep else ''
        if self.name:
            s += self.name
            if self.major is not None:
                s += ns
        if self.prefix_str:
            s += self.prefix_str
        # Use _str_parts if we parsed
        if self._str_parts:
            use_parts = self._str_parts
        else:
            use_parts = self.version
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
            s += self.suffix_str
        return s

    def __str__(self):
        return python6_str(self.__unicode__())

    def __repr__(self):
        return "Version('" + self.__str__() + "')"


    @classmethod
    def parse_pure(cls, s, version_obj=None):
        """Parse a 'pure' version string, i.e. without any
           package name or extraneous trailing string data.
        """
        if version_obj is None:
            v = Version()
        else:
            v = version_obj

        s_len = len(s)
        parts = []
        part_chars = list(string.digits + string.ascii_letters + '-+')

        i = 0
        if s[:2].lower() in ('v/', 'r/'):
            v.prefix_str = s[:2]
            i += 2
        elif s[:1].lower() in ('v', 'r'):
            v.prefix_str = s[:1]
            i += 1
        print("s = {}".format(s))
        while i < s_len:
            start_offset = i
            while i < s_len and s[i] in part_chars: 
                i += 1
            part = s[start_offset:i]
            # Check for build_meta
            if '+' in part:
                p0, p1 = part.split('+')
                v.build_meta = p1
                part = p0
            # Save string part for round-trip stringify
            v._str_parts.append(part)
            # Save parts
            if str_is_all_digits(part):
                part = int(part)
                parts.append(part)
                v._chunks.append([part])
            elif '-' in part and len(parts) == 0:
                raise VersionParseError()
            else:
                chunks = chunk_part(part)
                chunks = [int(x) if str_is_all_digits(x) else x \
                          for x in chunks]
                parts.append(part)
                v._chunks.append(chunks)
            if i < s_len:
                v._separators.append(s[i])
            i += 1
            print("parts  = {}".format(parts))
            print("chunks = {}".format(v._chunks))

        if len(parts) > len(cls._named_fields):
            raise VersionParseError("Too many parts")

        for i, part in enumerate(parts):
            field_name = cls._named_fields[i]
            setattr(v, field_name, part)

        return v


    @classmethod
    def parse(cls, s, version_obj=None):
        if version_obj is None:
            v = Version()
        else:
            v = version_obj
        return cls.parse_pure(s, v)

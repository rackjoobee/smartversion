
########
# Version class
########

class Version(object):

    # For mocking
    date_class = datetime.date

    # Used to represent "release_date not set", and still allow sorting
    _timedelta_epoch = None      # set on __init__


    @classmethod
    def parse_patch(cls, patch, version_obj):
        """Parse and update the patch string for a Version object. 
           Often and in (e.g.) Semver, this is just
           an integer, but can be more complicated. Return 
           the updated Version object."""
        assert(version_obj is not None)
        assert(version_obj.__class__ is cls)

        v = version_obj

        if patch is None:
            v.patch = v.patch1 = v.patch2 = v.patch_str = None
            return v
        if type(patch) is int:
            v.patch = patch
            v.patch1 = patch
            v.patch2 = v.patch_str = None
            return v
        if type(patch) not in STR_TYPES:
            raise TypeError(
                "'patch' arg to parse_patch() must be string or int")

        patch = coerce_to_unicode(patch)

        assert(patch[0] not in [' ', '\t'])

        # Do the parse 
        v.patch = patch     # might be changed later
        v.patch1 = None
        v.patch2 = None
        v.patch_str = None

        if v.patch[0] == 'p' and v._openssh_moved_p:
            v.patch = v.patch[1:]
            v.patch_str = 'p'

        # If just numeric, handle that
        tmp_zp = count_zero_prefixes(v.patch)
        try:
            tmp_pi = int(v.patch)
        except ValueError:
            tmp_pi = ''
        if tmp_pi != '' and len(v.patch) == len(str(tmp_pi)) + tmp_zp:
            v.patch = tmp_pi
            v.patch1 = tmp_pi
            v.zero_prefixes['patch'] = tmp_zp
            v.zero_prefixes['patch1'] = tmp_zp
            return v
        
        # Otherwise handle complicated stuff
        if v.patch[0] in string.digits:
            _, patch1_str = first_digits(v.patch)
            start_idx = len(patch1_str)
            v.patch1  = int(patch1_str)
            v.zero_prefixes['patch1']  = count_zero_prefixes(patch1_str)
        elif v.patch[0] in WILDCARDS:
            v.patch1 = patch1_str = v.patch[0]
            start_idx = 1
        else:
            start_idx = 0

        # If all digits, whole patch is now in patch1.
        # Otherwise parse any trailing digits (e.g. "rc2")
        #if v.patch1 != None and len(v.patch) > len(patch1_str): 
        # Either all non-digit trailing or there's a patch2
        if v.patch[-1] in string.digits:
            _, tmp = first_digits(v.patch[::-1])
            patch2_str = tmp[::-1]
            v.patch2 = int(patch2_str)
            v.zero_prefixes['patch2'] = count_zero_prefixes(patch2_str)
        if v.patch[-1] in WILDCARDS:
            v.patch2 = patch2_str = v.patch[-1]

        # Make sure we don't duplicate patch1
        if v.patch1 is not None \
        and v.patch2 is not None \
        and len(patch2_str) == len(v.patch):
            v.patch2 = None

        # Now extract intermediate string, if any,
        # unless we already got an openssh string
        if v.patch2 is not None:
            end_range = len(v.patch) - len(patch2_str)
        else:
            end_range = len(v.patch)
        if v.patch_str is None:
            v.patch_str = patch[ start_idx:end_range ]
            if len(v.patch_str) == 0:
                v.patch_str = None

        v.patch = patch
        return v


    @classmethod
    def parse_version(cls, version_str, version_obj=None):
        """Parse version string proper (without package name), 
           returning a new Version object. Optionally take an 
           existing version object and update it."""
        if version_obj is None:
            v = Version()
        else:
            v = version_obj

        version_str = coerce_to_unicode(version_str)

        version_len = len(version_str)
        version     = version_str       # nicer name
        offset      = 0                 # offset into version str

        assert(version[0] not in [' ', '\t'])

        # Do parse

        # Handle 'vX.Y', 'rX.Y'
        if version[0].lower() in ['v', 'r']: 
            version = version[1:]

        # TODO version IS a date string
        # If there's a date string in the version string, set it aside
        # so it doesn't fuck up the parse.
        # Yes, this has been seen. 
        if any_digits_in_str(version):
            d = find_date(version)
            if d:
                _ver_date_start, _ver_date_end, release_date = d
                if version[_ver_date_end] in '/-_.':
                    if _ver_date_end < version_len-1:
                        _ver_date_end += 1
                _ver_date_str = version[_ver_date_start:_ver_date_end]

                # Set as release_date regardless
                v.release_date   = release_date
                
                # Only move if a) not the entire version number, 
                # b) not in build_meta
                tmp = version.find('+')
                if version_len != len(_ver_date_str) and \
                (tmp == -1 or _ver_date_start < tmp):
                    version = version[:_ver_date_start] + version[_ver_date_end:]
                    v._ver_date_start = _ver_date_start
                    v._ver_date_end   = _ver_date_end
                    v._ver_date_str   = _ver_date_str

        # Do the parse

        result = first_digits(version)
        if result is None:
            # Check major wildcard
            if version[0] in WILDCARDS:
                v.major = version[0]
                offset += 1
            else:
                raise VersionParseError("Couldn't get major version number")
        else:
            offset, major = result
            v.zero_prefixes['major'] = count_zero_prefixes(major)
            v.major = int(major)

        # Minor
        if offset > version_len - 1:
            v.minor = None
        else:
            # If we have a minor version number, store the version sep.
            # Store here since 2nd sep can be a special case value
            v.version_sep = version[offset]
            offset += 1
            # Then store minor, handling wildcards
            if version[offset:offset+2].lower() == 'x'+v.version_sep \
            or version[offset:].lower() == 'x'                     \
            or version[offset:offset+2].lower() == '*'+v.version_sep \
            or version[offset:].lower() == '*':
                v.minor = version[offset]
                offset += 1
            else:
                result = first_digits(version[offset:])
                if result is None:
                    raise VersionParseError("bad version string, wanted minor and got instead: '{}'".format(version[offset:]))
                tmp, minor = result
                offset += tmp
                v.zero_prefixes['minor'] = count_zero_prefixes(minor)
                v.minor = int(minor)
                # See if we have a prerelease id
                #if offset < version_len:
                #    if version[offset].lower() in ['a', 'b', 'c']:
                #        minor += version[offset]
                #        offset += 1
                #if version[offset:offset+2].lower() == 'rc':
                #    minor += version[offset:offset+2]
                #    offset += 2
                #    # Now grab any digits left
                #    while version[offset] in string.digits:
                #        minor += version[offset]
                #        offset += 1
            # Skip past next version sep
            offset += 1

        if offset > version_len - 1:
            v.patch = None
        else:
            patch = version[offset:version_len]
            # Handle Perl format (second version sep = '_')
            if offset > 0 and version[offset-1] == '_':
                v._perl_version_fmt = True
            # Handle extra shit instead of version sep
            if offset > 0 and version[offset-1] not in [v.version_sep, '_', 'p']:
                patch = version[offset-1] + patch
            # Handle the special cases OpenSSH X.YpZ and OpenSSH X.Y.pZ 
            # - put the 'p' in patch level, since it's useful 
            # information (p=portable), and p and non-p OpenSSH 
            # versions can be meaningfully compared
            if v.name_clean == 'openssh':
                if offset > 0 and version[offset-1] == 'p':
                    patch = 'p' + patch
                    v._openssh_moved_p = True
            
            # Build meta
            assert(patch != None)
            plus_idx = patch.find('+')
            if plus_idx != -1:
                v.build_meta = patch[plus_idx+1:]
                patch = patch[:plus_idx]

            cls.parse_patch(patch, v)


    @classmethod
    def parse(cls, s, version_obj=None, no_name=False):
        """Parse a string into a Version object"""
        if version_obj is None:
            v = Version()
        else:
            v = version_obj

        s = coerce_to_unicode(s)

        # clear the defaults
        v.name_sep    = None    
        v.version_sep = None

        # Normalize whitespace - may break round-trip 
        # stringify, but probably ok, and eases parsing
        s = s.rstrip().lstrip()
        s = re.sub(r'\s+', ' ', s)  

        if len(s) == 0:
            raise VersionParseError("got blank string")

        # Just name, no version
        if not any_digits_in_str(s) \
           and not any_in_seq(WILDCARDS, s):
            raise VersionParseError("No digits or wildcards - " +
                "this is not a version string")

        # Check explicit 'no name'
        if no_name:
            v.name = None
            cls.parse_version(s, version_obj=v)
            return v

        # Avoid various weird in-the-wild cases
        print(s)
        if s.startswith('(protocol'):
            raise VersionParseError("not a version")

        # Figure out name separator, if we have one
        have_pns = any_in_seq(NAME_SEPS, s)
        # TODO remove this once we have a proper find_version method
        if 'GNU' in s or 'protocol' in s: 
            gnu_idx = s.find('GNU')
            proto_idx = s.find('protocol')
            use_idx = max(gnu_idx, proto_idx)
            first_digit_offset = next_digit_offset(s, use_idx)
        else:
            first_digit_offset = next_digit_offset(s)
        name_sep = find_pns(s, first_digit_offset, have_pns)

        # Split into parts. 
        name = None
        version  = None
        parts    = [] 
        extra_str = None 
        # Handle blank name, and also edge case where 
        # form is "ProFTPD1.3.3" or so
        if name_sep == '': 
            parts.append( s[:first_digit_offset] )
            parts.append( s[first_digit_offset:] )
        else:
            parts = s.split(name_sep)

        parts_len = len(parts)

        print("parts = {}".format(parts))

        # Fail on vaguely version-like strings e.g. 'pop3d'
        if parts[0] != '' and name_sep == '' \
        and len(parts[1]) > 1                \
        and parts[1][1] not in VERSIONY_CHARS:
            raise VersionParseError("not a version")

        #print("parts={}".format(parts))
        ## If we have parens, join all parts in the parens
        #join_idx_low = join_idx_high = None
        #for i, p in enumerate(parts):
        #    if len(p) == 0:
        #        continue
        #    if p[0] == '(':
        #        join_idx_low = i
        #    if p[-1] == ')':
        #        join_idx_high = i
        #if join_idx_low != None and join_idx_high != None \
        #   and join_idx_low < join_idx_high:
        #    to_join = parts[join_idx_low:join_idx_high+1]
        #    del parts[join_idx_low:join_idx_high+1]
        #    joined = name_sep.join(to_join)
        #    parts.insert(join_idx_low, joined)
        #print("parts={}".format(parts))

        # If > 2 parts and name_sep isn't space, we probably have
        # name_sep in the version string - rejoin it
        if parts_len > 2 and name_sep != ' ':
            parts[1] += name_sep + name_sep.join(parts[2:])
            del parts[2:]

        # This handles all the fucking weird cases
        if parts_len > 2 and name_sep == ' ':
            #if not any_digits_in_str(parts[1]):
            #    parts[0] += ' ' + ' '.join(parts[1:parts_len-1])
            #    parts[1] = parts[-1]
            #else:
            # Handle modem model names like LANCOM 1611+ heuristically
            if '.' not in parts[1] and '_' not in parts[1] \
                and '+' in parts[1]:
                tmp = parts.pop(1)
                parts_len -= 1
                parts[0] = parts[0] + ' ' + tmp
            # Now assume part with most versiony chars is the version.
            # Versiony char is a digit, period (most common), or _
            # Anything before is part of name and anything
            # after goes in extra_str
            max_vc_idx = most_versiony_chars_idx(parts)
            # Check it's not a date, annoyingly being longer than
            # our version string. If so exclude that and try again
            if any_digits_in_str(parts[max_vc_idx]) \
            and find_date(parts[max_vc_idx]):
                tmp = list(parts)
                tmp.pop(max_vc_idx)
                max_vc_idx = most_versiony_chars_idx(tmp)
            add_parts_first = parts[1:max_vc_idx]
            add_parts_last  = parts[max_vc_idx+1:]
            if len(add_parts_first) > 0:
                parts[0] += ' ' + ' '.join(add_parts_first)
            parts[1] = parts[max_vc_idx]
            if len(add_parts_last) > 0:
                v.extra_str = ' '.join(add_parts_last)
            del parts[2:]

        v.name_sep = name_sep

        # name, version string
        # Note: name can be the empty string here
        assert(len(parts) == 2)

        # If no letters in parts[0] here - we got a no_name version string
        # without caller setting no_name
        if not any_letters_in_str(parts[0]):
            cls.parse_version(name_sep.join(parts), version_obj=v)
            return v

        # OK, we have a legit name. We want no whitespace in the 
        # clean name, but save orig too
        v.name       = parts[0]
        v.name_clean = v.name.lower().replace(' ', '')
        version      = parts[1]     # don't store raw version string in obj

        print("version={}".format(version))

        # This is a good heuristic - remove everything
        # after first space, if present. Only applies if 
        # name_sep != ' ' because split would remove that
        i = version.find(' ')
        if i != -1:
            v.extra_str = version[i:]    # keep for round-trip str()
            version = version[:i]

        if version[-1] == ')':
            if not v.extra_str:
                v.extra_str = ''
            v.extra_str += ')'
            version = version[:-1]

        # Sometimes a date is tacked onto the end of the version string,
        # so check for that
        if v.extra_str and any_digits_in_str(v.extra_str):
            date_tuple = find_date(v.extra_str)
            if date_tuple:
                _, _, v.release_date = date_tuple
        
        # Check if something's wrong with no_name logic
        assert(v.name != '' and v.name_clean != '')

        cls.parse_version(version, version_obj=v)

        #print("... parse complete:")
        #print("name  = {}".format(v.name))
        #print("major = {}".format(v.major))
        #print("minor = {}".format(v.minor))
        #print("version_sep = '{}'".format(v.version_sep))
        #print("patch = {}".format(v.patch))
        #print("patch1 = {}".format(v.patch1))
        #print("patch2 = {}".format(v.patch2))
        #print("zero prefixes = {}".format(v.zero_prefixes))

        return v


    def __init__(self, *args, **kwargs):
        args     = list(args)
        args_len = len(args)
        proc_keywords = ['name', 'major', 'minor', 'patch', 'patch1', 'patch2',
            'patch_str', 'pre_release', 'build_meta',
            'epoch', 'release', 'post_release', 'dev_release',
            'release_date', 'eol_date', 'extra_str']

        # Init all attrs 
        for kw in proc_keywords:
            setattr(self, kw, None)
        self.name_clean = None

        self.zero_prefixes  = {
            'major': 0,
            'minor': 0,
            'patch': 0,
            'patch1': 0,
            'patch2': 0,
            'epoch': 0,
            'release': 0,
            'pre_release': 0,
            'post_release': 0,
            'dev_release': 0,
        }

        # These 3 used to move an annoyingly placed date string to 
        # a more convenient location
        self._ver_date_start = None
        self._ver_date_end   = None
        self._ver_date_str   = None
        # Special case of OpenSSH X.YpZ, NOT 'OpenSSH X.Y.pZ'
        self._openssh_moved_p = False
        # Perl format X.YY_ZZ
        self._perl_version_fmt    = False

        # A bogus timedelta (before the UNIX epoch) used to
        # allow comparison and sorting TODO bad bad bad
        # TODO even badder, what if object lives > 1 day?
        self._timedelta_epoch = self.date_class.today() \
                             - datetime.date(1970, 1, 1) \
                             + datetime.timedelta(1)

        if 'have_clue' in kwargs:
            self.have_clue = kwargs['have_clue']
            del kwargs['have_clue']
        else:
            self.have_clue = False

        # Common case: init with a string to be parsed
        if args_len == 1 and type(args[0]) in STR_TYPES:
            # have_clue True means only name, no version info
            if not self.have_clue:
                self.__class__.parse(args[0], version_obj=self)
                # And skip rest of init, parse() calls blank init
                return
            else:
                self.name = args.pop(0)
                args_len -= 1
                proc_keywords.remove('name')
        # Got name, and explicit init
        elif args_len > 1 and type(args[0]) in STR_TYPES:
            self.name = args.pop(0)
            args_len -= 1
            proc_keywords.remove('name')
            
        # Otherwise like datetime.date(), and Semver format
        self.major = self.minor = self.patch = None
        if args_len > 0:
            self.major = args[0]
            proc_keywords.remove('major')
        if args_len > 1:
            self.minor = args[1]
            proc_keywords.remove('minor')
        if args_len > 2:
            self.patch = args[2]
            proc_keywords.remove('patch')

        # Check weird positional args
        if args_len >= 4:
            raise VersionInitError(
                "Bad positional args for init: {}".format(args))

        # Now keywords
        for kw in proc_keywords:
            if kw in kwargs:
                setattr(self, kw, kwargs[kw])
                del kwargs[kw]

        if 'name_sep' in kwargs:
            self.name_sep = kwargs['name_sep']
            if self.name_sep is None:
                self.name_sep = ''      # prevent errors later
            del kwargs['name_sep']
        else:
            self.name_sep = ' '

        if 'version_sep' in kwargs:
            self.version_sep = kwargs['version_sep']
            if self.version_sep is None:
                raise VersionInitError(
                    "Passed version_sep=None. What exactly does that mean?")
            del kwargs['version_sep']
        else:
            self.version_sep = '.'

        if len(kwargs) > 0:
            raise VersionInitError(
                "Got unexpected kwargs: {}".format(kwargs))

        # Other init checks and setup

        if self.name != None and \
           (self.major == None and self.release == None) \
           and not self.have_clue:
            raise VersionInitError("Passed name to version init(), but " +
                "no version numbers/wildcards. This is probably wrong. " +
                "Pass have_clue=True if you really want to do this.")

        if self.name is not None:
            self.name_clean = self.name.lower().replace(' ', '')

        if self.major is not None and self.major not in WILDCARDS:
            if type(self.major) in STR_TYPES: 
                self.major = int(self.major)
            if type(self.major) is not int:
                raise VersionInitError(
                    "Argument 'major' must be int or string (major={})".format(
                        major))
            if self.major < 0:
                raise VersionInitError(
                    "Can't have negative number in version (major={})".format(
                        major))

        if self.minor is not None and self.version_sep is None:
            raise VersionInitError("Passed minor=(not None) and version_sep=None, that's a bit silly")
        if self.minor is not None and self.minor not in WILDCARDS:
            if type(self.minor) in STR_TYPES:
                self.minor = int(self.minor)
            if type(self.minor) is not int:
                raise VersionInitError(
                    "Argument 'minor' must be string or int or None " + \
                    "type={}".format(type(self.minor)))
            if self.minor < 0:
                raise VersionInitError(
                    "Can't have negative number in version (minor={})".format(
                        minor))

        if self.patch is not None:
            self.__class__.parse_patch(self.patch, self)


    def __eq__(self, other):
        if type(other) is not self.__class__:
            return False
        if [self.major, other.major] == [None, None]:
            raise Exception("shouldn't happen")
        if self.name != other.name:
            return False
        # Ensure 'not set' compares equal to 0
        self_val  = 0 if self.major  is None else self.major
        other_val = 0 if other.major is None else other.major
        if self_val != other_val and       \
           not (self.major in WILDCARDS or \
                other.major in WILDCARDS):
            return False
        # A wildcard in self.major matches all versions of other,
        # and vice versa
        if self.major in WILDCARDS or other.major in WILDCARDS:
            return True
        # Ditto 
        self_val  = 0 if self.minor  is None else self.minor
        other_val = 0 if other.minor is None else other.minor
        if self_val != other_val and       \
           not (self.minor in WILDCARDS or \
                other.minor in WILDCARDS):
            return False
        if self.minor in WILDCARDS or other.major in WILDCARDS:
            return True

        # Must compare patch components too
        if self.patch == other.patch:
            return True

        if self.patch in WILDCARDS or other.patch in WILDCARDS:
            return True

        # patch1
        self_val  = 0 if self.patch1  is None else self.patch1
        other_val = 0 if other.patch1 is None else other.patch1
        if self_val != other_val and        \
           not (self.patch1 in WILDCARDS or \
            other.patch1 in WILDCARDS):
            return False

        # patch_str
        if self.patch_str != other.patch_str:
            return False

        # patch2
        self_val  = 0 if self.patch2  is None else self.patch2
        other_val = 0 if other.patch2 is None else other.patch2
        if self_val != other_val and        \
           not (self.patch2 in WILDCARDS or \
            other.patch2 in WILDCARDS):
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if [self.major, other.major] == [None, None]:
            raise Exception("shouldn't happen")
        if self.name != other.name:
            raise VersionNotComparableError(
                "Tried to compare versions for different packages: " \
              + "('{}' / '{}') - that doesn't make sense.".format(
                  self.name, other.name)
            )
        if self.__eq__(other):
            return False
        if self.major is None and other.major is not None:
            return True
        if self.major is not None and other.major is None:
            return False
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        if self.minor is None and other.minor is not None:
            return True
        if self.minor is not None and other.minor is None:
            return False
        if [self.minor, other.minor] != [None, None]:
            if self.minor < other.minor:
                return True
            if self.minor > other.minor:
                return False

        # Patch 
        if self.patch1 == None and other.patch1 != None:
            return True
        if self.patch1 != None and other.patch1 == None:
            return False
        if self.patch1 != None and other.patch1 != None:
            if self.patch1 < other.patch1:
                return True
            if self.patch1 > other.patch1:
                return False

        # 2.6.10-rc1 < 2.6.10   (but careful about 3.0.65.1)
        if self.patch_str != self.version_sep and \
           other.patch_str != other.version_sep:
            if self.patch_str != None and other.patch_str == None:
                return True
            if self.patch_str == None and other.patch_str != None:
                return False
        
        # 3.0.65 < 3.0.65.1
        if self.patch2 == None and other.patch2 != None:
            return True
        if self.patch2 != None and other.patch2 == None:
            return False
        if self.patch2 != None and other.patch2 != None:
            if self.patch2 < other.patch2:
                return True
            if self.patch2 > other.patch2:
                return False
        raise Exception("can't happen")     # TODO debug only
        return False

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    
    # TODO override assign to .patch to parse
    # need this because we rely on .patch being sane for sorting

    
    def get_version_str(self):
        s = ''
        if self.major is not None:
            s += "{}{}".format(
                '0' * self.zero_prefixes['major'],
                self.major)
        if self.minor is not None:
            s += "{}{}{}".format(
                self.version_sep, 
                '0' * self.zero_prefixes['minor'],
                self.minor)
        if self.patch is not None:
            vs = self.version_sep
            if type(self.patch) in STR_TYPES and self.patch[0] in '-_':
                vs = ''
            # Distinguish OpenSSH 4.2p1, 4.2.p1 (both used)
            if self.name_clean == 'openssh' and self.patch_str == 'p':
                if self._openssh_moved_p:
                    vs = 'p'
                else:
                    vs = '.'
            if self.patch_str and self.patch_str.lower() in ['alpha', 'beta']:
                vs = ''
            # Handle perl version
            if self._perl_version_fmt:
                vs = '_'
            s += "{}{}{}".format(
                vs, 
                '0' * self.zero_prefixes['patch'],
                self.patch)
        if self._ver_date_str is not None:
            s = s[:self._ver_date_start] + \
                self._ver_date_str + \
                s[self._ver_date_start:]
        return s


    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return '<Version {} ({})>'.format(id(self), self.__unicode__())

    # For wildcards
    def __contains__(self, item):
        # convert to range then use in VersionRange
        pass        # TODO

    # TODO released_before, released_after 


    def age(self):
        """Return a timedelta representing the age. If release_date is None,
           age will be more than number of days since the epoch (1970-1-1)."""
        if self.release_date is None:
            return self._timedelta_epoch 
        if type(self.release_date) is not datetime.date:
            raise TypeError(".age() called but release_date is not a datetime.date")
        return self.date_class.today() - self.release_date

    def age_human(self):
        if self.release_date is None:
            return 'none'
        return timedelta_to_human(self.age())

    # TODO let compare_to be a timedelta
    def is_older_than(self, compare_to):
        if self.release_date is None:
            raise RuntimeError("called is_older_than() when self.release_date is not set")
        if type(compare_to) is Version:
            if compare_to.release_date is None:
                raise RuntimeError("called is_older_than() when compare_to.release_date is not set")
            return self.release_date < compare_to.release_date
        if type(compare_to) is datetime.date:
            return self.release_date < compare_to
        if type(compare_to) in STR_TYPES: 
            return self.age() > human_to_timedelta(compare_to)
        raise TypeError("bad type for compare_to() arg")

    def is_newer_than(self, compare_to):
        if self.release_date is None:
            raise RuntimeError("called is_newer_than() when self.release_date is not set")
        if type(compare_to) is Version:
            if compare_to.release_date is None:
                raise RuntimeError("called is_newer_than() when compare_to.release_date is not set")
            return self.release_date > compare_to.release_date
        if type(compare_to) is datetime.date:
            return self.release_date > compare_to
        if type(compare_to) in STR_TYPES: 
            return self.age() < human_to_timedelta(compare_to)
        raise TypeError("bad type for compare_to() arg")

# TODO is_semver / is_pep440 etc
# TODO convert_to_semver etc


####
#### VersionRange class
####

class VersionRange(object):
    def __init__(self, *args, **kwargs):
        self.start = None
        self.end   = None

        # Allow empty
        if len(args) == 0 and kwargs == {}:
            return

        if len(args) != 0 and len(args) != 2:
            raise VersionInitError(
                "Bad positional args for VersionRange init: {}".format(args))
        if len(args) == 2:
            if kwargs == {}:
                self.start = args[0]
                self.end   = args[1]
            else:
                raise VersionInitError(
                    "Passed both args and kwargs to VersionRange init")

        if kwargs != {}:
            self.start = kwargs.get('start')
            self.end   = kwargs.get('end')
            if self.start is None or self.end is None:
                raise VersionInitError(
                    "Didn't pass both start and end as kwargs")

        if [type(self.start), type(self.end)] != [Version, Version]:
            raise VersionInitError("Args must be Version objects")


    def __contains__(self, item):
        if item >= self.start and item <= self.end:
            return True
        return False

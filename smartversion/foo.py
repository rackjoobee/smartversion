
def test_usage():
    l = []
    for i in range(20):
        l.append(Version(i, i))
    for i in range(20):
        assert(l[i] == Version(i, i))

    v1 = Version(0)
    v2 = Version(0)
    assert(v1 == v2)
    assert(hash(v1) == hash(v2))
    
    v1 = Version(1, 2, '3-rc6')
    v2 = Version(1, 2, 4)
    assert(v1 != v2)
    assert(hash(v1) != hash(v2))

    v2 = Version(1, 2, '3-rc6')
    assert(v1 == v2)
    assert(hash(v1) == hash(v2))

    d = {}
    for i in range(20):
        v = Version(i, i, i)
        d[v] = i
    for i in range(20):
        v = Version(i, i, i)
        assert(d[v] == i)

    v1 = Version(0, 1, 2)
    v2 = Version(0, 1, 3)
    s = set([v1, v2])
    assert(len(s) == 2)

    v2 = Version(0, 1, 2)
    s = set([v1, v2])
    assert(len(s) == 1)


def test_compare():
    compare = lambda l: l[0] == l[1]

    # TODO check both semver and pep404 comparisons (and interactions)
    # TODO check semantics where default is wrong

    # Equalities
    v1 = Version(major=0)
    v2 = Version()          # Implied 0
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1)
    v2 = Version('foo', 1)
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1)
    v2 = Version('foo', 1, 0)
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 1)
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 1, 0)
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, 1)
    v2 = Version('foo', 1, 1, 1)
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, '1')
    v2 = Version('foo', 1, 1, '1')
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, '1rc')
    v2 = Version('foo', 1, 1, '1rc')
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 1, '1rc1')
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, 'rc1')
    v2 = Version('foo', 1, 1, 'rc1')
    assert(v1 == v2)
    assert(v2 == v1)

    v1 = Version('foo', 1, 1, 'rc')
    v2 = Version('foo', 1, 1, 'rc')
    assert(v1 == v2)
    assert(v2 == v1)

    # extra_str shouldn't affect comparison
    v1 = Version('foo', 1, extra_str = 'asd')
    v2 = Version('foo', 1, extra_str = 'lkj')
    assert(v1 == v2)
    assert(v2 == v1)

    # nor release_date
    v1 = Version('foo', 1, release_date = date(2000, 1, 1))
    v2 = Version('foo', 1, release_date = date(2000, 1, 2))
    assert(v1 == v2)
    assert(v2 == v1)

    # nor build_meta
    v1 = Version('foo', 1, build_meta = 'lkasdjf')
    v2 = Version('foo', 1, build_meta = ';KFJDAa')
    assert(v1 == v2)
    assert(v2 == v1)

    # Inequalities
    v1 = Version(major=0)
    v2 = Version(major=1)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version(major=0, minor=0)
    v2 = Version(major=0, minor=1)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version(major=0, minor=0, patch=0)
    v2 = Version(major=0, minor=0, patch=1)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', have_clue=True)
    v2 = Version('bar', have_clue=True)
    #assert(v1 != v2)
    #assert(v2 != v1)

    v1 = Version('foo', 1)
    v2 = Version('foo', 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 1)
    v2 = Version('foo', 1, 1, 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, '1test')
    v2 = Version('foo', 1, 1, '1frob')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, '1test5')
    v2 = Version('foo', 1, 1, '1test6')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 'test5')
    v2 = Version('foo', 1, 1, 'test6')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 'test')
    v2 = Version('foo', 1, 1, 'frob')
    assert(v1 != v2)
    assert(v2 != v1)

    # Ordering
    v1 = Version(major=0)
    v2 = Version(major=1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1)
    v2 = Version('foo', 2)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, None)
    v2 = Version('foo', 1, 1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 2)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 2)
    v2 = Version('foo', 2, 1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, 1)
    v2 = Version('foo', 1, 1, 2)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, 2)
    v2 = Version('foo', 1, 2, 1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 2, 1)
    v2 = Version('foo', 2, 1, 1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, 'rc0')
    v2 = Version('foo', 1, 1, 'rc1')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, '1-rc1')
    v2 = Version('foo', 1, 1, 1)
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, 'rc0')
    v2 = Version('foo', 1, 1, '1rc0')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, '1rc0')
    v2 = Version('foo', 1, 1, '1rc1')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 1, '2rc0')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 2, '1rc1')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 2, '1rc1')
    v2 = Version('foo', 2, 1, '1rc1')
    assert(v1 < v2)
    assert(v2 > v1)

    v1 = Version('foo', 1, 1, 'rc1')
    v2 = Version('foo', 1, 1)
    assert(v1 < v2)
    assert(v2 > v1)


def test_compare_typical():

    # Normal usage
    v1 = Version.parse('linux-2.4.6')
    v2 = Version.parse('linux-2.4.8')
    v3 = Version.parse('linux-2.4.10-rc1')      # rc < version proper
    v4 = Version.parse('linux-2.4.10')
    v5 = Version.parse('linux-2.6.27.10')
    v6 = Version.parse('linux-2.6.27.11')
    v7 = Version.parse('linux-3.0')
    v8 = Version.parse('linux-3.0.1')
    v9 = Version.parse('linux-3.0.65')
    v10 = Version.parse('linux-3.0.65.1')
    v11 = Version.parse('linux-4.x')
    v12 = Version.parse('linux-5.X')

    assert(v1 < v2)
    assert(v2 > v1)
    assert(v1 != v2)
    assert(v2 != v1)

    # Make sure rc compare ABOVE lower version without patch_str
    assert(v2 < v3)
    assert(v3 > v2)
    assert(v2 != v3)
    assert(v3 != v2)

    assert(v3 < v4)
    assert(v4 > v3)
    assert(v3 != v4)
    assert(v4 != v3)

    assert(v4 < v5)
    assert(v5 > v4)
    assert(v4 != v5)
    assert(v5 != v4)

    assert(v5 < v6)
    assert(v6 > v5)
    assert(v5 != v6)
    assert(v6 != v5)

    assert(v6 < v7)
    assert(v7 > v6)
    assert(v6 != v7)
    assert(v7 != v6)

    assert(v7 < v8)
    assert(v8 > v7)
    assert(v7 != v8)
    assert(v8 != v7)

    assert(v8 < v9)
    assert(v9 > v8)
    assert(v8 != v9)
    assert(v9 != v8)

    assert(v9 < v10)
    assert(v10 > v9)
    assert(v9 != v10)
    assert(v10 != v9)
    
    assert(v10 < v11)
    assert(v11 > v10)
    assert(v10 != v11)
    assert(v11 != v10)

    assert(v11 < v12)
    assert(v12 > v11)
    assert(v11 != v12)
    assert(v12 != v11)

    l = sorted([v12, v11, v10, v9, v8, v7, v6, v5, v4, v3, v2, v1])
    for i in range(10):
        assert(l[0] == v1)
        assert(l[1] == v2)
        assert(l[2] == v3)
        assert(l[3] == v4)
        assert(l[4] == v5)
        assert(l[5] == v6)
        assert(l[6] == v7)
        assert(l[7] == v8)
        assert(l[8] == v9)
        assert(l[9] == v10)
        assert(l[10] == v11)
        assert(l[11] == v12)
        random.shuffle(l)
        l.sort()

    # TODO compare for
    # 1.71 (decimal) < 1.8


def test_wildcards():
    for char in ['x', 'X', '*']:
        # Equality
        v1 = Version(major=char)
        v2 = Version(major=1)
        assert(v1 == v2)
        assert(v2 == v1)

        # wildcard implies wildcard for any lesser fields
        v1 = Version(major=char)
        v2 = Version(major=1, minor=1)
        assert(v1 == v2)
        assert(v2 == v1)

        v2 = Version(major=1, minor=1, patch='1.1')
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=char, minor=char)
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=char)
        v2 = Version(major=0, minor=0)
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=0, patch=char)
        v2 = Version(major=0, minor=0, patch=0)
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=char, patch=0)
        v2 = Version(major=0, minor=9, patch=0)
        assert(v1 == v2)
        assert(v2 == v1)

        v2 = Version(major=0, minor=1, patch=0)
        assert(v1 == v2)
        assert(v2 == v1)

        v2 = Version(major=0, minor=char, patch=0)
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=0, patch=char)
        v2 = Version(major=0, minor=0, patch='1.5')
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=0, patch='1.'+char)
        v2 = Version(major=0, minor=0, patch='1.5')
        assert(v1 == v2)
        assert(v2 == v1)

        v1 = Version(major=0, minor=0, patch=char+'.5')
        v2 = Version(major=0, minor=0, patch='1.5')
        assert(v1 == v2)
        assert(v2 == v1)

        # Inequality
        v1 = Version(major=0, minor=char)
        v2 = Version(major=1, minor=1)
        assert(v1 != v2)
        assert(v2 != v1)

        v1 = Version(major=0, minor=0, patch=char)
        v2 = Version(major=0, minor=1, patch=char)
        assert(v1 != v2)
        assert(v2 != v1)

        v1 = Version(major=0, minor=0, patch='1.'+char)
        v2 = Version(major=0, minor=0, patch='2.5')
        assert(v1 != v2)
        assert(v2 != v1)

        v1 = Version(major=0, minor=0, patch=char+'.4')
        v2 = Version(major=0, minor=0, patch='1.5')
        assert(v1 != v2)
        assert(v2 != v1)

        # TODO a few more edge cases


def test_methods():
    class MyDate(date):
        @staticmethod
        def today():
            return date(2000, 2, 1)
    Version.date_class = MyDate

    #### .age()
    v1 = Version('foo', 1, 0, release_date=date(2000, 1, 1))
    assert(v1.age() == timedelta(31))
    assert(v1.age_human() == '1 month, 1 day')

    v2 = Version('foo', 1, 0, release_date=date(2000, 2, 1))
    assert(v2.age() == timedelta(0))
    assert(v2.age_human() == '0 days')

    v3 = Version('foo', 1, 0)
    assert(v3.age() > timedelta(10988))
    assert(v3.age_human() == 'none')

    v4 = Version('foo', 1, 0, release_date=date(1970, 1, 1)) 
    assert(v4.age() == timedelta(10988)) 
    assert(v4.age_human() == '30 years, 1 month, 8 days')

    #dup
    v5 = Version('foo', 1, 0, release_date=date(2000, 1, 1))
    assert(v5.age_human() == '1 month, 1 day')

    l = sorted([v2, v1, v5, v4, v3], key=lambda x: x.age())
    assert(l[0] == v2)
    assert(l[1] == v1)
    assert(l[2] == v5)
    assert(l[3] == v4)
    assert(l[4] == v3)

    v1 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    assert(v1.is_older_than('1m'))
    assert(v1.is_older_than('12m4d'))
    assert(v1.is_older_than('1y') is False)
    assert(v1.is_newer_than('2y'))
    assert(v1.is_newer_than('1y1d'))
    assert(v1.is_newer_than('1y') is False)
    assert(v1.is_newer_than('12m4d') is False)

    v1 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    v2 = Version('foo', 1, 1, release_date=date(1999, 3, 1))
    assert(v2.is_newer_than(v1))
    assert(v1.is_older_than(v2))

    assert(v1.is_older_than(date(1999, 2, 2)))
    assert(v1.is_older_than(date(1999, 2, 1)) is False)
    assert(v1.is_newer_than(date(1998, 2, 2)))
    assert(v1.is_newer_than(date(1999, 2, 1)) is False)

    v1 = Version('foo', 1, 1, release_date=date(2000, 2, 1))
    assert(v1.is_older_than('0d') is False)

    v1.release_date = date(2000, 1, 31)
    assert(v1.is_older_than('0d'))
    assert(v1.is_newer_than('1d') is False)
    assert(v1.is_older_than('1d') is False)
    assert(v1.is_newer_than('1d') is False)

    v1.release_date = date(2000, 1, 1)
    assert(v1.is_older_than('1m'))
    assert(v1.is_older_than('30d'))
    assert(v1.is_older_than('31d') is False)
    assert(v1.is_newer_than('32d'))
    assert(v1.is_newer_than('31d') is False)

    v1.release_date = date(1999, 2, 1)
    v2 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    assert(v1.is_older_than(v2) is False)
    assert(v1.is_newer_than(v2) is False)
    assert(v2.is_older_than(v1) is False)
    assert(v2.is_newer_than(v1) is False)

    v2.release_date = date(1999, 2, 2)
    assert(v1.is_older_than(v2))
    assert(v2.is_older_than(v1) is False)
    assert(v2.is_newer_than(v1))
    assert(v1.is_newer_than(v2) is False)

    v1 = Version('foo', 1, 1, release_date=date(1990, 2, 1))
    assert(v1.is_older_than('10y2d') is False)
    assert(v1.is_newer_than('10y2d') is False)
    assert(v1.is_newer_than('10y3d'))
    assert(v1.is_older_than('10y1d'))


def test_parse_version():
    pass    # TODO


def test_version_range():
    # Check Version.parse() handles ranges - should it? TODO
    
    v1 = Version(0, 1, 2)
    v2 = Version(0, 1, 8)

    # Empty
    vr = VersionRange()

    # Bad positional
    assert_raises(VersionInitError, VersionRange, v1)

    # Bad KW
    assert_raises(VersionInitError, VersionRange, {'start': v1})
    assert_raises(VersionInitError, VersionRange, {'end': v1})

    # Positional
    vr = VersionRange(v1, v2)
    assert(type(vr.start) is Version)
    assert(type(vr.end)   is Version)
    assert(vr.start == v1)
    assert(vr.end   == v2)

    # Kw
    vr = VersionRange(start=v1, end=v2)
    assert(type(vr.start) is Version)
    assert(type(vr.end)   is Version)
    assert(vr.start == v1)
    assert(vr.end   == v2)

    # Contains
    v1 = Version(1)
    v2 = Version(7)
    vr = VersionRange(v1, v2)
    assert(Version(0) not in vr)
    assert(Version(0, 9) not in vr)
    assert(Version(0, 9, 99) not in vr)
    assert(Version(1) in vr)
    assert(Version(1, 0) in vr)
    assert(Version(1, 0, 0) in vr)
    assert(Version(1, 0, 1) in vr)
    assert(Version(1, 1, 0) in vr)
    assert(Version(2) in vr)
    assert(Version(6) in vr)
    assert(Version(6, 9) in vr)
    assert(Version(6, 99, 999) in vr)
    assert(Version(7) in vr)
    assert(Version(7, 0) in vr)
    assert(Version(7, 0, 0) in vr)
    assert(Version(7, 0, 1) not in vr)
    assert(Version(7, 1, 0) not in vr)
    assert(Version(8) not in vr)

    v1 = Version(0, 1, 2)
    v2 = Version(0, 1, 8)
    vr = VersionRange(v1, v2)
    assert(Version(0) not in vr)
    assert(Version(0, 1) not in vr)
    assert(Version(0, 1, 1) not in vr)
    assert(Version(0, 1, 2) in vr)
    assert(Version(0, 1, 3) in vr)
    assert(Version(0, 1, 7) in vr)       # TODO fractional semantics
    assert(Version(0, 1, 8) in vr)
    assert(Version(0, 1, 9) not in vr)
    assert(Version(0, 2) not in vr)
    assert(Version(1) not in vr)

    v1 = Version(1, 345)
    v2 = Version(1, 456)
    vr = VersionRange(v1, v2)
    assert(Version(0) not in vr)
    assert(Version(1) not in vr)
    assert(Version(1, 0) not in vr)
    assert(Version(1, 111) not in vr)
    assert(Version(1, 344) not in vr)
    assert(Version(1, 344, 0) not in vr)
    assert(Version(1, 344, 1) not in vr)
    assert(Version(1, 345) in vr)
    assert(Version(1, 345, 0) in vr)
    assert(Version(1, 345, 1) in vr)
    assert(Version(1, 346) in vr)
    assert(Version(1, 400) in vr)
    assert(Version(1, 455) in vr)
    assert(Version(1, 456) in vr)
    assert(Version(1, 456, 0) in vr)
    assert(Version(1, 456, 1) not in vr)
    assert(Version(1, 457) not in vr)
    assert(Version(1, 457, 0) not in vr)
    assert(Version(1, 99999) not in vr)
    assert(Version(2) not in vr)

    # TODO epoch, prerelease, beta etc
    # TODO esp rc/alpha/beta edge cases

    # TODO few parse here too



def test_parse():
    # TODO SVN/cvs/rcs version numbers?

    ####
    #### In-the-wild / generally semver-compatible tests
    ####

    assert_raises(VersionParseError, Version.parse, '')

    s = 'OpenSSH'
    assert_raises(VersionParseError, Version.parse, s)

    s = 'OpenSSH 4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'OpenSSH')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH_4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == '_')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH-4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH_4.3'
    v = Version.parse(s)
    assert(type(v.name_clean) in STR_TYPES)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is int)
    assert(v.minor    == 3)
    assert(v.patch    is None)
    assert(v.patch_str is None)
    assert(v.name_sep == '_')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH_4.3'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.name_clean) in STR_TYPES)
    assert(v.major    == 4)
    assert(type(v.major) is int)
    assert(v.minor    == 3)
    assert(type(v.minor) is int)
    assert(v.patch     is None)
    assert(v.patch_str == None)
    assert(v.name_sep == '_')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH-4.3'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    == 3)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'Cisco-1.25'
    v = Version.parse(s)
    assert(v.name_clean == 'cisco')
    assert(v.name     == 'Cisco')
    assert(v.major    == 1)
    assert(v.minor    == 25)
    assert(type(v.minor) is int)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH_6.2'
    v = Version.parse(s)
    assert(type(v.name_clean) in STR_TYPES)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 6)
    assert(type(v.minor) is int)
    assert(v.minor    == 2)
    assert(str(v) == s) 

    s = 'OpenSSH_6.2p5'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 6)
    assert(v.minor    == 2)
    assert(type(v.patch) is int)
    assert(v.patch    == 5)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 5)
    assert(v.patch_str == 'p')
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'OpenSSH_5.5p1 Debian-6+squeeze2'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 5)
    assert(v.minor    == 5)
    assert(v.patch    == 1)
    assert(v.patch_str == 'p')
    assert(str(v) == s) 

    s = 'OpenSSH_4.3-HipServ'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    == 3)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '-HipServ')
    assert(str(v) == s) 

    #s = ''
    #v = Version.parse(s)
    #assert(str(v) == s)


    # Perl format

    s = 'Quux 1.12_15'
    v = Version.parse(s)
    assert(v._perl_version_fmt)
    assert(v.name_clean == 'quux')
    assert(v.name     == 'Quux')
    assert(type(v.major) is int)
    assert(v.major    == 1)
    assert(type(v.minor) is int)
    assert(v.minor    == 12)
    assert(type(v.patch) is int)
    assert(v.patch    == 15)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 15)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s)

    s = 'Quux 1.12_15_99'
    v = Version.parse(s)
    assert(v._perl_version_fmt)
    assert(v.name_clean == 'quux')
    assert(v.name     == 'Quux')
    assert(type(v.major) is int)
    assert(v.major    == 1)
    assert(type(v.minor) is int)
    assert(v.minor    == 12)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '15_99')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 15)
    assert(type(v.patch2) is int)
    assert(v.patch2   == 99)
    assert(v.patch_str == '_')
    assert(str(v) == s)

    s = 'Quux 1_12_15'
    v = Version.parse(s)
    assert(v._perl_version_fmt)
    assert(v.name_clean == 'quux')
    assert(v.name     == 'Quux')
    assert(v.major    == 1)
    assert(v.minor    == 12)
    assert(v.patch    == 15)
    assert(v.patch1   == 15)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(v.version_sep == '_')
    assert(str(v) == s)

    s = 'Quux_1_12_15'
    v = Version.parse(s)
    assert(v._perl_version_fmt)
    assert(v.name_clean == 'quux')
    assert(v.name     == 'Quux')
    assert(v.major    == 1)
    assert(v.minor    == 12)
    assert(v.patch    == 15)
    assert(v.patch1   == 15)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(v.version_sep == '_')
    assert(v.name_sep    == '_')
    assert(str(v) == s)


    # Whitespace cleanups

    s = 'openssh\t1.2.2p1'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'openssh')
    assert(v.major    == 1)
    assert(v.minor    == 2)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '2p1')
    assert(v.patch1   == 2)
    assert(v.patch2   == 1)
    assert(v.patch_str == 'p')
    assert(str(v) == 'openssh 1.2.2p1')

    s = '\t openssh  1.2.1pre18  \t'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'openssh')
    assert(v.major    == 1)
    assert(v.minor    == 2)
    assert(v.patch    == '1pre18')
    assert(v.patch1   == 1)
    assert(v.patch2   == 18)
    assert(v.patch_str == 'pre')
    assert(str(v) == 'openssh 1.2.1pre18')

    # ...

    s = 'openssh 4.2.p1'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    == 2)
    assert(not v._openssh_moved_p)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == 'p1')
    assert(v.patch1   is None)
    assert(type(v.patch2) is int)
    assert(v.patch2   == 1)
    assert(type(v.patch_str) in STR_TYPES)
    assert(v.patch_str == 'p')
    assert(str(v) == s)

    s = 'ARRIS_0.44_01'
    v = Version.parse(s)
    assert(v.name_clean == 'arris')
    assert(v.major    == 0)
    assert(v.minor    == 44)
    assert(v.zero_prefixes['patch'] == 1)
    assert(type(v.patch) is int)
    assert(v.patch    == 1)
    assert(v.zero_prefixes['patch1'] == 1)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 1)
    assert(v._perl_version_fmt)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'ProFTPD1.3.3'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(v.patch    == 3)
    assert(v.patch1   == 3)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'linux-3.0.77'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.name     == 'linux')
    assert(v.major    == 3)
    assert(v.minor    == 0)
    assert(type(v.patch) is int)
    assert(v.patch    == 77)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 77)
    assert(str(v) == s) 

    s = 'linux-2.6.27.10'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '27.10')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 27)
    assert(v.patch2   == 10)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 5.5p1 Debian 6+squeeze4 (protocol 2.0)'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'OpenSSH')
    assert(v.major    == 5)
    assert(v.minor    == 5)
    assert(v.patch    == 1)
    assert(v.patch1   == 1)
    assert(v.patch2   is None)
    assert(v.patch_str == 'p')
    assert(str(v) == s) 

    s = 'lighttpd 1.4.23'
    v = Version.parse(s)
    assert(v.name_clean == 'lighttpd')
    assert(v.major    == 1)
    assert(v.minor    == 4)
    assert(type(v.patch) is int)
    assert(v.patch    == 23)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 23)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'ProFTPD 1.3.3a'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '3a')
    assert(v.patch1   == 3)
    assert(type(v.patch1) is int)
    assert(v.patch_str == 'a')
    assert(str(v) == s) 

    s = 'BetaFTPD 0.0.8pre17'
    v = Version.parse(s)
    assert(v.name_clean == 'betaftpd')
    assert(v.major    == 0)
    assert(v.minor    == 0)
    assert(v.patch    == '8pre17')
    assert(v.patch1   == 8)
    assert(v.patch2   == 17)
    assert(v.patch_str == 'pre')
    assert(str(v) == s) 

    s = 'linux-2.6.0-rc1'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(v.patch    == '0-rc1')
    assert(v.patch1   == 0)
    assert(v.patch2   == 1)
    assert(v.patch_str == '-rc')
    assert(str(v) == s) 

    s = 'linux-2.6.0-test4'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '0-test4')
    assert(v.patch1   == 0)
    assert(v.patch2   == 4)
    assert(v.patch_str == '-test')
    assert(str(v) == s) 

    s = 'Gene6 FTP Server v3.10.0'
    v = Version.parse(s)
    assert(v.name_clean == 'gene6ftpserver')
    assert(v.name     == 'Gene6 FTP Server')
    assert(v.major    == 3)
    assert(v.minor    == 10)
    assert(v.patch    == 0)
    assert(v.patch1   == 0)
    assert(v.patch2 is None)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'IdeaWebServer httpd v0.70'
    v = Version.parse(s)
    assert(v.name_clean == 'ideawebserverhttpd')
    assert(v.name     == 'IdeaWebServer httpd')
    assert(v.major    == 0)
    assert(v.minor    == 70)
    assert(v.patch is None)
    assert(str(v) == s) 

    s = 'Multicraft 1.8.2 FTP server'
    v = Version.parse(s)
    assert(v.name_clean == 'multicraft')
    assert(v.major    == 1)
    assert(v.minor    == 8)
    assert(v.patch    == 2)
    assert(v.patch1   == 2)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'ProFTPD 1.3.3g Server'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.name     == 'ProFTPD')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(v.patch    == '3g')
    assert(v.patch1   == 3)
    assert(v.patch_str == 'g')
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Loxone FTP 5.66.4.23'
    v = Version.parse(s)
    assert(v.name_clean == 'loxoneftp')
    assert(v.name     == 'Loxone FTP')
    assert(v.major    == 5)
    assert(v.minor    == 66)
    assert(v.patch    == '4.23')
    assert(v.patch1   == 4)
    assert(v.patch2   == 23)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Exim smtpd 4.X'
    v = Version.parse(s)
    assert(v.name_clean == 'eximsmtpd')
    assert(v.name     == 'Exim smtpd')
    assert(v.major    == 4)
    assert(v.minor    == 'X')
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'MikroTik router ftpd 5.7'
    v = Version.parse(s)
    assert(v.name_clean == 'mikrotikrouterftpd')
    assert(v.name     == 'MikroTik router ftpd')
    assert(v.major    == 5)
    assert(v.minor    == 7)
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'Dropbear sshd 0.51'        # TODO
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'RapidLogic httpd 1.1'      # TODO
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'MySQL 5.0.91-log'
    v = Version.parse(s)
    assert(v.name_clean == 'mysql')
    assert(v.major    == 5)
    assert(v.minor    == 0)
    assert(v.patch    == '91-log')
    assert(v.patch1   == 91)
    assert(v.patch_str == '-log')
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Foowizard 12.1.99900.0'
    v = Version.parse(s)
    assert(v.name_clean == 'foowizard')
    assert(v.major    == 12)
    assert(v.minor    == 1)
    assert(v.patch    == '99900.0')
    assert(v.patch1   == 99900)
    assert(v.patch2   == 0)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Task Manager Pro 2.0245'
    v = Version.parse(s)
    assert(v.name_clean == 'taskmanagerpro')
    assert(v.name     == 'Task Manager Pro')
    assert(v.major    == 2)
    assert(v.minor    == 245)
    assert(v.patch    is None)
    assert(v.zero_prefixes['minor'] == 1)
    assert(str(v) == s) 

    s = 'Internet Download Helper 8.22.0.1234'
    v = Version.parse(s)
    assert(v.name_clean == 'internetdownloadhelper')
    assert(v.major    == 8)
    assert(v.minor    == 22)
    assert(v.patch    == '0.1234')
    assert(v.patch1   == 0)
    assert(v.patch2   == 1234)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Apache/2'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.major    == 2)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Linux/2.x'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 'x')
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'PHP/5.2.9-1'
    v = Version.parse(s)
    assert(v.name_clean == 'php')
    assert(v.major    == 5)
    assert(v.minor    == 2)
    assert(v.patch    == '9-1')
    assert(v.patch1   == 9)
    assert(v.patch2   == 1)
    assert(v.patch_str == '-')
    assert(str(v) == s) 

    s = 'lighttpd/1.4.28-devel-4979'
    v = Version.parse(s)
    assert(v.name_clean == 'lighttpd')
    assert(v.major    == 1)
    assert(v.minor    == 4)
    assert(v.patch    == '28-devel-4979')
    assert(v.patch1   == 28)
    assert(v.patch2   == 4979)
    assert(v.patch_str == '-devel-')
    assert(str(v) == s) 

    s = 'Apache/2.2.18'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.name     == 'Apache')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == 18)
    assert(v.patch1   == 18)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Apache/2_2_18'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.name     == 'Apache')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(type(v.patch) is int)
    assert(v.patch    == 18)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 18)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'Microsoft-IIS/6.0'
    v = Version.parse(s)
    assert(v.name_clean == 'microsoft-iis')
    assert(v.name     == 'Microsoft-IIS')
    assert(v.major    == 6)
    assert(v.minor    == 0)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Virata-EmWeb/R6_0_1'
    v = Version.parse(s)
    assert(v.name_clean == 'virata-emweb')
    assert(v.major    == 6)
    assert(v.minor    == 0)
    assert(type(v.patch) is int)
    assert(v.patch    == 1)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 1)
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'IdeaWebServer/v0.80'
    v = Version.parse(s)
    assert(v.name_clean == 'ideawebserver')
    assert(v.name     == 'IdeaWebServer')
    assert(v.major    == 0)
    assert(v.minor    == 80)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'mod_ssl/2.2.18'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_ssl')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == 18)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'Gemtek/0.899'
    v = Version.parse(s)
    assert(v.name_clean == 'gemtek')
    assert(v.major    == 0)
    assert(v.minor    == 899)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'OpenSSL/1.0.0-fips'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 1)
    assert(v.minor    == 0)
    assert(v.patch    == '0-fips')
    assert(v.patch1   == 0)
    assert(v.patch_str == '-fips')
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'KM-MFP-http/V0.0.1'
    v = Version.parse(s)
    assert(v.name_clean == 'km-mfp-http')
    assert(v.name     == 'KM-MFP-http')
    assert(v.major    == 0)
    assert(v.minor    == 0)
    assert(v.patch    == 1)
    assert(str(v) == s) 

    s = 'PHP/4.4.4-8+etch6'
    v = Version.parse(s)
    assert(v.name_clean == 'php')
    assert(v.major    == 4)
    assert(v.minor    == 4)
    assert(v.patch    == '4-8')
    assert(v.patch1   == 4)
    assert(v.patch2   == 8)
    assert(v.patch_str == '-')
    assert(v.build_meta == 'etch6')
    assert(str(v) == s) 

    s = 'IP_SHARER WEB 1.0'
    v = Version.parse(s)
    assert(v.name_clean == 'ip_sharerweb')
    assert(v.name     == 'IP_SHARER WEB')
    assert(v.major    == 1)
    assert(v.minor    == 0)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'mod_auth_passthrough/2.1'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_auth_passthrough')
    assert(v.name     == 'mod_auth_passthrough')
    assert(v.major    == 2)
    assert(v.minor    == 1)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'FrontPage/5.0.2.2635'
    v = Version.parse(s)
    assert(v.name_clean == 'frontpage')
    assert(v.major    == 5)
    assert(v.minor    == 0)
    assert(v.patch    == '2.2635')
    assert(v.patch1   == 2)
    assert(v.patch2   == 2635)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'OpenSSL/0.9.8r'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 0)
    assert(v.minor    == 9)
    assert(v.patch    == '8r')
    assert(v.patch1   == 8)
    assert(v.patch_str == 'r')
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'sendmail.8.14.7'
    v = Version.parse(s)
    assert(v.name_clean == 'sendmail')
    assert(v.name     == 'sendmail')
    assert(v.major    == 8)
    assert(v.minor    == 14)
    assert(type(v.patch) is int)
    assert(v.patch    == 7)
    assert(type(v.patch1) is int)
    assert(v.patch1   == 7)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s)

    s = 'Mercury POP3 server 1.48'
    v = Version.parse(s)
    assert(v.name_clean == 'mercurypop3server')
    assert(v.name     == 'Mercury POP3 server')
    assert(v.major    == 1)
    assert(v.minor    == 48)
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'Squid http proxy 3.0.STABLE20'
    v = Version.parse(s)
    assert(v.name_clean == 'squidhttpproxy')
    assert(v.name     == 'Squid http proxy')
    assert(v.major    == 3)
    assert(v.minor    == 0)
    assert(v.patch    == 'STABLE20')
    assert(v.patch1   is None)
    assert(v.patch_str == 'STABLE')
    assert(v.patch2   == 20)
    assert(str(v) == s)

    s = 'mod_apreq2-20090110/2.7.1'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_apreq2')
    assert(v.name     == 'mod_apreq2')
    assert(v.major    == 2)
    assert(v.minor    == 7)
    assert(v.patch    == 1)
    assert(v.patch1   == 1)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(v.release_date == date(2009, 1, 10))
    assert(str(v) == s) 

    s = 'mini_httpd/1.19 19dec2003'
    v = Version.parse(s)
    assert(v.name_clean == 'mini_httpd')
    assert(v.major    == 1)
    assert(v.minor    == 19)
    assert(v.patch    is None)
    assert(v.release_date == date(2003, 12, 19))
    assert(str(v) == s) 

    s = 'Allegro-Software-RomPager/4.34'
    v = Version.parse(s)
    assert(v.name_clean == 'allegro-software-rompager')
    assert(v.major    == 4)
    assert(v.minor    == 34)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Foobar 8.00.162'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.name     == 'Foobar')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_prefixes['minor'] == 1)
    assert(v.patch    == 162)
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'Foobar 8.00.0162'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.name     == 'Foobar')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_prefixes['minor'] == 1)
    assert(v.patch    == 162)
    assert(v.zero_prefixes['patch'] == 1)
    assert(v.patch1   == 162)
    assert(v.zero_prefixes['patch1'] == 1)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'LANCOM 1611+ 8.0.162'
    v = Version.parse(s)
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.patch    == 162)
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s)

    s = 'LANCOM 1611+ 8.00.162'
    v = Version.parse(s)
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_prefixes['minor'] == 1)
    assert(v.patch    == 162)
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s)

    s = 'LANCOM 1611+ 8.00.0162 / 16.06.2010'
    v = Version.parse(s)
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_prefixes['minor'] == 1)
    assert(v.patch    == 162)
    assert(v.zero_prefixes['patch'] == 1)
    assert(v.patch1   == 162)
    assert(v.zero_prefixes['patch1'] == 1)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(v.release_date == date(2010, 6, 16))
    assert(str(v) == s)

    s = 'OpenSSL/0.9.8e-fips-rhel5'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 0)
    assert(v.minor    == 9)
    assert(v.patch    == '8e-fips-rhel5')
    assert(v.patch1   == 8)
    assert(v.patch_str == 'e-fips-rhel')
    assert(v.patch2   == 5)     # Even though that's not ideal
    assert(str(v) == s) 

    s = 'Sun-ONE-ASP/4.0.3'
    v = Version.parse(s)
    assert(v.name_clean == 'sun-one-asp')
    assert(v.major    == 4)
    assert(v.minor    == 0)
    assert(v.patch    == 3)
    assert(v.patch1   == 3)
    assert(v.patch_str is None)
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'thttpd/2.23beta1 26may2002'
    v = Version.parse(s)
    assert(v.name_clean == 'thttpd')
    assert(v.major    == 2)
    assert(v.minor    == 23)
    assert(v.patch    == 'beta1')
    assert(v.patch1   is None)
    assert(v.patch2   == 1)
    assert(v.patch_str == 'beta')
    assert(v.release_date == date(2002, 5, 26))
    assert(str(v) == s) 

    # Test arbitary number of zero prefixes
    # TODO and interaction with strings in major/minor
    s = 'Foobar 0'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 0)
    assert(v.zero_prefixes['major'] == 0)
    assert(v.minor    is None)
    assert(str(v) == s)

    s = 'Foobar 03'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 1)
    assert(v.minor    is None)
    assert(str(v) == s)

    s = 'Foobar 003'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 2)
    assert(v.minor    is None)
    assert(str(v) == s)

    s = 'Foobar 00000000003'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 10)
    assert(v.minor    is None)
    assert(str(v) == s)

    s = 'Foobar 3.01'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 1)
    assert(str(v) == s)

    s = 'Foobar 3.001'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 2)
    assert(str(v) == s)

    s = 'Foobar 3.00000000001'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 10)
    assert(str(v) == s)

    s = 'Foobar 03.01'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 1)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 1)
    assert(str(v) == s)

    s = 'Foobar 000003.01'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 5)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 1)
    assert(str(v) == s)

    s = 'Foobar 000003.00000000001'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.zero_prefixes['major'] == 5)
    assert(v.minor    == 1)
    assert(v.zero_prefixes['minor'] == 10)
    assert(str(v) == s)

    s = 'Foobar 3.1.01'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.minor    == 1)
    assert(v.patch    == 1)
    assert(v.zero_prefixes['patch'] == 1)
    assert(v.patch1   == 1)
    assert(v.zero_prefixes['patch1'] == 1)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s)

    s = 'Foobar 3.1.1-01'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.major    == 3)
    assert(v.minor    == 1)
    assert(v.patch    == '1-01')
    assert(v.patch1   == 1)
    assert(v.patch2   == 1)
    assert(v.patch_str == '-')
    assert(str(v) == s)

    s = 'Foobar 3 (FB3-DX) 1.90.26'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'ProTools Basic Edition 5.0 Build 11'
    v = Version.parse(s)
    assert(v.name_clean == 'protoolsbasicedition')
    assert(v.name     == 'ProTools Basic Edition')
    assert(v.major    == 5)
    assert(v.minor    == 0)
    assert(v.patch    is None)
    assert(v.extra_str == 'Build 11')
    assert(str(v) == s) 

    s = 'Fiddlesticks 2.0 Beta 2'
    v = Version.parse(s)
    assert(v.name_clean == 'fiddlesticks')
    assert(v.name     == 'Fiddlesticks')
    assert(v.major    == 2)
    assert(v.minor    == 0)
    assert(v.patch    is None) 
    assert(v.extra_str == 'Beta 2')
    assert(str(v) == s) 

    s = 'IDA 5.19.1.1387.2314'
    #v = Version.parse(s)
    #assert(v.name_clean == 'ida')
    #assert(v.name     == 'IDA')
    #assert(v.major    == 5)
    #assert(v.minor    == 19)
    #assert(v.patch    == '')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 
    
#    s = 'IDA 5.19.1.1387.2314.0'
#    v = Version.parse(s)
#    assert(v.name_clean == 'php')
#    assert(v.name     == 'PHP')
#    assert(v.major    == 5)
#    assert(v.minor    == 2)
#    assert(v.patch    == '6-1+lenny15')
#    assert(v.patch1   == 6)
#    assert(v.patch2   == 1)
#    assert(v.patch_str == '-')
#    assert(str(v) == s) 
#    
#    s = 'IDA 5.19.1.1387.2314.0.1352135'
#    v = Version.parse(s)
#    assert(v.name_clean == 'php')
#    assert(v.name     == 'PHP')
#    assert(v.major    == 5)
#    assert(v.minor    == 2)
#    assert(v.patch    == '6-1+lenny15')
#    assert(v.patch1   == 6)
#    assert(v.patch2   == 1)
#    assert(v.patch_str == '-')
#    assert(str(v) == s) 

    s = 'Cyrus POP3 v2.2.13-Debian-2.2.13-14+lenny3 server'
    v = Version.parse(s)
    assert(v.name_clean == 'cyruspop3')
    assert(v.name     == 'Cyrus POP3')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == '13-Debian-2.2.13-14')
    assert(v.patch1   == 13)
    assert(v.patch2   == 14)
    assert(v.patch_str == '-Debian-2.2.13-')
    assert(v.build_meta == 'lenny3')
    assert(v.extra_str == ' server')
    assert(str(v) == s) 

    s = 'POP MDaemon 9.0.4'
    v = Version.parse(s)
    assert(v.name_clean == 'popmdaemon')
    assert(v.name     == 'POP MDaemon')
    assert(v.major    == 9)
    assert(v.minor    == 0)
    assert(v.patch    == 4)
    assert(v.patch1   == 4)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'POP3 Bigfoot v1.0 server'
    v = Version.parse(s)
    assert(v.name_clean == 'pop3bigfoot')
    assert(v.name     == 'POP3 Bigfoot')
    assert(v.major    == 1)
    assert(v.minor    == 0)
    assert(v.patch    is None) 
    assert(v.extra_str == ' server')
    assert(str(v) == s) 

    s = 'IMail 8.05 4000-1'
    v = Version.parse(s)
    assert(v.name_clean == 'imail')
    assert(v.name     == 'IMail')
    assert(v.major    == 8)
    assert(v.minor    == 5)
    assert(v.zero_prefixes['minor'] == 1)
    assert(v.patch    is None) 
    assert(v.extra_str == '4000-1')     # won't include ' ' if it's the name_sep
    assert(str(v) == s) 

    s = 'IdeaPop3Server v0.80'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'example.example Cyrus POP3 v2.3.7-Invoca-RPM-2.3.7-12.el5_7.2 server'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Qpopper (version 4.0.5)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'POP3 on WinWebMail [3.8.1.3]'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'Microsoft Exchange Server 2003 POP3 <A6><F8><AA>A<BE><B9><AA><A9><A5><BB> 6.5.7638.1 (example.local)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'Microsoft Windows POP3 Service Version 1.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'Microsoft Exchange 2000 POP3 server version 6.0.6249.0 (example.example.org)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'X1 NT-POP3 Server mail.example.org (IMail 8.03 304911-2)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'RaidenMAILD POP3 service v2205'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'Lotus Notes POP3 server version Release 8.5.3'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'X1 NT-POP3 Server example.org (IMail 9.23 64609-2757)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'IceWarp 10.3.5 RHEL5 POP3'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'XMail 1.27 POP3 Server'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Intoto Http Server v1.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Apache/2.2.15 (CentOS)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'mod_gzip/1.3.26.1a'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'mod_perl/1.29'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'DIR-600 Ver 2.11'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'mini_httpd/1.19 19dec2003'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Embedthis-Appweb/3.3.1'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Boa/0.94.14rc21'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'MailEnable-HTTP/5.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    # Fuck you Zope
    s = 'Zope/(Zope 2.11.4-final, python 2.5.4, linux2) ZServer/1.1'

    s = 'Mathopd/1.5p6'
    v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    # lenny15 should be treated as build meta and rest
    # in extra_str
    s = 'PHP/5.2.6-1+lenny15 with Suhosin-Patch'
    v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'squid/2.7.STABLE9'
    v = Version.parse(s)
    assert(v.name_clean == 'squid')
    assert(v.name     == 'squid')
    assert(v.major    == 2)
    assert(v.minor    == 7)
    assert(v.patch    == 'STABLE9')
    assert(v.patch1   is None)
    assert(v.patch2   == 9)
    assert(v.patch_str == 'STABLE')
    assert(str(v) == s) 

    s = 'lighttpd/1.4.26-devel-6243M'
    v = Version.parse(s)
    assert(v.name_clean == 'lighttpd')
    assert(v.name     == 'lighttpd')
    assert(v.major    == 1)
    assert(v.minor    == 4)
    assert(v.patch    == '26-devel-6243M')
    assert(v.patch1   == 26)
    assert(v.patch2   is None)
    assert(v.patch_str == '-devel-6243M')
    assert(str(v) == s) 

    s = 'Winstone Servlet Engine v0.9.10'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    s = 'PHP/5.3.10-1ubuntu3.11'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'F6D4630-4-v2/1.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'thttpd/2.25b 29dec2003'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Jetty(8.y.z-SNAPSHOT)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    ##assert(str(v) == s) 

    s = 'Microsoft-HTTPAPI/2.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'php')
    #assert(v.name     == 'PHP')
    #assert(v.major    == 5)
    #assert(v.minor    == 2)
    #assert(v.patch    == '6-1+lenny15')
    #assert(v.patch1   == 6)
    #assert(v.patch2   == 1)
    #assert(v.patch_str == '-')
    #assert(str(v) == s) 

    #s = 'GlassFish Server Open Source Edition  4.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'glassfishserveropensourceedition') # ergh
    #assert(v.name    == 'GlassFish Server Open Source Edition')
    #assert(v.major   == 4)
    #assert(v.minor   == 0)
    #assert(v.patch   is None)
    #assert(str(v) == s) 

    #s = 'David-WebBox/11.00a (0717)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'david-webbox')
    #assert(v.name     == 'David-WebBox')
    #assert(v.major    == 11)
    #assert(v.minor    == 0)
    #assert(v.patch    == 'a')
    #assert(v.patch1   is None)
    #assert(v.patch2   is None)
    #assert(v.patch_str == 'a')
    #assert(v.extra_str == ' (0717)')
    #assert(str(v) == s) 

    s = 'VOD server/4.9.0.01 (Unix)'
    v = Version.parse(s)
    # TODO extra str
    #assert(str(v) == s) 

    s = 'Boa/0.94.13-20100727-114000'
    v = Version.parse(s)
    assert(v.name_clean == 'boa')
    assert(v.name     == 'Boa')
    assert(v.major    == 0)
    assert(v.minor    == 94)
    assert(v.patch    == '13-114000')
    assert(v.patch1   == 13)
    assert(v.patch2   == 114000)
    assert(v.patch_str == '-')
    assert(str(v) == s) 

    s = 'distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))'
    v = Version.parse(s)
    #assert(v.name_clean == 'distccdv1')
    #assert(v.name    == 'distccd v1')
    #assert(v.major   == 4)
    #assert(v.minor   == 2)
    #assert(v.patch   == 4)
    #assert(v.patch1  == 4)
    #assert(v.patch_str is None)
    #assert(v.patch2    is None)
    #assert(str(v) == s) 

    s = 'ISC BIND 9.4.2'
    v = Version.parse(s)
    assert(v.name_clean == 'iscbind')
    assert(v.name     == 'ISC BIND')
    assert(v.major    == 9)
    assert(v.minor    == 4)
    assert(v.patch    == 2)
    assert(v.patch1   == 2)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 
    
    s = 'Apache Tomcat/Coyote JSP engine 1.1'   # TODO
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'FreeBSD 8.2-release-p7'
    v = Version.parse(s)
    assert(v.name_clean == 'freebsd')
    assert(v.name     == 'FreeBSD')
    assert(v.major    == 8)
    assert(v.minor    == 2)
    assert(v.patch    == '-release-p7')
    assert(v.patch1   is None)
    assert(v.patch2   == 7)
    assert(v.patch_str == '-release-p') 
    assert(str(v) == s) 

    s = 'Java SE 7u45'
    v = Version.parse(s)
    assert(v.name_clean == 'javase')
    assert(v.name     == 'Java SE')
    assert(v.major    == 7)
    assert(v.minor    == 45)
    assert(v.patch    is None)
    assert(v.version_sep == 'u')
    assert(str(v) == s) 

    s = 'blag 29999.50000'
    v = Version.parse(s)
    assert(v.name_clean == 'blag')
    assert(v.major    == 29999)
    assert(v.minor    == 50000)
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'blag 19999.00071'
    v = Version.parse(s)
    assert(v.name_clean == 'blag')
    assert(v.major    == 19999)
    assert(v.minor    == 71)
    assert(v.zero_prefixes['minor'] == 3)
    assert(v.patch    is None)
    assert(str(v) == s)


    s = 'blorg 1:4.8.2-1ubuntu6'
    #v = Version.parse(s)
    #assert(v.name_clean == 'blorg')
    #assert(v.epoch    == 1)
    #assert(v.major    == 4)
    #assert(v.minor    == 8)
    #assert(v.patch    == '2-1ubuntu6')
    #assert(v.patch1   == 2)
    #assert(v.patch2   == 6) # TODO?
    #assert(str(v) == s)

    s = 'foo 0.08-2'
    #v = Version.parse(s)
    #assert(v.name_clean == 'foo')
    #assert(v.major    == 0)
    #assert(v.minor    == 8)
    #assert(v.zero_prefixes['minor'] == 1)
    #assert(v.patch    == '2')
    #assert(v.patch1   == 2)
    #assert(str(v) == s)

    s = 'libalgorithm-perl 0.08-2'
    #v = Version.parse(s)
    #assert(v.name_clean == 'libalgorithm-perl')
    #assert(v.major    == 0)
    #assert(v.minor    == 8)
    #assert(v.zero_prefixes['minor'] == 1)
    #assert(v.patch    == '2')
    #assert(v.patch1   == 2)
    #assert(str(v) == s)

    s = 'foo 1.19.02-3'
    v = Version.parse(s)
    assert(v.name_clean == 'foo')
    assert(v.major    == 1)
    assert(v.minor    == 19)
    assert(v.patch    == '02-3')
    assert(v.patch1   == 2)
    assert(v.zero_prefixes['patch1'] == 1)
    assert(v.patch2   == 3)
    assert(str(v) == s)


    s = 'foo 0.5.1+14.04.20140409-0ubuntu1'
    v = Version.parse(s)
    assert(v.name_clean == 'foo')
    assert(v.major    == 0)
    assert(v.minor    == 5)
    assert(v.patch    == 1)
    assert(v.patch1   == 1)
    assert(v.patch2   is None)
    assert(v.build_meta == '14.04.20140409-0ubuntu1')
    assert(v.release_date == date(2014, 4, 9))
    assert(str(v) == s)

    s = 'foo 1.1svn5547-1'
    #v = Version.parse(s)
    #assert(v.name_clean == 'foo')
    #assert(v.major    == 1)
    #assert(v.minor    == 1)
    #TODO
    #assert(str(v) == s)

    s = 'foo 2.10.1-2build1'
    v = Version.parse(s)
    assert(v.name_clean == 'foo')
    assert(v.major    == 2)
    assert(v.minor    == 10)
    assert(v.patch    == '1-2build1')
    assert(v.patch1   == 1)
    assert(v.patch2   == 1) #TODO correct? patch2 == 2?
    assert(str(v) == s)

    s = '2:0.142.2389+git956c8d8-2'
    s = '6:9.13-0ubuntu0.14.04.1'
    s = '2014.01.13-1'
    s = 'libdirectfb-1.2-9'
    s = '0.15.1b-8ubuntu1'
    s = '2.1.4-0ubuntu14.04.1'

    # TODO list all versions in apt repo

    #s = ''
    #v = Version.parse(s)
    #assert(str(v) == s)


    ####
    #### Software with a digit in the protocol (e.g. POP3)
    ####

    # TODO RPC?
    #s = '2 (RPC #100000)'
    #v = Version.parse(s)
    #assert(str(v) == s)

    # TODO 
    #s = '2-4 (RPC #100003)'
    #assert(str(v) == s)

    s = 'VNC (protocol 3.3)'
    v = Version.parse(s)
    assert(str(v) == s)

    # legit case
    s = '(sshd version 1.2.3)'
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'Apache Jserv (Protocol v1.3)'
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'Apache Tomcat|Coyote JSP engine 1.1'
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'Ruby DRb RMI (Ruby 1.8; path |usr|lib|ruby|1.8|drb)'
    v = Version.parse(s)
    # TODO parens
    #assert(v.name == 'Ruby DRb RMI')
    #assert(v.name_clean == 'rubydrbrmi')
    #assert(v.major      == 1)
    #assert(v.minor      == 8)
    #assert(v.patch      is None)
    #assert(v.extra_str is not None)
    #assert(v.extra_str[0] == ';')
    #assert(str(v) == s)

    
    ####
    #### Apple NumVersion   # TODO
    ####

    ####
    #### distutils LooseVersion
    ####

#    1.5.2b2
#    3.10a
#    3.4j
#    1996.07.12
#    3.2.pl0
#    3.1.1.6
#    2g6
#    11g
#    0.960923
#    2.2beta29
#    1.13++
#    5.5.kw
#    2.0b1pl0

#                       semver          pep440
#    1.5.2b2            
#    3.10a
#    3.4j
#    1996.07.12
#    3.2.pl0
#    3.1.1.6
#    2g6
#    11g
#    0.960923
#    2.2beta29
#    1.13++
#    5.5.kw
#    2.0b1pl0

    ####
    #### distutils StrictVersion
    ####


#    0.4       0.4.0  (these two are equivalent)
#    0.4.1
#    0.5a1
#    0.5b3
#    0.5
#    0.9.6
#    1.0
#    1.0.4a3
#    1.0.4b1
#    1.0.4


    ####
    #### setuptools parse_version
    ####

    # just make sure we do a superset of that (close already)


    ####
    #### Misc
    ####

#1 (first draft)
#0.1.alphadev
#2008-03-29_r219





# TODO NB http://legacy.python.org/dev/peps/pep-0386/
# -> caveats of existing systems
# (try to solve these issues)
# (and address these points in FAQ/readme/whatever)

    ####
    #### Misc Tests
    ####


    # TODO see http://en.wikipedia.org/wiki/Software_versioning


    s = ''
    #v = Version.parse(s)
    #assert(str(v) == s)

    s = ''
    #v = Version.parse(s)
    #assert(str(v) == s)



def test_parse_pep440():

    ####
    #### PEP440 Tests
    ####

    # Various trivial cases are handled earlier

    # Format:
    # epoch, release, pre-release, post-release, dev-release
    # all numeric components - numeric value, not text strings

    s = '0'
    v = Version.parse(s)
    assert(v.name is None)
    assert(len(v.release) == 1)
    assert(v.release == (0,))
    assert(str(v) == s)

#    s = 'frob 1.0a1'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0b2'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0c1'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0rc1'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0.dev1'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0.post1'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0.dev456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0a2.dev456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0a12.dev456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0a12'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0b2.post345.dev456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0b2.post345'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0c1.dev456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0.post456.dev34'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 
#
#    s = 'frob 1.0.post456'
#    v = Version.parse(s)
#    assert(v.name_clean == 'frob')
#    assert(v.name     == 'frob')
#    assert(v.major    == 2012)
#    assert(v.minor    == 4)
#    assert(v.patch    is None)
#    assert(str(v) == s) 

    # Epoch

    # (implicit epoch is 0)

    # TODO see http://legacy.python.org/dev/peps/pep-0440/
    # for version matching

    s = 'frob 5:1'
    s = 'frob 5:1.0'
    s = 'frob 5:1.0a1'
    s = 'frob 5:1.0.dev1'
    s = 'frob 5:1.0.post1.dev456'
    s = 'frob 5:1.0rc2.post456'

    # Local version identifier
    s = 'frob 1-1'
    s = 'frob 1.0-1'
    s = 'frob 1.0a1-1'
    s = 'frob 1.0a1-1.1'
    s = 'frob 1.0.dev1-1.1'
    s = 'frob 1.1a.post345.dev789-88.99'
    s = 'frob 1000:1.1a.post345.dev789-88.99.11.22'


    # Date-as-version

    s = '2012.04'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'frob 2012.4'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'frob 2012.4.1'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'frob 2012.04.01'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'frob 20120401'
    #v = Version.parse(s)
    #assert(v.release_date == date(2012, 4, 1))

def test_parse_semver():

    ####
    #### Semver-specific tests (Semver 2.0.0)
    ####

    s = '0.0.0'     # legal according to semver 2.0.0
    v = Version.parse(s)
    assert(v.name   is None)
    assert(v.name_clean is None)
    assert(type(v.major) is int)
    assert(v.major  == 0)
    assert(type(v.minor) is int)
    assert(v.minor  == 0)
    assert(type(v.patch) is int)
    assert(v.patch  == 0)
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(str(v) == s)

    s = '0.0.1'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.name_clean is None)
    assert(v.major  == 0)
    assert(v.minor  == 0)
    assert(v.patch  == 1)
    assert(v.patch1 == 1)
    assert(str(v) == s)

    s = '0.0.99'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.name_clean is None)
    assert(v.major  == 0)
    assert(v.minor  == 0)
    assert(v.patch  == 99)
    assert(v.patch1 == 99)
    assert(str(v) == s)
    
    s = '0.0.99999999'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.name_clean is None)
    assert(type(v.major) is int)
    assert(v.major  == 0)
    assert(type(v.minor) is int)
    assert(v.minor  == 0)
    assert(type(v.patch) is int)
    assert(v.patch  == 99999999)
    assert(type(v.patch1) is int)
    assert(v.patch1 == 99999999)
    assert(str(v) == s)
    
    s = '0.999999999.0'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.name_clean is None)
    assert(v.major  == 0)
    assert(v.minor  == 999999999)
    assert(v.patch  == 0)
    assert(v.patch1 == 0)
    assert(str(v) == s)
    
    s = '99999999.0.0'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.name_clean is None)
    assert(v.major  == 99999999)
    assert(v.minor  == 0)
    assert(v.patch  == 0)
    assert(v.patch1 == 0)
    assert(str(v) == s)

    s = '1.0.0-alpha'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-alpha')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(v.patch2 is None)
    assert(v.patch_str == '-alpha')
    assert(str(v) == s)
    
    s = '1.0.0-alpha1'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-alpha1')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 1)
    assert(v.patch_str == '-alpha')
    assert(str(v) == s)
    
    s = '1.0.0-alpha.1'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-alpha.1')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 1)
    assert(v.patch_str == '-alpha.')
    assert(str(v) == s)
    
    s = '1.0.0-1'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-1')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 1)
    assert(v.patch_str == '-')
    assert(str(v) == s)
    
    s = '1.0.0-0.1'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-0.1')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 1)
    assert(v.patch_str == '-0.')
    assert(str(v) == s)
    
    s = '1.0.0-1-2-3-4-5'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-1-2-3-4-5')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 5)
    assert(v.patch_str == '-1-2-3-4-')
    assert(str(v) == s)
    
    s = '1.0.0-1-0-1-0-1'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-1-0-1-0-1')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(type(v.patch2) is int)
    assert(v.patch2 == 1)
    assert(v.patch_str == '-1-0-1-0-')
    assert(str(v) == s)
    
    s = '1.0.0-1a2b3c'
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0-1a2b3c')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(v.patch2 is None)
    assert(v.patch_str == '-1a2b3c')
    assert(str(v) == s)
    
    s = '1.0.0--'   # legal ""
    v = Version.parse(s)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch  == '0--')
    assert(type(v.patch1) is int)
    assert(v.patch1 == 0)
    assert(v.patch2 is None)
    assert(v.patch_str == '--')
    assert(str(v) == s)
    
    s = '1.0.0-a.b'         # TODO interface. this is wrong
    v = Version.parse(s)
    #assert(v.major  == 1)
    #assert(v.minor  == 0)
    #assert(type(v.patch) in STR_TYPES)
    #assert(v.patch  == '0-a.b')
    #assert(type(v.patch1) in STR_TYPES)
    #assert(v.patch1 == 'a')
    #assert(v.patch2 == 'b')
    #assert(v.patch_str == '-a.b')
    #assert(str(v) == s)
    
    s = '1.0.0-A.B'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(v.patch  == '0-A.B')
    assert(v.patch1 == 0)
    assert(v.patch2 is None)
    assert(v.patch_str == '-A.B')
    assert(str(v) == s)
    
    s = '1.0.0-a-.b-.c-.d-'
    v = Version.parse(s)
    assert(v.name is None)
    assert(v.major  == 1)
    assert(v.minor  == 0)
    assert(v.patch  == '0-a-.b-.c-.d-')
    assert(v.patch1 == 0)
    assert(v.patch2 is None)
    assert(str(v) == s)
    
    s = '1.0.0-0.33.44.55'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-999.fiddlesticks.whoomp-there-it-is.ohyeah'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.-'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.z'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.0'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+20130313144700'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-beta+exp.sha.5114f85'
    v = Version.parse(s)
    assert(str(v) == s)

    s = '1.0.0+alpha'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+alpha1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+alpha.1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+0.1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+1-2-3-4-5'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+1-0-1-0-1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+1a2b3c'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+-'   # legal ""
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a.b'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+A.B'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a-.b-.c-.d-'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+0.33.44.55'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+999.fiddlesticks.whoomp-there-it-is.ohyeah'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a.2.X.5'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a.2.X.5.-'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a.2.X.5.z'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0+a.2.X.5.0'
    v = Version.parse(s)
    assert(str(v) == s)

    s = '1.0.0-alpha+alpha'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-alpha1+alpha1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-alpha.1+alpha.1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-1+1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-0.1+0.1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-1-2-3-4-5+1-2-3-4-5'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-1-0-1-0-1+1-0-1-0-1'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-1a2b3c+1a2b3c'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0--+-'   # legal ""
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.b+a.b'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-A.B+A.B'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a-.b-.c-.+a-.b-.c-.d-'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-0.33.44.55+0.33.44.55'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-999.fiddlesticks.whoomp-there-it-is.ohyeah+999.fiddlesticks.whoomp-there-it-is.ohyeah'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5+a.2.X.5'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.-+a.2.X.5.-'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.z+a.2.X.5.z'
    v = Version.parse(s)
    assert(str(v) == s)
    
    s = '1.0.0-a.2.X.5.0+a.2.X.5.0'
    v = Version.parse(s)
    assert(str(v) == s)



def test_parse_wildcards():

    s = 'OpenSSH *'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) in STR_TYPES)
    assert(v.major    == '*')
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(str(v) == s) 

    s = 'OpenSSH x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) in STR_TYPES)
    assert(v.major    == 'x')
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(str(v) == s) 

    s = 'OpenSSH X'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) in STR_TYPES)
    assert(v.major    == 'X')
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(str(v) == s) 

    s = 'OpenSSH 4.x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == 'x')
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.X'
    v = Version.parse(s) 
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == 'X')
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.*'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == '*')
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.x.x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == 'x')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == 'x')
    assert(type(v.patch1) in STR_TYPES)
    assert(v.patch1   == 'x')
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.X.X'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == 'X')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == 'X')
    assert(type(v.patch1) in STR_TYPES)
    assert(v.patch1   == 'X')
    assert(v.patch2    is None)
    assert(v.patch_str is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.*.*'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == '*')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '*')
    assert(type(v.patch1) in STR_TYPES)
    assert(v.patch1   == '*')
    assert(v.patch2    is None)
    assert(v.patch_str is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')

    s = 'OpenSSH 4.*.*-*'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == '*')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '*-*')
    assert(type(v.patch1) in STR_TYPES)
    assert(v.patch1   == '*')
    assert(type(v.patch2) in STR_TYPES)
    assert(v.patch2   == '*')
    assert(type(v.patch_str) in STR_TYPES)
    assert(v.patch_str == '-')
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')

    s = 'OpenSSH *.*.*-*'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) in STR_TYPES)
    assert(v.major    == '*')
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == '*')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == '*-*')
    assert(type(v.patch1) in STR_TYPES)
    assert(v.patch1   == '*')
    assert(type(v.patch2) in STR_TYPES)
    assert(v.patch2   == '*')
    assert(type(v.patch_str) in STR_TYPES)
    assert(v.patch_str == '-')
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')

    s = 'OpenSSH x.x.x-x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) in STR_TYPES)
    assert(v.major    == 'x')
    assert(type(v.minor) in STR_TYPES)
    assert(v.minor    == 'x')
    assert(type(v.patch) in STR_TYPES)
    assert(v.patch    == 'x-x')
    assert(v.patch1   == 'x')
    assert(v.patch2   == 'x')
    assert(v.patch_str == '-')
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')


def test_parse_compare():
    v1 = Version.parse('OpenSSH 4')
    v2 = Version.parse('OpenSSH 5')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not(v1 > v2))
    assert(v2 > v1)
    assert(not(v2 < v1))

    v1 = Version.parse('OpenSSH_4')
    v2 = Version.parse('OpenSSH 5')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not(v1 > v2))
    assert(v2 > v1)
    assert(not(v2 < v1))
 
    v1 = Version.parse('OpenSSH_4')
    v2 = Version.parse('OpenSSH v5')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not(v1 > v2))
    assert(v2 > v1)
    assert(not(v2 < v1))

    v1 = Version.parse('OpenSSH *')
    v2 = Version.parse('OpenSSH 5')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(not (v1 < v2))
    assert(not (v1 > v2))
    assert(not (v2 > v1))
    assert(not (v2 < v1))

    v1 = Version.parse('OpenSSH_4.3')
    v2 = Version.parse('OpenSSH 4.3')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(not (v1 < v2))
    assert(not (v1 > v2))
    assert(not (v2 > v1))
    assert(not (v2 < v1))
 
    v1 = Version.parse('OpenSSH_4.3')
    v2 = Version.parse('OpenSSH 4.4')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not (v1 > v2))
    assert(v2 > v1)
    assert(not (v2 < v1))

    v1 = Version.parse('OpenSSH_5.5p1')
    v2 = Version.parse('OpenSSH_5.5p1 Debian-6+squeeze2')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(not (v1 < v2))
    assert(not (v1 > v2))
    assert(not (v2 > v1))
    assert(not (v2 < v1))

    v1 = Version.parse('OpenSSH_5.5p1')
    v2 = Version.parse('OpenSSH_6.5p1 Debian-6+squeeze2')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not (v1 > v2))
    assert(v2 > v1)
    assert(not (v2 < v1))

    v1 = Version.parse('OpenSSH_5.5p1')
    v2 = Version.parse('OpenSSH_5.6p1 Debian-6+squeeze2')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not (v1 > v2))
    assert(v2 > v1)
    assert(not (v2 < v1))

    v1 = Version.parse('OpenSSH_5.5p1')
    v2 = Version.parse('OpenSSH_5.5p2 Debian-6+squeeze2')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(v1 < v2)
    assert(not (v1 > v2))
    assert(v2 > v1)
    assert(not (v2 < v1))

    v1 = Version.parse('Quux 1.12_15')
    v2 = Version.parse('Quux 1.12_15')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(not (v1 < v2))
    assert(not (v1 > v2))
    assert(not (v2 < v1))
    assert(not (v2 > v1))


    # TODO few more here


def test_encodings():
    s = 'foo 1.0'
    v = Version.parse(s)
    if sys.version_info.major == 2:
        assert(str(v) == s)
        assert(unicode(v) == coerce_to_unicode(s))
    if sys.version_info.major == 3:
        assert(str(v) == coerce_to_unicode(s))

    s = u'foo 1.0'
    v = Version.parse(s)
    if sys.version_info.major == 2:
        assert(str(v) == str(s))
        assert(unicode(v) == s)
    if sys.version_info.major == 3:
        assert(str(v) == s)

    s = b'foo 1.0'
    v = Version.parse(s)
    if sys.version_info.major == 2:
        assert(str(v) == s)
        assert(unicode(v) == coerce_to_unicode(s))
    if sys.version_info.major == 3:
        assert(str(v) == coerce_to_unicode(s))


def test_bad():
    # Bogus data which shouldn't parse

    s = 'pop3d'
    assert_raises(VersionParseError, Version.parse, s)

    s = 'Dovecot pop3d'
    assert_raises(VersionParseError, Version.parse, s)

    s = '(protocol version 30)'
    assert_raises(VersionParseError, Version.parse, s)

    # TODO find_version
    #s = 'netkit-rsh rexecd None'
    #assert_raises(VersionParseError, Version.parse, s)

    # TODO find_version
    #s = 'Postfix smtpd None'
    #assert_raises(VersionParseError, Version.parse, s)

    # TODO find_version
    #s = 'Linux telnetd None'
    #assert_raises(VersionParseError, Version.parse, s)

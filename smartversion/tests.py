# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
import datetime
from datetime import date, timedelta
import random

from nose.tools import assert_raises

from .smartversion import *


today = date.today()

def test_helper():
    n = count_zero_prefixes('')
    assert(type(n) is int)
    assert(n == 0)
    n = count_zero_prefixes('0')
    assert(type(n) is int)
    # Interested in # prefix zeroes, not total count
    assert(n == 0)
    assert(count_zero_prefixes(1234) == 0)
    assert(count_zero_prefixes('asd') == 0)
    assert(count_zero_prefixes('a0') == 0)
    assert(count_zero_prefixes('00') == 1)
    assert(count_zero_prefixes('00000') == 4)
    assert(count_zero_prefixes('001') == 2)

    ds = first_digits('')
    assert(ds is None)
    ds = first_digits('asd')
    assert(ds is None)
    ds = first_digits('123')
    assert(type(ds) is tuple)
    assert(ds == (3, '123'))

    assert(first_digits('123foo') == (3, '123'))
    assert(first_digits('123456789a9') == (9, '123456789'))
    assert(first_digits('123foobar456') == (3, '123'))
    assert(first_digits('1a2') == (1, '1'))
    assert(first_digits('0a2') == (1, '0'))
    assert(first_digits('0 1') == (1, '0'))
    assert(first_digits('9 8') == (1, '9'))
    assert(first_digits('01')  == (2, '01'))
    assert(first_digits('asd001') == (6, '001'))

    x = first_int('123')
    assert(type(x) is int)
    assert(x == 123)

    assert(first_int('123foo') == 123)
    assert(first_int('123456789a9') == 123456789)
    assert(first_int('123foobar456') == 123)
    assert(first_int('1a2') == 1)
    assert(first_int('0a2') == 0)
    assert(first_int('0 1') == 0)
    assert(first_int('9 8') == 9)
    assert(first_int('09 08') == 9)

    x = last_int('123')
    assert(type(x) is int)
    assert(x == 123)

    assert(last_int('456foo123') == 123)
    assert(last_int('9a123456789') == 123456789)
    assert(last_int('1a2') == 2)
    assert(last_int('0a2') == 2)
    assert(last_int('0 1') == 1)
    assert(last_int('9 8') == 8)

    assert(any_digits_in_str('') is False)
    assert(any_digits_in_str('foo') is False)
    assert(any_digits_in_str('FOO') is False)
    assert(any_digits_in_str('1') is True)
    assert(any_digits_in_str('foo2') is True)
    assert(any_digits_in_str('SODI:HF:OIFD0') is True)
    assert(any_digits_in_str('765') is True)

    assert(any_letters_in_str('') is False)
    assert(any_letters_in_str('123') is False)
    assert(any_letters_in_str('._!@#') is False)
    assert(any_letters_in_str('a') is True)
    assert(any_letters_in_str('A') is True)
    assert(any_letters_in_str('a123') is True)
    assert(any_letters_in_str('A123') is True)
    assert(any_letters_in_str('123a') is True)
    assert(any_letters_in_str('123A') is True)
    assert(any_letters_in_str('123z') is True)

    assert(str_is_all_digits('') is False)
    assert(str_is_all_digits('foo') is False)
    assert(str_is_all_digits('foo1') is False)
    assert(str_is_all_digits('1foo') is False)
    assert(str_is_all_digits('1') is True)
    assert(str_is_all_digits('123') is True)
    assert(str_is_all_digits('123.456') is False)

    assert(next_digit_offset('') == -1)
    assert(next_digit_offset('foo') == -1)
    assert(next_digit_offset('1') == 0)
    assert(next_digit_offset('foo1') == 3)
    assert(next_digit_offset('foo1', 4) == -1)
    assert(next_digit_offset('foo1bar2', 4) == 7)
    assert(next_digit_offset('foo1bar2', 7) == 7)
    assert(next_digit_offset('foo1bar2', 8) == -1)

    # TODO find_pns?

    assert(find_version_sep('0') == '.')
    assert(find_version_sep('0.1') == '.')
    assert(find_version_sep('0.1.2') == '.')
    assert(find_version_sep('0_1') == '_')
    assert(find_version_sep('0_1_2') == '_')
    assert(find_version_sep('v0.1') == '.')
    assert(find_version_sep('0.1a') == '.')

    assert(find_pure_version('') is None)
    assert(find_pure_version('foobar') is None)
    assert(find_pure_version('1.2.3.4') == (0, 7, '1.2.3.4'))
    assert(find_pure_version('x.x') == (0, 3, 'x.x'))
    assert(find_pure_version('*.*.*.*') == (0, 7, '*.*.*.*'))
    assert(find_pure_version('OpenSSH 4') == (8, 9, '4'))
    assert(find_pure_version('OpenSSH-4') == (8, 9, '4'))
    assert(find_pure_version('OpenSSH_4') == (8, 9, '4'))
    assert(find_pure_version('OpenSSH_4.3') == (8, 11, '4.3'))
    assert(find_pure_version('OpenSSH_4.35') == (8, 12, '4.35'))
    assert(find_pure_version('OpenSSH_6.2p5') == (8, 13, '6.2p5'))
    assert(find_pure_version('OpenSSH_4.3-HipServ') == (8, 19, '4.3-HipServ'))
    assert(find_pure_version('Quux 1.12_15') == (5, 12, '1.12_15'))
    assert(find_pure_version('openssh 4.2.p1') == (8, 14, '4.2.p1'))
    assert(find_pure_version('ARRIS_0.44_01') == (6, 13, '0.44_01'))
    assert(find_pure_version('ProFTPD1.3.3') == (7, 12, '1.3.3'))
    assert(find_pure_version('OpenSSH 5.5p1 Debian 6+squeeze4 (protocol 2.0)') \
            == (8, 13, '5.5p1'))
    assert(find_pure_version('foo x.x.x') == (4, 9, 'x.x.x'))
    assert(find_pure_version('foo v3.5 blah') == (4, 8, 'v3.5'))

    assert(chunk_part('') == [])
    assert(chunk_part('foo') == ['foo'])
    assert(chunk_part('1') == [1])
    assert(chunk_part('1foo') == [1, 'foo'])
    assert(chunk_part('1foo1') == [1, 'foo', 1])
    assert(chunk_part('1foo1foo') == [1, 'foo', 1, 'foo'])
    assert(chunk_part('1foo1foo1') == [1, 'foo', 1, 'foo', 1])
    assert(chunk_part('foo1foo1foo1') == ['foo', 1, 'foo', 1, 'foo', 1])
    assert(chunk_part('1foo1foo1foo') == [1, 'foo', 1, 'foo', 1, 'foo'])
    assert(chunk_part('foo-1') == ['foo', 1])
    assert(chunk_part('1-foo') == [1, 'foo'])
    assert(chunk_part('foo1-foo') == ['foo', 1, 'foo'])
    assert(chunk_part('foo-1foo') == ['foo', 1, 'foo'])
    assert(chunk_part('3-Hipserv') == [3, 'Hipserv'])
    assert(chunk_part('1.foo') == [1, 'foo'])
    assert(chunk_part('foo.1') == ['foo', 1])
    assert(chunk_part('1_foo') == [1, 'foo'])
    assert(chunk_part('foo_1') == ['foo', 1])


    l = []
    assert(most_versiony_chars_idx(l) == -1)
    l = [' ']
    assert(most_versiony_chars_idx(l) == -1)
    l = [' ', 'foobar', 'aoaisjodiaoisd']
    assert(most_versiony_chars_idx(l) == -1)
    l = ['0']
    assert(most_versiony_chars_idx(l) == 0)
    l = [' ', '0']
    assert(most_versiony_chars_idx(l) == 1)
    l = ['a', 'a', 'a', '9']
    assert(most_versiony_chars_idx(l) == 3)
    l = ['a', 'a9', 'a99']
    assert(most_versiony_chars_idx(l) == 2)
    l = ['99', 'a', 'a', 'a9']
    assert(most_versiony_chars_idx(l) == 0)
    l = ['99', '9.9']
    assert(most_versiony_chars_idx(l) == 1)
    l = ['99', '9.9', '9.99']
    assert(most_versiony_chars_idx(l) == 2)
    l = ['99', '9.9', '9.9.9', 'a9.9']
    assert(most_versiony_chars_idx(l) == 2)
    l = ['IMail', '8.05', '4000-1']
    assert(most_versiony_chars_idx(l) == 1)

    assert(find_date('20090110') == (0, 8, date(2009, 1, 10)))
    assert(find_date('19690110') is None)
    assert(find_date('30000110') is None)
    assert(find_date('20091330') is None)
    assert(find_date('20091232') is None)
    assert(find_date('19990110') == (0, 8, date(1999, 1, 10)))
    assert(find_date('19700101') == (0, 8, date(1970, 1, 1)))
    assert(find_date('29991231') == (0, 8, date(2999, 12, 31)))
    assert(find_date('20093112') == (0, 8, date(2009, 12, 31)))
    assert(find_date('20094512') is None)
    assert(find_date('20093113') is None)
    assert(find_date('01101999') == (0, 8, date(1999, 10, 1)))
    assert(find_date('01231999') == (0, 8, date(1999, 1, 23)))
    assert(find_date('2009-01-10') == (0, 10, date(2009, 1, 10)))
    assert(find_date('01-10-2009') == (0, 10, date(2009, 10, 1)))
    assert(find_date('01 Jan 2009') == (0, 11, date(2009, 1, 1)))
    assert(find_date('1 jan 2009')  == (0, 10, date(2009, 1, 1)))
    assert(find_date('jan 1, 2009')  == (0, 11, date(2009, 1, 1)))
    assert(find_date('Mar 22, 2006')  == (0, 12, date(2006, 3, 22)))
    assert(find_date('v6.0 Mar 22, 2006')  == (5, 17, date(2006, 3, 22)))
    assert(find_date('01-Jan-2009') == (0, 11, date(2009, 1, 1)))
    assert(find_date('Jan 01, 2009') == (0, 12, date(2009, 1, 1)))
    assert(find_date('January 01, 2009') == (0, 16, date(2009, 1, 1)))
    assert(find_date('January 01 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('01 January 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('1 January 2009') == (0, 14, date(2009, 1, 1)))
    assert(find_date('January 1 2009') == (0, 14, date(2009, 1, 1)))
    assert(find_date('January 1, 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('2009-Jan-01') == (0, 11, date(2009, 1, 1)))
    assert(find_date('1998-Aug-28') == (0, 11, date(1998, 8, 28)))
    assert(find_date('1970-January-31') == (0, 15, date(1970, 1, 31)))
    assert(find_date('2525 Dec 20') == (0, 11, date(2525, 12, 20)))
    assert(find_date('2999 May 8') == (0, 10, date(2999, 5, 8)))
    assert(find_date('9 Aug 09') == (0, 8, date(2009, 8, 9)))
    assert(find_date('18_Mar_81') == (0, 9, date(1981, 3, 18)))
    assert(find_date('29may2003') == (0, 9, date(2003, 5, 29)))
    assert(find_date('2003may29') == (0, 9, date(2003, 5, 29)))
    assert(find_date('libapreq 2012-06-13') == (9, 19, date(2012, 6, 13)))
    assert(find_date('3.0.77') is None)
    assert(find_date('2.6.10.77') is None)
    assert(find_date('mini_httpd/1.19 19dec2003') == (16, 25, date(2003, 12, 19)))
    assert(find_date('26may2002') == (0, 9, date(2002, 5, 26)))
    assert(find_date('Mar 10 2007') == (0, 11, date(2007, 3, 10)))

    # TODO fill in year if implied - check month/day before/after today

    assert(human_to_timedelta('0') == timedelta(0))
    assert(human_to_timedelta('1') == timedelta(1))
    assert(human_to_timedelta('12345') == timedelta(12345))
    assert(human_to_timedelta('0d') == timedelta(0))
    assert(human_to_timedelta('1d') == timedelta(1))
    assert(human_to_timedelta('1 d') == timedelta(1))
    assert(human_to_timedelta('1 D') == timedelta(1))
    assert(human_to_timedelta('1 day') == timedelta(1))
    assert(human_to_timedelta('1y') == timedelta(365))
    assert(human_to_timedelta('1year') == timedelta(365))
    assert(human_to_timedelta('1 year') == timedelta(365))
    assert(human_to_timedelta('1Y') == timedelta(365))
    assert(human_to_timedelta('1 YEAR') == timedelta(365))
    assert(human_to_timedelta('1 YEAR') == timedelta(365))
    assert(human_to_timedelta('1y1d') == timedelta(366))
    assert(human_to_timedelta('1y,1d') == timedelta(366))
    assert(human_to_timedelta('1y10d') == timedelta(375))
    assert(human_to_timedelta('1y, 10d') == timedelta(375))
    assert(human_to_timedelta('1 year, 10 days') == timedelta(375))
    assert(human_to_timedelta('10 years') == timedelta(3650))
    assert(human_to_timedelta('10years') == timedelta(3650))
    assert(human_to_timedelta('10y') == timedelta(3650))
    assert(human_to_timedelta('1 y, 0m, 2 d') == timedelta(367))
    assert(human_to_timedelta('0d, 0m, 1y') == timedelta(365))
    assert(human_to_timedelta('0m, 1 years, 0d') == timedelta(365))
    assert(human_to_timedelta('1m') == timedelta(30))
    assert(human_to_timedelta('2m') == timedelta(60))
    assert(human_to_timedelta('6m') == timedelta(180))
    assert(human_to_timedelta('12m') == timedelta(360))
    assert(human_to_timedelta('24m') == timedelta(720))
    assert(human_to_timedelta('24m') == human_to_timedelta('1y11m25d'))
    assert(human_to_timedelta('1y12m') == human_to_timedelta('725d'))
    assert(human_to_timedelta('1d 1m 1y') == timedelta(396))
    assert(human_to_timedelta('1d 12m 1y') == timedelta(726))
    assert(human_to_timedelta('1d 12m 1y') == human_to_timedelta('726d'))

    assert(timedelta_to_human(timedelta(0)) == '0 days')
    assert(timedelta_to_human(timedelta(1)) == '1 day')
    assert(timedelta_to_human(timedelta(2)) == '2 days')
    assert(timedelta_to_human(timedelta(30)) == '1 month')
    assert(timedelta_to_human(timedelta(31)) == '1 month, 1 day')
    assert(timedelta_to_human(timedelta(59)) == '1 month, 29 days')
    assert(timedelta_to_human(timedelta(60)) == '2 months')
    assert(timedelta_to_human(timedelta(180)) == '6 months')
    assert(timedelta_to_human(timedelta(360)) == '12 months')
    assert(timedelta_to_human(timedelta(364)) == '12 months, 4 days')
    assert(timedelta_to_human(timedelta(365)) == '1 year')
    assert(timedelta_to_human(timedelta(366)) == '1 year, 1 day')
    assert(timedelta_to_human(timedelta(729)) == '1 year, 12 months, 4 days')
    assert(timedelta_to_human(timedelta(730)) == '2 years')
    assert(timedelta_to_human(timedelta(760)) == '2 years, 1 month')
    assert(timedelta_to_human(timedelta(789)) == '2 years, 1 month, 29 days')
    assert(timedelta_to_human(timedelta(3650)) == '10 years')

    h2td = human_to_timedelta
    td2h = timedelta_to_human
    assert(td2h( h2td('1y') ) == '1 year')
    assert(td2h( h2td('1y1m1d') ) == '1 year, 1 month, 1 day')
    assert(td2h( h2td('1y, 0 months, 20DAYS') ) == '1 year, 20 days')

    assert(h2td( td2h(timedelta(0)) ) == timedelta(0))
    assert(h2td( td2h(timedelta(1)) ) == timedelta(1))
    assert(h2td( td2h(timedelta(2)) ) == timedelta(2))
    assert(h2td( td2h(timedelta(30)) ) == timedelta(30))
    assert(h2td( td2h(timedelta(59)) ) == timedelta(59))
    assert(h2td( td2h(timedelta(180)) ) == timedelta(180))
    assert(h2td( td2h(timedelta(360)) ) == timedelta(360))
    assert(h2td( td2h(timedelta(365)) ) == timedelta(365))
    assert(h2td( td2h(timedelta(366)) ) == timedelta(366))
    assert(h2td( td2h(timedelta(719)) ) == timedelta(719))
    assert(h2td( td2h(timedelta(720)) ) == timedelta(720))
    assert(h2td( td2h(timedelta(724)) ) == timedelta(724))
    assert(h2td( td2h(timedelta(725)) ) == timedelta(725))
    assert(h2td( td2h(timedelta(730)) ) == timedelta(730))


def test_versionpart():
    p = VersionPart(0)
    assert(p == 0)
    assert(p == '0')
    assert(p == VersionPart(0))
    assert(p == VersionPart('0'))
    assert(p != VersionPart('00'))
    assert(p != '00')
    assert(p != 1)
    assert(p != '1')
    assert(p != VersionPart(1))
    assert(p != VersionPart('1'))
    assert(p != '01')
    assert(p != VersionPart(01))
    assert(p != VersionPart('01'))

    p = VersionPart('0')
    assert(p == 0)
    assert(p == '0')
    assert(p == VersionPart(0))
    assert(p == VersionPart('0'))
    assert(p != VersionPart('00'))
    assert(p != '00')
    assert(p != 1)
    assert(p != '1')
    assert(p != VersionPart(1))
    assert(p != VersionPart('1'))
    assert(p != '01')
    assert(p != VersionPart(01))
    assert(p != VersionPart('01'))

    p = VersionPart('00')
    assert(p == 0)
    assert(p == VersionPart('00'))
    assert(p != '0')
    assert(p != VersionPart('0'))
    assert(p != 1)
    assert(p != '1')
    assert(p != VersionPart('1'))
    assert(p != '01')
    assert(p != VersionPart('01'))

    p = VersionPart('01')
    assert(p == 1)
    assert(p == '01')
    assert(p == VersionPart('01'))
    assert(p != '1')
    assert(p != '001')
    assert(p != VersionPart('001'))

    p = VersionPart(1)
    assert(p == 1)
    assert(p == '1')
    assert(p == VersionPart('1'))
    assert(p != 0)
    assert(p != '0')
    assert(p != VersionPart('0'))
    assert(p != '01')
    assert(p != VersionPart('01'))

    p1 = VersionPart(1)
    assert(p1 < 2)
    assert(p1 <= 2)
    assert(2 > p1)
    assert(2 >= p1)
    assert(p1 < '2')
    assert(p1 < 'foo')
    assert('2' > p1)
    assert('foo' > p1)

    p2 = VersionPart(2)
    assert(p1 < p2)
    assert(p1 <= p2)
    assert(p2 > p1)
    assert(p2 >= p1)


def test_versionparts():
    assert_raises(TypeError, lambda: VersionParts())
    assert_raises(TypeError, lambda: VersionParts())
    assert_raises(TypeError, lambda: VersionParts(max_length=0))
    assert_raises(TypeError, lambda: VersionParts(1,2,3))
    #assert_raises(TypeError, lambda: VersionParts(1,2,3, max_length=0))
    #assert_raises(IndexError, lambda: VersionParts(1,2, max_length=1))
    #assert_raises(IndexError, lambda: VersionParts(1,2,3, max_length=2))
    #args = [1] * 101
    #assert_raises(IndexError, lambda: VersionParts(*args, max_length=100))

    vp = VersionParts(max_length=1)
    assert(len(vp) == 0)
    vp = VersionParts(max_length=100)
    assert(len(vp) == 0)
    vp = VersionParts(0, max_length=1)
    assert(len(vp) == 1)

    vp = VersionParts(1,2,3, max_length=9)
    assert(len(vp) == 3)
    assert(vp[0] == 1)
    assert(vp[0] == '1')
    assert(vp[1] == 2)
    assert(vp[1] == '2')
    assert(vp[2] == 3)
    assert(vp[2] == '3')
    with assert_raises(IndexError):
        vp[9] = 10

    vp[0] = 50
    assert(vp[0] == 50)
    assert(vp == [50, 2, 3])
    assert(50 in vp)
    vp.append('test4')
    assert(len(vp) == 4)
    assert(vp == [50, 2, 3, 'test4'])
    assert(vp == VersionParts(50, 2, 3, 'test4', max_length=1000))

    vp = VersionParts(1, 2, 3, max_length=9)
    assert(len(vp) == 3)
    vp[6] = 7
    assert(len(vp) == 7)
    assert(vp == [1, 2, 3, 0, 0, 0, 7])
    assert(vp == VersionParts(1, 2, 3, 0, 0, 0, 7, max_length=100))

    vp = VersionParts(1,2,3, max_length=9)
    assert(len(vp) == 3)
    assert(2 in vp)
    del vp[1]
    assert(2 not in vp)
    assert(len(vp) == 2)
    assert(vp == [1, 3])
    assert(vp == VersionParts(1, 3, max_length=100))

    vp = VersionParts(0, 1, '2a6', max_length=9)
    assert(len(vp) == 3)
    assert(vp == [0, 1, '2a6'])

    vp[2] = 2
    assert(len(vp) == 3)
    assert(vp[2] == 2)

    vp[2] = '0-alpha4'
    assert(len(vp) == 3)
    assert(vp[2] == '0-alpha4')

    # vp = VersionParts( VersionParts(1,2,3, max_length=9), max_length=9)
    # assert(len(vp) == 3)
    # assert(vp == [1, 2, 3])
    # assert(vp == VersionParts(1, 2, 3, max_length=100))

    vp = VersionParts(1,2,3, max_length=9)
    assert(vp[0] == 1)
    assert(vp[1] == 2)
    assert(vp[2] == 3)
    assert(vp[3] == 0)
    assert(vp[4] == 0)
    assert(vp[5] == 0)
    assert(vp[6] == 0)
    assert(vp[7] == 0)
    assert(vp[8] == 0)
    del vp[1]
    assert(vp[1] == 3)
    vp[8] = 99
    assert(vp[8] == 99)
    del vp[8]
    assert(vp[8] == 0)

    #TODO slicing


def test_versionparts_compare():
    # Equalities
    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 0, 0, 0, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(0, max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(0, 1, max_length=9)
    vp2 = VersionParts(0, 1, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(0, 1, 'test4', max_length=9)
    vp2 = VersionParts(0, 1, 'test4', max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    vp1 = VersionParts(0, 1, 2, 3, 4, 5, 6, 7, 8, max_length=9)
    vp2 = VersionParts(0, 1, 2, 3, 4, 5, 6, 7, 8, max_length=9)
    assert(vp1 == vp2)
    assert(vp2 == vp1)

    # Inequalities
    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(1, 0, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(1, 0, 0, 0, 0, 0, 0, 0, 0, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts('4', max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts('foo6', max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 1, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 1, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 0, 0, 1, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 0, 0, 'foo', max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(0, max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    vp1 = VersionParts(0, 1, max_length=9)
    vp2 = VersionParts(0, 1, 2, max_length=9)
    assert(vp1 != vp2)
    assert(vp2 != vp1)

    # Numeric comparison
    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 0, 0, 1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 0, 0, 'foo', max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 1, max_length=9)
    vp2 = VersionParts(0, 1, 2, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 1, max_length=9)
    vp2 = VersionParts(0, 1, 2, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 1, 2, max_length=9)
    vp2 = VersionParts(0, 1, 2, 3, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 0, 0, 0, 0, 0, 1, 2, 3, max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 0, 0, 0, 0, 0, 1, 2, 3, max_length=9)
    vp2 = VersionParts(0, 0, 0, 0, 0, 0, 2, 2, 3, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'a', max_length=9)
    vp2 = VersionParts(0, 'b', max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'a', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'alpha', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'b', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'beta', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'c', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'rc', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(0, 'pre', max_length=9)
    vp2 = VersionParts(0, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(1, 'pre', max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(1, '0pre', max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    vp1 = VersionParts(1, '7pre9', max_length=9)
    vp2 = VersionParts(1, max_length=9)
    assert(vp1 < vp2)
    assert(vp1 <= vp2)
    assert(vp2 > vp1)
    assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 'rc11'], max_length=9)
    # vp2 = VersionParts([1], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 0, 0, 'rc11'], max_length=9)
    # vp2 = VersionParts([1], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, '3a'], max_length=9)
    # vp2 = VersionParts([1, 3, 3], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, '3a'], max_length=9)
    # vp2 = VersionParts([1, 3, 4], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 2], max_length=9)
    # vp2 = VersionParts([1, 3, '3a'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 'alpha'], max_length=9)
    # vp2 = VersionParts([1, 3, 2], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 'foo'], max_length=9)
    # vp2 = VersionParts([1, 3, 2], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'dev'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'alpha'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'devel'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'alpha'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'dev'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'beta'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'devel'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'beta'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'devel'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'c'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'dev'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'c'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'dev'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'rc'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'dev'], max_length=9)
    # vp2 = VersionParts([1, 3, 0, 'pre'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)

    # vp1 = VersionParts([1, 3, 0, 'pre'], max_length=9)
    # # really 1.3.0.6
    # vp2 = VersionParts([1, 3, 0, '6dev8'], max_length=9)
    # assert(vp1 < vp2)
    # assert(vp1 <= vp2)
    # assert(vp2 > vp1)
    # assert(vp2 >= vp1)


def test_instantiation():
    # Accept empty - fill in progressively
    v = Version()
    assert(v.name  is None)
    assert(v.major is 0)
    assert(v.minor is 0)
    assert(v.micro is 0)
    assert(v.nano  is 0)
    assert(v.pico  is 0)
    assert(v.femto is 0)
    assert(v.atto  is 0)
    assert(v.zepto is 0)
    assert(v.yocto is 0)
    assert(v.parts == [])
    assert(str(v) == '')

    # Single string arg just sets name
    v = Version('foobar')
    assert(v.name  == 'foobar')
    assert(v.major is 0)
    assert(v.minor is 0)
    assert(v.micro is 0)
    assert(v.nano  is 0)
    assert(v.pico  is 0)
    assert(v.femto is 0)
    assert(v.atto  is 0)
    assert(v.zepto is 0)
    assert(v.yocto is 0)
    assert(v.parts == [])
    assert(str(v) == 'foobar')

    # As does single kw
    v = Version(name='foobar')
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(v.micro == 0)
    assert(v.nano  == 0)
    assert(v.pico  == 0)
    assert(v.femto == 0)
    assert(v.atto  == 0)
    assert(v.zepto == 0)
    assert(v.yocto == 0)
    assert(v.parts == [])
    assert(str(v) == 'foobar')


def test_basic_api():

    # Allow name-less versions
    v = Version(0)
    assert(v.name is None)
    assert(v.parts[1] == 0)
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(v.micro == 0)
    assert(v.nano  == 0)
    assert(v.pico  == 0)
    assert(v.femto == 0)
    assert(v.atto  == 0)
    assert(v.zepto == 0)
    assert(v.yocto == 0)
    assert(v.parts == [0])
    assert(str(v) == '0')

    v = Version()
    v.major = 0
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(v.parts == [0])
    assert(str(v) == '0')

    v = Version(0, 1)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 0)
    assert(v.parts == [0, 1])
    assert(str(v) == '0.1')

    v = Version()
    v.major = 0
    v.minor = 1
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 0)
    assert(v.parts == [0, 1])
    assert(str(v) == '0.1')

    v = Version(0, 1, 2)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(v.parts[2] == 2)
    assert(v.parts == [0, 1, 2])
    assert(str(v) == '0.1.2')

    v = Version()
    v.major = 0
    v.minor = 1
    v.micro = 2
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(v.parts == [0, 1, 2])
    assert(str(v) == '0.1.2')

    v = Version(0, 1, 2, 3)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 0)
    assert(v.parts == [0, 1, 2, 3])
    assert(str(v) == '0.1.2.3')

    v = Version()
    v.major = 0
    v.minor = 1
    v.micro = 2
    v.nano  = 3
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 0)
    assert(v.parts == [0, 1, 2, 3])
    assert(str(v) == '0.1.2.3')

    v = Version(0, 1, 2, 3, 4)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 0)
    assert(v.parts == [0,1,2,3,4])
    assert(str(v) == '0.1.2.3.4')

    v = Version()
    v.major = 0
    v.minor = 1
    v.micro = 2
    v.nano  = 3
    v.pico  = 4
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 0)
    assert(v.parts == [0,1,2,3,4])
    assert(str(v) == '0.1.2.3.4')

    v = Version(0, 1, 2, 3, 4, 5, 6, 7, 8)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 5)
    assert(v.atto  == 6)
    assert(v.zepto == 7)
    assert(v.yocto == 8)
    assert(v.parts[8] == 8)
    assert(v.parts == [0,1,2,3,4,5,6,7,8])
    assert(str(v) == '0.1.2.3.4.5.6.7.8')

    # Extra positional args get ignored
    v = Version(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 5)
    assert(v.atto  == 6)
    assert(v.zepto == 7)
    assert(v.yocto == 8)
    assert(v.parts == [0,1,2,3,4,5,6,7,8])
    assert(str(v) == '0.1.2.3.4.5.6.7.8')

    # Setting parts explicitly also means extra are ignored
    v = Version()
    v.parts = (0,1,2,3,4,5,6,7,8,9,10,11)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 5)
    assert(v.atto  == 6)
    assert(v.zepto == 7)
    assert(v.yocto == 8)
    assert(v.parts == [0,1,2,3,4,5,6,7,8])
    assert(str(v) == '0.1.2.3.4.5.6.7.8')

    v = Version()
    v.parts = [0,1,2,3,4,5,6,7,8,9,10,11]
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 5)
    assert(v.atto  == 6)
    assert(v.zepto == 7)
    assert(v.yocto == 8)
    assert(v.parts == [0,1,2,3,4,5,6,7,8])
    assert(str(v) == '0.1.2.3.4.5.6.7.8')

    # Assign components positionally with .parts
    v = Version(0, 1, 2)
    assert(v.name  is None)
    assert(v.major == 0)
    v.parts[0] = 3
    assert(v.major == 3)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.parts == [3,1,2])
    assert(str(v) == '3.1.2')

    # Allow named versions with name as first arg, rest positional
    v = Version('foobar', 0, 1, 2)
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,2])
    assert(str(v) == 'foobar 0.1.2')

    # Allow named args
    v = Version(name='foobar', major=1)
    assert(v.name  == 'foobar')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.parts == [1])
    assert(str(v) == 'foobar 1')

    # Coerce type where appropriate
    v = Version(name='foobar', major='1')
    assert(v.name  == 'foobar')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.parts == [1])
    assert(str(v) == 'foobar 1')

    v = Version(major=0, minor=1, micro=4)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 4)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,4])
    assert(str(v) == '0.1.4')

    # Support _str args
    v = Version(name='foobar', major=0, minor=1, micro=4, suffix_str='asd')
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 4)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,4])
    assert(v.suffix_str == 'asd')
    assert(str(v) == 'foobar 0.1.4 asd')

    v = Version(name='foobar', major=0, minor=1, micro=4, prefix_str='v/')
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 4)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,4])
    assert(v.prefix_str == 'v/')
    assert(str(v) == 'foobar v/0.1.4')

    # Support build_meta
    v = Version(name='foobar', major=0, minor=1, build_meta='20090106')
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 0)
    assert(v.parts == [0,1])
    assert(v.build_meta == '20090106')
    assert(str(v) == 'foobar 0.1+20090106')


    # Allow combined
    v = Version(0, 1, 2, name='foobar')
    assert(v.name  == 'foobar')
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,2])
    assert(str(v) == 'foobar 0.1.2')

    # Single string arg gets parsed
    s = '0.1.2'
    v = Version(s)
    assert(v.name is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(v.parts == [0,1,2])
    assert(str(v) == s)

    # And with name
    #s = 'foobar 0.1.2'
    #v = Version(s)
    #assert(v.name == 'foobar')
    #assert(v.major == 0)
    #assert(v.minor == 1)
    #assert(v.micro == 2)
    #assert(v.nano  is None)
    #assert(v.version == (0,1,2))
    #assert(str(v) == s)

    # 'patch' is a synonym for 'micro'
    v = Version(0, 1, 2)
    assert(v.micro == 2)
    assert(v.patch == 2)
    assert(v.parts == [0,1,2])
    assert(str(v) == '0.1.2')

    v = Version(0, 1, 2)
    v.patch = 5
    assert(v.parts == [0,1,5])
    assert(str(v) == '0.1.5')


#    v = Version(major=0, minor=1, patch=2)
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 1)
#    assert(v.micro == 2)
#    assert(v.patch == 2)
#    assert(v.nano  is None)
#    assert(v.version == (0,1,2))
#    assert(str(v) == '0.1.2')
#
#    v.patch = None
#    assert(v.micro is None)
#    assert(v.patch is None)
#
#    v.micro = 5
#    assert(v.micro == 5)
#    assert(v.patch == 5)
#
#    x = lambda: Version(major=0, minor=1, micro=1, patch=1)
#    assert_raises(VersionInitError, x)
#    x = lambda: Version(major=0, minor=1, micro=1, patch=2)
#    assert_raises(VersionInitError, x)
#
#    x = lambda: Version(0, 1, 2, patch=2)
#    assert_raises(VersionInitError, x)
#    x = lambda: Version(0, 1, 2, patch=3)
#    assert_raises(VersionInitError, x)
#
#    # Change name separator
#    v = Version('foobar', 0, 1, name_sep='_')
#    assert(v.name  == 'foobar')
#    assert(v.major == 0)
#    assert(v.minor == 1)
#    assert(v.micro is None)
#    assert(v.version == (0,1))
#    assert(str(v) == 'foobar_0.1')
#
#    v = Version('foobar', 0, 1)
#    v.name_sep = '_'
#    assert(str(v) == 'foobar_0.1')
#
#    # Does nothing if no name set
#    v = Version(0, 1, name_sep='_')
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 1)
#    assert(v.version == (0,1))
#    assert(str(v) == '0.1')
#
#    # Change version separator
#    v = Version(0, 1, 2, version_sep='_')
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 1)
#    assert(v.micro == 2)
#    assert(v.nano  is None)
#    assert(v.version == (0,1,2))
#    assert(str(v) == '0_1_2')
#
#    v = Version(0, 1, 2)
#    v.version_sep = '_'
#    assert(str(v) == '0_1_2')
#
#    # Does nothing if no minor ->
#    v = Version(0, version_sep='_')
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor is None)
#    assert(v.version == (0,))
#    assert(str(v) == '0')
#
#    #
#
#
def test_parse_pure():
    s = '0'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(str(v) == s)

    s = '0.1'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 0)
    assert(str(v) == s)

    s = '0.1.2'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(str(v) == s)

    s = '0_1_2'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 0)
    assert(str(v) == s)

    s = '0.1.2.3'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 0)
    assert(str(v) == s)

    s = '0.1.2.3.4.5.6.7.8'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 1)
    assert(v.micro == 2)
    assert(v.nano  == 3)
    assert(v.pico  == 4)
    assert(v.femto == 5)
    assert(v.atto  == 6)
    assert(v.zepto == 7)
    assert(v.yocto == 8)
    assert(str(v) == s)

    # Zero prefixes
    s = '0.01'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '01')
    assert(v.micro == 0)
    assert(v.parts == [0, '01'])
    assert(str(v) == s)

    s = '0.0.01'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(v.micro == '01')
    assert(v.parts == [0, 0, '01'])
    assert(str(v) == s)

    s = '0.00.01'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '00')
    assert(v.micro == '01')
    assert(v.parts == [0, '00', '01'])
    assert(str(v) == s)

    s = '8.009.0003.5.000003'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 8)
    assert(v.minor == '009')
    assert(v.micro == '0003')
    assert(v.nano  == 5)
    assert(v.pico  == '000003')
    assert(v.parts == [8, '009', '0003', 5, '000003'])
    assert(str(v) == s)

    # Alpha, beta, rc, etc
    s = '0.1a'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1a')
    assert(v.micro == 0)
    assert(v.parts == [0, '1a'])
    assert(str(v) == s)

    s = '0.1alpha'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1alpha')
    assert(v.micro == 0)
    assert(v.parts == [0, '1alpha'])
    assert(str(v) == s)

    s = '0.1-alpha'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1-alpha')
    assert(v.micro == 0)
    assert(v.parts == [0, '1-alpha'])
    assert(str(v) == s)

    s = '0.1a5'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1a5')
    assert(v.micro == 0)
    assert(v.parts == [0, '1a5'])
    assert(str(v) == s)

    s = '0.1-alpha6'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1-alpha6')
    assert(v.micro == 0)
    assert(v.parts == [0, '1-alpha6'])
    assert(str(v) == s)

    s = '0.1-alpha-6'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == '1-alpha-6')
    assert(v.micro == 0)
    assert(v.parts == [0, '1-alpha-6'])
    assert(str(v) == s)

    s = '1.3.3a'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 1)
    assert(v.minor == 3)
    assert(v.micro == '3a')
    assert(v.nano  == 0)
    assert(v.parts == [1, 3, '3a'])
    assert(v.parts == ['1', '3', '3a'])
    assert(str(v) == s)

    s = '2.23beta1'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 2)
    assert(v.minor == '23beta1')
    assert(v.micro == 0)
    assert(v.parts == [2, '23beta1'])
    assert(v.parts == ['2', '23beta1'])
    assert(str(v) == s)

    s = '0.0.8pre17'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 0)
    assert(v.micro == '8pre17')
    assert(v.nano  == 0)
    assert(v.parts == [0, 0, '8pre17'])
    assert(v.parts == ['0', '0', '8pre17'])
    assert(str(v) == s)

#    s = '0.0.8.4pre17'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 0)
#    assert(v.micro == 8)
#    assert(v.nano  == '4pre17')
#    assert(v.version == (0, 0, 8, '4pre17'))
#    assert(str(v) == s)
#
#    s = '2.6.27-rc4'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 2)
#    assert(v.minor == 6)
#    assert(v.micro == '27-rc4')
#    assert(v.nano  is None)
#    assert(v.version == (2, 6, '27-rc4'))
#    assert(str(v) == s)
#
#    s = '2.6.0-test4'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 2)
#    assert(v.minor == 6)
#    assert(v.micro == '0-test4')
#    assert(v.nano  is None)
#    assert(v.version == (2, 6, '0-test4'))
#    assert(str(v) == s)
#
#
    # SSH special case
    s = '6.2p5'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 6)
    assert(v.minor == 2)
    assert(v.micro == 5)
    assert(v.parts == [6, 2, 5])
    assert(str(v) == s)

    s = '1-1'
    assert_raises(VersionParseError, lambda: Version.parse_pure(s))

    s = '1.2-1'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 1)
    assert(v.minor == '2-1')
    assert(v.parts == [1, '2-1'])
    assert(v.parts == ['1', '2-1'])
    assert(str(v) == s)
#
#    s = '1.2.3-1'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 1)
#    assert(v.minor == 2)
#    assert(v.micro == '3-1')
#    assert(v.version == (1, 2, '3-1'))
#    assert(str(v) == s)
#
    s = '4.3-Hipserv'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 4)
    assert(v.minor == '3-Hipserv')
    assert(v.micro == 0)
    assert(v.parts == [4, '3-Hipserv'])
    assert(str(v) == s)

    s = '1.12_15'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 1)
    assert(v.minor == 12)
    assert(v.micro == 15)
    assert(v.nano  == 0)
    assert(v.parts == [1, 12, 15])
    assert(str(v) == s)
#
#    s = '1.12_15_99'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 1)
#    assert(v.minor == 12)
#    assert(v.micro == 15)
#    assert(v.nano  == 99)
#    assert(v.version == (1, 12, 15, 99))
#    assert(str(v) == s)
#
    s = '1_12_15'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 1)
    assert(v.minor == 12)
    assert(v.micro == 15)
    assert(v.nano  == 0)
    assert(v.parts == [1, 12, 15])
    assert(str(v) == s)

    s = '0.44_01'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 0)
    assert(v.minor == 44)
    assert(v.micro == 1)
    assert(v.micro == '01')
    assert(v.nano == 0)
    assert(v.parts == [0, 44, '01'])
    assert(str(v) == s)

    s = '2.6.27.10'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 2)
    assert(v.minor == 6)
    assert(v.micro == 27)
    assert(v.nano  == 10)
    assert(v.pico  == 0)
    assert(v.parts == [2, 6, 27, 10])
    assert(str(v) == s)
#
#    s = 'v3'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 3)
#    assert(v.minor is None)
#    assert(v.version == (3,))
#    assert(v.prefix_str == 'v')
#    assert(str(v) == s)
#
#    s = 'v3.1'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 3)
#    assert(v.minor == 1)
#    assert(v.micro is None)
#    assert(v.version == (3, 1))
#    assert(v.prefix_str == 'v')
#    assert(str(v) == s)
#
    s = 'v3.10.0'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 3)
    assert(v.minor == 10)
    assert(v.micro == 0)
    assert(v.nano  == 0)
    assert(v.parts == [3, 10, 0])
    assert(v.prefix_str == 'v')
    assert(str(v) == s)
#
#    s = 'v2205'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 2205)
#    assert(v.minor is None)
#    assert(v.version == (2205,))
#    assert(v.prefix_str == 'v')
#    assert(str(v) == s)
#
#    s = 'V0.0.1'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 0)
#    assert(v.micro == 1)
#    assert(v.nano  is None)
#    assert(v.version == (0, 0, 1))
#    assert(v.prefix_str == 'V')
#    assert(str(v) == s)
#
    s = '5.0.91-log'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 5)
    assert(v.minor == 0)
    assert(v.micro == '91-log')
    assert(v.nano  == 0)
    assert(v.parts == [5, 0, '91-log'])
    assert(str(v) == s)
#
#    s = '12.1.99900.0'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 12)
#    assert(v.minor == 1)
#    assert(v.micro == 99900)
#    assert(v.nano  == 0)
#    assert(v.pico  is None)
#    assert(v.version == (12, 1, 99900, 0))
#    assert(str(v) == s)
#
#    s = '1.4.28-devel-4979'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 1)
#    assert(v.minor == 4)
#    assert(v.micro == '28-devel-4979')
#    assert(v.nano  is None)
#    assert(v.version == (1, 4, '28-devel-4979'))
#    assert(str(v) == s)
#
#    s = 'R6_0_1'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 6)
#    assert(v.minor == 0)
#    assert(v.micro == 1)
#    assert(v.nano  is None)
#    assert(v.version == (6, 0, 1))
#    assert(v.prefix_str == 'R')
#    assert(str(v) == s)
#
#    s = '1.0.0-fips'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 1)
#    assert(v.minor == 0)
#    assert(v.micro == '0-fips')
#    assert(v.nano  is None)
#    assert(v.version == (1, 0, '0-fips'))
#    assert(str(v) == s)
#
#    s = '4.4.4-8+etch6'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 4)
#    assert(v.minor == 4)
#    assert(v.micro == '4-8')
#    assert(v.nano  is None)
#    assert(v.version == (4, 4, '4-8'))
#    assert(v.build_meta == 'etch6')
#    assert(str(v) == s)
#
    s = '3.0.STABLE20'
    v = Version.parse_pure(s)
    assert(v.name  is None)
    assert(v.major == 3)
    assert(v.minor == 0)
    assert(v.micro == 'STABLE20')
    assert(v.nano  == 0)
    assert(v.parts == [3, 0, 'STABLE20'])
    assert(str(v) == s)
#
#    s = '1.3.26.1a'
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 1)
#    assert(v.minor == 3)
#    assert(v.micro == 26)
#    assert(v.nano  == '1a')
#    assert(v.version == (1, 3, 26, '1a'))
#    assert(str(v) == s)
#
#    s = '0.9.8e-fips-rhel5'     # TODO comparisons
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 0)
#    assert(v.minor == 9)
#    assert(v.micro == '8e-fips-rhel5')
#    assert(v.nano  is None)
#    assert(v.version == (0, 9, '8e-fips-rhel5'))
#    assert(str(v) == s)
#
#    s = '5.0 Build 11'      # TODO comparisons
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 5)
#    assert(v.minor == 0)
#    assert(v.micro == 'Build')
#    assert(v.nano  == 11)
#    assert(v.pico  is None)
#    assert(v.version == (5, 0, 'Build', 11))
#    assert(str(v) == s)
#
#    s = '2.0 Beta 2'        # TODO comparisons
#    v = Version.parse_pure(s)
#    assert(v.name  is None)
#    assert(v.major == 2)
#    assert(v.minor == 0)
#    assert(v.micro == 'Beta')
#    assert(v.nano  == 2)
#    assert(v.pico  is None)
#    assert(v.version == (2, 0, 'Beta', 2))
#    assert(str(v) == s)

    s = '5.19.1.1387.2314'

    s = 'v2.2.13-Debian-2.2.13-14+lenny3'   # TODO extraction

    s = '8.05 4000-1'   # TODO extraction

    s = 'v2.3.7-Invoca-RPM-2.3.7-12.el5_7.2'    # TODO extraction

    s = '0.94.14rc21'

    s = '2.11.4-final'

    s = '5.2.6-1+lenny15'

    s = '1.4.26-devel-6243M'

    s = '5.3.10-1ubuntu3.11'    # TODO extraction

    # TODO set version_obj


def test_compare_parsed_pure():

    # Equalities

    v1 = Version.parse_pure('0')
    v2 = Version.parse_pure('0')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    v1 = Version.parse_pure('0.1')
    v2 = Version.parse_pure('0.1')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    v1 = Version.parse_pure('0.1.2')
    v2 = Version.parse_pure('0.1.2')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    v1 = Version.parse_pure('0.1.2')
    v2 = Version.parse_pure('0_1_2')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    v1 = Version.parse_pure('0.1.2.3.4.5.6.7.8')
    v2 = Version.parse_pure('0.1.2.3.4.5.6.7.8')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    v1 = Version.parse_pure('0.1.2+foo')
    v2 = Version.parse_pure('0.1.2+bar')
    assert(v1 == v2)
    assert(v2 == v1)
    assert(hash(v1) == hash(v2))

    # Inequalities

    v1 = Version.parse_pure('0')
    v2 = Version.parse_pure('1')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))

    v1 = Version.parse_pure('0.0')
    v2 = Version.parse_pure('0.1')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))

    v1 = Version.parse_pure('0.0.0')
    v2 = Version.parse_pure('0.0.1')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))

    v1 = Version.parse_pure('0.1.2.3.4.5.6.7.8')
    v2 = Version.parse_pure('0.1.2.3.4.5.6.7.9')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))

    v1 = Version.parse_pure('0')
    v2 = Version.parse_pure('0.0.1')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))

    v1 = Version.parse_pure('0.0')
    v2 = Version.parse_pure('0.0.1')
    assert(v1 != v2)
    assert(v2 != v1)
    assert(hash(v1) != hash(v2))


# TODO check different names always compare unequal

def test_parse():
    s = 'foo 1.2'
    v = Version.parse(s)
    assert(v.name == 'foo')
    assert(v.major == 1)
    assert(v.minor == 2)
    assert(v.micro == 0)
    assert(v.parts == [1, 2])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'foo')
    assert(v.major == 1)
    assert(v.minor == 2)
    assert(v.micro == 0)
    assert(v.parts == [1, 2])
    assert(str(v) == s)

    s = 'linux-2.6.7-rc1'
    v = Version.parse(s)
    assert(v.name == 'linux')
    assert(v.major == 2)
    assert(v.minor == 6)
    assert(v.micro == '7-rc1')
    assert(v.parts == [2, 6, '7-rc1'])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'linux')
    assert(v.major == 2)
    assert(v.minor == 6)
    assert(v.micro == '7-rc1')
    assert(v.parts == [2, 6, '7-rc1'])
    assert(str(v) == s)

    s = 'openssl-fips-1.0.0'
    v = Version.parse(s)
    assert(v.name == 'openssl-fips')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.micro == 0)
    assert(v.parts == [1, 0, 0])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'openssl-fips')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.micro == 0)
    assert(v.parts == [1, 0, 0])
    assert(str(v) == s)

    s = 'Apache/2.2.15'
    v = Version.parse(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 15)
    assert(v.parts == [2, 2, 15])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 15)
    assert(v.parts == [2, 2, 15])
    assert(str(v) == s)

    s = 'Apache/2.2.23 (Unix) DAV/2'
    v = Version.parse(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 23)
    assert(v.parts == [2, 2, 23])
    assert(v.suffix_str == '(Unix) DAV/2')
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 23)
    assert(v.parts == [2, 2, 23])
    assert(v.suffix_str == '(Unix) DAV/2')
    assert(str(v) == s)

    s = 'Sun-ONE-Web-Server/6.1'
    v = Version.parse(s)
    assert(v.name == 'Sun-ONE-Web-Server')
    assert(v.major == 6)
    assert(v.minor == 1)
    assert(v.parts == [6, 1])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Sun-ONE-Web-Server')
    assert(v.major == 6)
    assert(v.minor == 1)
    assert(v.parts == [6, 1])
    assert(str(v) == s)

    s = 'Microsoft-IIS/8.0'
    v = Version.parse(s)
    assert(v.name == 'Microsoft-IIS')
    assert(v.major == 8)
    assert(v.minor == 0)
    assert(v.parts == [8, 0])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Microsoft-IIS')
    assert(v.major == 8)
    assert(v.minor == 0)
    assert(v.parts == [8, 0])
    assert(str(v) == s)

    s = 'mod_ssl/2.2.15'
    v = Version.parse(s)
    assert(v.name == 'mod_ssl')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 15)
    assert(v.parts == [2, 2, 15])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'mod_ssl')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 15)
    assert(v.parts == [2, 2, 15])
    assert(str(v) == s)

    s = 'Apache/2.2.23 (Unix) mod_jk/1.2.37'
    v = Version.parse(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 23)
    assert(v.parts == [2, 2, 23])
    assert(v.suffix_str == '(Unix) mod_jk/1.2.37')
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Apache')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 23)
    assert(v.parts == [2, 2, 23])
    assert(v.suffix_str == '(Unix) mod_jk/1.2.37')
    assert(str(v) == s)

    s = 'Apache Coyote/1.0'
    v = Version.parse(s)
    assert(v.name == 'Apache Coyote')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.parts == [1, 0])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'Apache Coyote')
    assert(v.major == 1)
    assert(v.minor == 0)
    assert(v.parts == [1, 0])
    assert(str(v) == s)

    s = 'lighttpd/1.4.26'
    v = Version.parse(s)
    assert(v.name == 'lighttpd')
    assert(v.major == 1)
    assert(v.minor == 4)
    assert(v.micro == 26)
    assert(v.parts == [1, 4, 26])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'lighttpd')
    assert(v.major == 1)
    assert(v.minor == 4)
    assert(v.micro == 26)
    assert(v.parts == [1, 4, 26])
    assert(str(v) == s)

    s = 'PHP/5.3.2-1ubuntu4.26 with Suhosin-Patch'
    v = Version.parse(s)
    assert(v.name == 'PHP')
    assert(v.major == 5)
    assert(v.minor == 3)
    assert(v.micro == '2-1ubuntu4.26')
    assert(v.parts == [5, 3, '2-1ubuntu4.26'])
    assert(v.suffix_str == 'with Suhosin-Patch')
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'PHP')
    assert(v.major == 5)
    assert(v.minor == 3)
    assert(v.micro == '2-1ubuntu4.26')
    assert(v.parts == [5, 3, '2-1ubuntu4.26'])
    assert(v.suffix_str == 'with Suhosin-Patch')
    assert(str(v) == s)

    s = 'openssl-fips-ecp-2.0.6'
    v = Version.parse(s)
    assert(v.name == 'openssl-fips-ecp')
    assert(v.major == 2)
    assert(v.minor == 0)
    assert(v.micro == 6)
    assert(v.parts == [2, 0, 6])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'openssl-fips-ecp')
    assert(v.major == 2)
    assert(v.minor == 0)
    assert(v.micro == 6)
    assert(v.parts == [2, 0, 6])
    assert(str(v) == s)

    s = 'dovecot 2.2.alpha1'
    v = Version.parse(s)
    assert(v.name == 'dovecot')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 'alpha1')
    assert(v.parts == [2, 2, 'alpha1'])
    assert(str(v) == s)

    v = Version(s)
    assert(v.name == 'dovecot')
    assert(v.major == 2)
    assert(v.minor == 2)
    assert(v.micro == 'alpha1')
    assert(v.parts == [2, 2, 'alpha1'])
    assert(str(v) == s)


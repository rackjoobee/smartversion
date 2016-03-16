smartversion 
============

Painlessly handle software version information.

smartversion is a library for handling version numbers. It can parse a wide variety of real-world version strings and is fully compatible with Semver 2.0.0. (PEP440 coming soon.)

Quickstart
----------

.. code-block:: pycon
   $ pip install smartversion
   $ python
   >>> from smartversion import Version
   >>> v = Version(0, 1, 4)
   >>> str(v)
   '0.1.4'

Full Demo:
----------

.. code-block:: pycon
    >>> from smartversion import Version

    # Store version data
    >>> v = Version(major=0, minor=1, patch=4)
    >>> v.major
    0
    >>> v.minor
    1
    >>> v.patch
    4
    >> str(v)
    '0.1.4'

    # Compare versions
    >>> v1 = Version(major=0, minor=1)
    >>> v2 = Version(major=0, minor=2)
    >>> str(v1)
    '0.1'
    >>> str(v2)
    '0.2'
    >>> v2 > v1
    True

    # Parse complex version strings
    >>> v = Version.parse('linux-2.4.6-rc1') 
    >>> v.name
    'linux'
    >>> v.major
    2
    >>> v.minor
    4
    >>> v.patch
    '6-rc1'
    >>> v.patch1
    6
    >>> v.patch_str
    '-rc'
    >>> v.patch2
    1

    # Compare complex versions
    >>> v1 = Version.parse('linux-2.4.6-rc1')
    >>> v2 = Version.parse('linux-2.4.6-rc4')
    >>> v3 = Version.parse('linux-2.4.6')
    >>> str(v1)
    'linux-2.4.6-rc1'
    >>> str(v2)
    'linux-2.4.6-rc4'
    >>> v1 < v2
    True
    >>> str(v2)
    'linux-2.4.6-rc4'
    >>> str(v3)
    'linux-2.4.6'
    >>> v2 < v3
    True    # yes, the release candidate comes first :o)

    # You can also set version parameters positionally
    >>> v = Version("Bob's Amazing Software", 1, 0, 1)
    >>> str(v)
    "Bob's Amazing Software 1.0.1"

    ...

smartversion is like a combination of LooseVersion from distutils and parse_version from setuptools. It was written to handle various real-world version strings that LooseVersion cannot. smartversion also does age-based comparisons based on a release date and comes with an extremely long-winded test suite. 

Above all, smartversion aims to be *useful*. It's in the category of libraries that abstract lots of messy, real-world cases into a clean interface.

This was originally written to help with network security auditing, because version data is messy and very annoying. But it has applications beyond that, hence the separate library.

Features
--------

- Parses an enormous range of version formats (lots of 'in-the-wild')
- Fully compatible with Semver 2.0.0
- Python 2.7, 3+
- Version objects compare properly (==, !=, <, ...)
  - ... and obey Semver and (soon) PEP404 comparison rules as appropriate
- No extra-stdlib dependencies to install 
- Not only parses version numbers, but handles packages that put annoying
  shit between the package name and the version number. And gracefully.
  - If you doubt, read the test suite.
- Wildcards for comparison
- Version age comparison (based on release date)
- Human-friendly age comparison ('2 years, 3 months' / '2y3m')
- Reasonably quick
- Extensive test suite 

Coming soon
-----------

- Full PEP440 support
- Full unicode support
- i18n

Installation
------------

TODO coming soon

To install smartversion:

.. code-block:: bash

    $ pip install smartversion

Documentation
-------------

Coming soon (:S). For now, refer to this document and the test suite.

Warnings & Caveats
------------------

- API isn't 100% stable yet (until 1.0.0)
- When parsing real-world version strings, parsed data needs to be
  more granular if the version string doesn't exactly match Semver
  or PEP440
- The parser isn't deterministic. That is, it can't tell you whether 
  the string you're parsing matches some grammar, because there is
  no grammar. Instead the goal is "parse everything that could possibly 
  be parsed as a version and do what you want." 
- Age calculation code has no psychic powers. If you want to calculate
  the age of a software version, you have to supply the release date
  yourself (sorry).
- No i18n support (for now).

import pytest
import rpm
from rpmlint.pkg import parse_deps, rangeCompare

from Testing import get_tested_package


def test_parse_deps():
    for (arg, exp) in (
        ('a, b < 1.0 c = 5:2.0-3 d',
         [('a', 0, (None, None, None)),
          ('b', rpm.RPMSENSE_LESS, (None, '1.0', None)),
          ('c', rpm.RPMSENSE_EQUAL, (5, '2.0', '3')),
          ('d', 0, (None, None, None))]),
    ):
        assert parse_deps(arg) == exp


def test_range_compare():
    for (req, prov) in (
        (('foo', rpm.RPMSENSE_LESS, (None, '1.0', None)),
         ('foo', rpm.RPMSENSE_EQUAL, (1, '0.5', None))),
    ):
        assert not rangeCompare(req, prov)


@pytest.mark.parametrize('package', ['binary/python311-pytest-xprocess'])
def test_extract(package, tmp_path):
    get_tested_package(package, tmp_path)

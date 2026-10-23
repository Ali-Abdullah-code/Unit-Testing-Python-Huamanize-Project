"""
Unit tests for humanize.filesize module.
Module Author  : 24F-3109 Ali Abdullah
Functions Under Test:
    - humanize.naturalsize()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): decimal mode, binary mode, GNU mode, negative
    - Boundary Value Analysis (BVA): 0, 1 byte, 999/1000 byte boundaries, 1024 boundary
    - Parameterization: data-driven tables for all three modes
"""

import pytest
import humanize


# naturalsize – converts byte counts to human-readable file sizes


@pytest.mark.filesize
@pytest.mark.smoke
@pytest.mark.order(1)
class TestNaturalSizeDecimalMode:
    """
    Tests for humanize.naturalsize() in default decimal (SI) mode.
    Decimal: 1 kB = 1000 bytes, suffixes: B, kB, MB, GB, TB, PB, EB, ZB, YB
    """

    @pytest.mark.parametrize("value, expected", [
        (0,               "0 Bytes"),     # BVA: zero bytes
        (1,               "1 Byte"),      # BVA: singular byte
        (2,               "2 Bytes"),     # BVA: plural bytes
        (999,             "999 Bytes"),   # BVA: just below 1 kB
        (1000,            "1.0 kB"),      # BVA: exactly 1 kB
        (1500,            "1.5 kB"),
        (1_000_000,       "1.0 MB"),      # BVA: exactly 1 MB
        (1_500_000,       "1.5 MB"),
        (1_000_000_000,   "1.0 GB"),      # BVA: exactly 1 GB
        (1_000_000_000_000, "1.0 TB"),    # BVA: exactly 1 TB
    ])
    def test_decimalSuffixes(self, value, expected):
        """ECP + BVA: SI decimal suffixes at boundary values."""
        assert humanize.naturalsize(value) == expected

    def test_zeroReturnsBytes(self):
        """BVA: zero bytes is '0 Bytes'."""
        assert humanize.naturalsize(0) == "0 Bytes"

    def test_oneByteSingular(self):
        """BVA: exactly 1 byte uses singular 'Byte'."""
        assert humanize.naturalsize(1) == "1 Byte"

    def test_twoBytesPlural(self):
        """BVA: 2 bytes uses plural 'Bytes'."""
        assert humanize.naturalsize(2) == "2 Bytes"

    def test_returnsString(self):
        """naturalsize always returns a string."""
        assert isinstance(humanize.naturalsize(1024), str)

    def test_stringInput(self):
        """ECP: string numeric input is accepted."""
        result = humanize.naturalsize("1000")
        assert result == "1.0 kB"


@pytest.mark.filesize
@pytest.mark.order(2)
class TestNaturalSizeBinaryMode:
    """
    Tests for humanize.naturalsize(binary=True).
    Binary: 1 KiB = 1024 bytes, suffixes: KiB, MiB, GiB, TiB
    """

    @pytest.mark.parametrize("value, expected", [
        (1023,       "1023 Bytes"),  # BVA: just below 1 KiB
        (1024,       "1.0 KiB"),     # BVA: exactly 1 KiB
        (1025,       "1.0 KiB"),     # BVA: just above 1 KiB
        (1048576,    "1.0 MiB"),     # BVA: exactly 1 MiB (1024^2)
        (1073741824, "1.0 GiB"),     # BVA: exactly 1 GiB (1024^3)
    ])
    def test_binarySuffixes(self, value, expected):
        """ECP + BVA: binary (IEC) suffixes at boundary values."""
        assert humanize.naturalsize(value, binary=True) == expected

    def test_binaryUsesKibNotKb(self):
        """ECP: binary mode uses 'KiB' not 'kB'."""
        result = humanize.naturalsize(1024, binary=True)
        assert "KiB" in result
        assert "kB" not in result

    def test_negativeBinary(self):
        """ECP: negative values in binary mode."""
        result = humanize.naturalsize(-4096, binary=True)
        assert result == "-4.0 KiB"


@pytest.mark.filesize
@pytest.mark.order(3)
class TestNaturalSizeGnuMode:
    """
    Tests for humanize.naturalsize(gnu=True).
    GNU mode: ls -sh style, uses K, M, G (without 'i' or 'B').
    """

    @pytest.mark.parametrize("value, expected", [
        (300,       "300B"),  # BVA: below threshold, raw bytes
        (3000,      "2.9K"),  # ECP: kilobytes in GNU
        (3_000_000, "2.9M"),  # ECP: megabytes in GNU
    ])
    def test_gnuSuffixes(self, value, expected):
        """ECP: GNU mode uses short K/M/G style suffixes."""
        assert humanize.naturalsize(value, gnu=True) == expected

    def test_gnuNoSpace(self):
        """ECP: GNU mode has no space between number and suffix for bytes."""
        result = humanize.naturalsize(300, gnu=True)
        assert " " not in result


@pytest.mark.filesize
@pytest.mark.order(4)
class TestNaturalSizeEdgeCases:
    """Edge cases and custom format for naturalsize."""

    def test_customFormatPrecision(self):
        """ECP: custom format string for more decimal places."""
        result = humanize.naturalsize(3000, gnu=True, format="%.3f")
        assert "2.930K" == result

    def test_veryLargeValue(self):
        """BVA: extremely large values use high SI prefixes."""
        result = humanize.naturalsize(10 ** 28)
        assert "RB" in result

    def test_negativeDecimal(self):
        """ECP: negative value in decimal mode."""
        result = humanize.naturalsize(-1000)
        assert result == "-1.0 kB"

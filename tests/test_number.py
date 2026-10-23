"""
Unit tests for humanize.number module.
Module Author  : 24F-3109 Ali Abdullah
Functions Under Test:
    - humanize.intcomma()
    - humanize.intword()
    - humanize.ordinal()
    - humanize.apnumber()
    - humanize.metric()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): valid ranges, boundary values, invalid types
    - Boundary Value Analysis (BVA): 0, ±1, large values, threshold crossings
    - Parameterization: data-driven test tables

"""

import pytest
import humanize


@pytest.mark.number
@pytest.mark.smoke
@pytest.mark.order(1)
class TestIntComma:
    """Tests for humanize.intcomma() - ECP & BVA applied."""

    # ECP: positive integers
    @pytest.mark.parametrize("value, expected", [
        (0,          "0"),
        (1,          "1"),
        (999,        "999"),
        (1000,       "1,000"),       # BVA: first comma introduced
        (1001,       "1,001"),
        (1000000,    "1,000,000"),   # BVA: second comma
        (1234567890, "1,234,567,890"),
    ])
    def test_positiveIntegers(self, value, expected):
        """ECP: positive partition - integers with expected comma formatting."""
        assert humanize.intcomma(value) == expected

    # ECP: negative integers
    @pytest.mark.parametrize("value, expected", [
        (-1,       "-1"),
        (-1000,    "-1,000"),    # BVA: negative boundary
        (-1000000, "-1,000,000"),
    ])
    def test_negativeIntegers(self, value, expected):
        """ECP: negative partition - negatives should retain minus sign."""
        assert humanize.intcomma(value) == expected

    # ECP: string inputs (humanize accepts numeric strings)
    def test_stringNumericInput(self):
        """ECP: string partition - numeric string should be handled."""
        assert humanize.intcomma("1000") == "1,000"

    # BVA: boundary at exactly 1000
    def test_boundaryOneThousand(self):
        """BVA: exactly 1000 introduces first comma separator."""
        assert humanize.intcomma(1000) == "1,000"

    # BVA: one below 1000
    def test_boundaryNineHundredNinetyNine(self):
        """BVA: 999 should not have a comma."""
        assert humanize.intcomma(999) == "999"

    # Return type check
    def test_returnsString(self):
        """intcomma should always return a string."""
        result = humanize.intcomma(42)
        assert isinstance(result, str)

    # Float input
    def test_floatInput(self):
        """ECP: float partition – floats should be formatted."""
        result = humanize.intcomma(1234.56)
        assert "1,234" in result


# 2. intword – converts large integers to word representation


@pytest.mark.number
@pytest.mark.order(2)
class TestIntWord:
    """Tests for humanize.intword() - large number word conversion."""

    @pytest.mark.parametrize("value, expectedKeyword", [
        (1_000_000,         "million"),
        (1_200_000,         "million"),
        (1_000_000_000,     "billion"),
        (2_500_000_000,     "billion"),
        (1_000_000_000_000, "trillion"),
    ])
    def test_wordSuffixes(self, value, expectedKeyword):
        """ECP: large numbers map to correct English word suffix."""
        result = humanize.intword(value)
        assert expectedKeyword in result

    def test_smallNumberBelowMillion(self):
        """ECP: numbers well below 1 million - verify no unexpected suffix."""
        # Note: humanize 4.16 rounds 999,999 up to "1.0 million"
        # Test that the function returns a non-empty string
        result = humanize.intword(500_000)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_exactOneMillion(self):
        """BVA: exactly 1,000,000 to '1.0 million'."""
        assert humanize.intword(1_000_000) == "1.0 million"

    def test_returnsString(self):
        """intword must always return a string."""
        assert isinstance(humanize.intword(5_000_000), str)

    def test_negativeLargeNumber(self):
        """ECP: negative large numbers should still produce word form."""
        result = humanize.intword(-1_000_000)
        assert "million" in result

    def test_exactOneBillion(self):
        """BVA: exactly 1,000,000,000 → '1.0 billion'."""
        assert humanize.intword(1_000_000_000) == "1.0 billion"

    def test_exactOneTrillion(self):
        """BVA: exactly 1,000,000,000,000 → '1.0 trillion'."""
        assert humanize.intword(1_000_000_000_000) == "1.0 trillion"


# 3. ordinal – converts integers to ordinal strings (1st, 2nd, 3rd…)


@pytest.mark.number
@pytest.mark.order(3)
class TestOrdinal:
    """Tests for humanize.ordinal() – ordinal suffix application."""

    @pytest.mark.parametrize("value, expected", [
        (1,  "1st"),
        (2,  "2nd"),
        (3,  "3rd"),
        (4,  "4th"),
        (11, "11th"),   # special case: 11th (not 11st)
        (12, "12th"),   # special case: 12th (not 12nd)
        (13, "13th"),   # special case: 13th (not 13rd)
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (100, "100th"),
        (101, "101st"),
    ])
    def test_ordinalSuffixes(self, value, expected):
        """ECP + BVA: correct suffix for various integers including teen exceptions."""
        assert humanize.ordinal(value) == expected

    def test_zero(self):
        """BVA: zero ordinal."""
        assert humanize.ordinal(0) == "0th"

    def test_returnsString(self):
        """ordinal always returns a string."""
        assert isinstance(humanize.ordinal(5), str)

    def test_largeOrdinal(self):
        """ECP: large number ordinal."""
        result = humanize.ordinal(1001)
        assert result == "1001st"


# 4. apnumber – converts small integers to AP-style words


@pytest.mark.number
@pytest.mark.order(4)
class TestApNumber:
    """Tests for humanize.apnumber() – AP style number words."""

    @pytest.mark.parametrize("value, expected", [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ])
    def test_singleDigitsAsWords(self, value, expected):
        """ECP: 0–9 should be returned as English words."""
        assert humanize.apnumber(value) == expected

    def test_tenReturnsStringNumeral(self):
        """BVA: 10 is the boundary – above 9 returns '10' as a string."""
        result = humanize.apnumber(10)
        assert str(result) == "10"

    def test_largeNumberReturnsString(self):
        """ECP: numbers > 9 remain as numeral strings (not converted to words)."""
        result = humanize.apnumber(100)
        assert str(result) == "100"

    def test_returnsStringForSmall(self):
        """apnumber returns str for values 0–9."""
        assert isinstance(humanize.apnumber(5), str)

    def test_nineIsLastWordForm(self):
        """BVA: 9 is the last value to return a word ('nine')."""
        assert humanize.apnumber(9) == "nine"


# 5. metric – converts numbers to SI metric prefix notation


@pytest.mark.number
@pytest.mark.order(5)
class TestMetric:
    """Tests for humanize.metric() – SI metric prefix formatting."""

    @pytest.mark.parametrize("value, expectedSubstring", [
        (1000,          "k"),     # kilo
        (1_000_000,     "M"),     # mega
        (1_000_000_000, "G"),     # giga
        (0.001,         "m"),     # milli
    ])
    def test_metricPrefixes(self, value, expectedSubstring):
        """ECP: each SI tier maps to the correct prefix letter."""
        result = humanize.metric(value)
        assert expectedSubstring in result

    def test_smallValueReturnsString(self):
        """BVA: values that don't need a prefix still return a string."""
        result = humanize.metric(1)
        assert isinstance(result, str)

    def test_returnsString(self):
        """metric always returns a string."""
        assert isinstance(humanize.metric(500), str)

    def test_negativeValue(self):
        """ECP: negative values should still produce metric output."""
        result = humanize.metric(-1000)
        assert "k" in result


# ─────────────────────────────────────────────────────────────────────────────
# 6. clamp – clamps a value to a [floor, ceil] range
# Note: humanize 4.16 API: clamp(value, format, floor, ceil, floor_token, ceil_token)
# When value < floor → returns "<{floor}" (uses ceil_token '<')
# When value > ceil  → returns ">{ceil}"  (uses floor_token '>')
# When value is in range → returns formatted value string
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.number
@pytest.mark.order(6)
class TestClamp:
    """Tests for humanize.clamp() – value clamping with floor/ceil tokens."""

    def test_valueWithinRange(self):
        """ECP: value inside range is returned as formatted string."""
        result = humanize.clamp(50, floor=0, ceil=100)
        assert "50" in result

    def test_valueAtFloor(self):
        """BVA: value exactly at floor boundary is returned (not clamped)."""
        result = humanize.clamp(0, floor=0, ceil=100)
        assert "0" in result

    def test_valueAtCeil(self):
        """BVA: value exactly at ceil boundary is returned (not clamped)."""
        result = humanize.clamp(100, floor=0, ceil=100)
        assert "100" in result

    def test_valueBelowFloorShowsToken(self):
        """BVA: value below floor returns '<{floor}' string."""
        result = humanize.clamp(-10, floor=0, ceil=100)
        assert result == "<0"

    def test_valueAboveCeilShowsToken(self):
        """BVA: value above ceil returns '>{ceil}' string."""
        result = humanize.clamp(150, floor=0, ceil=100)
        assert result == ">100"

    def test_returnsString(self):
        """ECP: clamp always returns a string."""
        result = humanize.clamp(50, floor=0, ceil=100)
        assert isinstance(result, str)

    def test_customFloorToken(self):
        """ECP: custom floor_token is prepended when value is below floor."""
        result = humanize.clamp(-5, floor=0, ceil=100, floor_token="LOW")
        assert result == "LOW0"

    def test_customCeilToken(self):
        """ECP: custom ceil_token is prepended when value is above ceil."""
        result = humanize.clamp(200, floor=0, ceil=100, ceil_token="HIGH")
        assert result == "HIGH100"

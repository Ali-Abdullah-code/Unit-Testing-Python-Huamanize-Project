"""
Unit tests for humanize.time module (precisedelta function).
Module Author  : 24F-3109 Ali Abdullah
Functions Under Test:
    - humanize.precisedelta()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): seconds, minutes, hours, days, weeks, months, years
    - Boundary Value Analysis (BVA): 0 seconds, 59s/60s, 3599s/3600s, 86399s/86400s
    - Parameterization: data-driven tables for different timedelta inputs

"""

import pytest
import datetime
import humanize


# precisedelta – human-readable precise time delta


@pytest.mark.duration
@pytest.mark.smoke
@pytest.mark.order(1)
class TestPreciseDeltaBasic:
    """
    Basic tests for humanize.precisedelta() with timedelta objects.
    ECP: zero duration, seconds, minutes, hours, days.
    """

    def test_zeroSeconds(self):
        """BVA: zero duration returns '0 seconds'."""
        result = humanize.precisedelta(datetime.timedelta(seconds=0))
        assert result == "0 seconds"

    def test_oneSecond(self):
        """BVA: exactly 1 second returns '1 second' (singular)."""
        result = humanize.precisedelta(datetime.timedelta(seconds=1))
        assert result == "1 second"

    def test_twoSeconds(self):
        """BVA: 2 seconds – plural form."""
        result = humanize.precisedelta(datetime.timedelta(seconds=2))
        assert result == "2 seconds"

    def test_fiftyNineSeconds(self):
        """BVA: 59 seconds – just below 1 minute threshold."""
        result = humanize.precisedelta(datetime.timedelta(seconds=59))
        assert "seconds" in result

    def test_sixtySecondsOneMinute(self):
        """BVA: exactly 60 seconds → '1 minute'."""
        result = humanize.precisedelta(datetime.timedelta(seconds=60))
        assert result == "1 minute"

    def test_ninetySeconds(self):
        """ECP: 1 minute 30 seconds → compound output."""
        result = humanize.precisedelta(datetime.timedelta(seconds=90))
        assert "minute" in result and "30 seconds" in result

    def test_oneHour(self):
        """BVA: exactly 3600 seconds → '1 hour'."""
        result = humanize.precisedelta(datetime.timedelta(seconds=3600))
        assert result == "1 hour"

    def test_oneHourOneMinuteOneSecond(self):
        """ECP: compound duration with hours, minutes, seconds."""
        result = humanize.precisedelta(datetime.timedelta(seconds=3661))
        assert "hour" in result
        assert "minute" in result
        assert "second" in result

    def test_oneDay(self):
        """BVA: exactly 1 day → '1 day'."""
        result = humanize.precisedelta(datetime.timedelta(days=1))
        assert result == "1 day"

    def test_twoDays(self):
        """ECP: 2 days plural."""
        result = humanize.precisedelta(datetime.timedelta(days=2))
        assert result == "2 days"


@pytest.mark.duration
@pytest.mark.order(2)
class TestPreciseDeltaWeeksMonthsYears:
    """ECP: tests for week-, month-, and year-scale durations."""

    def test_sevenDays(self):
        """ECP: exactly 7 days → '7 days' (humanize 4.16 does not convert to weeks)."""
        result = humanize.precisedelta(datetime.timedelta(days=7))
        assert "7 days" == result

    def test_fourteenDays(self):
        """ECP: 14 days → '14 days'."""
        result = humanize.precisedelta(datetime.timedelta(days=14))
        assert "14 days" == result

    def test_oneMonth(self):
        """ECP: ~30 days – humanize 4.16 shows '30 days' at this scale."""
        result = humanize.precisedelta(datetime.timedelta(days=30))
        assert "days" in result or "month" in result

    def test_oneYear(self):
        """ECP: ~365 days → output contains 'year'."""
        result = humanize.precisedelta(datetime.timedelta(days=365))
        assert "year" in result

    def test_twoYears(self):
        """ECP: ~730 days → output contains '2 years'."""
        result = humanize.precisedelta(datetime.timedelta(days=730))
        assert "2 years" in result


@pytest.mark.duration
@pytest.mark.order(3)
class TestPreciseDeltaOptions:
    """Tests for precisedelta optional parameters: minimum_unit, suppress."""

    @pytest.mark.parametrize("minimumUnit, valueSeconds, forbidden", [
        ("minutes", 30, "seconds"),
        ("hours",   90, "minutes"),
    ])
    def test_minimumUnitSuppressesSmaller(self, minimumUnit, valueSeconds, forbidden):
        """ECP: minimumUnit suppresses smaller units from output."""
        result = humanize.precisedelta(
            datetime.timedelta(seconds=valueSeconds),
            minimum_unit=minimumUnit
        )
        assert forbidden not in result

    def test_suppressRemovesComponent(self):
        """ECP: suppress parameter hides listed unit components."""
        result = humanize.precisedelta(
            datetime.timedelta(seconds=3661),
            suppress=["seconds"]
        )
        assert "second" not in result
        assert "hour" in result

    def test_returnsString(self):
        """precisedelta always returns a string."""
        result = humanize.precisedelta(datetime.timedelta(hours=5))
        assert isinstance(result, str)

    def test_integerInput(self):
        """ECP: integer seconds as input (not timedelta)."""
        result = humanize.precisedelta(3600)
        assert "hour" in result

    def test_negativeDuration(self):
        """ECP: negative timedelta value produces a string result."""
        result = humanize.precisedelta(datetime.timedelta(seconds=-60))
        assert isinstance(result, str)

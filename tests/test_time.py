"""
test_time.py
============
Unit tests for humanize.time module.
Module Author  : 24P-3060
Functions Under Test:
    - humanize.naturaltime()
    - humanize.naturalday()
    - humanize.naturaldelta()
    - humanize.naturaldate()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): past/future, seconds/minutes/hours/days
    - Boundary Value Analysis (BVA): 0 seconds, 59s/60s boundaries, exact day boundaries
    - Parameterization: data-driven tables for various timedelta inputs
"""

import pytest
import datetime
import humanize


# 1. naturaltime – relative time like "3 minutes ago" / "in 5 hours"


@pytest.mark.time
@pytest.mark.smoke
@pytest.mark.order(1)
class TestNaturalTime:
    """Tests for humanize.naturaltime() with past and future datetimes."""

    def test_nowReturnsNow(self):
        """BVA: datetime.now() with 0 offset → 'now'."""
        result = humanize.naturaltime(datetime.datetime.now())
        assert result == "now"

    def test_oneSecondAgo(self):
        """BVA: 1 second in the past."""
        past = datetime.datetime.now() - datetime.timedelta(seconds=1)
        result = humanize.naturaltime(past)
        assert "second" in result and "ago" in result

    def test_thirtySecondsAgo(self):
        """ECP: 30 seconds in the past."""
        past = datetime.datetime.now() - datetime.timedelta(seconds=30)
        result = humanize.naturaltime(past)
        assert "seconds ago" in result

    def test_oneMinuteAgo(self):
        """BVA: exactly 60 seconds ago → 'a minute ago'."""
        past = datetime.datetime.now() - datetime.timedelta(seconds=60)
        result = humanize.naturaltime(past)
        assert "minute" in result and "ago" in result

    def test_twoHoursAgo(self):
        """ECP: 2 hours in the past."""
        past = datetime.datetime.now() - datetime.timedelta(hours=2)
        result = humanize.naturaltime(past)
        assert "hours ago" in result

    def test_futureOneSecond(self):
        """ECP: a few seconds in the future → 'a second from now'."""
        # Use 2 seconds to avoid race with the 'now' boundary
        future = datetime.datetime.now() + datetime.timedelta(seconds=2)
        result = humanize.naturaltime(future)
        assert "from now" in result

    def test_futureFiveMinutes(self):
        """ECP: 5 minutes in the future."""
        future = datetime.datetime.now() + datetime.timedelta(minutes=5)
        result = humanize.naturaltime(future)
        assert "minutes from now" in result

    def test_pastOneDay(self):
        """ECP: 1 day ago."""
        past = datetime.datetime.now() - datetime.timedelta(days=1)
        result = humanize.naturaltime(past)
        assert "ago" in result

    def test_returnsString(self):
        """naturaltime always returns a string."""
        result = humanize.naturaltime(datetime.datetime.now())
        assert isinstance(result, str)

    @pytest.mark.parametrize("secondsDelta, keyword", [
        (-5,    "seconds ago"),
        (-60,   "ago"),
        (-3600, "ago"),
        (5,     "from now"),
        (60,    "from now"),
    ])
    def test_parametrizedRelativeTimes(self, secondsDelta, keyword):
        """ECP parametrized: various past/future offsets produce correct keywords."""
        dt = datetime.datetime.now() + datetime.timedelta(seconds=secondsDelta)
        result = humanize.naturaltime(dt)
        assert keyword in result


# 2. naturalday – returns "today", "yesterday", "tomorrow" or a date string


@pytest.mark.time
@pytest.mark.order(2)
class TestNaturalDay:
    """Tests for humanize.naturalday() – named day relative to today."""

    def test_today(self):
        """BVA: today's date → 'today'."""
        assert humanize.naturalday(datetime.date.today()) == "today"

    def test_yesterday(self):
        """BVA: yesterday → 'yesterday'."""
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        assert humanize.naturalday(yesterday) == "yesterday"

    def test_tomorrow(self):
        """BVA: tomorrow → 'tomorrow'."""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        assert humanize.naturalday(tomorrow) == "tomorrow"

    def test_twoDaysAgoIsFormatted(self):
        """ECP: 2 days ago returns a formatted date string (not 'yesterday')."""
        two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
        result = humanize.naturalday(two_days_ago)
        assert result != "today"
        assert result != "yesterday"
        assert isinstance(result, str)

    def test_futureTwoDaysIsFormatted(self):
        """ECP: 2 days in future returns a formatted date string."""
        future = datetime.date.today() + datetime.timedelta(days=2)
        result = humanize.naturalday(future)
        assert result != "tomorrow"
        assert isinstance(result, str)

    def test_returnsString(self):
        """naturalday always returns a string."""
        assert isinstance(humanize.naturalday(datetime.date.today()), str)

    @pytest.mark.parametrize("daysOffset, expected", [
        (0,  "today"),
        (-1, "yesterday"),
        (1,  "tomorrow"),
    ])
    def test_parametrizedNamedDays(self, daysOffset, expected):
        """ECP parametrized: ±1 day produces named labels."""
        date = datetime.date.today() + datetime.timedelta(days=daysOffset)
        assert humanize.naturalday(date) == expected


# ─────────────────────────────────────────────────────────────────────────────
# 3. naturaldelta – human-readable time span (no past/future direction)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.time
@pytest.mark.order(3)
class TestNaturalDelta:
    """Tests for humanize.naturaldelta() – duration without direction."""

    @pytest.mark.parametrize("delta, expectedKeyword", [
        (datetime.timedelta(seconds=0),   "moment"),
        (datetime.timedelta(seconds=1),   "second"),
        (datetime.timedelta(seconds=30),  "seconds"),
        (datetime.timedelta(minutes=1),   "minute"),
        (datetime.timedelta(hours=1),     "hour"),
        (datetime.timedelta(hours=2),     "hours"),
        (datetime.timedelta(days=1),      "day"),
        # humanize 4.16 returns "7 days"
        (datetime.timedelta(days=7),      "days"),
        (datetime.timedelta(days=30),     "month"),
        (datetime.timedelta(days=365),    "year"),
    ])
    def test_naturalDeltaKeywords(self, delta, expectedKeyword):
        """ECP + BVA: naturaldelta output contains correct time keyword."""
        result = humanize.naturaldelta(delta)
        assert expectedKeyword in result

    def test_noAgoSuffix(self):
        """naturaldelta must NOT contain 'ago' (direction-free)."""
        past = datetime.timedelta(hours=3)
        result = humanize.naturaldelta(past)
        assert "ago" not in result

    def test_returnsString(self):
        """naturaldelta always returns a string."""
        assert isinstance(humanize.naturaldelta(
            datetime.timedelta(hours=1)), str)


# 4. naturaldate – full human-readable date including year


@pytest.mark.time
@pytest.mark.order(4)
class TestNaturalDate:
    """Tests for humanize.naturaldate() – full date including year context."""

    def test_todayReturnsToday(self):
        """BVA: today → 'today'."""
        assert humanize.naturaldate(datetime.date.today()) == "today"

    def test_pastIncludesYearIfDifferent(self):
        """ECP: far past date includes the year."""
        old_date = datetime.date(2020, 6, 15)
        result = humanize.naturaldate(old_date)
        assert "2020" in result

    def test_returnsString(self):
        """naturaldate always returns a string."""
        assert isinstance(humanize.naturaldate(datetime.date.today()), str)

    def test_specificDateFormat(self):
        """ECP: a specific historical date has month and year in output."""
        date = datetime.date(2023, 3, 25)
        result = humanize.naturaldate(date)
        # Should mention March and 2023
        assert "March" in result or "2023" in result

"""
conftest.py
===========
Shared pytest fixtures and suite configuration for the Humanize test suite.
Provides:
    - Common fixtures (fixed datetime, fixed date)
    - Suite filtering helpers
    - Hooks for test ordering and reporting
"""

import pytest
import datetime
import humanize


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def fixed_past_datetime():
    """Returns a fixed datetime 1 hour in the past (for deterministic time tests)."""
    return datetime.datetime(2024, 6, 15, 10, 0, 0)


@pytest.fixture
def fixed_future_datetime():
    """Returns a fixed datetime 1 hour in the future."""
    return datetime.datetime(2099, 1, 1, 0, 0, 0)


@pytest.fixture
def fixed_today():
    """Returns a fixed date (today at test-run time)."""
    return datetime.date.today()


@pytest.fixture
def one_hour_delta():
    """Returns a timedelta of exactly 1 hour."""
    return datetime.timedelta(hours=1)


@pytest.fixture
def deactivate_locale():
    """
    Fixture that deactivates any humanize locale before and after a test.
    Use in i18n tests to ensure clean locale state.
    """
    humanize.deactivate()
    yield
    humanize.deactivate()


@pytest.fixture(params=[1000, 1_000_000, 1_000_000_000])
def large_number(request):
    """
    Parametrized fixture providing a set of large numbers.
    Used to test number formatting functions across multiple magnitudes.
    """
    return request.param


# ─────────────────────────────────────────────────────────────────────────────
# Hooks
# ─────────────────────────────────────────────────────────────────────────────

def pytest_configure(config):
    """Register custom markers to prevent PytestUnknownMarkWarning."""
    config.addinivalue_line("markers", "number: Tests for humanize.number module")
    config.addinivalue_line("markers", "filesize: Tests for humanize.filesize module")
    config.addinivalue_line("markers", "duration: Tests for humanize.duration module")
    config.addinivalue_line("markers", "time: Tests for humanize.time module")
    config.addinivalue_line("markers", "i18n: Tests for humanize.i18n module")
    config.addinivalue_line("markers", "lists: Tests for humanize.lists module")
    config.addinivalue_line("markers", "smoke: Quick sanity smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests for known edge-cases")
    config.addinivalue_line("markers", "parametrize: Data-driven parametrized test cases")
    config.addinivalue_line("markers", "csv_driven: Tests consuming data from external CSV files")


def pytest_collection_modifyitems(config, items):
    """
    Enforce global test execution order by module/marker:
    Suite Order:
        1. smoke tests
        2. number tests
        3. filesize tests
        4. duration tests
        5. time tests
        6. i18n tests
        7. lists tests
        8. csv_driven tests
    Within each group, @pytest.mark.order(N) controls fine-grained order.
    """
    SUITE_ORDER = ["smoke", "number", "filesize", "duration", "time", "i18n", "lists", "csv_driven"]

    def suite_priority(item):
        for idx, marker_name in enumerate(SUITE_ORDER):
            if item.get_closest_marker(marker_name):
                return idx
        return len(SUITE_ORDER)  # unclassified tests run last

    items.sort(key=suite_priority)

"""

CSV-driven unit tests satisfying Task 3 requirements.
Tests consume input/expected data from external CSV files in tests/data/.

Modules Covered:
    - humanize.naturalsize  (from naturalsize_decimal.csv)
    - humanize.intcomma     (from intcomma_data.csv)
    - humanize.ordinal      (from ordinal_data.csv)
    - humanize.natural_list (from natural_list_data.csv)

Test Design: Data-driven testing with CSV as external data source.
"""

import csv
import os
import pytest
import humanize

# Path to CSV data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def loadCsv(filename):
    """Helper: load a CSV file and return list of rows as dicts."""
    filePath = os.path.join(DATA_DIR, filename)
    with open(filePath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


# CSV Test: naturalsize (decimal mode)
naturalSizeData = [
    (int(row["input_value"]), row["expected_output"])
    for row in loadCsv("naturalsize_decimal.csv")
]


@pytest.mark.filesize
@pytest.mark.csv_driven
@pytest.mark.order(10)
class TestNaturalSizeFromCsv:
    """Data-driven tests for naturalsize() reading from naturalsize_decimal.csv."""

    @pytest.mark.parametrize("value, expected", naturalSizeData)
    def test_naturalSizeDecimalCsv(self, value, expected):
        assert humanize.naturalsize(value) == expected


# ─────────────────────────────────────────────────────────────────────────────
# CSV Test: intcomma
# ─────────────────────────────────────────────────────────────────────────────

intCommaData = [
    (int(row["input_value"]), row["expected_output"])
    for row in loadCsv("intcomma_data.csv")
]


@pytest.mark.number
@pytest.mark.csv_driven
@pytest.mark.order(11)
class TestIntCommaFromCsv:
    """Data-driven tests for intcomma() reading from intcomma_data.csv."""

    @pytest.mark.parametrize("value, expected", intCommaData)
    def test_intCommaCsv(self, value, expected):
        """
        CSV-driven: for each (input_value, expected_output) pair in CSV,
        verify humanize.intcomma(value) matches expected.
        """
        assert humanize.intcomma(value) == expected


# CSV Test: ordinal
ordinalData = [
    (int(row["input_value"]), row["expected_output"])
    for row in loadCsv("ordinal_data.csv")
]


@pytest.mark.number
@pytest.mark.csv_driven
@pytest.mark.order(12)
class TestOrdinalFromCsv:
    """Data-driven tests for ordinal() reading from ordinal_data.csv."""

    @pytest.mark.parametrize("value, expected", ordinalData)
    def test_ordinalCsv(self, value, expected):
        """
        CSV-driven: for each (input_value, expected_output) pair in CSV,
        verify humanize.ordinal(value) matches expected.
        """
        assert humanize.ordinal(value) == expected


# ─────────────────────────────────────────────────────────────────────────────
# CSV Test: natural_list
# Format: list_items column uses '|' as item separator
# ─────────────────────────────────────────────────────────────────────────────

def loadNaturalListCsv():
    """Parse the natural_list CSV; items separated by '|' inside the cell."""
    rows = loadCsv("natural_list_data.csv")
    result = []
    for row in rows:
        itemsRaw = row["list_items"].strip('"')
        items = itemsRaw.split("|")
        expected = row["expected_output"].strip('"')
        result.append((items, expected))
    return result


naturalListData = loadNaturalListCsv()


@pytest.mark.lists
@pytest.mark.csv_driven
@pytest.mark.order(13)
class TestNaturalListFromCsv:
    """Data-driven tests for natural_list() reading from natural_list_data.csv."""

    @pytest.mark.parametrize("items, expected", naturalListData)
    def test_naturalListCsv(self, items, expected):
        """
        CSV-driven: for each (list_items, expected_output) in CSV,
        verify humanize.natural_list(items) matches expected.
        Items in CSV are separated by '|' character.
        """
        result = humanize.natural_list(items)
        assert result == expected

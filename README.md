# Unit Testing Python Humanize Project

## SQE Assignment 3 – Build Unit Test Automation Solution

### Open-Source Project: [humanize](https://github.com/python-humanize/humanize)

> **humanize** converts Python data into human-readable text — numbers, file sizes, dates, time deltas, and lists.

---

## 👥 Team Members & Module Allocation

| Roll Number | Modules Covered                                                                                     |
|-------------|-----------------------------------------------------------------------------------------------------|
| 24F-3109    | `number` (intcomma, intword, ordinal, apnumber, metric), `filesize` (naturalsize), `duration` (precisedelta) |
| 24P-3060    | `time` (naturaltime, naturalday, naturaldelta, naturaldate), `i18n` (activate, deactivate, separators), `lists` (natural_list) |

---

## Project Structure

```
Unit-Testing-Python-Huamanize-Project/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              ← Shared fixtures, suite ordering hooks
│   ├── test_number.py           ← 24F-3109: intcomma, intword, ordinal, apnumber, metric
│   ├── test_filesize.py         ← 24F-3109: naturalsize
│   ├── test_duration.py         ← 24F-3109: precisedelta
│   ├── test_time.py             ← 24P-3060: naturaltime, naturalday, naturaldelta, naturaldate
│   ├── test_i18n.py             ← 24P-3060: activate, deactivate, decimal_separator
│   ├── test_lists.py            ← 24P-3060: natural_list
│   ├── test_csv_driven.py       ← Task 3: CSV-driven tests for all modules
│   └── data/
│       ├── naturalsize_decimal.csv
│       ├── intcomma_data.csv
│       ├── ordinal_data.csv
│       └── natural_list_data.csv
│
├── docs/
│   └── Test_Cases.xlsx          ← Task 3: Excel test case documentation
│
├── reports/                     ← Auto-generated HTML reports
│
├── pytest.ini                   ← Pytest configuration (parallel, suites, markers)
├── requirements.txt
├── generate_excel.py            ← Script to generate Excel sheet
└── README.md
```

---

## Setup Instructions (Task 1)

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone or download the project
cd Unit-Testing-Python-Huamanize-Project

# Install all dependencies
pip install -r requirements.txt
```

---

## Running Tests (Task 4)

### Run all tests

```bash
pytest
```

### Run tests in parallel (uses all CPU cores)

```bash
pytest -n auto
```

### Run a specific suite/module

```bash
# Run only number module tests
pytest -m number

# Run only filesize tests
pytest -m filesize

# Run only smoke tests
pytest -m smoke

# Run only CSV-driven tests
pytest -m csv_driven

# Run 24F-3109's modules
pytest -m "number or filesize or duration"

# Run 24P-3060's modules
pytest -m "time or i18n or lists"
```

### Run with 4 parallel workers

```bash
pytest -n 4
```

### Generate HTML test report

```bash
pytest --html=reports/test_report.html --self-contained-html
```

### Run with coverage

```bash
pytest --cov=. --cov-report=html:reports/coverage
```

---

## Test Groups (Markers / Suites)

| Marker       | Description                                      | Execution Order |
|--------------|--------------------------------------------------|-----------------|
| `smoke`      | Quick sanity tests across all modules            | 1st             |
| `number`     | Tests for `humanize.number` module               | 2nd             |
| `filesize`   | Tests for `humanize.filesize` module             | 3rd             |
| `duration`   | Tests for `humanize.time.precisedelta`           | 4th             |
| `time`       | Tests for `humanize.time` (naturaltime etc.)     | 5th             |
| `i18n`       | Tests for `humanize.i18n` module                 | 6th             |
| `lists`      | Tests for `humanize.lists` module                | 7th             |
| `csv_driven` | Data-driven tests reading from CSV files         | 8th             |

---

## Test Design Techniques

### Equivalence Class Partitioning (ECP)

Divides inputs into partitions where all values behave identically:

- **Valid integers** (positive, negative, zero)
- **Large numbers** (millions, billions, trillions)
- **Different file size modes** (decimal, binary, GNU)
- **Future vs past** datetime values

### Boundary Value Analysis (BVA)

Tests at and around boundary values where behavior changes:

- `999` vs `1000` for `intcomma` (comma introduction)
- `1023` vs `1024` for `naturalsize(binary=True)` (KiB boundary)
- `0` seconds vs `1` second for `precisedelta`
- `9` vs `10` for `apnumber` (word vs numeral boundary)
- `today`, `yesterday`, `tomorrow` for `naturalday`

---

## Test Parameterization

Tests use `@pytest.mark.parametrize` extensively:

```python
@pytest.mark.parametrize("value, expected", [
    (1000,    "1,000"),
    (1000000, "1,000,000"),
])
def test_intcomma(self, value, expected):
    assert humanize.intcomma(value) == expected
```

---

## CSV-Driven Tests (Task 3)

Four CSV files in `tests/data/` provide external test data:

| CSV File                 | Tests               | Rows |
|--------------------------|---------------------|------|
| `naturalsize_decimal.csv`| naturalsize decimal | 10   |
| `intcomma_data.csv`      | intcomma            | 8    |
| `ordinal_data.csv`       | ordinal             | 10   |
| `natural_list_data.csv`  | natural_list        | 6    |


---

## Expected Test Count

| Module       | Test Classes | Approx Tests |
|--------------|-------------|-------------|
| number       | 6 classes   | ~45 tests   |
| filesize     | 4 classes   | ~25 tests   |
| duration     | 3 classes   | ~20 tests   |
| time         | 4 classes   | ~30 tests   |
| i18n         | 3 classes   | ~18 tests   |
| lists        | 3 classes   | ~18 tests   |
| csv_driven   | 4 classes   | ~34 tests   |
| **Total**    | **27**      | **~190**    |

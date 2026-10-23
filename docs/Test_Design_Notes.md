# Test Design Notes – ECP & BVA Analysis
## SQE Assignment 3 | Humanize Library Test Planning

---

## Module 1: `humanize.number` (Member 1)

### Functions: `intcomma`, `intword`, `ordinal`, `apnumber`, `metric`

---

### `intcomma(value)`

**Purpose:** Format a number with comma separators (e.g., `1,000,000`).

#### ECP (Equivalence Class Partitioning)

| Class ID | Partition          | Representative Value | Expected Output |
|----------|--------------------|----------------------|-----------------|
| ECP-N1   | Positive integers  | 1234567              | "1,234,567"     |
| ECP-N2   | Negative integers  | -1000                | "-1,000"        |
| ECP-N3   | Numeric strings    | "1000"               | "1,000"         |
| ECP-N4   | Float values       | 1234.56              | "1,234.56"      |
| ECP-N5   | Zero               | 0                    | "0"             |

#### BVA (Boundary Value Analysis)

| Boundary       | Value  | Expected   | Reason                        |
|----------------|--------|------------|-------------------------------|
| Below 1st comma | 999   | "999"      | No comma below 1000           |
| At 1st comma    | 1000  | "1,000"    | First comma introduced        |
| Above 1st comma | 1001  | "1,001"    | Comma remains after boundary  |

---

### `intword(value)`

**Purpose:** Convert large integers to word form (e.g., "1.2 million").

#### ECP

| Class ID | Partition      | Value       | Expected         |
|----------|----------------|-------------|------------------|
| ECP-W1   | Millions       | 1,200,000   | "1.2 million"    |
| ECP-W2   | Billions       | 2,500,000,000 | "2.5 billion"  |
| ECP-W3   | Trillions      | 1,000,000,000,000 | "1.0 trillion" |
| ECP-W4   | Below million  | 999,999     | no word suffix   |

#### BVA

| Boundary     | Value     | Expected       |
|--------------|-----------|----------------|
| Below million | 999,999  | no conversion  |
| At million    | 1,000,000 | "1.0 million"  |

---

### `ordinal(value)`

**Purpose:** Return ordinal string (1st, 2nd, 3rd, 4th...).

#### ECP

| Class ID | Partition         | Values         | Expected              |
|----------|-------------------|----------------|-----------------------|
| ECP-O1   | Normal integers   | 1,2,3,4,5      | 1st, 2nd, 3rd, 4th, 5th |
| ECP-O2   | Teen exceptions   | 11, 12, 13     | 11th, 12th, 13th      |
| ECP-O3   | Tens after 20     | 21, 22, 23     | 21st, 22nd, 23rd      |

#### BVA

| Boundary     | Value | Expected |
|--------------|-------|----------|
| Zero         | 0     | "0th"    |
| Teen start   | 11    | "11th"   |
| Teen end     | 13    | "13th"   |
| Post-teen 21 | 21    | "21st"   |

---

### `apnumber(value)`

**Purpose:** AP style – spell out numbers 0-9 as words.

#### ECP / BVA

| Class ID | Partition     | Values  | Expected         |
|----------|---------------|---------|------------------|
| ECP-A1   | 0 through 9   | 0-9     | zero through nine |
| ECP-A2   | 10 and above  | 10, 100 | returns the number |

**Critical Boundary:** 9 (word) vs 10 (numeral)

---

### `metric(value)`

**Purpose:** SI metric prefix notation (k, M, G, m...).

#### ECP

| Class   | Value       | Contains |
|---------|-------------|----------|
| kilo    | 1,000       | "k"      |
| mega    | 1,000,000   | "M"      |
| giga    | 1,000,000,000 | "G"    |
| milli   | 0.001       | "m"      |
| base    | 1-999       | no prefix |

---

## Module 2: `humanize.filesize` (Member 1)

### Function: `naturalsize(value, binary, gnu, format)`

**Purpose:** Format byte counts as human-readable file sizes.

#### ECP (Three Mode Partitions)

| Class      | Mode           | Example Input | Expected      |
|------------|----------------|---------------|---------------|
| ECP-F1     | Decimal (default) | 1000       | "1.0 kB"      |
| ECP-F2     | Binary (binary=True) | 1024    | "1.0 KiB"     |
| ECP-F3     | GNU (gnu=True) | 3000          | "2.9K"        |
| ECP-F4     | Negative       | -1000         | "-1.0 kB"     |

#### BVA

| Boundary         | Value | Expected    |
|------------------|-------|-------------|
| Zero bytes       | 0     | "0 Bytes"   |
| Singular byte    | 1     | "1 Byte"    |
| Just below 1 kB  | 999   | "999 Bytes" |
| Exactly 1 kB     | 1000  | "1.0 kB"    |
| Just below KiB   | 1023  | "1023 Bytes"|
| Exactly 1 KiB    | 1024  | "1.0 KiB"   |

---

## Module 3: `humanize.time (precisedelta)` (Member 1)

### Function: `precisedelta(value, minimum_unit, suppress)`

#### ECP

| Class    | Partition        | Input              | Contains       |
|----------|------------------|--------------------|----------------|
| ECP-D1   | Zero duration    | timedelta(0)       | "moment"       |
| ECP-D2   | Seconds          | timedelta(sec=30)  | "seconds"      |
| ECP-D3   | Minutes          | timedelta(sec=60)  | "minute"       |
| ECP-D4   | Hours            | timedelta(sec=3600)| "hour"         |
| ECP-D5   | Days             | timedelta(days=1)  | "day"          |
| ECP-D6   | Weeks            | timedelta(days=7)  | "week"         |
| ECP-D7   | Months           | timedelta(days=30) | "month"        |
| ECP-D8   | Years            | timedelta(days=365)| "year"         |

#### BVA

| Boundary      | Value      | Expected         |
|---------------|------------|------------------|
| 0 seconds     | 0s         | "a moment"       |
| 1 second      | 1s         | "a second"       |
| 59 seconds    | 59s        | contains "seconds"|
| 60 seconds    | 60s        | "a minute"       |
| 3599 seconds  | 3599s      | minutes + seconds|
| 3600 seconds  | 3600s      | "an hour"        |

---

## Module 4: `humanize.time` (Member 2)

### Functions: `naturaltime`, `naturalday`, `naturaldelta`, `naturaldate`

#### `naturaltime` ECP Partitions

| Class    | Partition  | Input              | Expected              |
|----------|------------|--------------------|-----------------------|
| ECP-T1   | Exact now  | now()              | "now"                 |
| ECP-T2   | Past secs  | now()-30s          | "X seconds ago"       |
| ECP-T3   | Past mins  | now()-2min         | "X minutes ago"       |
| ECP-T4   | Past hours | now()-2h           | "X hours ago"         |
| ECP-T5   | Future     | now()+5min         | "in X minutes"        |

#### `naturalday` BVA

| Boundary  | Input     | Expected    |
|-----------|-----------|-------------|
| -1 day    | yesterday | "yesterday" |
| 0 days    | today     | "today"     |
| +1 day    | tomorrow  | "tomorrow"  |
| ±2+ days  | any other | formatted   |

---

## Module 5: `humanize.i18n` (Member 2)

### Functions: `activate`, `deactivate`, `decimal_separator`, `thousands_separator`

#### ECP

| Class    | Partition           | Input              | Expected                    |
|----------|---------------------|--------------------|-----------------------------|
| ECP-I1   | Valid locale        | "de_DE"            | no error, returns translation|
| ECP-I2   | Invalid locale      | "xx_INVALID"       | raises FileNotFoundError    |
| ECP-I3   | Default (English)   | deactivate()       | decimal='.', thousands=','  |
| ECP-I4   | German locale       | activate("de_DE")  | decimal=',', thousands='.'  |

---

## Module 6: `humanize.lists` (Member 2)

### Function: `natural_list(lst, conjunction)`

#### ECP / BVA

| Class    | Partition       | Input           | Expected                  |
|----------|-----------------|-----------------|---------------------------|
| ECP-L1   | Empty list      | []              | ""                        |
| ECP-L2   | Single item     | ["a"]           | "a"                       |
| ECP-L3   | Two items       | ["a","b"]       | "a and b"                 |
| ECP-L4   | Three+ items    | ["a","b","c"]   | "a, b, and c"             |
| ECP-L5   | Custom conj.    | [...], "or"     | uses "or" instead of "and"|

**BVA:** Boundaries at list size 0→1→2→3 where output format changes.

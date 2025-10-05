<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cmun@0.2.2/cmun.css">

# Apside — High-Precision Conversion Between Gregorian and Julian Dates

**Author:** Venkata Siddharth Pendyala  
**Email:** [venkatasiddharthpendyala@outlook.com](mailto:venkatasiddharthpendyala@outlook.com)  
**License:** MIT

---

## Overview

**Apside** provides exact, arbitrarily precise conversions between **Gregorian calendar datetimes** and **Julian Dates (JD)**.  
This implementation upgrades the classic approach by using:

- **Exact integer Julian Day Number (JDN)** via the Fliegel–Van Flandern algorithm (no 365.25 or 30.6001 approximations).  
- **Arbitrary-precision fractional days** with `decimal.Decimal` (configurable precision).  
- **Nanosecond-level time components** with rollover-safe normalization.

The result is strictly reversible JD↔Gregorian conversion with precision limited only by the `Decimal` context.

---

## What’s New vs. Typical Implementations

- Exact integer calendar arithmetic for the date part (no floating-point floors).  
- `Decimal` fractional day with configurable precision (e.g., 50–100 significant digits).  
- Support for **nanoseconds** in both directions.  
- Correct automatic handling of the **1582-10-15** Gregorian reform boundary.

> Note: This module operates on civil time (UTC). For timescale conversions (UTC↔TAI↔TT↔TDB), leap seconds, ΔT, and relativistic corrections, integrate IERS/JPL data or use a companion timescale module.

---

## Installation

Copy `apside.py` into your project, or package it as desired. No external dependencies.

---

## API

### `gregToJulian(y, m, d, hour=0, minute=0, second=0, microsecond=0, nanosecond=0) -> Decimal`
Exact civil datetime → **JD** (as `Decimal`).  
- Calendar boundary: automatically selects Julian vs. Gregorian with the historical switchover at 1582-10-15.  
- Fractional day is computed from hour:minute:second:microsecond:nanosecond using `Decimal`.  
- JD is referenced to the standard astronomical convention (noon origin handled internally).

### `jdToGreg(jd: Decimal) -> tuple[int, int, int, int, int, int, int, int]`
**JD** (`Decimal`) → `(year, month, day, hour, minute, second, microsecond, nanosecond)` in UTC.  
- Uses only integer calendar arithmetic for the date.  
- Fractional day is expanded to time with rollover normalization.

---

## Precision

- Default `Decimal` precision in this file is set to **50 significant digits** (`getcontext().prec = 50`).  
- Increase the precision for sub-nanosecond JD resolution (e.g., 80–100) depending on your needs.  
- Reversibility: JD→Gregorian→JD round-trips within the configured decimal precision.

---

## Example

```python
from decimal import getcontext
from apside import gregToJulian, jdToGreg

# Increase precision if needed
getcontext().prec = 80

# Gregorian → JD (with nanoseconds)
jd = gregToJulian(2025, 10, 4, 12, 30, 0, microsecond=123456, nanosecond=789)
print(jd)  # Decimal JD with ~80-digit precision

# JD → Gregorian (reversible, with nanos)
print(jdToGreg(jd))
# (2025, 10, 4, 12, 30, 0, 123456, 789)

from datetime import datetime, timezone
import math

def gregToJulian(y, m, d, hour=0, minute=0, second=0, microsecond=0):
    """
    :param y: The year of Gregorian Date to convert
    :param m: The month of Gregorian Date to convert
    :param d: The day of Gregorian Date to convert
    :param hour: The hour of Gregorian Date to convert
    :param minute: The minute of Gregorian Date to convert
    :param second: The second of Gregorian Date to convert
    :param microsecond: The microsecond of Gregorian Date to convert
    :return: The Julian Date that corresponds to the Gregorian date that was converted, with
    the fractional part included.

    Contact siddhu.pendyala@outlook.com for further information if any questions! Always open
    to questions, comments, concerns, or anything you guys can think of!
    """
    # fractional day
    day = float(d) + (hour + minute/60 + second/3600 + microsecond/3.6e9) / 24.0
    is_gregorian = (y > 1582) or (y == 1582 and (m > 10 or (m == 10 and day >= 15.0)))
    if m <= 2:
        y -= 1
        m += 12

    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4) if is_gregorian else 0

    # Use floor, not int, for mathematical correctness (esp. BCE)
    C = math.floor(365.25 * y)
    D = math.floor(30.6001 * (m + 1))

    jd = B + C + D + day + 1720994.5
    return jd

def jdDatetime(dt: datetime):
    """
    :param dt: The date and time to convert to Julian. If the date is naive (no timezone info), it is
    assumed to be local time and is converted to UTC. Else, the julian date is calculated for the given
    timestamp.
    :return: Julian date with fractional part included.
    """
    # Ensure 'dt' is timezone-aware. If naive, assume local time:
    if dt.tzinfo is None:
        dt = dt.astimezone()  # attach local tz
    dt_utc = dt.astimezone(timezone.utc)

    return gregToJulian(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour, dt_utc.minute, dt_utc.second, dt_utc.microsecond)

def jdToGreg(jd):
    """
    Convert Julian Date (JD) to Gregorian calendar date + time (UTC).
    Returns (year, month, day, hour, minute, second, microsecond).
    """
    # Split into integer & fractional parts with noon anchor handled
    jd += 0.5
    Z = math.floor(jd)   # integer part
    F = jd - Z           # fractional part

    # Gregorian vs Julian calendar
    if Z >= 2299161:
        alpha = math.floor((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - math.floor(alpha / 4)
    else:
        A = Z

    B = A + 1524
    C = math.floor((B - 122.1) / 365.25)
    D = math.floor(365.25 * C)
    E = math.floor((B - D) / 30.6001)

    # Day with fractional part
    day = B - D - math.floor(30.6001 * E) + F

    # Month
    if E < 14:
        month = E - 1
    else:
        month = E - 13

    # Year
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    # Extract time from fractional day
    day_int = int(math.floor(day))
    frac = day - day_int
    hours = int(math.floor(frac * 24.0))
    frac = frac * 24.0 - hours
    minutes = int(math.floor(frac * 60.0))
    frac = frac * 60.0 - minutes
    seconds = int(math.floor(frac * 60.0))
    frac = frac * 60.0 - seconds
    microseconds = int(round(frac * 1000000))

    # Normalize potential rounding overflow
    if microseconds == 1000000:
        microseconds = 0
        seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        hours += 1
    if hours == 24:
        hours = 0
    return (year, month, day_int, hours, minutes, seconds, microseconds)

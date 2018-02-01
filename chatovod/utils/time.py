
def twelve_to_24_clock(hour, period):
    """Convert 12-hour clock format to 24-hour clock format.

    :param hour: the current hour.
    :param period: the current time period. `AM` or `PM`.
    Other values raise an `Exception`.
    """
    if not (hour >= 0 and hour <= 12):
        raise ValueError("Invalid 12-hour clock time. Got {0}".format(hour))

    if period == 'AM':
        if hour == 12:
            return 0
    elif period == 'PM':
        if hour < 12:
            return hour + 12
    else:
        raise ValueError("Unknown time period {0!r}".format(period))

    return hour

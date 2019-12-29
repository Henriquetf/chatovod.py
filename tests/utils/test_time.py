import pytest

from chatovod.utils.time import twelve_to_24_clock


@pytest.mark.parametrize(
    "hour,period,expected",
    [
        (12, "AM", 0),
        (1, "AM", 1),
        (11, "AM", 11),
        (1, "PM", 13),
        (11, "PM", 23),
        (12, "PM", 0),
    ],
)
def test_twelve_to_24_clock(hour, period, expected):
    assert twelve_to_24_clock(hour, period) == expected


@pytest.mark.parametrize(
    "hour,period", [(0, "AM"), (0, "PM"), (13, "AM"), (13, "PM"), (10, "AMPM")],
)
def test_invalid_hours(hour, period):
    with pytest.raises(ValueError):
        twelve_to_24_clock(hour, period)

import datetime

from chatovod.structures.base import Model
from chatovod.structures.field import Field, ExtraField
from chatovod.util.time import twelve_to_24_clock


def parse_until(fields):
    minute = int(fields.get('minute'))
    hour = int(fields.get('hour'))
    day = int(fields.get('day'))
    month = int(fields.get('month'))
    year = int(fields.get('year'))

    # Converting 12 to 24 hours clock
    period = fields.get('period')
    if period is not None:
        hour = twelve_to_24_clock(hour, period)

    until = datetime.datetime(year, month, day, hour, minute)

    return until


class BanEntry(Model):

    id = Field(int, 'id')
    nickname = Field(str, 'nickname')
    author = Field(str, 'author')
    comment = Field(str, 'comment')
    duration = Field(int, 'duration')
    until = ExtraField(parse_until)

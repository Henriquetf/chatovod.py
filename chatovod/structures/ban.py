import datetime

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


class BanEntry:

    def __init__(self, *, event):
        self.id = event['id']
        self.nickname = event['nickname']
        self.author = event['author']
        self.comment = event['comment']
        self.duration = event['duration']

        # TODO: Find out how the hell parse_until was called before
        self.until = parse_until()

# -*- encoding: UTF-8 -*-

import re
from datetime import date, time

from bs4 import BeautifulSoup, SoupStrainer

from .time import twelve_to_24_clock

# Makes BeautifulSoup parse only label elements
PARSE_ONLY_BAN_ENTRIES = SoupStrainer("label")

# RegEx to extract informations from the ban list.
# This is meant to be used for tt(Tatar) language.
# az(Azeri) is the least likely to break, however
# the nickname of the banned user doesn't show up in it(server-side bug).
# Tatar seems to be the second most reliable option
# since it is not used that much in Chatovod,
# considering the default language URL redirection.
# ### Example ###
# 'Fluffy дат(тан) 12.31.2016 12.50 AM чаклы (120 minutes) '
# 'модераторларга EvilModerator, комментарий: I banned you'


parse_ban_message = re.compile(
    r"""([ ]+)? # There is an space between the banEntry tag and the nickname
        (?P<nickname>.{1,25}?) # A nickname may contain 25 characters at most
        ([ ]\S*[ ])            # Single space, non-space characters, single space
        (?P<month>[0-9]{1,2})  # Month
        .(?P<day>[0-9]{1,2})   # Day
        .(?P<year>[0-9]{1,4})  # Year
        [ ]                    # Space
        (?P<hour>[0-9]{1,2}).(?P<minute>[0-9]{1,2}) # Hour and minute
                                                    # in 12-hour clock format
        [ ]
        (?P<period>AM|PM) # Period of the day - AM or PM
        ([ ]\S*[ ])
        \(                        # The following will be wrapped in parenthesis
            (?P<duration>[0-9,]+) # Duration of the ban in minutes
            ([ ]\w+)              # Space, word minutes
        \)                        # Close parenthesis
        ([ ]\S*[ ])
        (?P<author>.{1,25}?)  # Nickname of the author of the ban
        (,[ ]комментарий:[ ]) # We need this to know when the author nickname
                              # ends and when the ban comment starts
        (?P<comment>(.|\n){,256}?)$""",
    re.VERBOSE,
)


def patch_ban_info(ban_info):
    patched_year = 2000 + int(ban_info["year"])
    patched_month = int(ban_info["month"])
    patched_day = int(ban_info["day"])

    patched_hour = twelve_to_24_clock(int(ban_info["hour"]), ban_info["period"])
    patched_minute = int(ban_info["minute"])

    patched_nickname = ban_info["nickname"].strip()
    # Strips the commas out of the duration string
    patched_duration = int(join_all_numbers(ban_info["duration"]))

    patched_ban = {
        "id": ban_info["id"],
        "nickname": patched_nickname,
        "time": time(patched_hour, patched_minute),
        "date": date(patched_year, patched_month, patched_day),
        "duration": patched_duration,
        "author": ban_info["author"],
        "comment": ban_info["comment"],
    }

    return patched_ban


def generate_bans_info_from_html(html_ban_list, parser="html.parser"):
    """An utility function for parsing HTML ban lists.

    :param ban_list: the HTML ban list returned by the Chatovod API.
    """

    # A soup containing all ban entry elements found in the HTML string
    ban_entries_soup = BeautifulSoup(
        html_ban_list, parser, parse_only=PARSE_ONLY_BAN_ENTRIES
    )

    for ban_entry in ban_entries_soup:
        # Match the child element which contains the ID of the ban
        # Used to identify valid ban entries
        ban_data = ban_entry.find(class_="banEntry")
        if ban_data is None:
            continue

        ban_info_match = parse_ban_message.search(ban_entry.text)
        ban_info = ban_info_match.groupdict()
        ban_info["id"] = ban_data["value"]

        yield ban_info


def join_all_numbers(string, separator=""):
    return separator.join([char for char in string if char.isdigit()])

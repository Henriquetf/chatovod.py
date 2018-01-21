# -*- encoding: UTF-8 -*-

from bs4 import BeautifulSoup, SoupStrainer
from re import compile as re_compile


# Makes BeautifulSoup parse only ban entry elements
only_ban_entries = SoupStrainer('label')

# RegEx to extract informations from the ban list.
# This is meant to be used for tt(Tatar) language.
# az(Azeri) is the least likely to break, however
# the nickname of the banned user doesn't show up in it(server-side bug).
# Tatar seems to be the second most reliable option
# since it is not used that much in Chatovod,
# considering the default language URL redirection.
parse_ban_message = re_compile(
    r'(?P<nickname>.{,25}?) дат\(тан\) '
    r'(?P<month>[0-9]+).(?P<day>[0-9]+).(?P<year>[0-9]+) '
    r'(?P<hour>[0-9]+).(?P<minute>[0-9]+) (?P<period>AM|PM) чаклы '
    r'\((?P<duration>[0-9,]+) \w+\) модераторларга '
    r'(?P<author>.{,25}?), комментарий: (?P<comment>(.|\n){,256}?)')


def patch_ban_info(ban_info, ban_data):
    # Add 'id' field contained in the child element
    # And strips the commas out of the duration string
    ban_info['id'] = ban_data['value']
    ban_info['duration'] = join_all_numbers(ban_info['duration'])

    return ban_info


def generate_bans_info_from_html(html_ban_list, parser='html.parser'):
    """An utility function for parsing HTML ban lists.

    :param ban_list: the HTML ban list returned by the Chatovod API.
    """

    # A soup containing all ban entry elements found in the HTML string
    ban_entries_soup = BeautifulSoup(html_ban_list,
                                     parser,
                                     parse_only=only_ban_entries)

    for ban_entry in ban_entries_soup:
        # Match the child element which contains the ID of the ban
        # Used to identify valid ban entries
        ban_data = ban_entry.find(class_='banEntry')
        if ban_data is None:
            continue

        ban_info_match = parse_ban_message.search(ban_entry.text)
        ban_info = patch_ban_info(ban_info_match.groupdict(), ban_data)

        yield ban_info


def join_all_numbers(string, separator=''):
    return separator.join([char for char in string if char.isdigit()])

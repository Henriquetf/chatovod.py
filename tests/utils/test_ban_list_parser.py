from datetime import date, time
from typing import List, NamedTuple

import pytest

from chatovod.utils.parsers import generate_bans_info_from_html, patch_ban_info


class BanInfo(NamedTuple):
    html: str
    expected_parse: dict
    expected_patch: dict


BanInfoList = List[BanInfo]


BAN_LIST: BanInfoList = [
    BanInfo(
        html='    <p><label><input type="checkbox" class="banEntry" value="2479317"/> P&atilde;o Macio дат(тан) 6/26/17 7:27 PM чаклы (44,640 минут) модераторларга Kryptonite, комментарий: &lt;label&gt;&lt;/label&gt;&lt;/html&gt;</label></p>\r\n',  # noqa
        expected_parse={
            "id": "2479317",
            "nickname": "Pão Macio",
            "day": "26",
            "month": "6",
            "year": "17",
            "minute": "27",
            "hour": "7",
            "period": "PM",
            "duration": "44,640",
            "author": "Kryptonite",
            "comment": "<label></label></html>",
        },
        expected_patch={
            "id": "2479317",
            "nickname": "Pão Macio",
            "date": date(2017, 6, 26),
            "time": time(19, 27),
            "duration": 44640,
            "author": "Kryptonite",
            "comment": "<label></label></html>",
        },
    ),
    BanInfo(
        html='    <p><label><input type="checkbox" class="banEntry" value="2477617"/> Test ban дат(тан) 6/1/17 8:49 PM чаклы (10,080 минут) модераторларга Kryptonite, комментарий: afsfsafsafs@$@$</label></p>\r\n',  # noqa
        expected_parse={
            "id": "2477617",
            "nickname": "Test ban",
            "day": "1",
            "month": "6",
            "year": "17",
            "minute": "49",
            "hour": "8",
            "period": "PM",
            "duration": "10,080",
            "author": "Kryptonite",
            "comment": "afsfsafsafs@$@$",
        },
        expected_patch={
            "id": "2477617",
            "nickname": "Test ban",
            "date": date(2017, 6, 1),
            "time": time(20, 49),
            "duration": 10080,
            "author": "Kryptonite",
            "comment": "afsfsafsafs@$@$",
        },
    ),
    BanInfo(
        html='    <p><label><input type="checkbox" class="banEntry" value="2477613"/> bah64 дат(тан) 6/25/17 8:49 PM чаклы (44,640 минут) модераторларга Kryptonite, комментарий: test</label></p>\r\n',  # noqa
        expected_parse={
            "id": "2477613",
            "nickname": "bah64",
            "day": "25",
            "month": "6",
            "year": "17",
            "minute": "49",
            "hour": "8",
            "period": "PM",
            "duration": "44,640",
            "author": "Kryptonite",
            "comment": "test",
        },
        expected_patch={
            "id": "2477613",
            "nickname": "bah64",
            "date": date(2017, 6, 25),
            "time": time(20, 49),
            "duration": 44640,
            "author": "Kryptonite",
            "comment": "test",
        },
    ),
]


@pytest.fixture
def ban_list():
    return BAN_LIST


@pytest.fixture(params=BAN_LIST)
def bans_loop(request):
    return request.param


@pytest.fixture
def html_ban_list(ban_list):
    return (
        '    <p><input type="button" class="refresh" value="Яңартырга"/> <input type="button" class="unban" value="Билгеләнгәннәрне банга кую"/></p>\r\n'  # noqa
        + "".join([ban.html for ban in ban_list])
    )


def test_parse_returns_correct_size(html_ban_list):
    assert len(list(generate_bans_info_from_html(html_ban_list))) == 3


def test_parse_bans(bans_loop: BanInfo):
    assert (
        next(generate_bans_info_from_html(bans_loop.html)) == bans_loop.expected_parse
    )


def test_patch_bans(bans_loop: BanInfo):
    assert patch_ban_info(bans_loop.expected_parse) == bans_loop.expected_patch


def test_all_parses(html_ban_list, ban_list: BanInfoList):
    for index, parse in enumerate(generate_bans_info_from_html(html_ban_list)):
        assert parse == ban_list[index].expected_parse


def test_all_patches(html_ban_list, ban_list: BanInfoList):
    for index, patch in enumerate(generate_bans_info_from_html(html_ban_list)):
        assert patch_ban_info(patch) == ban_list[index].expected_patch

"""Routine functions for Infomark Platform CLI."""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Match, Optional, Tuple, Union

from dateutil.relativedelta import relativedelta
from infomark_cli.session import Session

session = Session()

# pylint: disable=too-many-statements,eval-used,consider-iterating-dictionary
# pylint: disable=too-many-branches,too-many-return-statements

# Necessary for Infomark keywords
MONTHS_VALUE = {
    "JANUARY": 1,
    "FEBRUARY": 2,
    "MARCH": 3,
    "APRIL": 4,
    "MAY": 5,
    "JUNE": 6,
    "JULY": 7,
    "AUGUST": 8,
    "SEPTEMBER": 9,
    "OCTOBER": 10,
    "NOVEMBER": 11,
    "DECEMBER": 12,
}

WEEKDAY_VALUE = {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2,
    "THURSDAY": 3,
    "FRIDAY": 4,
    "SATURDAY": 5,
    "SUNDAY": 6,
}

def is_reset(command: str) -> bool:
    """Test whether a command is a reset command.

    Parameters
    ----------
    command : str
        The command to test

    Returns
    -------
    bool
        Whether the command is a reset command
    """
    return "reset" in command or command in ("r", "r\n")

def match_and_return_infomark_keyword_date(keyword: str) -> str:  # noqa: PLR0911
    """Return Infomark keyword into date.

    Parameters
    ----------
    keyword : str
        String with potential Infomark keyword (e.g. 1MONTHAGO,LASTFRIDAY,3YEARSFROMNOW,NEXTTUESDAY)

    Returns
    -------
    str
        Date with format YYYY-MM-DD
    """
    now = datetime.now()
    for i, regex in enumerate([r"^\$(\d+)([A-Z]+)AGO$", r"^\$(\d+)([A-Z]+)FROMNOW$"]):
        match = re.match(regex, keyword)
        if match:
            integer_value = int(match.group(1))
            time_unit = match.group(2)
            clean_time = time_unit.upper()
            kwargs = {time_unit.lower(): integer_value}
            if i == 0:
                return (now - relativedelta(**kwargs)).strftime("%Y-%m-%d")
            return (now + relativedelta(**kwargs)).strftime("%Y-%m-%d")

    match

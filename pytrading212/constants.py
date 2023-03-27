"""Constants"""
from enum import Enum

LOGIN_URL = "https://www.trading212.com/en/login"
COOKIES_NOTICE_BUTTON = "'CookiesNotice_button__q5YaL'"


class Mode(Enum):
    DEMO = "demo",
    LIVE = "live"


class Trading(Enum):
    CFD = "CFD",
    EQUITY = "EQUITY",


class Period(Enum):
    LAST_DAY = "LAST_DAY",
    LAST_WEEK = "LAST_WEEK",
    LAST_MONTH = "LAST_MONTH",
    LAST_THREE_MONTHS = "LAST_THREE_MONTHS",
    LAST_YEAR = "LAST_YEAR",
    ALL = "ALL",


class OrderType(Enum):
    LIMIT = "LIMIT"
    STOP = "STOP"
    MARKET = "MARKET"
    STOP_LIMIT = "STOP_LIMIT"


class TimeValidity(Enum):
    DAY = "DAY",
    GOOD_TILL_CANCEL = "GOOD_TILL_CANCEL"

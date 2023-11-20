"""General Constants"""
from enum import Enum

URL_LOGIN = "https://www.trading212.com/en/login"
CLASS_COOKIES_NOTICE_BUTTON = "CookiesNotice_button__q5YaL"
CLASS_LOGIN_BUTTON = "SubmitButton_input__IV2dl"
CLASS_EQUITY_ICON = "equity-icon"
CLASS_CFD_ICON = "cfd-icon"
PYTRADING212_VERSION = "0.2.5"

ONE_WEEK = "ONE_WEEK"

class Mode(Enum):
    """Mode Type"""
    DEMO = "demo",
    LIVE = "live"


class Trading(Enum):
    """Trading Type"""
    CFD = "CFD",
    EQUITY = "EQUITY",


class Period(Enum):
    """Period of Portfolio Performance"""
    LAST_DAY = "LAST_DAY",
    LAST_WEEK = "LAST_WEEK",
    LAST_MONTH = "LAST_MONTH",
    LAST_THREE_MONTHS = "LAST_THREE_MONTHS",
    LAST_YEAR = "LAST_YEAR",
    ALL = "ALL",



class OrderType(Enum):
    """Order Type"""
    LIMIT = "LIMIT"
    STOP = "STOP"
    MARKET = "MARKET"
    STOP_LIMIT = "STOP_LIMIT"


class TimeValidity(Enum):
    """Time Validity for Limit/Stop Orders"""
    DAY = "DAY",
    GOOD_TILL_CANCEL = "GOOD_TILL_CANCEL"

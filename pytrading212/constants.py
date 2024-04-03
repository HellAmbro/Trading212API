"""General Constants"""
from enum import Enum

URL_LOGIN = "https://www.trading212.com/en/login"
CLASS_COOKIES_NOTICE_BUTTON = "CookiesNotice_button__q5YaL"
CLASS_LOGIN_BUTTON = "SubmitButton_input__IV2dl"
CLASS_EQUITY_ICON = "equity-icon"
CLASS_CFD_ICON = "cfd-icon"
PYTRADING212_VERSION = "0.2.6"
SELECTOR_NEW_APP = ("#root > div > div > div > div > div > div > div:nth-child(1) > "
                    "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > "
                    "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > div > div > div > div "
                    "> div > div > div > div.css-175oi2r.r-13awgt0 > div > "
                    "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div:nth-child(2) > div "
                    "> div.css-175oi2r.r-13awgt0.r-1udh08x > div > div.css-175oi2r.r-13awgt0 > div > div > div > div "
                    "> div > div > div.css-175oi2r.r-13awgt0 > div > "
                    "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div:nth-child(2) > div "
                    "> div.css-175oi2r.r-13awgt0.r-1udh08x > div > div.css-175oi2r.r-13awgt0 > div > div > "
                    "div.css-175oi2r.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > "
                    "div.css-175oi2r.r-1loqt21.r-1otgn73 > div > div")
SELECTOR_MENU_BUTTON = ("#root > div > div > div > div > div > div > div:nth-child(1) > div > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div > div > "
                        "div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(5) > div > span > div")
SELECTOR_LIVE_ACCOUNT = ("#root > div > div > div > div > div > div > div:nth-child(1) > div > "
                         "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div > div > "
                         "div:nth-child(1) > div > div > div:nth-child(3) > div:nth-child(1) > div > div > div")
SELECTOR_LIVE_EQUITY = ("#root > div > div > div > div > div > div > div:nth-child(1) > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > div:nth-child(3) > "
                        "div > div.css-175oi2r.r-12vffkv > div > div > "
                        "div.css-175oi2r.r-150rngu.r-eqz5dr.r-16y2uox.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > "
                        "div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div.css-175oi2r")
SELECTOR_DEMO_EQUITY = ("#root > div > div > div > div > div > div > div:nth-child(1) > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-105ug2t > div:nth-child(3) > "
                        "div > div.css-175oi2r.r-12vffkv > div > div > "
                        "div.css-175oi2r.r-150rngu.r-eqz5dr.r-16y2uox.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > "
                        "div:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
SELECTOR_MENU_LIST = ("#root > div > div > div > div > div > div > div:nth-child(1) > div > "
                      "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div > div > "
                      "div:nth-child(2) > div > div > div:nth-child(2) > div > div > div > div > div > "
                      "div.css-175oi2r.r-13awgt0 > div > "
                      "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div:nth-child(2) > "
                      "div > div > div > div.css-175oi2r.r-13awgt0 > div > div:nth-child(1)")
SELECTOR_SWITCH_DEMO = ("#root > div > div > div > div > div > div > div:nth-child(1) > div > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div > div > "
                        "div:nth-child(2) > div > div > div:nth-child(2) > div > div > div > div > div > "
                        "div.css-175oi2r.r-13awgt0 > div > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div:nth-child(2) > "
                        "div > div > div > div.css-175oi2r.r-13awgt0 > div > div:nth-child(1) > div > div > div > div "
                        "> div.css-175oi2r.r-13awgt0 > div > "
                        "div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div:nth-child(2) > "
                        "div > div.css-175oi2r.r-13awgt0.r-1udh08x > div > div.css-175oi2r.r-13awgt0 > div > "
                        "div:nth-child(2) > div.css-175oi2r.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r"
                        "-1rnoaur.r-1sncvnh > div > div:nth-child(3) > "
                        "div.css-175oi2r.r-1otgn73.r-1loqt21.r-1awozwy.r-1777fci.r-utggzx")

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

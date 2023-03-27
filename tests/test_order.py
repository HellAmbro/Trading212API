import pytest

from pytrading212 import constants


@pytest.fixture
def test_order():
    from pytrading212 import EquityOrder
    def test_order(equity_order: EquityOrder, expected_json: str):
        assert equity_order.to_json().replace(" ", "") == expected_json.replace(" ", "")

    return test_order


def test_market_order(test_order):
    from pytrading212 import MarketOrder
    test_order(
        equity_order=MarketOrder(instrument_code="AAPL_US_EQ", quantity=1),
        expected_json='{"instrumentCode":"AAPL_US_EQ","orderType":"MARKET","quantity":1}'
    )


def test_limit_order(test_order):
    from pytrading212 import LimitOrder
    test_order(
        equity_order=LimitOrder(instrument_code="AAPL_US_EQ",
                                quantity=2,
                                limit_price=150,
                                time_validity=constants.TimeValidity.DAY),
        expected_json='{"instrumentCode":"AAPL_US_EQ","orderType":"LIMIT",'
                      '"quantity":2,"limitPrice":150,"timeValidity":"DAY"}'
    )


def test_stop_order(test_order):
    from pytrading212 import StopOrder
    test_order(equity_order=StopOrder(instrument_code="AAPL_US_EQ", quantity=1, stop_price=150,
                                      time_validity=constants.TimeValidity.GOOD_TILL_CANCEL),
               expected_json='{"instrumentCode":"AAPL_US_EQ","orderType":"STOP","quantity":1,"stopPrice":150,'
                             '"timeValidity":"GOOD_TILL_CANCEL"}')


def test_stop_limit_order(test_order):
    from pytrading212 import StopLimitOrder
    test_order(equity_order=StopLimitOrder(instrument_code="AAPL_US_EQ", quantity=1, limit_price=150, stop_price=160,
                                           time_validity=constants.TimeValidity.DAY),
               expected_json='{"instrumentCode":"AAPL_US_EQ","orderType":"STOP_LIMIT","quantity":1,"limitPrice":150,'
                             '"stopPrice":160,"timeValidity":"DAY"}')


def test_value_order(test_order):
    from pytrading212 import ValueOrder
    test_order(equity_order=ValueOrder(instrument_code="AAPL_US_EQ", value=2500.0),
               expected_json='{"instrumentCode":"AAPL_US_EQ","orderType":"MARKET","value":2500.0}')

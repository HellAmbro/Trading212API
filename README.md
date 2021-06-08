# Trading212 API

**Unofficial** API for Trading212 broker.

#### CFD are not suppoerted yet (only experimental for now). Investing only.

#### Support project

<a href="https://www.buymeacoffee.com/hellambro" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="50" ></a>

LTC: LbAzhtHBvQ2JCGhrcefUuvwNrv9VrQJoyJ  

BTC: 1JWhMC3tiSjyR6t7BJuM7YRDg3xvPM2MDk

ETH: 0x51f1f0061eadc024ab4bd1f3658d249044160006

### Disclaimer

#### Nor me or Trading212 are responsible for the use of this API, first make sure that everything works well through the use of a **DEMO** account, then switch to **REAL** mode.

### Prerequisites

WebDriver [Getting started with WebDriver](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/)

### Troubleshooting

[Driver requirements](https://www.selenium.dev/documentation/en/webdriver/driver_requirements)

### Install

````python
pip3 install pytrading212
````

### Usage

Refer here: [example.py](https://github.com/HellAmbro/Trading212API/blob/master/example.py)

````python
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from pytrading212 import *  # just for simplicity, not recommended, import only what you use
from pytrading212.trading212 import Period

# Use your preferred web driver with your custom options
# options = Options()
# headless (optional)
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# Chrome
driver = webdriver.Chrome()
# or Firefox
# driver = webdriver.Firefox()

trading212 = Trading212('myemail', 'mypass', driver, mode=Mode.DEMO)

market_order = trading212.execute_order(
    MarketOrder(instrument_code="AMZN_US_EQ", quantity=2)
)

limit_order = trading212.execute_order(
    LimitOrder(
        instrument_code="AMZN_US_EQ",
        quantity=2,
        limit_price=3000,
        time_validity=TimeValidity.DAY,
    )
)

stop_order = trading212.execute_order(
    StopOrder(
        instrument_code="AMZN_US_EQ",
        quantity=2,
        stop_price=4000,
        time_validity=TimeValidity.GOOD_TILL_CANCEL,
    )
)

stop_limit = trading212.execute_order(
    StopLimitOrder(
        instrument_code="AMZN_US_EQ",
        quantity=2,
        limit_price=3000,
        stop_price=4000,
        time_validity=TimeValidity.GOOD_TILL_CANCEL,
    )
)

quantity_order = trading212.execute_order(
    EquityOrder(
        "AMZN_US_EQ",
        quantity=2,
        limit_price=3000,
        stop_price=4000,
        time_validity=TimeValidity.GOOD_TILL_CANCEL,
    )
)

value_order = trading212.execute_value_order(ValueOrder("AMZN_US_EQ", value=100))

# sell an equity that you own

value_sell_order = trading212.execute_value_order(
    ValueOrder("AMZN_US_EQ", value=-100)
)

sell_limit = trading212.execute_order(
    LimitOrder(
        instrument_code="AMZN_US_EQ",
        quantity=-2,
        limit_price=4000,
        time_validity=TimeValidity.GOOD_TILL_CANCEL,
    )
)

print(quantity_order)
print(value_order)

funds = trading212.get_funds()
orders = trading212.get_orders()

print(funds)
print(orders)

portfolio = trading212.get_portfolio_composition()
performance = trading212.get_portfolio_performance(Period.LAST_DAY)

print(portfolio)
print(performance)
# Pandas integration examples
funds_df = pd.DataFrame(funds)
orders_df = pd.DataFrame(orders)
portfolio_df = pd.DataFrame(portfolio)
performance_df = pd.DataFrame(performance)

# close webdriver 
trading212.close()
````
### Funds (as DataFrame)
````
accountId                                            XXXXXXX                                   XXXXXXX
tradingType                                           EQUITY                                       CFD
currency                                                 EUR                                       EUR
freeForWithdraw                                      2784.75                                  47680.45
freeForCfdTransfer                                   2784.75                                         0
total                                               10075.08                                  47680.45
lockedCash          {'totalLockedCash': 0, 'lockedCash': []}  {'totalLockedCash': 0, 'lockedCash': []}
````

### Portfolio

````python
portfolio = trading212.get_portfolio_composition()
````

````
[
  {
    'logo_url': 'https://trading212equities.s3.eu-central-1.amazonaws.com/BABA_US_EQ.png',
    'instrument_code': 'BABA_US_EQ',
    'value': '€9.28',
    'quantity': '0.0479677 shares',
    'total_return': '€0.28 (3.11%)'
  },
  {
    'logo_url': 'https://trading212equities.s3.eu-central-1.amazonaws.com/AMZN_US_EQ.png',
    'instrument_code': 'AMZN_US_EQ',
    'value': '€15,625.60',
    'quantity': '6.00353784 shares',
    'total_return': '€75.57 (0.49%)'
  },
]
````

### Performance

````python
trading212.get_portfolio_performance(Period.LAST_DAY)
````

````
{
  'snapshots': [
    {
      'investment': 16438.3,
      'ppl': -159.81,
      'result': -17.92,
      'pieCash': 0.05,
      'time': '2021-01-13T11:00:00Z'
    },
    {
      'investment': 16438.3,
      'ppl': -158.06,
      'result': -17.92,
      'pieCash': 0.05,
      'time': '2021-01-13T11:15:00Z'
    },
    -- snip --
````

### How can I get instrument code?

Lookup in companies.json, key "ticker"

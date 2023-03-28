<div align="center">

# PyTrading212 API

### Unofficial API for Trading212

### [Documentation](https://hellambro.github.io/Trading212API/)

</div>

<div align="left">

## Installation

```bash
pip install pytrading212
```
### Warning :warning:
When you are using the API you cannot access Trading212 from other devices and browsers, except for the webdriver.A new access from another browser may disconnect the current session, invalidating the _cookie_ and making the API not work.
### Example PyTrading212 Usage

Complete code

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pytrading212 import Equity
from pytrading212 import Mode, EquityOrder, OrderType

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
equity = Equity(email='your_email', password='your_password', driver=driver, mode=Mode.DEMO)

# Invalid order: voluntary typo-error in instrument code
order = EquityOrder(instrument_code="AAPLL_US_EQ", order_type=OrderType.MARKET, quantity=1)
is_valid, reason = equity.check_order(order)
if is_valid:
    print("Your order is valid, can be executed")
else:
    print("The reason is: ", reason)

# Valid order
order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=2)

# Check order validity (recommended)
if equity.check_order(order)[0]:
    # Review order (recommended)
    print(equity.review_order(order))
    # Execute order
    print(equity.execute_order(order))

equity.finish()
```

### PyTrading212 initialization
:warning: As now March 2023 only one instance at time is supported. :warning:

:x: This means that you cannot initialize both **Equity** and **CFD** :x:

PyTrading212 **Equity** instance
```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
equity = Equity(email='your_email', password='your_password', driver=driver, mode=Mode.DEMO)
```
PyTrading212 **CFD** instance
```python
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
cfd = CFD(email='your_email', password='your_password', driver=driver, mode=Mode.DEMO)
```
### PyTrading212 close session
Close the session, also the webdriver is closed.
```python
equity.finish()
```
## Documentation

### Structure

![order](docs/imgs/order_structure.png)

### [Equity Order](https://hellambro.github.io/Trading212API/order.html#pytrading212.order.EquityOrder)

It's possible to create **equity orders** directly from `EquityOrder` class

```python
order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=1)
```

or alternatively

```python
market_order = MarketOrder(instrument_code="AAPL_US_EQ", quantity=1)
```

These two orders are equivalent, you can use both ways indifferently.

All other **equity order classes** are wrappers of the `EquityOrder`

#### Wrappers for equity orders

- MarketOrder
- LimitOrder
- StopOrder
- StopLimitOrder
- ValueOrder

These classes allow to simplify the creation of orders, avoiding errors for omitted parameters,
improving code readability, as the order type is specified.

### Useful resources

- [Use Trading212 for Automatic Trading: an introduction to pytrading212](https://medium.com/@francescoelambroambrosini/use-trading212-for-automatic-trading-an-introduction-to-pytrading212-367449b40a6)
- [Driver requirements](https://www.selenium.dev/documentation/en/webdriver/driver_requirements)
- [Getting started with WebDriver](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/)

### Support the project

<a href="https://www.buymeacoffee.com/hellambro" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="50" ></a>

LTC: LbAzhtHBvQ2JCGhrcefUuvwNrv9VrQJoyJ

BTC: 1JWhMC3tiSjyR6t7BJuM7YRDg3xvPM2MDk

ETH: 0x51f1f0061eadc024ab4bd1f3658d249044160006

### Disclaimer

Nor me or Trading212 are responsible for the use of this API, first make sure that everything works well through the use
of a **DEMO** account, then switch to **REAL** mode.

All trademarks, logos and brand names are the property of their respective owners. All company, product and service
names used in this website are for identification purposes only.

</div>
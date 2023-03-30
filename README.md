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

When you are using the API you cannot access Trading212 from other devices and browsers, except for the webdriver.New
access from another browser may disconnect the current session, invalidating the _cookie_ and making the API not work.

## PyTrading212 Usage

For a full reference please look inside **examples** folder

### Equity Example

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

### CFD Example

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pytrading212 import CFD, CFDOrder, CFDMarketOrder
from pytrading212 import Mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
cfd = CFD(email='your_email', password='your_password', driver=driver, mode=Mode.DEMO)

instrument_code = "AAPL"

cfd_order = CFDOrder(instrument_code=instrument_code,
                     quantity=-0.1,  # Sell (quantity is negative)
                     target_price=cfd.get_current_price(instrument_code=instrument_code)
                     )

print(cfd.execute_order(order=cfd_order))
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

```python
cfd.finish()
```

## Documentation

### Structure

![order](docs/imgs/order_structure.png)

### [Equity Order](https://hellambro.github.io/Trading212API/order.html#pytrading212.order.EquityOrder)

It's possible to create **equity orders** directly from `EquityOrder` class

```python
# Buy
order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=1)
equity.execute_order(order=order)
```

or alternatively

```python
# Buy
market_order = MarketOrder(instrument_code="AAPL_US_EQ", quantity=1)
equity.execute_order(order=market_order)
```

These two orders are equivalent, you can use both ways indifferently.
or alternatively

For selling stocks (**that you own**, for short-selling see CFD section below) you just need to change the sign of
_quantity_ or _value_ property

```python
# Sell
order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=-1)
equity.execute_order(order=order)
```

or alternatively

```python
# Sell
market_order = MarketOrder(instrument_code="AAPL_US_EQ", quantity=-1)
equity.execute_order(order=market_order)
```

All other **equity order classes** are wrappers of the `EquityOrder`

#### Wrappers for Equity Orders

- MarketOrder

```python
market_order = MarketOrder(instrument_code="AAPL_US_EQ", quantity=1)
```

- LimitOrder

```python
limit_order = LimitOrder(instrument_code="AAPL_US_EQ",
                         quantity=2,
                         limit_price=150.0,
                         time_validity=constants.TimeValidity.DAY)
```

- StopOrder

```python
stop_order = StopOrder(instrument_code="AAPL_US_EQ",
                       quantity=-3,  # Sell
                       stop_price=180.0,
                       time_validity=constants.TimeValidity.GOOD_TILL_CANCEL)
```

- StopLimitOrder

```python
stop_limit_order = StopLimitOrder(instrument_code="AAPL_US_EQ",
                                  quantity=1,
                                  limit_price=150,
                                  stop_price=180,
                                  time_validity=constants.TimeValidity.DAY)
```

- ValueOrder

```python
value_order = ValueOrder(instrument_code="AAPL_US_EQ", value=2500.0)
```

These classes allow to simplify the creation of orders, avoiding errors for omitted parameters,
improving code readability.

### [CFD Order](https://hellambro.github.io/Trading212API/order.html#pytrading212.order.CFDOrder)

It's possible to create **cfd orders** directly from `CFDOrder` class

```python
cfd_order = CFDOrder(instrument_code=instrument_code,
                     quantity=-0.1,  # Sell (quantity is negative)
                     target_price=cfd.get_current_price(instrument_code=instrument_code)
                     )
```

or alternatively

```python
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.1,  # Buy (quantity is positive)
                           target_price=cfd.get_current_price(instrument_code=instrument_code))
```

These two orders are equivalent, you can use both ways indifferently.

All other **cfd order classes** are wrappers of the `CFDOrder`

#### Wrappers for CFD Orders

- MarketOrder

```python
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.1,  # Buy (quantity is positive)
                           target_price=cfd.get_current_price(instrument_code=instrument_code))
```

- MarketOrder with Take Profit (limit_distance)

```python
instrument_code = "AAPL"
current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           limit_distance=5.0)
```

- MarketOrder with Stop Loss (stop_distance)

```python
instrument_code = "AAPL"
current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           stop_distance=2.0)
```

- MarketOrder with Stop Loss and Take Profit

```python
instrument_code = "AAPL"
current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           limit_distance=4.0,
                           stop_distance=2.0,
                           )
```


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
# Trading212 API
**Unofficial** API for Trading212 broker. 
### CFD are not suppoerted yet. Investing only.
## Disclaimer
#### Nor me or Trading212 are responsible for the use of this API, first make sure that everything works well through the use of a **DEMO** account, then switch to **REAL** mode.
### Prerequisites
chromedriver in your PATH,
##### Download the latest stable release of chromedriver from https://chromedriver.chromium.org/, extract and move it to /usr/local/bin

### Install
````
pip install pytrading212
````
### Usage
#### save_cookies=True
after logging in, the session cookie will be saved, if the cookie is still valid you will not be logged in

````
trading212 = Trading212('your_email', 'password', mode=Mode.DEMO, save_cookies=True)

market_order = trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=2))

limit_order = trading212.execute_order(
    LimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, time_validity=TimeValidity.DAY))

stop_order = trading212.execute_order(
    StopOrder(instrument_code="AMZN_US_EQ", quantity=2, stop_price=4000, time_validity=TimeValidity.GOOD_TILL_CANCEL))

stop_limit = trading212.execute_order(
    StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, stop_price=4000,
                   time_validity=TimeValidity.GOOD_TILL_CANCEL))

trading212.get_funds()
trading212.get_orders()
trading212.cancel_order(14238041)
````

### How can I get instrument code?
Search the stock, open dev-tools of your browser, network, look for a request called 'batch', request payload, ticker, [Example](https://imgur.com/a/7ZZCjku)
#### instrument_code will be mapped in further release of this API, so you can buy Amazon simply writing AMZN or Amazon for example.

### I wrote this API during a trip, I prioritized functionality, there is still a lot to work on the code to make it more elegant and readable. Also this is one of the first projects I do using python so don't be too mean. Any requests, help, advice, suggestions are welcome. HellAmbro.  </span>

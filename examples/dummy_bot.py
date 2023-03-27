"""
Author: HellAmbro

I wrote this dummy bot in 5 minutes just to show how a bot could look like
Please don't use this bot for real purposes
I use alpha vantage to get ticker data, use whatever you want if you are more familiar with

"""

import sys
import time

from alpha_vantage.timeseries import TimeSeries
from selenium import webdriver

from pytrading212 import Trading212, Mode, MarketOrder

email = sys.argv[1]
password = sys.argv[2]

driver = webdriver.Chrome(executable_path='chromedriver.exe')
trading212 = Trading212(email=email, password=password, driver=driver, mode=Mode.DEMO)

# Get json object with the intraday data and another with  the call's metadata
ts = TimeSeries(key='99X56PNBXN3V0SDT', output_format='pandas')

# not really necessary, if you do not have shares available to sell (or money to buy)
# trading212 will return a business exception and your order fails
is_bought = False

# iterate indefinitely
while True:
    data, meta_data = ts.get_intraday(symbol='AMZN', interval='1min', outputsize='compact')
    # get the last close price (1 minute candle)
    last_price = data['4. close'][0]
    # bought amazon if price drop < 3000
    # i think you should use more sophisticated indicators
    if last_price < 3000 and not is_bought:
        # BUY
        trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=1))
        is_bought = True
    # 16% profit! Not bad
    elif last_price > 3500 and is_bought:
        # SELL (note 'quantity=-1')
        trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=-1))
        is_bought = False

    # wait 1 minute for the next tick
    time.sleep(60)

# I know this bot is ridiculous but it's just for example purpose, I hope nobody use it
# If you're writing a trading bot (a real bot of course, not this) contact me if you want

# I'm trying to do the same think, i can help you.
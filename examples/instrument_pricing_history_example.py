import configparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pytrading212 import Equity, Company
from pytrading212 import Mode
from pytrading212.constants import ONE_WEEK

config = configparser.ConfigParser()
config.read('../config.ini')

if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service())
    equity = Equity(
        email=config['ACCOUNT']['email'], password=config['ACCOUNT']['password'],
        driver=driver, mode=Mode.DEMO
    )

    # Create a new instrument
    instrument = Company(instrument_code="AAPL_US_EQ", isin="")

    # Request pricing history for the instrument, this requires a time interval
    # and a trading 212 instance
    print(
        instrument.get_pricing_history(interval=ONE_WEEK, headers=equity.headers, trading_instance=equity)
    )

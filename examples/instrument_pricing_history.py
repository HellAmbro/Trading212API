import configparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pytrading212 import Equity, Company
from pytrading212 import Mode, EquityOrder, OrderType
from pytrading212.constants import ONE_WEEK


config = configparser.ConfigParser()
config.read('../config.ini')


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    equity = Equity(
        email=config['ACCOUNT']['email'], password=config['ACCOUNT']['password'],
        driver=driver, mode=Mode.DEMO
    )

    # Create a new instrument
    instrument = Company(instrument_code="AAPLL_US_EQ", isin="")

    # Request pricing history for the instrument, this requires a time interval
    # and a trading 212 instance
    print(
        instrument.get_pricing_history(interval=ONE_WEEK, trading_instance=equity)
    )

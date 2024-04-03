"""API for Trading212 Platform"""

import json
import logging
import re
import time
from datetime import datetime
from time import strftime
from urllib.parse import urlencode

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from pytrading212 import constants, console
from pytrading212.instrument import CFDInstrument
from pytrading212.order import CFDOrder, EquityOrder
from pytrading212.position import Position


class Trading212:
    def __init__(
            self,
            email: str,
            password: str,
            driver: webdriver,
            mode: constants.Mode = constants.Mode.DEMO,
            trading: constants.Trading = constants.Trading.EQUITY,
    ):
        self.session = f"TRADING212_SESSION_{mode.name}"
        self.base_url = f"https://{mode.name.lower()}.trading212.com"

        console.log(f"Starting PyTrading212 v{constants.PYTRADING212_VERSION}\n"
                    f"Trading: [green]{trading.name}[/green] \n"
                    f"Mode: [green]{mode.name}[/green]")

        self.driver = driver
        self.driver.get(constants.URL_LOGIN)

        # Click Accept all cookies if it appears
        try:
            console.log("Closing 'Cookies Popup'")
            self.driver.find_element(By.CLASS_NAME, constants.CLASS_COOKIES_NOTICE_BUTTON).click()
        except NoSuchElementException:
            pass  # ignore

        console.log("Authenticating")

        WebDriverWait(self.driver, 120).until(expected_conditions.visibility_of_element_located((By.NAME, "email")))

        # Authenticate
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)

        # Click login button
        self.driver.find_element(By.CLASS_NAME, constants.CLASS_LOGIN_BUTTON).click()

        # Close new app button, should be removed later
        try:
            WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, constants.SELECTOR_NEW_APP)))
            self.driver.find_element(By.CSS_SELECTOR, constants.SELECTOR_NEW_APP).click()
        except NoSuchElementException:
            pass

        self.user_agent = self.driver.execute_script("return navigator.userAgent;")

        # Switch to get also DEMO token
        self.switch()
        # Get session cookie
        cookies = self.driver.get_cookies()
        if cookies is not None:
            for cookie in cookies:
                # Get appropriate cookie for this session, live or demo
                if self.session in cookie['name']:
                    self.cookie = f"{self.session}={cookie['value']};"
        else:
            raise Exception("Unable to get cookies, aborting.")

        # Necessary headers for requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "Cookie": self.cookie,
        }

        self.companies = self.get_companies()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

    def finish(self):
        console.log("Closing session.")
        self.driver.close()

    def switch(self):
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, constants.SELECTOR_MENU_BUTTON)))
        self.driver.find_element(By.CSS_SELECTOR, constants.SELECTOR_MENU_BUTTON).click()

        self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);",
                                   self.driver.find_element(By.CSS_SELECTOR, constants.SELECTOR_MENU_LIST))
        self.driver.find_element(By.CSS_SELECTOR, constants.SELECTOR_SWITCH_DEMO).click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, constants.SELECTOR_DEMO_EQUITY)))
        self.driver.find_element(By.CSS_SELECTOR, constants.SELECTOR_DEMO_EQUITY).click()
        # Wait some seconds to initialize cookies
        time.sleep(5)

    def get_funds(self):
        """Get your funds, free, available."""
        response = requests.get(
            f"{self.base_url}/rest/v2/customer/accounts/funds", headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def last_hour_hotlist(self):
        """Trading 212 last hour hotlist"""
        response = requests.get(
            f"{self.base_url}/trading212.com/rest/positions-tracker/deltas/hourly/1"
        )
        return json.loads(response.content.decode("utf-8"))

    def get_orders(self, older_than: datetime, newer_than: datetime):
        """Get orders within a range of dates"""
        params = {
            'olderThan': strftime(older_than.isoformat()),
            'newerThan': strftime(newer_than.isoformat())
        }

        response = requests.get(
            f"{self.base_url}/rest/history/orders", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_transactions(self, older_than: datetime, newer_than: datetime):
        """Get transactions within a range of dates"""
        params = {
            'olderThan': strftime(older_than.isoformat()),
            'newerThan': strftime(newer_than.isoformat())
        }
        response = requests.get(
            f"{self.base_url}/rest/history/transactions", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_order_details(self, details_path):
        """Get Order Details"""
        response = requests.get(f"{self.base_url}/rest/history{details_path}", headers=self.headers)
        return json.loads(response.content.decode("utf-8"))

    def get_dividends(self, older_than: datetime, newer_than: datetime):
        """Get dividends within a range of dates"""
        params = {'olderThan': strftime(older_than.isoformat()),
                  'newerThan': strftime(newer_than.isoformat())
                  }

        response = requests.get(
            f"{self.base_url}/rest/history/dividends", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_fundamentals(self, ticker, language_code: str = "en"):
        """Get fundamentals of a company by its isin"""
        params = {'ticker': ticker,
                  'languageCode': language_code
                  }

        response = requests.get(f"{self.base_url}/rest/companies/v2/fundamentals",
                                params=params)
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_performance(self, time_period: constants.Period):
        """Get Portfolio Performance"""
        response = requests.get(
            url=f"{self.base_url}/rest/v2/portfolio?period={time_period}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_composition(self):
        """Get Portfolio Composition"""
        # click portfolio section on right-sidepanel
        right_sidepanel_portfolio_class = 'portfolio-icon'
        condition = expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, right_sidepanel_portfolio_class)
        )
        WebDriverWait(self.driver, 30).until(condition)
        self.driver.find_element(By.CLASS_NAME, right_sidepanel_portfolio_class).click()

        positions = []
        try:
            # click on investments
            self.driver.find_element(By.CLASS_NAME, 'investment-tab').click()
            for item in self.driver.find_elements(By.CLASS_NAME, "investment-item"):
                ticker = item.get_attribute("data-qa-item")
                value = item.find_element(By.CLASS_NAME, "total-value").text
                quantity = item.find_element(By.CLASS_NAME, "quantity").text
                total_return = item.find_element(By.CLASS_NAME, "return").text
                position = Position(ticker, value, quantity, total_return)
                positions.append(position.__dict__)
        except Exception as e:
            logging.error(e)  # portfolio is empty
        return positions

    def get_companies(self):
        """Get Ticker of all Trading212 tradable companies"""
        response = requests.get(
            url=f"{self.base_url}/rest/companies",
            headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def search(self, query):
        """Search a company"""
        found = []
        companies = self.get_companies()
        for company in companies:
            if query in company["ticker"]:
                found.append(company["ticker"])

        response = requests.post(
            f"{self.base_url}/charting/prices?withFakes=false",
            headers=self.headers,
            data=found.__str__().replace("'", '"'),
        )  # ' with " for Trading212 compatibility
        return json.loads(response.content.decode("utf-8"))


class Equity(Trading212):
    """Trading 212 Equity"""

    def __init__(self, email: str, password: str, driver: webdriver, mode: constants.Mode = constants.Mode.DEMO):
        super().__init__(email, password, driver, mode, constants.Trading.EQUITY)

    def review_order(self, order: EquityOrder):
        """Preview of the order, with added costs and other useful data"""
        # Check if it is a 'value' order or a 'quantity' order
        if hasattr(order, 'value'):
            url = f"{self.base_url}/rest/v1/equity/value-order/review"
        else:
            url = f"{self.base_url}/rest/public/added-costs"
        response = requests.post(
            url=url,
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def execute_order(self, order: EquityOrder):
        """Execute equity order"""
        # Check if it is a 'value' order or a 'quantity' order
        if hasattr(order, 'value'):
            url = f"{self.base_url}/rest/v1/equity/value-order"
        else:
            url = f"{self.base_url}/rest/public/v2/equity/order"
        response = requests.post(
            url=url,
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def cancel_order(self, order_id):
        """Cancel a pending order"""
        response = requests.delete(
            url=f"{self.base_url}/rest/public/v2/equity/order/{order_id}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def check_order(self, equity_order: EquityOrder) -> [bool, str]:
        """Check if Order is valid."""
        is_valid_ticker = False, f"Instrument Code {equity_order.instrument_code} is not a valid Trading212 Ticker"
        for company in self.get_companies():
            if company['ticker'] == equity_order.instrument_code:
                is_valid_ticker = True, f"Instrument Code {equity_order.instrument_code} is valid Trading212 Ticker"

        return is_valid_ticker

    def min_max_sell_buy(self, instrument_code: str):
        params = {'instrumentCode': instrument_code}
        response = requests.get(
            f"{self.base_url}/rest/v1/equity/value-order/min-max",
            headers=self.headers,
            params=params
        )
        return json.loads(response.content.decode("utf-8"))


class CFD(Trading212):
    """ Trading 212 CFD """

    def __init__(self, email: str, password: str, driver: webdriver, mode: constants.Mode = constants.Mode.DEMO):
        super().__init__(email, password, driver, mode, constants.Trading.CFD)

    def execute_order(self, order: CFDOrder):
        """Execute CFD order"""

        # Check if it is Limit Stop Order
        if hasattr(order, 'is_limit_stop') and order.is_limit_stop == True:
            url = f"{self.base_url}/rest/v2/pending-orders/entry-dep-limit-stop/{order.instrument_code}"
        # Check if it is OCO Order
        elif hasattr(order, 'is_oco') and order.is_oco == True:
            url = f"{self.base_url}/rest/v2/pending-orders/entry-oco/{order.instrument_code}"
        # Market Order
        else:
            url = f"{self.base_url}/rest/v2/trading/open-positions"

        response = requests.post(
            url=url,
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def trading_additional_info(self, order: CFDOrder):
        """Get additional trading info before executing order."""
        params = {'instrumentCode': order.instrument_code,
                  'quantity': order.quantity,
                  'positionId': 'null'}
        response = requests.get(
            f"{self.base_url}/rest/v1/tradingAdditionalInfo",
            headers=self.headers,
            params=params
        )
        return json.loads(response.content.decode("utf-8"))

    def close_position(self, position_id):
        """Close an open position."""
        response = requests.delete(
            url=f"{self.base_url}/rest/v2/trading/open-positions/close/{position_id}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def get_current_price(self, instrument_code):
        """Workaround to get the current price of a CFD."""
        # Simulate an order with target price 0, T212 will respond with a business exception so we can get the
        # current price
        cfd_order = CFDOrder(instrument_code=instrument_code,
                             target_price=0.0,
                             quantity=0.1)
        # Return only the current price
        return float(self.execute_order(cfd_order)['context']['current'])

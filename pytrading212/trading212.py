"""API for Trading212 Platform"""

import json
import logging
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
from pytrading212.order import ValueOrder, CFDOrder, EquityOrder
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

        console.log(f"Starting PyTrading212 in [green]{mode.name}[/green] Mode")

        self.driver = driver
        self.driver.get(constants.LOGIN_URL)
        # Click Accept all cookies if it appears
        try:
            self.driver.find_element(By.CLASS_NAME, constants.COOKIES_NOTICE_BUTTON).click()
        except NoSuchElementException:
            pass  # ignore
        console.log(f"Authenticating")

        # Authenticate
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)

        # Click login button
        self.driver.find_element(By.CLASS_NAME, constants.LOGIN_BUTTON).click()

        # wait until the site is fully loaded
        condition = expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "company-logo")
        )

        # 120 seconds is a lot, but the site sometimes is very slow
        WebDriverWait(self.driver, 120).until(condition)

        self.user_agent = self.driver.execute_script("return navigator.userAgent;")

        # Redirect to correct mode, DEMO or LIVE
        if mode.name not in self.driver.current_url:
            self.driver.get(self.base_url)

        # Switch between CFD or Equity
        try:
            self.driver.find_element(By.CLASS_NAME, "equity")
            self.is_equity = True
        except NoSuchElementException:
            self.is_equity = False

        if trading == constants.Trading.EQUITY and not self.is_equity:
            self.switch()
        elif trading == constants.Trading.CFD and self.is_equity:
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

        # necessary headers for requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "Cookie": self.cookie,
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

    def finish(self):
        self.driver.close()

    def switch(self):
        """todo"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "Cookie": f"{self.driver.get_cookies()}",
        }
        requests.post(f"{self.base_url}/rest/v1/account/switch", headers=headers)

    def last_hour_hotlist(self):
        """todo"""
        response = requests.get(
            f"{self.base_url}/trading212.com/rest/positions-tracker/deltas/hourly/1"
        )
        return json.loads(response.content.decode("utf-8"))

    def get_funds(self):
        response = requests.get(
            f"{self.base_url}/rest/customer/accounts/funds", headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def get_orders(self, older_than: datetime, newer_than: datetime):
        """todo"""
        params = {
            'olderThan': strftime(older_than.isoformat()),
            'newerThan': strftime(newer_than.isoformat())
        }

        response = requests.get(
            f"{self.base_url}/rest/history/orders", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_transactions(self, older_than: datetime, newer_than: datetime):
        """todo"""
        params = {
            'olderThan': strftime(older_than.isoformat()),
            'newerThan': strftime(newer_than.isoformat())
        }
        response = requests.get(
            f"{self.base_url}/rest/history/transactions", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_order_details(self, details_path):
        """todo"""
        response = requests.get(f"{self.base_url}/rest/history{details_path}", headers=self.headers)
        return json.loads(response.content.decode("utf-8"))

    def get_dividends(self, older_than: datetime, newer_than: datetime):
        """todo"""
        params = {'olderThan': strftime(older_than.isoformat()),
                  'newerThan': strftime(newer_than.isoformat())
                  }

        response = requests.get(
            f"{self.base_url}/rest/history/dividends", headers=self.headers, params=urlencode(params)
        )
        return json.loads(response.content.decode("utf-8"))

    def get_fundamentals(self, isin):
        """todo"""
        params = {'isin': isin}
        response = requests.get(f"{self.base_url}/rest/companies/fundamentals", params=params)
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_performance(self, time_period: constants.Period):
        """todo"""
        response = requests.get(
            url=f"{self.base_url}/rest/v2/portfolio?period={time_period}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_composition(self):
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
        response = requests.get(
            url=f"{self.base_url}/rest/companies",
            headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def max_sell_quantity(self, instrument_code: str):
        response = requests.get(
            f"{self.base_url}/rest/v1/equity/value-order/min-max?instrumentCode={instrument_code}", headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def search(self, query):
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
    """todo"""

    def __init__(self, email: str, password: str, driver: webdriver, mode: constants.Mode = constants.Mode.DEMO):
        super().__init__(email, password, driver, mode, constants.Trading.EQUITY)

    def review_order(self, order: EquityOrder):
        """todo"""
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
        """todo"""
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
        """todo"""
        response = requests.delete(
            url=f"{self.base_url}/rest/public/v2/equity/order/{order_id}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))


class CFD(Trading212):
    """ Experimental CFD support"""

    def __init__(self, email: str, password: str, driver: webdriver, mode: constants.Mode = constants.Mode.DEMO):
        super().__init__(email, password, driver, mode, constants.Trading.CFD)

    def execute_order(self, order: CFDOrder):
        """https://demo.trading212.com/rest/v2/pending-orders/entry-dep-limit-stop/AAPL"""
        """Execute CFD market order, stop loss and take profit not yet supported"""
        response = requests.post(
            url=f"{self.base_url}/rest/v2/trading/open-positions",
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def close_position(self, position_id):
        """Close an open position, position_id is needed"""
        response = requests.delete(
            url=f"{self.base_url}/rest/v2/trading/open-positions/close/{position_id}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    """{instrumentCode: "AAPL", targetPrice: 159.85, limitDistance: null, stopDistance: null, quantity: 1.5,…}
instrumentCode
: 
"AAPL"
limitDistance
: 
null
notify
: 
"NONE"
quantity
: 
1.5
stopDistance
: 
null
targetPrice
: 
159.85"""
    # response = requests.post(https://demo.trading212.com/rest/v2/pending-orders/entry-dep-limit-stop/EURUSD)
    # {"notify": "NONE", "order1": {"price": 232, "quantity": -70}, "order2": {"price": 231.3, "quantity": -70}}
    # https://demo.trading212.com/rest/v2/pending-orders/entry-oco/VOW3
    # {"notify":"NONE","targetPrice":234.07,"takeProfit":null,"stopLoss":null,"quantity":1}
    # https://demo.trading212.com/rest/v2/pending-orders/entry-dep-limit-stop/VOW3
    # {"notify": "NONE", "targetPrice": 234.32, "quantity": 2, "instrumentCode": "VOW3"}
    # {"notify":"NONE","targetPrice":218.07,"limitDistance":6.85,"stopDistance":3.05,"quantity":1,"instrumentCode":"BIDU"}
    # def open_position(self):
    #    response = requests.post('https://demo.trading212.com/rest/v2/trading/open-positions', headers=headers)

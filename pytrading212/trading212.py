# API for Trading212 Platform

# Author: Francesco Ambrosini

import json
import logging
from enum import Enum

import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions, wait
from selenium.webdriver.support.ui import WebDriverWait

from pytrading212.order import ValueOrder
from pytrading212.position import Position


class Mode(Enum):
    DEMO = ("demo",)
    LIVE = ("live",)


class Trading(Enum):
    CFD = (0,)
    EQUITY = (1,)


class Period(Enum):
    LAST_DAY = (0,)
    LAST_WEEK = (1,)
    LAST_MONTH = (2,)
    LAST_THREE_MONTHS = (3,)
    LAST_YEAR = (4,)
    ALL = (5,)


class InstrumentCodeNotFound(Exception):
    pass


class Trading212:
    def __init__(
            self,
            username: str,
            password: str,
            driver: webdriver,
            mode: Mode = Mode.DEMO,
            trading: Trading = Trading.EQUITY,
    ):
        self.session = f"TRADING212_SESSION_{mode.name}"
        self.base_url = f"https://{mode.name.lower()}.trading212.com"

        self.driver = driver

        # authenticate
        
        self.driver.get("https://www.trading212.com/en/login")
        self.driver.find_element_by_name("email").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(password)
        time.sleep(1) #Let the Accept all cookies popup arrive
        self.driver.find_element_by_class_name("button_button__tDDzY.button_accent__dYsGU.cookies-notice_button__3K8cT.cookies-notice_button-accent__2rm8R").click() #Click Accept all cookies
        self.driver.find_element_by_class_name("submit-button_input__3s_QD").click() #Click login button

     
 


        # wait until the site is fully loaded
        condition = expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "company-logo")
        )

        # 120 seconds is a lot, but the site sometimes is very slow
        WebDriverWait(self.driver, 120).until(condition)

        self.user_agent = self.driver.execute_script("return navigator.userAgent;")

        # redirect to correct mode, DEMO or LIVE
        if self.base_url not in self.driver.current_url:
            self.driver.get(self.base_url)

        # switch between CFD or Equity
        try:
            self.driver.find_element_by_class_name("trading-type")
            self.is_equity = True
        except NoSuchElementException:
            self.is_equity = False

        if trading == Trading.EQUITY and not self.is_equity:
            self.switch()
        elif trading == Trading.CFD and self.is_equity:
            self.switch()

        # get session cookie
        cookies = self.driver.get_cookies()
        if cookies is not None:
            for cookie in cookies:
                # Get appropriate cookie for this session, live or demo
                if cookie['name'] == self.session:
                    self.cookie = method_decorator(f"{self.session}={cookie['value']};")
        else:
            raise Exception("Unable to get cookies, aborting.")

        # necessary headers for requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "Cookie": self.cookie,
        }

    def finish(self):
        self.driver.close()

    def switch(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
            "Cookie": f"{self.driver.get_cookies()}",
        }
        requests.post(f"{self.base_url}/rest/v3/account/switch", headers=headers)

    def last_hour_hotlist(self):
        response = requests.get(
            f"{self.base_url}/trading212.com/rest/positions-tracker/deltas/hourly/1"
        )
        return json.loads(response.content.decode("utf-8"))

    def get_funds(self):
        response = requests.get(
            f"{self.base_url}/rest/customer/accounts/funds", headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def get_orders(self):
        response = requests.get(
            f"{self.base_url}/rest/history/orders", headers=self.headers
        )
        return json.loads(response.content.decode("utf-8"))

    def get_fundamentals(self, isin):
        response = requests.get(
            f"{self.base_url}/rest/companies/fundamentals?isin={isin}"
        )
        return json.loads(response.content.decode("utf-8"))

    def execute_order(self, order):
        response = requests.post(
            url=f"{self.base_url}/rest/public/v2/equity/order",
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def execute_value_order(self, order: ValueOrder):
        response = requests.post(
            url=f"{self.base_url}/rest/v1/equity/value-order",
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    def cancel_order(self, order_id):
        response = requests.delete(
            url=f"{self.base_url}/rest/public/v2/equity/order/{order_id}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_performance(self, time_period=Period.LAST_DAY):
        response = requests.get(
            url=f"{self.base_url}/rest/v2/portfolio?period={time_period.name}",
            headers=self.headers,
        )
        return json.loads(response.content.decode("utf-8"))

    def get_portfolio_composition(self):
        # click portfolio section on right-sidepanel
        right_sidepanel_xpath = '//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/div'
        condition = expected_conditions.visibility_of_element_located(
            (By.XPATH, right_sidepanel_xpath)
        )
        WebDriverWait(self.driver, 60).until(condition)
        self.driver.find_element_by_xpath(right_sidepanel_xpath).click()

        positions = []
        try:
            # click on investments
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div'
            ).click()
            for item in self.driver.find_elements_by_class_name("investment-item"):
                ticker = item.get_attribute("data-qa-item")
                value = item.find_element_by_class_name("total-value").text
                quantity = item.find_element_by_class_name("quantity").text
                total_return = item.find_element_by_class_name("return").text
                position = Position(ticker, value, quantity, total_return)
                positions.append(position.__dict__)
        except Exception as e:
            logging.error(e)  # portfolio is empty
        return positions

    def get_companies(self):
        response = requests.get(
            url=f"{self.base_url}/rest/companies", headers=self.headers
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


# todo move here equity orders and logic
class Equity(Trading212):
    pass

# todo improve this experimental class
class CFD(Trading212):
    """ Experimental CFD support"""

    def __init__(
            self, username: str, password: str, driver: webdriver, mode: Mode = Mode.DEMO
    ):
        super().__init__(username, password, driver, mode, Trading.CFD)

    def execute_order(self, order):
        """Execute CFD market order, stop loss and take profit not yet supported"""
        response = requests.post(
            url=f"{self.base_url}/rest/v2/trading/open-positions",
            headers=self.headers,
            data=order.to_json(),
        )
        return json.loads(response.content.decode("utf-8"))

    # response = requests.post(https://demo.trading212.com/rest/v2/pending-orders/entry-dep-limit-stop/EURUSD)
    # {"notify": "NONE", "order1": {"price": 232, "quantity": -70}, "order2": {"price": 231.3, "quantity": -70}}
    # https://demo.trading212.com/rest/v2/pending-orders/entry-oco/VOW3
    # {"notify":"NONE","targetPrice":234.07,"takeProfit":null,"stopLoss":null,"quantity":1}
    # https://demo.trading212.com/rest/v2/pending-orders/entry-dep-limit-stop/VOW3
    # {"notify": "NONE", "targetPrice": 234.32, "quantity": 2, "instrumentCode": "VOW3"}
    # {"notify":"NONE","targetPrice":218.07,"limitDistance":6.85,"stopDistance":3.05,"quantity":1,"instrumentCode":"BIDU"}
    # def open_position(self):
    #    response = requests.post('https://demo.trading212.com/rest/v2/trading/open-positions', headers=headers)

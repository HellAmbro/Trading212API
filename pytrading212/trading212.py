# API for Trading212 Platform

# Author: Francesco Ambrosini

import json
from enum import Enum

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from pytrading212.order import ValueOrder
from pytrading212.position import Position


class Mode(Enum):
    DEMO = 0,
    LIVE = 1


class Period(Enum):
    LAST_DAY = 0,
    LAST_WEEK = 1,
    LAST_MONTH = 2,
    LAST_THREE_MONTHS = 3,
    LAST_YER = 4,
    ALL = 5,


class UnknownModeException(Exception):
    pass


class Trading212:

    def __init__(self, username, password, mode=Mode.DEMO, headless=True):
        if mode == Mode.DEMO:
            self._session = "TRADING212_SESSION_DEMO"
            self._base_url = 'https://demo.trading212.com'
        elif mode == Mode.REAL:
            self._session = "TRADING212_SESSION_LIVE"
            self._base_url = 'https://live.trading212.com'
        else:
            raise UnknownModeException(f"{mode} is not valid")

        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self._driver = webdriver.Chrome(chrome_options=options)

        self._driver.get('https://www.trading212.com/it/login')

        # authenticate
        self._driver.find_element_by_name("login[username]").send_keys(username)
        self._driver.find_element_by_name("login[password]").send_keys(password)
        self._driver.find_element_by_class_name("button-login").click()

        # wait until the site is fully loaded
        condition = expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'company-logo'))
        # 120 seconds is a lot, but the site sometimes is very slow
        WebDriverWait(self._driver, 120).until(condition)

        # todo support CFD
        # for now only invest is supported, so switch to investing to get cookies
        try:
            account_info = self._driver.find_element_by_class_name('account-menu-info')
            if "CFD" in account_info.text:
                self._switch_to_invest()
        except:
            pass

        # redirect to correct mode, DEMO or LIVE
        if self._base_url not in self._driver.current_url:
            self._driver.get(self._base_url)

        for cookie in self._driver.get_cookies():
            if cookie['name'] == self._session:
                self._cookie = f"{self._session}={cookie['value']};"

        # necessary headers for requests
        self._headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json',
                         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/87.0.4280.141 Safari/537.36 ',
                         'Cookie': self._cookie}

    def finish(self):
        self._driver.close()

    def _switch_to_invest(self):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'User-Agent': 'Chrome/86.0.4240.75 Safari/537.36',
                   'Cookie': f"{self._driver.get_cookies()}"}
        requests.post('https://demo.trading212.com/rest/v2/account/switch', headers=headers)

    def last_hour_hotlist(self):
        response = requests.get(f'{self._base_url}/trading212.com/rest/positions-tracker/deltas/hourly/1')
        return json.loads(response.content.decode('utf-8'))

    def get_funds(self):
        response = requests.get(f'{self._base_url}/rest/customer/accounts/funds', headers=self._headers)
        return json.loads(response.content.decode('utf-8'))

    def get_orders(self):
        response = requests.get(f"{self._base_url}/rest/history/orders", headers=self._headers)
        return json.loads(response.content.decode('utf-8'))

    def execute_order(self, order):
        response = requests.post(url=f"{self._base_url}/rest/public/v2/equity/order",
                                 headers=self._headers,
                                 data=order.to_json())
        return json.loads(response.content.decode('utf-8'))

    def execute_value_order(self, order: ValueOrder):
        response = requests.post(url=f"{self._base_url}/rest/v1/equity/value-order",
                                 headers=self._headers,
                                 data=order.to_json())
        return json.loads(response.content.decode('utf-8'))

    def cancel_order(self, order_id):
        response = requests.delete(url=f"{self._base_url}/rest/public/v2/equity/order/{order_id}",
                                   headers=self._headers)
        return json.loads(response.content.decode('utf-8'))

    def get_portfolio_performance(self, time_period=Period.LAST_DAY):
        response = requests.get(url=f"{self._base_url}/rest/v2/portfolio?period={time_period.name}",
                                headers=self._headers)
        return json.loads(response.content.decode('utf-8'))

    def get_portfolio_composition(self):
        # click portfolio section on right-sidepanel
        self._driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/div').click()
        # click on investments
        self._driver.find_element_by_xpath(
            '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div').click()
        positions = []
        elements = self._driver.find_elements_by_class_name('investment-item')
        for el in elements:
            logo_url = el.find_element_by_class_name('instrument-logo-image').get_attribute('src')
            ticker = el.get_attribute('data-qa-item')
            value = el.find_element_by_class_name('total-value').text
            quantity = el.find_element_by_class_name('quantity').text
            total_return = el.find_element_by_class_name('return').text
            position = Position(ticker, value, quantity, total_return)
            positions.append(position.__dict__)
        return positions

    def get_companies(self):
        response = requests.get(url=f"{self._base_url}/rest/companies")
        return json.loads(response.content.decode('utf-8'))

    # todo implement this function, replace variables naming
    def search(self, query):
        """
        What it should do: search for tickers in the companies.json file, you will get a list of tickers,
        for example AMZ -> AMZN, AMZN_US_EQ,..., and so on that will be passed in the post call"""
        list = ["AMZN_US_EQ", ]  # dummy ticker
        response = requests.post(f"{self._base_url}/charting/prices?withFakes=false", headers=self._headers,
                                 data=list.__str__().replace('\'',
                                                             '\"'))  # replace ' with " for Trading212 compatibility
        return json.loads(response.content.decode('utf-8'))

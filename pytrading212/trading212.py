# API for Trading212 Platform

# Author: Francesco Ambrosini

import json
import os
from enum import Enum

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Mode(Enum):
    DEMO = 0,
    LIVE = 1


class UnknownModeException(Exception):
    pass


_FILE_COOKIES = "cookies.json"
_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
_TRADING212_SESSION_LIVE = "TRADING212_SESSION_LIVE"
_TRADING212_SESSION_DEMO = "TRADING212_SESSION_DEMO"


class Trading212:

    def __init__(self, username, password, mode=Mode.DEMO, save_cookies=True):
        self._cookies = ""
        if mode == Mode.DEMO:
            self._session = _TRADING212_SESSION_DEMO
            self._base_url = 'https://demo.trading212.com'
        elif mode == Mode.REAL:
            self._session = _TRADING212_SESSION_LIVE
            self._base_url = 'https://live.trading212.com'
        else:
            raise UnknownModeException(f"{mode} is not valid")

        # necessary headers for requests
        self._headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json',
                         'User-Agent': _USER_AGENT}

        # check if cookies are saved and if they are still valid, in this case login isn't needed
        if save_cookies:
            self._cookies = self._get_cookies_from_file()

        if not self._are_cookies_valid():
            self._driver = webdriver.Chrome()
            self._driver.get('https://www.trading212.com/it/login')
            # authenticate
            self._driver.find_element_by_name("login[username]").send_keys(username)
            self._driver.find_element_by_name("login[password]").send_keys(password)
            self._driver.find_element_by_class_name("button-login").click()

            # wait until the site is fully loaded
            condition = expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'company-logo'))
            # 120seconds is a lot, but the site sometimes is very slow
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

            if save_cookies:
                self._save_cookies_to_file()
                self._cookies = self._get_cookies_from_file()
            self._driver.close()
        self._headers['Cookie'] = self._cookies

    def _save_cookies_to_file(self):
        file_cookies = open(_FILE_COOKIES, 'w+')
        cookies_to_save = {}
        for cookie in self._driver.get_cookies():
            if cookie['name'] == self._session:
                cookies_to_save[self._session] = cookie
                file_cookies.write(json.dumps(cookies_to_save))
                file_cookies.close()
                break

    # switch from CFD to Invest
    def _switch_to_invest(self):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'User-Agent': 'Chrome/86.0.4240.75 Safari/537.36',
                   'Cookie': f"{self._driver.get_cookies()}"}
        requests.post('https://demo.trading212.com/rest/v2/account/switch', headers=headers)

    def _get_cookies_from_file(self):
        if os.path.exists(_FILE_COOKIES):
            file_cookies = open(_FILE_COOKIES, "r")
            cookie = f"{self._session}={json.load(file_cookies)[self._session]['value']};"
            file_cookies.close()
            return cookie

    def _are_cookies_valid(self):
        """Check if cookies are still valid"""
        # file can be corrupted (empty or with wrong json format), catch exception and return false
        try:
            file_cookies = open(_FILE_COOKIES, 'r')
            saved_cookies = json.load(file_cookies)
            headers = self._headers
            if saved_cookies[self._session]['value']:
                headers['Cookie'] = f"{self._session}={saved_cookies[self._session]['value']};"
            file_cookies.close()
            return requests.get(f'{self._base_url}/rest/customer/accounts/funds', headers=headers).status_code == 200
        except:
            return False

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

    def cancel_order(self, order_id):
        response = requests.delete(url=f"{self._base_url}/rest/public/v2/equity/order/{order_id}",
                                   headers=self._headers)
        return json.loads(response.content.decode('utf-8'))

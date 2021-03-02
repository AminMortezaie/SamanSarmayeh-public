import time
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import plotly.graph_objects as go
import json
from akhzaDatabase import AkhzaDataBase


class Broker:
    def __init__(self, driver):
        self.driver = driver
        self.db = AkhzaDataBase()
        self.bought_stocks = []
        self.create_basics()

    def loadElement(self, xpath, mode="slow"):
        if mode == "slow":
            return WebDriverWait(self.driver, 3000).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "fast":
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "medium":
            return WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "super_fast":
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))

    def create_basics(self):
        self.driver.get("https://mehr.exirbroker.com/login")
        time.sleep(5)
        self.loadElement("/html/body/div[2]/header/a").click()
        self.loadElement(
            "/html/body/div[1]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div[1]/form/div[2]/input").send_keys("0311804421")
        self.loadElement(
            "/html/body/div[1]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div[1]/form/div[3]/input").send_keys("@Amin4416")
        try:
            time.sleep(3)
            self.loadElement(
                """//*[@id="mat-radio-7"]/label/div[1]/div[1]""").click()
        except:
            pass

    def buy_stock(self, index, stock_id, price, volume):
        # choose stock
        self.driver.switch_to.window(
            self.driver.window_handles[0])
        flag = True

        try:
            self.loadElement(
                """//*[@id="marketViewTable"]/tbody/tr["""+str(stock_id)+"""]/td[1]/div[5]/div/div[2]/mat-icon[1]/i""", mode='super_fast').click()
            self.loadElement(
                """//*[@id="orderPrice"]""", mode='super_fast').send_keys(price)
            self.loadElement(
                """//*[@id="mat-input-18"]""", mode='super_fast').send_keys(volume)
            self.loadElement(
                """//*[@id="buy_1"]/button[1]""", mode='super_fast').click()
            self.loadElement(
                """//*[@id="popupOrder1"]/div[1]/div[1]/button/span""", mode='super_fast').click()
            flag = False
        except:
            self.driver.refresh()

        self.loadElement(
            """//*[@id="mat-radio-7"]/label/div[1]/div[1]""").click()
        self.driver.switch_to.window(
            self.driver.window_handles[index])

    def sell_stock(self, index, stock_id, price, volume):
        self.driver.switch_to.window(
            self.driver.window_handles[0])
        self.loadElement(
            """//*[@id="marketViewTable"]/tbody/tr["""+str(stock_id)+"""]/td[1]/div[5]/div/div[2]/mat-icon[2]/i""").click()
        self.loadElement("""//*[@id="orderPrice"]""").send_keys(price)
        self.loadElement("""//*[@id="mat-input-18"]""").send_keys(volume)
        self.loadElement("""//*[@id="buy_1"]/button[1]""").click()
        self.loadElement(
            """//*[@id="popupOrder1"]/div[1]/div[1]/button/span""").click()
        self.bought_stocks.append([stock_id, price])
        self.driver.refresh()
        self.loadElement(
            """//*[@id="mat-radio-7"]/label/div[1]/div[1]""").click()

        self.driver.switch_to.window(
            self.driver.window_handles[index])

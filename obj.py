
import math
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import threading
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

logging.basicConfig(filename='output.log', level=logging.INFO)


class fetch_data:
    def __init__(self, filter_list, filter_name):
        self.flist = filter_list
        self.fname = filter_name
        self.data = []
        self.namad = []
        try:
            self.driver = webdriver.Chrome('chromedriver.exe')
        except:
            print('could not open driver.')
            logging.info('could not open driver.')
            self.driver = webdriver.Chrome('chromedriver.exe')

        self.url = 'http://www.tsetmc.com/Loader.aspx?ParTree=15131F#'
        self.driver.get(self.url)
        e = self.driver.find_element_by_xpath('//*[@id="id1"]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner1"]/div[1]/div[23]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner2"]/div[1]/div[6]')
        e.click()
        e = self.driver.find_element_by_xpath('//*[@id="id1"]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner3"]/div[1]/div[24]')
        e.click()
        # e=self.driver.find_element_by_xpath('//*[@id="id1"]')
        # e.click()
        # time.sleep(1)
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner4"]/div[1]/div[26]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner5"]/div[1]/div[27]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner6"]/div[1]/div[28]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner7"]/div[1]/div[29]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner8"]/div[1]/div[30]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner9"]/div[1]/div[32]')
        e.click()
        e = self.driver.find_element_by_xpath('//*[@id="id1"]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner10"]/div[1]/div[33]')
        e.click()
        # time.sleep(1)
        e = self.driver.find_element_by_xpath('//*[@id="id1"]')
        e.click()
        e = self.driver.find_element_by_xpath(
            '//*[@id="ModalWindowInner11"]/div[1]/div[34]')
        e.click()
        # time.sleep(1)
        e = self.driver.find_element_by_xpath('//*[@id="id1"]')
        e.click()

    def openUrl(self, url, number):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[number])
        self.driver.get(url)

    def close(self):
        self.driver.quit()
        del(self)

    def initiate_page(self):
        e = self.driver.find_element_by_xpath(
            '//*[@id="SettingsDesc"]/div[1]/a[7]')
        e.click()

        new_filter = self.driver.find_element_by_css_selector(
            '#FilterIndex > div.awesome.black')
        new_filter.click()

        selected_filter = self.driver.find_elements_by_xpath(
            '//*[@id="FilterIndex"]/div[1]')
        selected_filter[0].click()
        try:
            filter_area = self.driver.find_element_by_id('InputFilterCode')
            # print(self.flist)
            filter_area.send_keys(self.flist[0])
        except IndexError:
            raise Exception(IndexError)
        except:
            print('could not found text area')
            logging.info('could not found text area')
            filter_area = self.driver.find_element_by_id('InputFilterCode')
            filter_area.send_keys(self.flist[0])
        save = self.driver.find_element_by_css_selector(
            '#FilterContent > div.awesome.blue')
        save.click()
        for i in range(len(self.flist)-1):
            add_next_filter = self.driver.find_element_by_css_selector(
                '#FilterIndex > div.awesome.black')
            add_next_filter.click()
        for i in range(1, len(self.flist)):
            filter_btn = self.driver.find_element_by_css_selector(
                '#FilterIndex > div:nth-child(%i)' % (i+2))
            filter_btn.click()
            filter_area = self.driver.find_element_by_id('InputFilterCode')
            filter_area.send_keys(self.flist[i])
            save = self.driver.find_element_by_css_selector(
                '#FilterContent > div.awesome.blue')
            save.click()

    def check(self):
        data = []
        namad = []
        for i in range(len(self.flist)):
            filter_btn = self.driver.find_element_by_css_selector(
                '#FilterIndex > div:nth-child(%i)' % (i+2))
            filter_btn.click()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            a = soup.findAll('div', {'class': "{c}"})
            namad_list = []
            n = []
            for tag in a:
                d = {}
                d['namad'] = tag.find('a').text
                d['price'] = tag.find('div', {'class': "t0c t0c3 ch0"}).text
                n.append(d['namad'])
                namad_list.append(d)
            data.append(namad_list)
            namad.append(n)
        # intersection
        init = namad[0]
        for i in namad[1:]:
            s = list(set(init) & set(i))
            init = s
        # init is result
        # print(init)
        # print(data)
        return init, data

    def login(self):
        print("Im in Login Function.")
        self.openUrl('https://online.emofid.com/Login', 1)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div[3]/div/form/input[1]").send_keys("mfdonline2600406")
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[1]/div[3]/div/form/input[2]").send_keys("AliR2989")
        time.sleep(10)
        self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[1]/div[4]").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[10]/div[2]").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[1]/span[2]").click()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def loadElement(self, xpath):
        return WebDriverWait(self.driver, 300).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))

    def searchNamad(self, namad):
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(4)
        self.loadElement(
            "/html/body/app-container/app-content/div/div/div/div[3]/div[1]/ul[1]/li[2]/div/symbol-search/div/angucomplete/div/input").send_keys(namad)
        self.loadElement(
            "/html/body/app-container/app-content/div/div/div/div[3]/div[1]/ul[1]/li[2]/div/symbol-search/div/angucomplete/div/div[2]/div[3]/div").click()
        self.loadElement(
            "/html/body/app-container/app-content/div/div/div/div[3]/div[2]/div/div/widget/div/div/div/div[2]/send-order/div/div[1]/div[1]/div").click()

    def check_balance(self):
        return self.loadElement("/html/body/app-container/app-header/div/section[1]/customer-balance/div[1]/div[2]/span[2]/span[2]").text

    def orderBuy(self, price, total):
        balance = self.makeNumber(self.check_balance())
        print(balance)
        print("\n\n\n\n\n\n\n")
        time.sleep(10)
        if(len(price) > 3):
            price = int(price.split(",")[0]+price.split(",")[1])
        try:
            if(balance > total):
                tedad = math.floor(total/int(price))
            else:
                tedad = math.floor(balance/int(price))

            self.loadElement(
                "/html/body/app-container/app-content/div/div/div/div[3]/div[2]/div/div/widget/div/div/div/div[2]/send-order/div/div[5]/div[2]/div/div[2]/input").send_keys(price)
            time.sleep(2)
            self.loadElement(
                "/html/body/app-container/app-content/div/div/div/div[3]/div[2]/div/div/widget/div/div/div/div[2]/send-order/div/div[5]/div[1]/div/div[2]/input").send_keys(tedad)
            time.sleep(3)
            self.loadElement(
                "/html/body/app-container/app-content/div/div/div/div[3]/div[2]/div/div/widget/div/div/div/div[2]/send-order/div/div[7]/div[2]/a/div").click()
            time.sleep(3)
            self.loadElement(
                "/html/body/app-container/app-content/div/div/div/div[3]/div[1]/ul[1]/li[2]").click()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            self.driver.refresh()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def makeNumber(self, threeDigitNumber):
        array = threeDigitNumber.split(",")
        number = ''
        for ele in array:
            number += ele
        return int(number)


if __name__ == '__main__':
    a = fetch_data(['''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) == (pmin) && (pl) <=
(pmax)-((pmax)-(pmin))*0.05 && (pl) >= (pmax)-((pmax)-(pmin))*0.2)
        {
        return true;
    }
        else
        {
        return false;
    }
}()''', '''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) >=
((pmin)+((pmax)-(pmin))*0.05) && (pf) <= ((pmin)+((pmax)-(pmin))*0.2)
&& (pl) >= (pmax)-((pmax)-(pmin))*0.05)
        {
        return true;
    }
        else
        {
        return false;
    }
}()''', '''true==function()
{
        if( ((pmax)-(pmin))/(pl) >= 0.04 && (pf) == (pmin) && (pl) <=
(pmax)-((pmax)-(pmin))*0.05 && (pl) >= (pmax)-((pmax)-(pmin))*0.2)
        {
        return true;
    }
        else
        {
        return false;
    }
}()'''], [1, 2, 3])
    a.initiate_page()
    n, d = a.check()
    print(d)
    a.close()

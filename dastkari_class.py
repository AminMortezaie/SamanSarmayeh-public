
import time
import os
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import json


class FindDastkari:
    def __init__(self, namad):
        self.namad = namad
        self.data = []
        self.isRunning = True
        self.result = ""
        try:
            self.driver = webdriver.Chrome('chromedriver.exe')
        except:
            print('could not open driver.')
            self.driver = webdriver.Chrome('chromedriver.exe')

    def stopIsRunning(self):
        self.isRunning = False

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

    def startBot(self):
        self.driver.get("http://www.tsetmc.com/Loader.aspx?ParTree=15")
        self.loadElement("/html/body/div[3]/div[2]/a[5]").click()
        action = webdriver.ActionChains(self.driver)
        action.move_by_offset(10, 20).perform()
        self.loadElement(
            "/html/body/div[5]/section/div/input").send_keys(self.namad)
        self.loadElement(
            "/html/body/div[5]/section/div/div/div/div[2]/table/tbody/tr/td[1]/a").click()
        self.loadElement(
            "/html/body/div[4]/form/div[3]/div[1]/div[2]/div[2]").click()
        return "Bot Started Successfully."

    def number(self, number):
        try:
            return(int(number.split(".")[0]))
        except:
            return(number.split(".")[0])

    def makeNumber(self, threeDigitNumber):
        if type(threeDigitNumber) == int:
            return int(threeDigitNumber)
        array = threeDigitNumber.split(",")
        number = ''
        for ele in array:
            number += ele
        return int(number)

    def makeThreeDigitsThreeDigits(self, numberString):
        if(len(numberString) < 3):
            return numberString
        else:
            comaCount = int((len(numberString)-1)/3)
            count = 0
            iterator = -3
            while count < comaCount:
                value = iterator + count*-4
                numberString = numberString[:value] +\
                    ',' + numberString[value:]
                count += 1
        return numberString

    def makeTime(self, timeArrayObj, state=0):
        hi = 0
        mi = 0
        hour = int(timeArrayObj.split(":")[0])
        minute = int(timeArrayObj.split(":")[1])
        second = int(timeArrayObj.split(":")[2])

        if(int(timeArrayObj.split(":")[1]) > 60):
            minute = minute-60
            hi += 1
        if(int(timeArrayObj.split(":")[2]) > 60):
            second = second-60
            mi += 1
        if state == 0:
            return (datetime.time(hour+hi, minute+mi, second))
        if state == 1:
            if second < 30:
                return (datetime.time(hour+hi, minute+mi, second+30))
            else:
                if minute+mi+1 < 60:
                    return (datetime.time(hour+hi, minute+mi+1, second+30-60))
                else:
                    return (datetime.time(hour+hi+1, minute+mi+1-60, second+30-60))

    def checkTime(self, origTimeArrayObj, checkTimeArrayObj):
        origTime = self.makeTime(origTimeArrayObj)
        origInterval = self.makeTime(origTimeArrayObj, 1)
        checkTime = self.makeTime(checkTimeArrayObj)
        if (origTime < checkTime < origInterval):
            return True
        else:
            return False

    def arzeshConverter(self, arzesh):
        if type(arzesh) == int:
            return arzesh
        elif("B" in arzesh):
            return float(self.makeNumber(self.number(arzesh.split("B")[0])))*1000000000

    def calculator(self):
        haghighi_percent = 100
        arzesh = 1
        tedad_haghighi = 1
        try:
            haghighi_percent = self.loadElement(
                "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[3]/div[1]/table/tbody/tr[2]/td[3]/div[2]", mode="fast").text

            arzesh = self.loadElement(
                "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[2]/div", mode="fast").text
        except:
            try:
                haghighi_percent = self.loadElement(
                    "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[3]/div[2]", mode="fast").text

                arzesh = self.loadElement(
                    "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[3]/div[3]/table/tbody/tr[3]/td[2]/div", mode="fast").text
            except:
                pass

        print(float(haghighi_percent)/100*self.arzeshConverter(arzesh))
        try:
            tedad_haghighi = self.makeNumber(self.loadElement(
                "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[3]/div[1]/table/tbody/tr[6]/td[3]", mode="fast").text)

        except:
            try:
                tedad_haghighi = self.makeNumber(self.loadElement(
                    "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[4]/div[1]/table/tbody/tr[5]/td[3]", mode="fast").text)
            except:
                pass

        return tedad_haghighi, float(haghighi_percent)/100*self.arzeshConverter(arzesh)

    def getData(self):
        print("Im fetching...")
        try:
            self.loadElement(
                "/html/body/div[5]/section/div/div/div[2]/div/ul/li[4]/ul/li[2]/a").click()  # open
            self.loadElement(
                "/html/body/div[6]/section/div/div/div[2]/table/tbody/tr[2]/td[1]", mode='medium')
            self.loadElement(
                "/html/body/div[6]/section/div/div/div[1]/table/tbody/tr[2]/td[3]/div").click()
            self.data = self.loadElement(
                "/html/body/div[6]/section/div/div/div[2]/table").text.split("\n")
            self.loadElement("/html/body/div[6]/div[2]").click()  # close
        except:
            try:
                self.driver.refresh()
                self.loadElement(
                    "/html/body/div[4]/form/div[3]/div[1]/div[2]/div[2]").click()
                self.loadElement(
                    "/html/body/div[5]/section/div/div/div[2]/div/ul/li[4]/ul/li[2]/a").click()  # open
                self.loadElement(
                    "/html/body/div[6]/section/div/div/div[2]/table/tbody/tr[2]/td[1]", mode='medium')
                self.loadElement(
                    "/html/body/div[6]/section/div/div/div[1]/table/tbody/tr[2]/td[3]/div").click()
                self.data = self.loadElement(
                    "/html/body/div[6]/section/div/div/div[2]/table").text.split("\n")
                self.loadElement("/html/body/div[6]/div[2]").click()  # close
            except:
                self.driver.refresh()
                self.loadElement(
                    "/html/body/div[4]/form/div[3]/div[1]/div[2]/div[2]").click()
                self.loadElement(
                    "/html/body/div[5]/section/div/div/div[2]/div/ul/li[4]/ul/li[2]/a").click()  # open
                self.loadElement(
                    "/html/body/div[6]/section/div/div/div[2]/table/tbody/tr[2]/td[1]", mode='medium')
                self.loadElement(
                    "/html/body/div[6]/section/div/div/div[1]/table/tbody/tr[2]/td[3]/div").click()
                self.data = self.loadElement(
                    "/html/body/div[6]/section/div/div/div[2]/table").text.split("\n")
                self.loadElement("/html/body/div[6]/div[2]").click()  # close

    def processData(self):
        print("Im processing...")
        data1 = []
        for item in self.data:
            temp = item.split(" ")
            data1.append(temp)
        self.data = data1

    def makeSpy(self):
        time.sleep(3)
        print("Im analyzing...")
        spy = []
        for trade in self.data:
            if(self.number(trade[3])*int(trade[2]) < 10000000):
                if(int(trade[2]) < 2000):
                    print(trade)
                    spy.append(trade)
        return spy

    def analyzeData(self, spy):
        vol = ''
        tim = ''
        co = 0
        vol_mashkok = []
        vol_seen = []
        counter = 0
        # print(spy)
        for item in spy:
            vol = item[2]
            print("Chosen item is "+str(vol))
            for item1 in spy:
                if item1[2] in vol_seen:
                    # print("Vol "+str(item1[2])+" is in vol_seen")
                    pass

                if (item1[2] == vol and item1[2] not in vol_seen):
                    # print("Vol "+str(item1[2])+" is in my basket")
                    co += 1
                    # print("Co is added to "+str(co))

            if (co > 3):
                vol_mashkok.append(vol)
            co = 0
            vol_seen.append(vol)

        print(vol_mashkok)
        print("\n\n")
        lst = []

        for vol in vol_mashkok:
            for item in spy:
                if item[2] == vol:
                    lst.append(item)
        file1 = open("data.txt", 'w')
        for spy1 in lst:
            file1.write(str(spy1)+"\n")

        list_of_time = []
        list_vol = []

        # vol = vol_mashkok[1]
        for vol in vol_mashkok:
            for item in lst:
                if(item[2] == vol):
                    # print("hi it's vol "+str(vol))
                    vol1 = item[2]
                    tim = item[1]
                    index = item[0]
                    for i in range(len(lst)):
                        if lst[i][2] == vol:
                            if(self.checkTime(tim, lst[i][1])):
                                # print("hello to my world! it's vol "+str(lst[i][2]))
                                # print(checkTime(tim, lst[i][1]))
                                # print(tim)
                                if((index, tim, vol1) not in list_of_time):
                                    list_of_time.append((index, tim, vol1))
                                    list_vol.append(vol)
                                # print(lst[i][1])
                                if((lst[i][0], lst[i][1], lst[i][2]) not in list_of_time):
                                    list_of_time.append(
                                        (lst[i][0], lst[i][1], lst[i][2]))
                                    list_vol.append(vol)
        print(list_of_time)
        print('\n\n\n')
        delete_items = ['100', '200']
        for i in range(len(list_vol)):

            if(list_vol.count(list_vol[i]) < 4):
                if(list_vol[i] not in delete_items):
                    delete_items.append(list_vol[i])

        print(delete_items)

        for item in delete_items:
            list_vol = [s for s in list_vol if s != item]

        print("\n\nThis is final ")
        print(list_vol)
        tedad_dastkari = len(list_vol)

        return tedad_dastkari

    def run(self):
        self.startBot()
        tedad_haghighi, arzesh = self.calculator()
        self.getData()
        self.processData()
        spy_list = self.makeSpy()
        tedad_dastkari = self.analyzeData(spy_list)

        print("ارزش ذکر شده در سایت بورس:"+"\t" +
              str(arzesh/tedad_haghighi)+"\n" +
              "ارزش واقعی پس از حذف دستکاری در سهم :"+"\t" +
              str(arzesh/(tedad_haghighi-tedad_dastkari))
              )
        v1 = int(arzesh/tedad_haghighi/10)
        v2 = int(arzesh/(tedad_haghighi-tedad_dastkari)/10)

        try:
            tmp = str(int(((v1-v2)/v1)*100))+"%"
        except:
            tmp = "غیرقابل محاسبه"

        result = "سرانه فروش تابلو:"+"\n" + self.makeThreeDigitsThreeDigits(str(int(arzesh/tedad_haghighi/10)))+"\n" + "سرانه فروش واقعی :" + "\n" + self.makeThreeDigitsThreeDigits(
            str(int(arzesh/(tedad_haghighi-tedad_dastkari)/10))) + "\n" + "درصد تغییر: "+"\t"+tmp

        return result

    def runner(self):
        tedad_haghighi, arzesh = self.calculator()
        self.getData()
        self.processData()
        spy_list = self.makeSpy()
        tedad_dastkari = self.analyzeData(spy_list)

        print("ارزش ذکر شده در سایت بورس:"+"\t" +
              str(arzesh/tedad_haghighi)+"\n" +
              "ارزش واقعی پس از حذف دستکاری در سهم :"+"\t" +
              str(arzesh/(tedad_haghighi-tedad_dastkari))
              )

        v1 = int(arzesh/tedad_haghighi/10)
        v2 = int(arzesh/(tedad_haghighi-tedad_dastkari)/10)

        try:
            tmp = str(int(((v1-v2)/v1)*100))+"%"
        except:
            tmp = "غیرقابل محاسبه"

        result = "سرانه فروش تابلو:"+"\n" + self.makeThreeDigitsThreeDigits(str(int(arzesh/tedad_haghighi/10)))+"\n" + "سرانه فروش واقعی :" + "\n" + self.makeThreeDigitsThreeDigits(
            str(int(arzesh/(tedad_haghighi-tedad_dastkari)/10))) + "\n" + "درصد تغییر: "+"\t"+tmp

        return result

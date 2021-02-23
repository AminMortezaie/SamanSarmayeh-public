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
from broker_class import Broker


class OnlineData:
    def __init__(self):
        Path = 'chromedriver.exe'
        self.driver = webdriver.Chrome(Path)
        self.broker = Broker(self.driver)
        self.db = AkhzaDataBase()
        self.color = "black"
        self.tim = 0.0001
        self.dataNumber = 35
        self.VALUES = []
        self.nullStocks = []
        self.fullTradeHistory = []
        self.sortedFullHistory = []
        self.tradeHistory = []
        self.yArray_ = []
        self.counter = 0
        self.totalCounter = 0
        self.stockNumber = 0
        self.tc = 0
        self.value1 = 0
        self.volume1 = 0
        self.flag = self.dataNumber
        self.minusYtm = 0
        self.averageFlag = False
        self.dailyDate = date(datetime.datetime.now().year,
                              datetime.datetime.now().month, datetime.datetime.now().day)
        with open('stocks.json') as f:
            self.data = json.load(f)

    def findYtmAverage(self):
        sum = 0
        count = self.dataNumber
        for number in range(self.dataNumber):
            if(self.VALUES[number-1][2] == 0):
                count -= 1
            if(self.VALUES[number-1][2] != -0.0):
                sum += self.VALUES[number-1][2]
        return sum/count

    def convertToDate(self, str):
        dat = str.split("-")
        return datetime.date(int(dat[2]), int(dat[1]), int(dat[0]))

    def convertToValue(self, price):
        if len(price) > 3:
            li = []
            li = str(price).split(',')
            newPrice = str(li[0])+str(li[1])
            return int(newPrice)
        try:
            return int(price)
        except:
            return price

    def openUrl(self, url, number):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[number])
        self.driver.get(url)

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

    def loadElementAkhza(self, xpath):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        except:
            self.loadElement("/html/body/div[6]/div[2]").click()
            self.loadElement("/html/body/div[5]/div[2]").click()
            tradeCount = self.loadElement(
                "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]").text
            print("tradeCount:"+str(tradeCount))
            if (tradeCount == '0'):
                return ''

    def loadElementFast(self, xpath):
        return WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))

    # Print iterations progress

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    # 0 mode is value  1  mode is VolumeCounter 2 mode is TradeCounter 3 mode is Price

    def makeArrayPlot(self, historyArray, mode=0):
        xArray, yArray = [], []

        time9 = datetime.time(9, 0, 0)
        time920 = datetime.time(9, 20, 0)
        time930 = datetime.time(9, 30, 0)
        time940 = datetime.time(9, 40, 0)
        time10 = datetime.time(10, 0, 0)
        time1020 = datetime.time(10, 20, 0)
        time1030 = datetime.time(10, 30, 0)
        time1040 = datetime.time(10, 40, 0)
        time11 = datetime.time(11, 0, 0)
        time1120 = datetime.time(11, 20, 0)
        time1130 = datetime.time(11, 30, 0)
        time1140 = datetime.time(11, 40, 0)
        time12 = datetime.time(12, 0, 0)
        time1210 = datetime.time(12, 10, 0)
        time1215 = datetime.time(12, 15, 0)
        time1220 = datetime.time(12, 20, 0)
        time1225 = datetime.time(12, 25, 0)
        time1230 = datetime.time(12, 30, 0)

        counter1, counter2, counter3, counter4, counter5, counter6, counter7, counter8, counter9, counter10, counter11, counter12, counter13, counter14, counter15, counter16, counter17 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        counter1_, counter2_, counter3_, counter4_, counter5_, counter6_, counter7_, counter8_, counter9_, counter10_, counter11_, counter12_, counter13_, counter14_, counter15_, counter16_, counter17_ = 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000, 100000000
        for i in range(len(historyArray)):
            date = datetime.time(
                int(historyArray[i][0].split(":")[0]), int(historyArray[i][0].split(":")[1]), int(historyArray[i][0].split(":")[2]))

            if(time9 <= date <= time920):
                if (mode == 0):
                    counter1 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter1 += int(historyArray[i][2])

                elif (mode == 2):
                    counter1 += 1

                elif (mode == 3):
                    if(counter1 < (int(historyArray[i][1].split(".")[0]))):
                        counter1 = (int(historyArray[i][1].split(".")[0]))
                    if(counter1_ > (int(historyArray[i][1].split(".")[0]))):
                        counter1_ = (int(historyArray[i][1].split(".")[0]))

            elif(time920 <= date <= time930):
                if (mode == 0):
                    counter2 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter2 += int(historyArray[i][2])

                elif (mode == 2):
                    counter2 += 1

                elif (mode == 3):
                    if(counter2 < (int(historyArray[i][1].split(".")[0]))):
                        counter2 = (int(historyArray[i][1].split(".")[0]))
                    if(counter2_ > (int(historyArray[i][1].split(".")[0]))):
                        counter2_ = (int(historyArray[i][1].split(".")[0]))

            elif(time930 <= date <= time940):
                if (mode == 0):
                    counter3 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter3 += int(historyArray[i][2])

                elif (mode == 2):
                    counter3 += 1

                elif (mode == 3):
                    if(counter3 < (int(historyArray[i][1].split(".")[0]))):
                        counter3 = (int(historyArray[i][1].split(".")[0]))
                    if(counter3_ > (int(historyArray[i][1].split(".")[0]))):
                        counter3_ = (int(historyArray[i][1].split(".")[0]))

            elif(time940 <= date <= time10):
                if (mode == 0):
                    counter4 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter4 += int(historyArray[i][2])

                elif (mode == 2):
                    counter4 += 1

                elif (mode == 3):
                    if(counter4 < (int(historyArray[i][1].split(".")[0]))):
                        counter4 = (int(historyArray[i][1].split(".")[0]))
                    if(counter4_ > (int(historyArray[i][1].split(".")[0]))):
                        counter4_ = (int(historyArray[i][1].split(".")[0]))

            elif(time10 <= date <= time1020):
                if (mode == 0):
                    counter5 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter5 += int(historyArray[i][2])

                elif (mode == 2):
                    counter5 += 1

                elif (mode == 3):
                    if(counter5 < (int(historyArray[i][1].split(".")[0]))):
                        counter5 = (int(historyArray[i][1].split(".")[0]))
                    if(counter5_ > (int(historyArray[i][1].split(".")[0]))):
                        counter5_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1020 <= date <= time1030):
                if (mode == 0):
                    counter6 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter6 += int(historyArray[i][2])

                elif (mode == 2):
                    counter6 += 1

                elif (mode == 3):
                    if(counter6 < (int(historyArray[i][1].split(".")[0]))):
                        counter6 = (int(historyArray[i][1].split(".")[0]))
                    if(counter6_ > (int(historyArray[i][1].split(".")[0]))):
                        counter6_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1030 <= date <= time1040):
                if (mode == 0):
                    counter7 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter7 += int(historyArray[i][2])

                elif (mode == 2):
                    counter7 += 1

                elif (mode == 3):
                    if(counter7 < (int(historyArray[i][1].split(".")[0]))):
                        counter7 = (int(historyArray[i][1].split(".")[0]))
                    if(counter7_ > (int(historyArray[i][1].split(".")[0]))):
                        counter7_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1040 <= date <= time11):
                if (mode == 0):
                    counter8 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter8 += int(historyArray[i][2])

                elif (mode == 2):
                    counter8 += 1

                elif (mode == 3):
                    if(counter8 < (int(historyArray[i][1].split(".")[0]))):
                        counter8 = (int(historyArray[i][1].split(".")[0]))
                    if(counter8_ > (int(historyArray[i][1].split(".")[0]))):
                        counter8_ = (int(historyArray[i][1].split(".")[0]))

            elif(time11 <= date <= time1120):
                if (mode == 0):
                    counter9 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter9 += int(historyArray[i][2])

                elif (mode == 2):
                    counter9 += 1

                elif (mode == 3):
                    if(counter9 < (int(historyArray[i][1].split(".")[0]))):
                        counter9 = (int(historyArray[i][1].split(".")[0]))
                    if(counter9_ > (int(historyArray[i][1].split(".")[0]))):
                        counter9_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1120 <= date <= time1130):
                if (mode == 0):
                    counter10 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter10 += int(historyArray[i][2])

                elif (mode == 2):
                    counter10 += 1

                elif (mode == 3):
                    if(counter10 < (int(historyArray[i][1].split(".")[0]))):
                        counter10 = (int(historyArray[i][1].split(".")[0]))
                    if(counter10_ > (int(historyArray[i][1].split(".")[0]))):
                        counter10_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1130 <= date <= time1140):
                if (mode == 0):
                    counter11 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter11 += int(historyArray[i][2])

                elif (mode == 2):
                    counter11 += 1

                elif (mode == 3):
                    if(counter11 < (int(historyArray[i][1].split(".")[0]))):
                        counter11 = (int(historyArray[i][1].split(".")[0]))
                    if(counter11_ > (int(historyArray[i][1].split(".")[0]))):
                        counter11_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1140 <= date <= time12):
                if (mode == 0):
                    counter12 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter12 += int(historyArray[i][2])

                elif (mode == 2):
                    counter12 += 1

                elif (mode == 3):
                    if(counter12 < (int(historyArray[i][1].split(".")[0]))):
                        counter12 = (int(historyArray[i][1].split(".")[0]))
                    if(counter12_ > (int(historyArray[i][1].split(".")[0]))):
                        counter12_ = (int(historyArray[i][1].split(".")[0]))

            elif(time12 <= date <= time1210):
                if (mode == 0):
                    counter13 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter13 += int(historyArray[i][2])

                elif (mode == 2):
                    counter13 += 1

                elif (mode == 3):
                    if(counter13 < (int(historyArray[i][1].split(".")[0]))):
                        counter13 = (int(historyArray[i][1].split(".")[0]))
                    if(counter13_ > (int(historyArray[i][1].split(".")[0]))):
                        counter13_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1210 <= date <= time1215):
                if (mode == 0):
                    counter14 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter14 += int(historyArray[i][2])

                elif (mode == 2):
                    counter14 += 1

                elif (mode == 3):
                    if(counter14 < (int(historyArray[i][1].split(".")[0]))):
                        counter14 = (int(historyArray[i][1].split(".")[0]))
                    if(counter14_ > (int(historyArray[i][1].split(".")[0]))):
                        counter14_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1215 <= date <= time1220):
                if (mode == 0):
                    counter15 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter15 += int(historyArray[i][2])

                elif (mode == 2):
                    counter15 += 1

                elif (mode == 3):
                    if(counter15 < (int(historyArray[i][1].split(".")[0]))):
                        counter15 = (int(historyArray[i][1].split(".")[0]))
                    if(counter15_ > (int(historyArray[i][1].split(".")[0]))):
                        counter15_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1220 <= date <= time1225):
                if (mode == 0):
                    counter16 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter16 += int(historyArray[i][2])

                elif (mode == 2):
                    counter16 += 1

                elif (mode == 3):
                    if(counter16 < (int(historyArray[i][1].split(".")[0]))):
                        counter16 = (int(historyArray[i][1].split(".")[0]))
                    if(counter16_ > (int(historyArray[i][1].split(".")[0]))):
                        counter16_ = (int(historyArray[i][1].split(".")[0]))

            elif(time1225 <= date <= time1230):
                if (mode == 0):
                    counter17 += (int(historyArray[i][1].split(
                        ".")[0])*int(historyArray[i][2]))

                elif(mode == 1):
                    counter17 += int(historyArray[i][2])

                elif (mode == 2):
                    counter17 += 1

                elif (mode == 3):
                    if(counter17 < (int(historyArray[i][1].split(".")[0]))):
                        counter17 = (int(historyArray[i][1].split(".")[0]))
                    if(counter17_ > (int(historyArray[i][1].split(".")[0]))):
                        counter17_ = (int(historyArray[i][1].split(".")[0]))

            xArray = ["9:00-9:20", "9:20-9:30", "9:30-9:40",
                      "9:40-10:00", "10:00-1020", "10:20-1030",
                      "10:30-1040", "10:40-11:00", "11:00-11:20",
                      "11:20-11:30", "11:30-11:40", "11:40-12:00",
                      "12:00-12:10", "12:10-12:15", "12:15-12:20",
                      "12:20-12:25", "12:25-12:30"]

            yArray = [counter1, counter2, counter3,
                      counter4, counter5, counter6,
                      counter7, counter8, counter9,
                      counter10, counter11, counter12,
                      counter13, counter14, counter15,
                      counter16, counter17]

            yArray_ = [counter1_, counter2_, counter3_,
                       counter4_, counter5_, counter6_,
                       counter7_, counter8_, counter9_,
                       counter10_, counter11_, counter12_,
                       counter13_, counter14_, counter15_,
                       counter16_, counter17_]
            delete = []
            t = 0
            for i in range(len(yArray)):
                if(yArray[i] == 0):
                    delete.append(i)
            for i in range(len(delete)):
                del xArray[delete[i]-t]
                del yArray[delete[i]-t]
                del yArray_[delete[i]-t]
                t += 1

        return xArray, yArray

    def start(self):
        self.openUrl(self.data[0]["url"], 1)
        for i in range(1, self.dataNumber):
            self.openUrl(self.data[i]["url"], i+1)
        print(self.nullStocks)

    def run(self):
        # while True:
        # time.sleep(2)
        print("counter: "+str(self.counter))
        if self.counter < self.dataNumber-1:
            self.counter += 1
        else:
            self.counter = 0

        self.driver.switch_to.window(
            self.driver.window_handles[self.counter+1])

        value = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/form/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]')))

        if(not isinstance(value.text, str)):
            self.value1 = 0
        elif(value.text != '' and value.text != ' '):
            self.value1 = self.convertToValue(value.text)
        elif(value.text == ' '):
            self.value1 = 1000000

        volume = self.loadElement(
            '/html/body/div[4]/form/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[5]')

        if(not isinstance(volume.text, str)):
            self.volume1 = 0
        elif(volume.text != '' and volume.text != ' '):
            self.volume1 = self.convertToValue(volume.text)
        elif(volume.text == ' '):
            self.volume1 = 1000000

        if(self.flag > 0):
            self.VALUES.append([str(self.value1),
                                str(self.volume1), 0.1])
            self.flag -= 1
        else:
            self.VALUES[self.counter][0] = str(self.value1)
            self.VALUES[self.counter][1] = str(self.volume1)
            self.VALUES[self.counter][2] = self.db.find_ytm_with_date(
                str(self.dailyDate), self.db.fetch_payment_date_from_database(self.counter+1), self.value1)
        print(self.VALUES)
        if(self.counter == self.dataNumber-1):
            self.averageFlag = True
        if(self.averageFlag):
            # print("\n\n")
            # print("Ytm Average: " + str(self.findYtmAverage()))
            # print("-----------S I G N A L---------------")
            s = ''
            for iterator in range(len(self.VALUES)):
                try:
                    if(29 > self.VALUES[iterator][2] > 24):
                        self.broker.buy_stock(self.counter+1,
                                              iterator+1, self.VALUES[iterator][0], 3)
                        s += "StockNumber:" + str(self.db.make_query(
                            """select stock_name from stock where stock_id= """+str(iterator+1))[0][0])+'\n' +\
                            "Price:  "+str(self.VALUES[iterator][0])+"\n" +\
                            "StockYtm: " + str(self.VALUES[iterator][2])+"\n" +\
                            "-------------------------"+'\n'
                        print(s)
                except:
                    pass
            return s

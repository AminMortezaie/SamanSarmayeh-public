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
from jalali import *
from akhzaDatabase import AkhzaDataBase

fullTradeHistory = []
tradeHistory = []
stockNumber = 0
Path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")  # fatal
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(Path)
dataNumber = 29
flag = dataNumber
tc = 0
counter = 0
totalCounter = 0
db = AkhzaDataBase()

with open('stocks.json') as f:
    data = json.load(f)


def loadElement(xpath, mode="slow"):
    if mode == "slow":
        return WebDriverWait(driver, 3000).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    if mode == "fast":
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    if mode == "medium":
        return WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))


def loadElementFast(xpath):
    try:
        return WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    except:
        return False


def loadElementAkhza(xpath):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    except:
        loadElement("/html/body/div[6]/div[2]").click()
        loadElement("/html/body/div[5]/div[2]").click()
        tradeCount = loadElement(
            "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]").text
        print(stockNumber)
        print("tradeCount:"+str(tradeCount))
        return ''


def loadPreviousData(stockName, month, day):
    counter = 0
    global totalCounter
    global stockNumber
    total = 0
    tradeCount = loadElement(
        "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[1]/table/tbody/tr[4]/td[1]").text

    if(int(tradeCount != 0)):
        loadElement(
            "/html/body/div[4]/form/div[3]/div[1]/div[2]/div[2]").click()

        loadElement(
            "/html/body/div[5]/section/div/div/div[2]/div/ul/li[4]/ul/li[2]/a").click()
        ele = loadElementAkhza(
            "/html/body/div[6]/section/div/div/div[2]/table/tbody/tr[2]")
        if(ele == ''):
            data = ''
            print("Nothing Fetched!")
            persian_date = str(1399)+"-"+str(month)+"-"+str(day)
            name_of_file = stockName+'-data-' + \
                persian_date + "-" + \
                Persian(persian_date).gregorian_string()+'.txt'
            save_path = 'DetailsData\\' + str(stockName)
            completeName = os.path.join(save_path, name_of_file)
            file1 = open(completeName, 'w')
            file1.close()
        else:
            data = loadElement("/html/body/div[6]/section/div/div").text
            print(stockName+" data fetched!")
            persian_date = str(1399)+"-"+str(month)+"-"+str(day)
            name_of_file = stockName+'-data-' + \
                persian_date + "-" + \
                Persian(persian_date).gregorian_string()+'.txt'
            save_path = 'DetailsData\\' + str(stockName)
            completeName = os.path.join(save_path, name_of_file)
            file1 = open(completeName, 'w')
            file1.writelines(data[16:])
            file1.close()
            file1 = open(completeName, 'r')
            Lines = file1.readlines()
            for line in Lines:
                total += 1
            printProgressBar(0, total, prefix='Progress:',
                             suffix='Complete', length=50)
            for line in Lines:
                tim = line.split(" ")[1]
                price = line.split(" ")[3].split("\n")[0]
                volume = line.split(" ")[2]
                fullTradeHistory.append(
                    [tim, price, volume, stockName])
                counter += 1
                printProgressBar(counter, total, prefix='Progress:',
                                 suffix='Complete', length=50)
                totalCounter += 1
    tradeHistory.append([])
    for i in range(totalCounter-counter, totalCounter):
        tradeHistory[len(tradeHistory)-1].append(fullTradeHistory[i])


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
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


def openUrl(url, number):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[number])
    driver.get(url)


# def fetchUrlDate(number):
#     action = ActionChains(driver)
#     span = loadElement(
#         "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[3]/div[2]/div/div[5]/span")
#     if(span.text == 'مخفی'):
#         span.click()
#     loadElementFast(
#         "/html/body/div[4]/form/div[3]/div[2]/div[2]/div[6]/div[1]").click()
#     loadElementFast(
#         "/html/body/div[4]/form/div[3]/div[19]/div[1]/div[1]/table/tbody/tr[2]/td[12]")

#     date = loadElementFast(
#         "/html/body/div[4]/form/div[3]/div[19]/div[1]/div[2]/table/tbody/tr[2]/td[16]")
#     month = months[int(date.text.split("/")[1])-1]
#     day = int(date.text.split("/")[2])
#     action.double_click(date).perform()
#     driver.switch_to.window(driver.window_handles[number+1])
#     url = driver.current_url
#     return url, day, month


def fetchOldData():
    global db
    global data
    global totalCounter
    total = 0
    counter = 0
    stockNumber = 0
    data11 = data
    while stockNumber < 35:
        stockName = "stock"+str(stockNumber+1)
        driver.get(data11[int(stockNumber)]["url"])
        showTrades = loadElement(
            "/html/body/div[4]/form/div[3]/div[2]/div[1]/div[3]/div[2]/div/div[5]/span")
        if(showTrades.text == "مخفی"):
            showTrades.click()
        # sabeghe moamelat button
        loadElement(
            "/html/body/div[4]/form/div[3]/div[2]/div[2]/div[6]/div[1]").click()

        try:
            for j in range(1):
                loadElement(
                    "/html/body/div[4]/form/div[3]/div[19]/div[1]/div[1]/table/tbody/tr[2]/td[12]", mode='medium')
                for i in range(2, 3):
                    # days for click
                    day = loadElement(
                        "/html/body/div[4]/form/div[3]/div[19]/div[1]/div[2]/table/tbody/tr["+str(i)+"]/td[16]", mode='medium')
                    text = day.text
                    actionChains = ActionChains(driver)
                    monthShamsi, dayShamsi = day.text.split(
                        "/")[1], day.text.split("/")[2]
                    actionChains.double_click(day).perform()
                    # details for trades button in bottom of page
                    driver.switch_to.window(driver.window_handles[1])
                    # salMiladi = (driver.current_url.split("=")[3])[0:4]
                    loadElement(
                        "/html/body/div[4]/form/span/div/ul/li[2]/a").click()
                    loadElement(
                        "/html/body/div[4]/form/div[2]/div[3]/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div").click()
                    ele = loadElement(
                        "/html/body/div[4]/form/div[2]/div[3]/div/div/div/div[2]/table").text
                    if(ele == ''):
                        data = ''
                        print(str(text)+"Nothing Fetched!")
                        persian_date = str(1399)+"-" + \
                            str(monthShamsi)+"-"+str(dayShamsi)
                        name_of_file = stockName+'-data-' + \
                            persian_date + \
                            "-" + \
                            Persian(persian_date).gregorian_string()+'.txt'
                        save_path = 'DetailsData\\' + str(stockName)
                        completeName = os.path.join(
                            save_path, name_of_file)
                        file1 = open(completeName, 'w')
                        file1.close()
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    else:
                        data = loadElement(
                            "/html/body/div[4]/form/div[2]/div[3]/div/div/div/div[2]/table").text
                        print(str(text)+" data fetched!")
                        persian_date = str(1399)+"-" + \
                            str(monthShamsi)+"-"+str(dayShamsi)
                        name_of_file = stockName+'-data-' + \
                            persian_date + \
                            "-" + \
                            Persian(persian_date).gregorian_string()+'.txt'
                        save_path = 'DetailsData\\' + str(stockName)
                        completeName = os.path.join(
                            save_path, name_of_file)
                        file1 = open(completeName, 'w')
                        file1.writelines(data)
                        file1.close()
                        print(db.make_query(
                            '''select stock_name from stock where stock_id= '''+str(stockName.split('stock')[1]))[0][0])
                        db.add_record_from_tse(
                            stockName.split('stock')[1], persian_date, name_of_file)
                        file1 = open(completeName, 'r')
                        Lines = file1.readlines()
                        for line in Lines:
                            total += 1
                        printProgressBar(0, total, prefix='Progress:',
                                         suffix='Complete', length=50)
                        for line in Lines:
                            tim = line.split(" ")[1]
                            price = line.split(" ")[3].split("\n")[0]
                            volume = line.split(" ")[2]
                            fullTradeHistory.append(
                                [tim, price, volume, stockName])
                            counter += 1
                            printProgressBar(counter, total, prefix='Progress:',
                                             suffix='Complete', length=50)
                            totalCounter += 1
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                try:
                    loadElement(
                        "/html/body/div[4]/form/div[3]/div[19]/div[2]/div/a["+str(j+2)+"]", mode='medium').click()
                except:
                    print("this page is not valid.")
        except:
            print("hey there!")
        stockNumber += 1
        print("stockNUMBER: "+str(stockNumber))
        driver.get(data11[stockNumber]["url"])
    driver.quit()


def fetcherByHand(tableUrl):
    driver.get(tableUrl)
    loadElement("/html/body/div[4]/form/span/div/ul/li[2]/a").click()
    loadElement(
        "/html/body/div[4]/form/div[2]/div[3]/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div").click()
    print(loadElement(
        "/html/body/div[4]/form/div[2]/div[3]/div/div/div/div[2]").text)


fetchOldData()
driver.quit()

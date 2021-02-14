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

day = 27
month = "aban"
dayMiladi = day-10
monthMiladi = 11

Path = 'C:\\Program Files (x86)\\chromedriver.exe'
driver = webdriver.Chrome(Path)
color = "black"
tim = 0.0001
dataNumber = 3
VALUES = []
nullStocks = []
fullTradeHistory = []
sortedFullHistory = []
tradeHistory = []
yArray_ = []
counter = 0
totalCounter = 0
stockNumber = 0
tc = 0
value1 = 0
volume1 = 0
flag = dataNumber
minusYtm = 0
averageFlag = False
dailyDate = date(datetime.datetime.now().year,
                 datetime.datetime.now().month, datetime.datetime.now().day)


with open('stocks.json') as f:
    data = json.load(f)


def plotter(xArray, yArray, xLabel, yLabel, title):
    global color
    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=xArray, y=yArray, name='name',
                             line=dict(color=color, width=4)))
    fig.update_layout(title=title,
                      xaxis_title=xLabel,
                      yaxis_title=yLabel)
    fig.show()


def findYtmAverage():
    sum = 0
    count = dataNumber
    for number in range(dataNumber):
        if(VALUES[number-1][2] == 0):
            count -= 1
        if(VALUES[number-1][2] != -0.0):
            sum += VALUES[number-1][2]
    return sum/count


def convertToDate(str):
    dat = str.split("-")
    return datetime.date(int(dat[2]), int(dat[1]), int(dat[0]))


def xirr(cashflows):
    years = [(ta[0] - cashflows[0][0]).days / 365. for ta in cashflows]
    residual = 1.0
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i, trans in enumerate(cashflows):
            residual += trans[1] / pow(guess, years[i])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess - 1


def convertToValue(price):
    if len(price) > 3:
        li = []
        li = str(price).split(',')
        newPrice = str(li[0])+str(li[1])
        return int(newPrice)
    return int(price)


def openUrl(url, number):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[number])
    driver.get(url)


def findYtm(stockNumber):
    return round(xirr([(convertToDate(data[stockNumber-1]["payment_date"]), 1000000), (dailyDate, -int(VALUES[stockNumber-1][0]))])*100, 3)


def findYtmWithDate(stockNumber, date):
    return round(xirr([(convertToDate(data[stockNumber-1]["payment_date"]), 1000000), (date, -int(VALUES[stockNumber-1][0]))])*100, 3)


def loadElement(xpath):
    return WebDriverWait(driver, 300).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)))


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
        print("tradeCount:"+str(tradeCount))
        if (tradeCount == '0'):
            return ''


def loadElementFast(xpath):
    return WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)))

# Print iterations progress


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


# 0 mode is value  1  mode is VolumeCounter 2 mode is TradeCounter 3 mode is Price
def makeArrayPlot(historyArray, mode=0):
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


def makePlot(historyArray):
    pass


def fetchHistory(stockName):
    global sortedFullHistory
    counter = 0
    global totalCounter
    global stockNumber
    total = 0
    file1 = open(stockName+'_data_'+month+'_'+str(day)+"_2020_" +
                 str(monthMiladi)+"_"+str(dayMiladi) + '.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        total += 1
    if total == 0:
        nullStocks.append(stockName)
        return
    printProgressBar(0, total, prefix='Progress:',
                     suffix='Complete', length=50)
    for line in Lines:
        tim = line.split(" ")[1]
        price = line.split(" ")[3].split("\n")[0]
        volume = line.split(" ")[2]
        fullTradeHistory.append(
            [tim, price, volume, stockName])
        counter += 1
        printProgressBar(counter, total, prefix=stockName+':',
                         suffix='Complete', length=50)
        totalCounter += 1
    tradeHistory.append([])
    for i in range(totalCounter-counter, totalCounter):
        tradeHistory[len(tradeHistory)-1].append(fullTradeHistory[i])
    sortedFullHistory = sorted(
        fullTradeHistory, key=lambda ele: ele[0], reverse=False)


# for i in range(0, dataNumber):
#     fetchHistory("stock"+str(i+1))
driver.get(data[0]["url"])
for i in range(1, dataNumber):

    openUrl(data[i]["url"], i)


print(nullStocks)
# plotter(makeArrayPlot(sortedFullHistory)[0],
#         makeArrayPlot(sortedFullHistory)[1],
#         "Time",
#         "Price",
#         "Full History All Akhza "+str(day)+" "+month + " Time/Price")

# sorttt = sorted(
#     fullTradeHistory, key=lambda ele: ele[0], reverse=False)


while True:
    print("counter: "+str(counter))
    if counter < dataNumber-1:
        counter += 1
    else:
        counter = 0

    driver.switch_to.window(driver.window_handles[counter])

    value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/form/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]')))

    if(not isinstance(value.text, str)):
        value1 = 0
    elif(value.text != '' and value.text != ' '):
        value1 = convertToValue(value.text)
    elif(value.text == ' '):
        value1 = 1000000

    volume = loadElement(
        '/html/body/div[4]/form/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[5]')

    if(not isinstance(volume.text, str)):
        volume1 = 0
    elif(volume.text != '' and volume.text != ' '):
        volume1 = convertToValue(volume.text)
    elif(volume.text == ' '):
        volume1 = 1000000

    if(flag > 0):
        VALUES.append([str(value1),
                       str(volume1), 0.1])
        flag -= 1
    else:
        VALUES[counter][0] = str(value1)
        VALUES[counter][1] = str(volume1)
        VALUES[counter][2] = findYtm(counter+1)
    print(VALUES)
    if(counter == dataNumber-1):
        averageFlag = True
    if(averageFlag):
        print("Ytm Average: " + str(findYtmAverage()))
        print("-----------S I G N A L---------------")
        for iterator in range(len(VALUES)):
            if(VALUES[iterator][2] > findYtmAverage()):
                print("StockNumber:" + str(iterator+1))
                print("StockYtm: " + str(VALUES[iterator][2]))
                print("-------------------------")
        print("\n\n\n\n\n\n\n\n\n")

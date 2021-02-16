import os
import datetime
from datetime import date
# this function has some modes mode 1 is for find ytm for one paper in some range
import json
import os.path
from os import listdir
from os.path import isfile, join
from jalali import *

stocksName = ['910', '713', '716', '718',
              '720', '721', '722', '723',
              '804', '805', '806', '807',
              '808', '809', '810', '811',
              '812', '813', '814', '815',
              '816', '817', '818', '819',
              '820', '821', '902', '903',
              '904', '905', '906', '907',
              '908', '909']


YtmArray = []
sortedFullHistory = []
totalCounter = 0
stockNumber = 0
nullStocks = []
fullTradeHistory = []
tradeHistory = []
dataNumber = 29

with open('stocks.json') as f:
    data = json.load(f)

# make split with three digits


def makeThreeDigitsThreeDigits(numberString):
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


def convertToDate(str):
    dat = str.split("-")
    return datetime.date(int(dat[2]), int(dat[1]), int(dat[0]))


def findYtmWithDate(stockNumber, date, price):
    return round(xirr([(convertToDate(data[stockNumber-1]["payment_date"]), 1000000), (convertToDate(date), -int(price))])*100, 3)


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

# fetch data from details


def fetchHistory(stockName):
    global stocksName
    global YtmArray
    global sortedFullHistory
    counter = 0
    global totalCounter
    global stockNumber
    total = 0
    persian_date = str(1399)+"-"+str(month)+"-"+str(day)
    name_of_file = stockName+'-data-' + \
        persian_date + "-" + \
        Persian(persian_date).gregorian_string()+'.txt'
    save_path = 'DetailsData\\' + str(stockName)
    completeName = os.path.join(save_path, name_of_file)
    file1 = open(completeName, 'r')
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
        price = line.split(" ")[3].split("\n")[0].split(".")[0]
        volume = line.split(" ")[2]
        date1 = str(dayMiladi)+"-"+str(monthMiladi)+"-2020"
        # print(convertToDate(date1))
        stockNumber = int(stockName.split("stock")[1])
        ytm = findYtmWithDate(stockNumber, date1, price)

        temp1 = []
        temp1.append(str(day)+"/"+str(month)+"/"+str(1399))
        temp1.append(
            "Akhza"+str(stocksName[int(stockName.split("stock")[1])-1]) +
            "("+stockName+")")
        temp1.append(float(ytm))
        temp1.append(tim)
        temp1.append(int(int(price)*int(volume)/10))
        YtmArray.append(temp1)
        YtmArray = sorted(YtmArray, key=lambda ele: ele[2], reverse=True)

        fullTradeHistory.append(
            [tim, price, volume, ytm, stockName])
        counter += 1
        printProgressBar(counter, total, prefix=stockName+':',
                         suffix='Complete', length=50)
        totalCounter += 1
    tradeHistory.append([])
    for i in range(totalCounter-counter, totalCounter):
        tradeHistory[len(tradeHistory)-1].append(fullTradeHistory[i])
    sortedFullHistory = sorted(
        fullTradeHistory, key=lambda ele: ele[0], reverse=False)

# find Ytm


def findAverageYtmForOnePaper(number):
    maxi = 0
    mini = 100
    counter = 0
    total = 0
    for j in range(len(tradeHistory[number])):
        total += tradeHistory[number][j][3]
        if(tradeHistory[number][j][3] > maxi):
            maxi = tradeHistory[number][j][3]
            maxiTime = tradeHistory[number][j][0]
        if(tradeHistory[number][j][3] < mini):
            mini = tradeHistory[number][j][3]
            miniTime = tradeHistory[number][j][0]
        counter += 1
        stockName = tradeHistory[number][0][4]
        average = total/counter
    return stockName, mini, miniTime, maxi, maxiTime, average

# make stat data


def fullHistoryForDay():
    for number in range(len(tradeHistory)):
        stockName, mini, miniTime, maxi, maxiTime, average = findAverageYtmForOnePaper(
            number)
        persian_date = str(1399)+"-"+str(month)+"-"+str(day)
        name_of_file = stockName+'-stat-data-' + \
            persian_date + "-" + \
            Persian(persian_date).gregorian_string()+'.txt'
        save_path = 'StatData\\' + str(stockName)
        completeName = os.path.join(save_path, name_of_file)
        file1 = open(completeName, 'w')
        file1.writelines("StockName: "+stockName+"\n")
        file1.writelines("Date: "+str(day)+"/"+str(month)+"/"+"1399"+"\n")
        file1.writelines("Minimum YTM: "+str(mini)+"\n")
        file1.writelines("Minimum YTM Time: "+str(miniTime)+"\n")
        file1.writelines("Maximum YTM: "+str(maxi)+"\n")
        file1.writelines("Maximum YTM Time: "+str(maxiTime)+"\n")
        file1.writelines("Average YTM: "+str(average)+"\n")
        file1.close()

# make complete data


def makeDetailsForAll():
    maxi = 0
    mini = 100
    maxiStock = ''
    miniStock = ''
    miniTime = ''
    maxiTime = ''
    for stockNumber in range(dataNumber):
        stockName = "stock" + str(stockNumber+1)
        persian_date = str(1399)+"-"+str(month)+"-"+str(day)
        name_of_file = stockName+'-stat-data-' + \
            persian_date + "-" + \
            Persian(persian_date).gregorian_string()+'.txt'
        save_path = 'StatData\\' + str(stockName)
        completeName = os.path.join(save_path, name_of_file)
        try:
            temp = []
            file1 = open(completeName, 'r')
            lines = file1.readlines()

            # temp.append(str(day)+"/"+str(month)+"/"+str(1399))
            # temp.append("Akhza"+str(stocksName[int(lines[0].split(" ")[1].split("\n")[0].split(
            #     "stock")[1])-1])+"("+lines[0].split(" ")[1].split("\n")[0]+")")
            # temp.append(float(lines[4].split(" ")[2].split("\n")[0]))
            # temp.append(lines[5].split(" ")[3].split("\n")[0])
            # YtmArray.append(temp)
            # YtmArray = sorted(YtmArray, key=lambda ele: ele[2], reverse=True)

            if(maxi < float(lines[4].split(" ")[2].split("\n")[0])):
                maxiStock = lines[0].split(" ")[1].split("\n")[0]
                maxi = float(lines[4].split(" ")[2].split("\n")[0])
                maxiTime = lines[5].split(" ")[3].split("\n")[0]

            # temp = []
            # temp.append(str(day)+"/"+str(month)+"/"+str(1399))
            # temp.append("Akhza"+str(stocksName[int(lines[0].split(" ")[1].split("\n")[0].split(
            #     "stock")[1])-1])+"("+lines[0].split(" ")[1].split("\n")[0]+")")
            # temp.append(float(lines[2].split(" ")[2].split("\n")[0]))
            # temp.append(lines[3].split(" ")[3].split("\n")[0])
            # YtmArray.append(temp)
            # YtmArray = sorted(YtmArray, key=lambda ele: ele[2], reverse=True)

            if(mini > float(lines[2].split(" ")[2].split("\n")[0])):
                miniStock = lines[0].split(" ")[1].split("\n")[0]
                mini = float(lines[2].split(" ")[2].split("\n")[0])
                miniTime = lines[3].split(" ")[3].split("\n")[0]
        except:
            pass
    return miniStock, mini, miniTime, maxiStock, maxi, maxiTime

# write on file day information


def writeDailyData(miniStock, mini, miniTime, maxiStock, maxi, maxiTime):
    global nullStocks
    name_of_file = 'complete_data_'+str(month)+'_' + \
        str(day) + '_2020_'+str(monthMiladi)+"_"+str(dayMiladi)+'.txt'
    save_path = 'D:\\Sadra\\WebDriver\\Akhza\\StatData\\Days'
    completeName = os.path.join(save_path, name_of_file)
    file1 = open(completeName, 'w')
    file1.writelines("Date: "+str(day)+"/"+str(month)+"/"+"1399"+"\n")
    file1.writelines("Best BuyChance Stock: "+"Akhza" +
                     str(stocksName[int(maxiStock.split("stock")[1])-1])+"("+str(maxiStock)+")"+"\n")
    file1.writelines("Best BuyChance Ytm: "+str(maxi)+"\n")
    file1.writelines("Best Time To Buy: "+str(maxiTime)+"\n")
    file1.writelines("Best SellChance Stock: " + "Akhza" +
                     str(stocksName[int(miniStock.split("stock")[1])-1])+"("+str(miniStock)+")"+"\n")
    file1.writelines("Best SellChance Ytm: "+str(mini)+"\n")
    file1.writelines("Best Time To Sell: "+str(miniTime)+"\n")
    file1.writelines("No Trade Papers: ")
    for i in range(len(nullStocks)):
        file1.writelines(
            "Akhza" + str(stocksName[int(nullStocks[i].split("stock")[1])-1])+"("+str(nullStocks[i])+")"+" ")
    nullStocks = []

# make one file for all


def completeDataFromFirstTime():
    YtmRanking = []
    save_path = "D:\\Sadra\\WebDriver\\Akhza\\StatData\\days"
    onlyfiles = [f for f in listdir(save_path) if isfile(join(save_path, f))]
    counter = 1
    for name_of_file in onlyfiles:
        if(counter < 80):
            completeName = os.path.join(save_path, name_of_file)
            f = open(completeName, 'r')
            lineCount = 1
            tempMin = []
            tempMax = []
            for line in f.readlines():
                if(lineCount == 1):
                    tempMax.append(line.split(":")[1].split(
                        "\n")[0])
                    tempMin.append(line.split(":")[1].split("\n")[0])
                if(1 < lineCount < 4):
                    if(lineCount != 3):
                        tempMax.append(line.split(":")[1].split("\n")[0])
                    else:
                        tempMax.append(
                            float(line.split(":")[1].split("\n")[0].split(" ")[1]))
                if (lineCount == 4):
                    tempMax.append(line.split(":")[1].split("\n")[
                        0]+":"+line.split(":")[2].split("\n")[0]+":"+line.split(":")[3].split("\n")[0])
                if(4 < lineCount < 7):
                    if(lineCount != 6):
                        tempMin.append(line.split(":")[1].split("\n")[0])
                    else:
                        tempMin.append(
                            float(line.split(":")[1].split("\n")[0].split(" ")[1]))
                if(lineCount == 7):
                    tempMin.append(line.split(":")[1].split("\n")[
                        0]+":"+line.split(":")[2].split("\n")[0]+":"+line.split(":")[3].split("\n")[0])
                lineCount += 1
            YtmRanking.append(tempMax)
            YtmRanking.append(tempMin)
            YtmRanking = sorted(
                YtmRanking, key=lambda ele: ele[2], reverse=True)
        counter += 1
    save_path = "D:\\Sadra\\WebDriver\\Akhza\\StatData\\CompleteData"
    name_of_file = "completed_data_for_all_days.txt"
    completeName = os.path.join(save_path, name_of_file)
    f = open(completeName, 'w')
    f.write(
        "maximumYtmDate: "+YtmRanking[0][0]+"\n" +
        "maximumYtmPaper: "+YtmRanking[0][1]+"\n" +
        "maximumYtm: "+str(YtmRanking[0][2])+"\n" +
        "maximumYtmTime: "+YtmRanking[0][3]+"\n" +
        "minimumYtmDate: "+YtmRanking[-1][0]+"\n" +
        "minimumYtmPaper: "+YtmRanking[-1][1]+"\n" +
        "minimumYtm: "+str(YtmRanking[-1][2])+"\n" +
        "minimumYtmTime: "+YtmRanking[-1][3]+"\n"
    )
    f.close()
    name_of_file = "ranking_data_for_all_days.txt"
    completeName = os.path.join(save_path, name_of_file)
    f = open(completeName, "w")
    for rank in range(len(YtmRanking)):
        f.write(
            str(rank+1)+" "+str(YtmRanking[rank][0])+" " + str(YtmRanking[rank][1])+"  " +
            str(YtmRanking[rank][2])+" " +
            str(YtmRanking[rank][3])+"\n"
        )
    f.close()
    name_of_file = "completed_ranking_data_for_all_days.txt"
    completeName = os.path.join(save_path, name_of_file)
    f = open(completeName, "w")
    for rank in range(len(YtmArray)):
        f.write(
            str(rank+1)+" "+str(YtmArray[rank][0])+" " + str(YtmArray[rank][1])+" " +
            str(YtmArray[rank][2])+" " +
            str(YtmArray[rank][3]) + " " +
            makeThreeDigitsThreeDigits(str(YtmArray[rank][4]))+"\n"
        )
    f.close()
# runs fetching data for our arrays


def runFetch():
    for i in range(0, dataNumber):
        try:
            fetchHistory("stock"+str(i+1))
        except:
            print(dataNumber+1)
    showDetails()
    fullHistoryForDay()
    miniStock, mini, miniTime, maxiStock, maxi, maxiTime = makeDetailsForAll()
    writeDailyData(miniStock, mini, miniTime, maxiStock, maxi, maxiTime)
    completeDataFromFirstTime()

# show some details


def showDetails():
    print("\nDate: "+str(day)+" "+str(month))
    print("Null Stocks: ", end='')
    for array in nullStocks:
        print(str(array)+" ", end='')

# make all calculate


def datesRun():
    global month
    global day
    global dayMiladi
    global monthMiladi
    path = "D:\\Sadra\\WebDriver\\Akhza\\DetailsData\\stock12"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file1 in onlyfiles:
        month = file1.split("_")[2]
        day = file1.split("_")[3]
        monthMiladi = file1.split("_")[5]
        dayMiladi = file1.split("_")[6].split(".")[0]
        runFetch()
    completeDataFromFirstTime()


# runFetch()
datesRun()

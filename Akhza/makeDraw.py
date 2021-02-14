import datetime
from datetime import date
import plotly.graph_objects as go
from random import randint
import os
from os import listdir
from os.path import isfile, join
import json


color = 'black'
with open('stocks.json') as f:
    data = json.load(f)

dataNumber = 29
yArrayForAll = ["12/aban/1399\n", "17/aban/1399\n", "19/aban/1399\n",
                "20/aban/1399\n", "21/aban/1399\n", "24/aban/1399\n",
                "25/aban/1399\n", "26/aban/1399\n", "27/aban/1399\n",
                "28/aban/1399\n", "1/azar/1399\n", "2/azar/1399\n",
                "4/azar/1399\n"]
xArrayForAll = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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


arrayForAll = []

for i in range(29):
    value1 = []
    value2 = []
    for j in range(10):
        value2.append(j+1)
    for _ in range(10):
        value1.append(randint(_+4*_, 210+_*20))
    arrayForAll.append([value1, value2, 'name'+str(i+1), data[i]["color"]])


def plotForAll(arrayForAll):
    fig = go.Figure()
    for array in arrayForAll:
        # array[0] =xArray , array[1]= yArray, array[2]= name, array[3]= color
        fig.add_trace(go.Scatter(x=array[1], y=array[0], name=array[2],
                                 line=dict(color=array[3], width=7)))
        fig.update_layout(title="title",
                          xaxis_title=array[2],
                          yaxis_title="yLabel")
    fig.show()


def makeYtmArray():
    pass


def fetchYtmFromFile(stockNumber):
    xArray = xArrayForAll
    save_path = 'D:\\Sadra\\WebDriver\\Akhza\\StatData\\' + \
        "stock"+str(stockNumber)
    fileNames = [f for f in listdir(save_path) if isfile(join(save_path, f))]
    for fileNo in range(len(fileNames)):
        name_of_file = fileNames[fileNo]
        completeName = os.path.join(save_path, name_of_file)
        if(fileNo != 0):
            file1 = open(completeName, 'r')
            mainArray = file1.readlines()
            print(mainArray)
            print(name_of_file)
            print(mainArray[1].split("Date: ")[1])


fetchYtmFromFile(1)

# Analyze Complete Data
import os
import plotly.graph_objects as go

color = 'black'
stocksName = ["Akhza704(stock1)", "Akhza713(stock2)", "Akhza716(stock3)",
              "Akhza718(stock4)", "Akhza720(stock5)", "Akhza721(stock6)",
              "Akhza722(stock7)", "Akhza723(stock8)", "Akhza804(stock9)",
              "Akhza805(stock10)", "Akhza806(stock11)", "Akhza807(stock12)",
              "Akhza808(stock13)", "Akhza809(stock14)", "Akhza810(stock15)",
              "Akhza811(stock16)", "Akhza812(stock17)", "Akhza813(stock18)",
              "Akhza814(stock19)", "Akhza815(stock20)", "Akhza816(stock21)",
              "Akhza817(stock22)", "Akhza818(stock23)", "Akhza819(stock24)",
              "Akhza820(stock25)", "Akhza821(stock26)", "Akhza902(stock27)",
              "Akhza903(stock28)", "Akhza904(stock29)"]
splitted = []
yArray = []
xArrays = []
dataCount = 0
stocksCompare = []

# fill stocksCompare array


def fillStocksCompare():
    global stocksCompare
    temp = []
    for i in range(12):
        for j in range(29):
            temp.append(0)
        stocksCompare.append(temp)
        temp = []


def howIsGood():
    global yArray
    global splitted
    global dataCount
    save_path = "D:\\Sadra\\WebDriver\\Akhza\\StatData\\CompleteData"
    name_of_file = "completed_ranking_data_for_all_days.txt"
    completeName = os.path.join(save_path, name_of_file)
    completeData = open(completeName, 'r')
    for line in completeData:
        splitedTemp = line.split(" ")
        splitted.append(splitedTemp)
    dataCount = len(splitted)

    yArray.append(str(splitted[int(dataCount*0.0005)][3]))
    yArray.append(str(splitted[int(dataCount*0.005)][3]))
    yArray.append(str(splitted[int(dataCount*0.01)][3]))
    yArray.append(str(splitted[int(dataCount*0.05)][3]))
    yArray.append(str(splitted[int(dataCount*0.08)][3]))
    yArray.append(str(splitted[int(dataCount*0.10)][3]))
    yArray.append(str(splitted[int(dataCount*0.15)][3]))
    yArray.append(str(splitted[int(dataCount*0.25)][3]))
    yArray.append(str(splitted[int(dataCount*0.40)][3]))
    yArray.append(str(splitted[int(dataCount*0.50)][3]))
    yArray.append(str(splitted[int(dataCount*0.75)][3]))
    yArray.append(str(splitted[int(dataCount*1)-1][3]))

# convert to real number


def makeNumber(threeDigitNumber):
    array = threeDigitNumber.split(",")
    number = ''
    for ele in array:
        number += ele
    return int(number)


def compareStocks():
    global splitted
    global dataCount
    for splittedIter in range(len(splitted)):
        for stockName in range(len(stocksName)):
            if(splitted[splittedIter][2] == stocksName[stockName]):
                if(splittedIter < int(dataCount*0.0005)):
                    stocksCompare[0][stockName] += 1
                if(splittedIter < int(dataCount*0.005)):
                    stocksCompare[1][stockName] += 1
                if(splittedIter < int(dataCount*0.01)):
                    stocksCompare[2][stockName] += 1
                if(splittedIter < int(dataCount*0.05)):
                    stocksCompare[3][stockName] += 1
                if(splittedIter < int(dataCount*0.8)):
                    stocksCompare[4][stockName] += 1
                if(splittedIter < int(dataCount*0.10)):
                    stocksCompare[5][stockName] += 1
                if(splittedIter < int(dataCount*0.15)):
                    stocksCompare[6][stockName] += 1
                if(splittedIter < int(dataCount*0.25)):
                    stocksCompare[7][stockName] += 1
                if(splittedIter < int(dataCount*0.40)):
                    stocksCompare[8][stockName] += 1
                if(splittedIter < int(dataCount*0.50)):
                    stocksCompare[9][stockName] += 1
                if(splittedIter < int(dataCount*0.75)):
                    stocksCompare[10][stockName] += 1
                if(splittedIter < int(dataCount)):
                    stocksCompare[11][stockName] += 1


# find out xArrays
def makeArraysForDraw():
    global xArrays
    xArrays = []
    for i in range(29):
        xArrays.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for iterator in range(len(stocksCompare)):
        for stockNumber in range(29):
            xArrays[stockNumber][iterator] = stocksCompare[iterator][stockNumber]


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


fillStocksCompare()
howIsGood()
compareStocks()
makeArraysForDraw()

import datetime
from datetime import date
import plotly.graph_objects as go
from random import randint
import os
from os import listdir
from os.path import isfile, join
import json
from akhzaDatabase import AkhzaDataBase
import plotly.express as px


class Plotter:
    def __init__(self):
        self.db = AkhzaDataBase()
        self.color = "#CDB599"
    def plotter(self,xArray, yArray, xLabel, yLabel, title):
        fig = px.bar()
        # Create and style traces
        fig.add_trace(go.Scatter(x=xArray, y=yArray, name='name',
                                line=dict(color=self.color, width=4)))
        fig.update_layout(
            title=title,
                        xaxis_title=xLabel,
                        yaxis_title=yLabel,
                        

            )
        fig.show()




    def plotForAll(self,arrayForAll,title,xaxis_title,yaxis_title):
        fig = go.Figure()
        for array in arrayForAll:
            # array[0] =xArray , array[1]= yArray, array[2]= name, array[3]= color
            fig.add_trace(go.Scatter(x=array[0], y=array[1], name=array[2],
                                    line=dict(color=array[3], width=5)))
            fig.update_layout(title=title,xaxis_title=xaxis_title,yaxis_title=yaxis_title)
        fig.show()
        
    def plot_profit_percent(self):
        #x =0 (name), y=1(percent), name=2, color=3
        arrayForAll=[]
        all_array = self.db.make_array_profit_percent(mode="all")
        mode0_array = self.db.make_array_profit_percent(mode="0")
        mode1_array = self.db.make_array_profit_percent(mode="1")
        mode2_array = self.db.make_array_profit_percent(mode="2")
        mode3_array = self.db.make_array_profit_percent(mode="3")
        mode4_array = self.db.make_array_profit_percent(mode="4")
        total =[(all_array,"all_delta_dates"), (mode0_array,"delta_date 0"),
                (mode1_array,"delta_date 1"), (mode2_array,"delta_date 2"),
                (mode3_array,"delta_date 3"), (mode4_array,"delta_date 4")]
        colors =["#5F4B8B","#E69A8D","#42EADD","#CDB599","#FC766A","#00203F"]
        co = 0
        for array in total:
            arrayForAll.append([array[0][0],array[0][1],array[1],colors[co]])
            co+=1
        return arrayForAll
    
    def plot_ytm(self):
        arrayForAll=[]
        lst_buy0901=self.db.make_array_counted_values_ytm(mode="buy",date="1399-09-01")
        lst_sell0901=self.db.make_array_counted_values_ytm(mode="sell",date="1399-09-01")
        
        
        lst_buy1001=self.db.make_array_counted_values_ytm(mode="buy",date="1399-10-01")
        lst_sell1001=self.db.make_array_counted_values_ytm(mode="sell",date="1399-10-01")
        
        lst_buy1101=self.db.make_array_counted_values_ytm(mode="buy",date="1399-11-01")
        lst_sell1101=self.db.make_array_counted_values_ytm(mode="sell",date="1399-11-01")
        
        colors =["#5F4B8B","#E69A8D","#42EADD","#CDB599","#FC766A","#00203F"]
        total= [(lst_buy0901,"buy_ytm 1399-09-01"),(lst_sell0901,"sell_ytm 1399-09-01"),(lst_buy1001,"buy_ytm 1399-10-01"),(lst_sell1001,"sell_ytm 1399-10-01"),(lst_buy1101,"buy_ytm 1399-11-01"),(lst_sell1101,"sell_ytm 1399-11-01")]
        co = 0
        for array in total:
            arrayForAll.append([array[0][0],array[0][1],array[1],colors[co]])
            co+=1
        return arrayForAll
        
        
    def plot_stocks(self):
        stocksName = ['910', '713', '716', '718',
              '720', '721', '722', '723',
              '804', '805', '806', '807',
              '808', '809', '810', '811',
              '812', '813', '814', '815',
              '816', '817', '818', '819',
              '820', '821', '902', '903',
              '904', '905', '906', '907',
              '908', '909']
        lst_stocks = self.db.make_array_profit_percent(mode="0",kind="t2.stock_id",comp=1,i_multiple=1,count=35)
        self.plotter(stocksName,lst_stocks[1],"stock_number","percent","stock/percent")
    
    
            

            






obj = Plotter()
# obj.plotForAll(obj.plot_ytm(),"مقایسه  میزان ytm بر حسب تعداد","ytm " , "درصد فراوانی")
obj.plot_stocks()

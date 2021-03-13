import datetime
from datetime import date
import plotly.graph_objects as go
from random import randint
import os
from os import listdir
from os.path import isfile, join
import json
from akhzaDatabase import AkhzaDataBase


class Plotter:
    def __init__(self):
        self.db = AkhzaDataBase()

    def plotter(self,xArray, yArray, xLabel, yLabel, title):
        global color
        fig = go.Figure()
        # Create and style traces
        fig.add_trace(go.Scatter(x=xArray, y=yArray, name='name',
                                line=dict(color=color, width=4)))
        fig.update_layout(
            title=title,
                        xaxis_title=xLabel,
                        yaxis_title=yLabel,
                        
            font=dict(
            family="B Yekan",
            size=18)
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
    
    
    
            
            
            






# obj = Plotter()
# obj.plotForAll(obj.plot_profit_percent(),"مقایسه درصدی میزان درصد سود در طی مدت های مختلف نگهداری","درصد سود " , "درصد فراوانی")



from broker_class import Broker
from akhzaDatabase import AkhzaDataBase
import datetime
from datetime import date
from datetime import datetime
from jalali import *


class BrokerControll:
    def __init__(self, driver):
        self.buy_history = []
        self.sell_history = []
        self.VALUES = []
        self.counter = 0
        self.bought_stocks = []
        self.broker = Broker(driver)
        self.db = AkhzaDataBase()
        self.bought_stocks = self.db.bought_stocks()

    def today(self):
        today = Gregorian(date.today().strftime(
            '20'+"%y-%m-%d")).persian_string()
        month = today.split('-')[1]
        day = today.split('-')[2]
        if int(month) < 10:
            month = '0'+month
            if int(day) < 10:
                day = '0'+day
        elif int(day) < 10:
            day = '0'+day
            if int(month) < 10:
                month = '0'+month
        return today.split('-')[0]+"-"+month+"-"+day

    def current_time(self):
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return str(current_time)

    def set_values(self, values_list):
        print("Im in set values")
        self.VALUES = values_list
        self.analyze_values()

    def set_counter(self, counter):
        self.counter = counter

    def set_bought_stocks(self, bought_stock):
        self.bought_stocks.append(bought_stock)

    def analyze_values(self):
        self.bought_stocks = self.db.bought_stocks()
        print("Im in analyze_values")
        self.run_buy_strategy()
        self.run_sell_strategy()

    def run_buy_strategy(self):
        print("Im in run buy")
        print(self.VALUES)
        for iterator in range(len(self.VALUES)):
            try:
                if(29 > self.VALUES[iterator][0][2] > 21):
                    print("Im in for loop")
                    if [iterator+1, self.VALUES[iterator][0][0]] not in self.bought_stocks:
                        self.broker.buy_stock(self.counter+1,
                                              iterator+1, self.VALUES[iterator][0][0], 3)
                        self.db.bought_stocks = self.bought_stocks

                        self.db.add_record_to_trade_history(
                            iterator+1, self.VALUES[iterator][0][0], 3, str(self.today()), str(self.current_time()), self.VALUES[iterator][0][2])
                        self.buy_history.append(
                            [iterator+1, self.VALUES[iterator][0][0], 3])
            except:
                print('Im in exception')
                pass

    def run_sell_strategy(self):
        pass

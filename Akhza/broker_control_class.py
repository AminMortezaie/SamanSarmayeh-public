
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
        self.bought_stocks, self.buy_history = self.db.bought_stocks()[
            0], self.db.bought_stocks()[1]
        print("fetchedBoughtStocks: " +
              str(self.bought_stocks))
        print("fetchedBuyHistory: " +
              str(self.buy_history))

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
        print("Im in analyze_values")
        self.run_buy_strategy()
        self.run_sell_strategy()

    def find_in_buy_history(self, stock_id, mode='sell'):
        for trade in self.buy_history:
            print(trade[0], stock_id)
            if str(trade[0]) == str(stock_id):
                if mode == 'sell':
                    return trade
                elif mode == 'buy':
                    return True
        return False

    def buy_stock(self, index, stock_id, price, volume, ytm):
        if len(self.bought_stocks) < 4:
            if not self.find_in_buy_history(stock_id, mode='buy'):
                self.broker.buy_stock(index, stock_id, price, volume)
                self.bought_stocks.append([stock_id, price])
                self.db.add_buy_record_to_trade_history(
                    stock_id, price, volume, str(self.today()), str(self.current_time()), ytm)
                self.buy_history.append(
                    [stock_id, price, str(self.current_time()), volume])
                print(self.buy_history)
            else:
                print("trade for this stock_id is exist!")
        else:
            print("should be sell first.")

    def sell_stock(self, index, stock_id, buy_price, sell_price, volume, ytm):
        self.broker.sell_stock(index, stock_id, sell_price, volume)
        ind = self.bought_stocks.index([stock_id, buy_price])
        del self.bought_stocks[ind]
        self.db.add_sell_record_to_trade_history(
            stock_id, buy_price, sell_price, volume, str(self.today()), str(self.current_time()), ytm)
        del self.buy_history[ind]
        print(self.buy_history)

    def run_buy_strategy(self):
        print("Im in run buy")
        print(self.VALUES)
        for iterator in range(len(self.VALUES)):
            try:
                if(29 > self.VALUES[iterator][0][2] > 20):
                    if [iterator+1, self.VALUES[iterator][0][0]] not in self.bought_stocks:
                        self.buy_stock(self.counter+1,
                                       iterator+1, self.VALUES[iterator][0][0], 1, self.VALUES[iterator][0][2])
            except:
                print("Im in buy exception")
                pass

    def run_sell_strategy(self):
        print("hello sell position!")
        print(self.VALUES)
        for iterator in range(len(self.VALUES)):
            try:
                sell_price = self.VALUES[iterator][1][0]
                stock_id = iterator+1
                sell_ytm = self.VALUES[iterator][1][2]
                print("stock_id:")
                print(stock_id)
                print("im before fetch")
                trade = self.find_in_buy_history(stock_id)
                print("trade is fetched")
                print(trade)
                buy_price = trade[1]
                print("this is specify trade:")
                print(trade)
                if trade != False:
                    if int(sell_price) > int(buy_price)*1.004:
                        print("sell position accepted.")
                        self.sell_stock(self.counter+1,
                                        stock_id, buy_price, sell_price, trade[3], sell_ytm)
                    else:
                        print("pass this.")
            except:
                print("Im in sell exception")

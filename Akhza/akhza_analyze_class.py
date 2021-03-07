from akhzaDatabase import AkhzaDataBase


class Analyze:
    def __init__(self):
        self.db = AkhzaDataBase()

    def find_variety(self):
        ytm = 0
        names = []
        variety = []
        for i in range(40):
            if i == 0:
                temp = ytm+17
                variety.append(len(self.db.make_query(
                    '''select * from trades where ytm>= ''' + str(ytm)+'''and ytm<'''+str(temp))))
                names.append("("+str(ytm)+"," + str(temp)+")")
            else:
                print()
                ytm = 17+(i-1)*0.25
                temp = ytm+0.25
                variety.append(len(self.db.make_query(
                    '''select * from trades where ytm>= ''' + str(ytm)+'''and ytm<'''+str(temp))))
                names.append("("+str(ytm)+"," + str(temp)+")")
        return variety, names

    def matching_algorithm(self, date):
        if len(self.db.return_list_above_average(date)) != 0:
            for k in range(len(self.db.return_list_above_average(date))):
                spec_trade = self.db.return_list_above_average(date)[k]
                average_ytm = self.db.average_ytm_by_date(date)
                print("trade id: "+str(spec_trade[0])+"\tstock id: "+str(spec_trade[1])+"\tdate:"+str(date))
                stock_id = spec_trade[1]
                price = spec_trade[3]
                for ele in range(len(self.db.calculate_days_after(stock_id, date, 5))):
                    x = self.db.calculate_days_after(stock_id, date, 5)
                    for i in range(len(self.db.find_trades_by_stock_id_above_price(stock_id, x[ele], price))):
                        if ele == 0:
                            y = self.db.find_trades_by_stock_id_above_price(
                                stock_id, x[ele], price)
                            if spec_trade[2] < y[i][2]:
                                try:
                                    self.db.add_record_to_analyze_options(
                                        spec_trade, y[i], ele)
                                except:
                                    pass
                            else:
                                pass
                        else:
                            y = self.db.find_trades_by_stock_id_above_price(
                                stock_id, x[ele], price)
                            try:
                                self.db.add_record_to_analyze_options(
                                    spec_trade, y[i], ele)
                            except:
                                pass

        else:
            pass

    def run_matching_algorithm(self, enter_date, exit_date):
        date = enter_date
        while date != exit_date:
            date = self.db.date_generator(date)
            self.matching_algorithm(date)


obj = Analyze()
date = '1399-01-01'
obj.run_matching_algorithm('1399-01-01','1399-04-01')
obj.run_matching_algorithm('1399-01-04','1399-08-01')
obj.run_matching_algorithm('1399-08-01','1399-12-01')

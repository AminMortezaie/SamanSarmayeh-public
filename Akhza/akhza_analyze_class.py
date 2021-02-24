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

    def maching_algorithm(self, date):
        print(self.db.calculate_days_after(24, date, 5)
              )


obj = Analyze()
obj.maching_algorithm('1399-12-04')

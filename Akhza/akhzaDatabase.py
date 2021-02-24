import psycopg2
from psycopg2 import Error
import os
import datetime
from datetime import date


class AkhzaDataBase:
    def __init__(self):
        try:
            """ Connect to an existing database """
            self.connection = psycopg2.connect(user="postgres",
                                               password="Amin4416",
                                               host="localhost",
                                               port="5432",
                                               database="akhza_db")

            self.cursor = self.connection.cursor()
            print("PostgreSQL server information")
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def make_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def create_table(self, table_query):
        """ take name and table query."""
        create_table_query = table_query
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Table created successfully in PostgreSQL ")

    def add_record_from_file(self, stock_id, name_of_file):
        """ this method adds data from files to main database """
        save_path = 'DetailsData\\stock' + str(stock_id)
        completeName = os.path.join(save_path, name_of_file)
        file1 = open(completeName, 'r')
        stock_id = name_of_file.split("-")[0].split("stock")[1]
        for line in file1.readlines():
            tim = line.split(" ")[1]
            price = line.split(" ")[3]
            volume = line.split(" ")[2]
            date_miladi = name_of_file.split(
                "-")[5]+'-'+name_of_file.split("-")[6]+"-"+name_of_file.split("-")[7].split('.')[0]
            date_shamsi = name_of_file.split(
                "-")[2]+'-'+name_of_file.split("-")[3]+"-"+name_of_file.split("-")[4]
            payment_date = self.fetch_payment_date_from_database(
                stock_id)
            ytm = self.find_ytm_with_date(date_miladi, payment_date, price)

            insert_query = """ INSERT INTO TRADES VALUES (DEFAULT,""" + \
                str(stock_id)+','+'\''+str(tim)+'\''+','+'\''+str(price)+'\''+',' +\
                '\''+str(volume)+'\''+','+'\''+str(ytm)+'\''+','+'\''+str(date_shamsi) + \
                '\''+','+'\''+str(date_miladi)+'\''+")"
            self.cursor.execute(insert_query)
            self.connection.commit()
            print("Record inserted successfully")

    def fetch_payment_date_from_database(self, stock_id):
        """ find payment_date from database """
        select_query = """select payment_date from stock where stock_id= """ + \
            str(stock_id)
        self.cursor.execute(select_query)
        self.connection.commit()
        return self.cursor.fetchall()[0][0]

    def is_exist_date(self, stock_id, date):
        """ find out the date is exist in db or not."""
        select_query = """select date_shamsi from trades where stock_id="""+str(stock_id) + """and date_shamsi= """ + \
            "\'"+str(date)+"\'"
        self.cursor.execute(select_query)
        self.connection.commit()
        if len(self.cursor.fetchall()) == 0:
            return False
        return True

    def find_ytm_with_date(self, date, payment_date, price):
        return round(self.xirr([(self.convertToDate(str(payment_date)), 1000000), (self.convertToDate(date), -int(price))])*100, 3)

    def convertToDate(self, str):
        dat = str.split("-")
        return datetime.date(int(dat[0]), int(dat[1]), int(dat[2]))

    def xirr(self, cashflows):
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

    def add_record_from_tse(self, stock_id, date, name_of_file):
        if not self.is_exist_date(stock_id, date):
            self.add_record_from_file(stock_id, name_of_file)
        else:
            print('This date is exist.')

    def transfer_old_record(self):
        """ this method will be implemented later
            transfer data of share that has been expired to old tables(old_stock && old_trades).
            todo
        """
        pass

    def average_ytm_by_date(self, date):
        """ date must be like '1399-08-28' """
        return self.make_query(
            ''' select avg(ytm) from trades where date_shamsi = \''''+str(date)+"\'")[0][0]

    def list_of_data_above_average(self, ytm, date):
        """ shows list of data above average in a specified date
            take ytm of average and date parameters.
         """
        return self.make_query(
            '''select * from trades where date_shamsi= \'''' +
            str(date)+"\' and volume>100 and ytm>" +
            str(ytm)+'''order by ytm desc'''
        )

    def return_list_above_average(self, date):
        lst = []
        query_result = self.list_of_data_above_average(
            min(self.average_ytm_by_date(date), 21), date)
        co = 0
        for ele in query_result:
            co += 1
            lst.append(ele[0:6])
        return lst

    def calculate_days_after(self, stock_id, date, day_count=5):
        days_lst = [date]
        while len(days_lst) != day_count:
            date = self.date_generator(date)
            if int(self.make_query(
                    '''select count(*) from trades where stock_id = '''+str(stock_id) +
                    '''and date_shamsi =\''''+str(date)+'''\'   ''')[0][0]) != 0:
                days_lst.append(date)
        return days_lst

    def date_generator(self, date):
        ''' date = '1399-08-28'
            it generates one day after date
         '''
        arr = date.split("-")
        year = arr[0]
        month = arr[1]
        day = arr[2]

        if int(month) == 12 and (int(day) == 30 or int(day) == 31):
            year = str(int(year) + 1)
            day = '01'
            month = '01'

        elif int(day) == 31:
            temp = int(month)+1
            if temp < 10:
                month = '0'+str(temp)
                day = '01'
            else:
                month = str(temp)
                day = '01'
        else:
            temp = int(day)+1
            if temp < 10:
                day = '0'+str(temp)
            else:
                day = str(temp)

        return year+'-'+month+'-'+day

from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from samansarmaye.ShareHolder.ShareHolder_Database import ShareHolderDataBase
import persian
class GetData_General:
    def __init__(self,url):
        self.chrome_webDriver = "D:\Github\samansarmaye\chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_webDriver)
        self.url = url
        self.driver.get(self.url)

    def loadElement(self,xpath, mode="medium"):
        if mode == "slow":
            return WebDriverWait(self.driver, 3000).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "fast":
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "medium":
            return WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
        if mode == "superFast":
            return WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))

    def load_share_table(self,name):
        # self.Set_Url("http://www.tsetmc.com/Loader.aspx?ParTree=15")
        action = ActionChains(self.driver)
        # click on green search icon in tsetmc
        self.loadElement("/html/body/div[3]/div[2]/a[5]").click()
        action.move_by_offset(10, 50).perform()
        # type the name in input field
        search_text = self.loadElement("/html/body/div[5]/section/div/input")
        search_text.send_keys(name)
        # get the first result of search

        first_result = self.loadElement("/html/body/div[5]/section/div/div/div/div[2]/table/tbody/tr[1]/td[1]/a")
        print(first_result.text)
        if ("قدیمی" in first_result.text):
          first_result = self.loadElement("/html/body/div[5]/section/div/div/div/div[2]/table/tbody/tr[2]/td[1]/a")
        try:
            # go to the first result page
            first_result.click()
        except:
            print(" نماد " + str(name) + " یافت نشد! ")


    def get_stock_data(self,stocks):
        names = []
        if type(stocks) == str:
            names.append(stocks)
        elif type(stocks) == list:
            names = stocks
        stock_data = []
        for name in names:
            self.load_share_table(name)
            try:
                stock_num_share = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[4]/table/tbody/tr[1]/td[2]/div",mode="fast").get_attribute("title")
            except:
                stock_num_share = ""
            try:
                stock_url = self.driver.current_url
            except:
                stock_url = ""
            stock_data_url = None   # later ...
            try:
                stock_base_volume = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[4]/table/tbody/tr[2]/td[2]/div",mode="fast").get_attribute("title")
            except:
                stock_base_volume = ""
            try:
                stock_floating = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[4]/table/tbody/tr[3]/td[2]",mode="fast").text
                stock_floating = stock_floating[:len(stock_floating) - 1]
            except:
                stock_floating = ""
            temp = [stock_num_share,stock_url,stock_data_url,stock_base_volume,stock_floating]
            stock_data.append(temp)
        return stock_data

    def Load_Holders(self):

        holders = []
        holders_counter = 1
        while(True):

            holder_iterator = "/html/body/div[4]/form/div[3]/div[9]/span/div[2]/div[2]/table/tbody/tr[" + str(holders_counter) + "]"
            holders_counter += 1
            try:
                holders.append([self.loadElement(holder_iterator , mode="fast"),holder_iterator])
            except:
                break

        return holders
    def get_share_holder_data(self):
        # share_holders = Fetch_Share_Holder_Data()
        # return share_holders.Fetch_Data(name)
        try:
            # open holders page
            "/html/body/div[4]/form/div[2]/div/ul/li[10]/a"
            holder_page = self.loadElement("/html/body/div[4]/form/div[2]/div/ul/li[10]/a").click()
        except:
            print("صفحه ی سهامداران باز نشد !")
        result = []
        holders = self.Load_Holders()
        counter = 1
        for holder in holders:
            # print(holder)
            holder_percent = self.loadElement("/html/body/div[4]/form/div[3]/div[9]/span/div[2]/div[2]/table/tbody/tr[" + str(counter) + "]/td[3]").text
            counter += 1
            holder_data = []
            holder[0].click()
            name = self.loadElement(holder[1] + "/td[1]").text
            header = [name,holder_percent]
            table = self.loadElement("/html/body/div[5]/section/div/div[2]/div[2]/table/tbody").text
            rows = len(table.split("\n"))
            last_volume = None
            for i in range(rows,0,-1):
                table_row = "/html/body/div[5]/section/div/div[2]/div[2]/table/tbody/tr[" + str(i) + "]"
                table_row_date = self.loadElement(table_row + "/td[1]").text
                table_row_volume = self.loadElement(table_row + "/td[2]/div").get_attribute("title")
                if (table_row_volume != last_volume):
                    last_volume = table_row_volume
                    holder_data.append([table_row_date, table_row_volume])
            holder_data.insert(0,header)
            result.append(holder_data)
            self.loadElement("/html/body/div[5]/div[2]").click()
        # self.driver.quit()
        return result

    def get_holding_data(self):
        try:
            group_pe = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[1]/td[6]",mode="superFast").text
        except:
            group_pe = ""
        try:
            pe = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[1]/td[4]",mode="superFast").text
        except:
            pe = ""
        try:
            eps = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[1]/td[2]",mode="superFast").text
        except:
            eps = ""
        try:
            month_average_volume = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[4]/table/tbody/tr[4]/td[2]/div",mode="superFast").get_attribute("title")
        except:
            month_average_volume = ""
        try:
            year_high = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[4]/td[2]",mode="superFast").text
        except:
            year_high = ""
        try:
            year_low = self.loadElement("/html/body/div[4]/form/div[3]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[4]/td[3]",mode="superFast").text
        except:
            year_low = ""

        res = [self.string_to_numerical(group_pe),self.string_to_numerical(pe),self.string_to_numerical(eps,int),
                self.string_to_numerical(month_average_volume,int),self.string_to_numerical(year_high,int),
                self.string_to_numerical(year_low,int)]

        # print(res,group_pe,pe,eps,month_average_volume,year_high,year_low)
        return res

    def string_to_numerical(self,string,mode=float):
        nums = string.split(",")
        res = ""
        for i in nums:
            res += i
        if res == "":
            return 0

        if mode == int:
            return int(res)
        else:
            return float(res)
    def share_holder_db(self):
        db_connector = ShareHolderDataBase(
            dataBase_name="share_holder_db",
            host_name="127.0.0.1",
            username="postgres",
            password="Amin4416"
        )
        names = db_connector.select_all_from_table("stocks_name",["stock_name"])
        print(names)
        names = names[17:]
        # names = [["خبهمن"]]
        for tuple_name in names:
            # self.driver.get(self.url)
            name = tuple_name[0]
            # self.load_share_table(name)
            try:
                stock_data = self.get_stock_data(name)
                holding_data = self.get_holding_data()
                share_holders_data = self.get_share_holder_data()

            except:
                print(name)
                # file = open("Unsuccessful.txt","a")
                # file.write(name + "\n")
                # file.close()
                pass
            # insert stock data into db
            stock_data = stock_data[0]
            stock_data.insert(0,name)
            name = persian.convert_ar_characters(name)
            if (len(db_connector.check_existance("stock","stock_name",name)) == 0):
                db_connector.insert_into_table("stock",stock_data,mode="HD")

            holding_data.insert(0,"*")
            holding_data.insert(0,"*")
            holding_data.append("*")
            holding_data.append("*")
            holding_data.append("*")
            # insert share holder data into db
            for share_holder_data in share_holders_data:
                share_holder_name = share_holder_data[0][0]
                share_holder_name = persian.convert_ar_characters(share_holder_name)
                if ( len(db_connector.check_existance("share_holder","holder_name",share_holder_name)) == 0):
                    db_connector.insert_into_table("share_holder",[share_holder_name,None,"True"],mode="HD")
                # insert holding data into db
                share_holder_date_volume = share_holder_data[1:]
                total_volume = 0
                last_volume = 0
                for date,volume in share_holder_date_volume:
                    tmp = date.split("/")
                    dash_date = ""
                    for k in tmp:
                        dash_date = dash_date + k + "-"
                    dash_date = dash_date[:len(dash_date)-1]
                    # print(date,volume)
                    int_volume = self.string_to_numerical(volume,int)
                    buy_or_sell_volume = int_volume - last_volume
                    total_volume += int_volume
                    holding_data[-1] = buy_or_sell_volume
                    holding_data[-2] = dash_date
                    holding_data[-3] = total_volume

                    stock_id = db_connector.search("stock","stock_name","\'" + name + "\'","stock_id")
                    share_holder_id = db_connector.search("share_holder","holder_name","\'" + share_holder_name + "\'","holder_id")
                    holding_data[0] = stock_id[0][0]
                    holding_data[1] = share_holder_id[0][0]
                    # print(holding_data)
                    db_connector.insert_into_table("holding",holding_data)


        db_connector.connection.close()



obj = GetData_General("http://www.tsetmc.com/Loader.aspx?ParTree=15")
obj.share_holder_db()


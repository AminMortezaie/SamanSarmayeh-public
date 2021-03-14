from samansarmaye.ShareHolder.GetData import GetData_General
from selenium.webdriver import ActionChains
from samansarmaye.GeneralDataBase import GeneralDataBase
import time
import persian
class Get_Stock_name():
    def __init__(self):
        # super(Get_Stock_name,self).__init__()
        self.url = "http://www.tsetmc.com/Loader.aspx?ParTree=15131F#"
        self.WebConnector = GetData_General(self.url)

        self.WebConnector.loadElement("/html/body/div[6]/div[1]/a[3]").click()
        action = ActionChains(self.WebConnector.driver)
        action.move_by_offset(10, 50).perform()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[23]").click()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[24]").click()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[26]").click()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[27]").click()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[28]").click()
        self.WebConnector.loadElement("/html/body/div[7]/section/div/div[1]/div[30]").click()
        self.WebConnector.loadElement("/html/body/div[7]/div[2]").click()
        time.sleep(5)
    def GSN(self):
        db_connector = GeneralDataBase(dataBase_name="share_holder_db",host_name="localhost",username="postgres",password="2448")
        for i in range(2,750):
            try:
                stock_name = self.WebConnector.loadElement("/html/body/div[4]/form/div[2]/div[3]/div[" + str(i) + "]/div[1]/a",mode="superFast").text
                stock_name = persian.convert_ar_characters(stock_name)
                db_connector.insert_into_table("stocks_name",[stock_name],mode="HD")
                print(stock_name)
            except:
                print("kir")
        db_connector.connection.close()

# obj = Get_Stock_name()
# obj.GSN()

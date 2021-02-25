from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Fetch_Share_Holder_Data():
    def __init__(self):
        self.chrome_webDriver = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_webDriver)
        self.driver.get("http://www.tsetmc.com/Loader.aspx?ParTree=15")
    def loadElement(self,xpath, mode="slow"):
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
    def Fetch_Data(self,name):
        action = ActionChains(self.driver)
        # click on green search icon in tsetmc
        self.loadElement("/html/body/div[3]/div[2]/a[5]").click()
        action.move_by_offset(10, 50).perform()
        # type the name in input field
        search_text = self.loadElement("/html/body/div[5]/section/div/input")
        search_text.send_keys(name)
        # get the first result of search
        first_result = "/html/body/div[5]/section/div/div/div/div[2]/table/tbody/tr[1]/td[1]/a"
        result = []
        try:
            # go to the first result page
            self.loadElement(first_result,mode="medium").click()
        except:
            print(" نماد " + str(name) + " یافت نشد! ")

        try:
            # open holders page
            holder_page = self.loadElement("/html/body/div[4]/form/div[2]/div/ul/li[10]/a").click()
        except:
            print(" صفحه ی سهامداران برای نماد " + str(name) + " باز نشد ! ")


        holders = self.Load_Holders()
        for holder in holders:
            holder[0].click()
            name = self.loadElement(holder[1] + "/td[1]").text
            table = self.loadElement("/html/body/div[5]/section/div/div[2]/div[2]/table/tbody").text
            table = table.split("\n")
            # print(table)
            changes_of_holder = []
            sorted_table = []
            for i in table[::-1]:
                sorted_table.append(i)
            changes_of_holder.append(sorted_table[0])
            for i in sorted_table:
                tmp = i.split(" ")
                checker = tmp[1] + " " + tmp[2]
                last_item = changes_of_holder[len(changes_of_holder) - 1]
                if (checker not in last_item):
                    changes_of_holder.append(i)
            for i in range(0,len(changes_of_holder)):
                changes_of_holder[i] = name + " " + changes_of_holder[i]
            result.append(changes_of_holder)
            self.loadElement("/html/body/div[5]/div[2]").click()
        return result

obj = Fetch_Share_Holder_Data()
names = [ "خساپا", "خودرو"]
for i in names:
    res = obj.Fetch_Data(i)
    print(res)
obj.driver.quit()





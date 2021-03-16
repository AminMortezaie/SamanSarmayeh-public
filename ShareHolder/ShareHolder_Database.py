from samansarmaye.GeneralDataBase import GeneralDataBase


# from samansarmaye.ShareHolder.GetData import GetData_General

class ShareHolderDataBase(GeneralDataBase):
    def __init__(self, host_name, dataBase_name, username, password):
        super(ShareHolderDataBase, self).__init__(host_name, dataBase_name, username, password)

    def insert_into_stock(self, stock_name, stock_num_share, stock_url, stock_base_volume, stock_floating):
        Query_to_stock_Table = '''INSERT INTO STOCK(STOCK_NAME,STOCK_NUM_SHARE,STOCK_URL,STOCK_BASE_VOLUME,STOCK_FLOATING) VALUES  ''' \
                               "(\'" + str(stock_name) + "\',\'" + str(stock_num_share) + "\',\'" + str(
            stock_url) + "\',\'" + str(stock_base_volume) + "\',\'" + str(
            stock_floating[:len(stock_floating) - 1]) + "\')"
        self.make_query(Query_to_stock_Table)

import psycopg2

class GeneralDataBase:
    def __init__(self,host_name,dataBase_name,username,password):
        try:
            self.connection = psycopg2.connect(host = host_name , dbname = dataBase_name , user = username , password = password)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def make_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        try:
            return self.cursor.fetchall()
        except:
            pass

    def create_table(self, table_query):
        """ take name and table query."""
        self.cursor.execute(table_query)
        self.connection.commit()
        print("Table created successfully in PostgreSQL ")

    def select_all_from_table(self,tableName,columns="*"):
        Query = '''SELECT '''
        if (columns == "*"):
            Query += '''* FROM ''' + str(tableName) + ''';'''
        elif (type(columns) == list):
            temp = ""
            for column in columns:
                temp += column + ","
            temp = temp[:len(temp)-1]
            Query += temp + ''' FROM ''' + str(tableName) + ''';'''
        return self.make_query(Query)

    def insert_into_table(self,tableName,tableData,mode="SD"):
        for i in range(0,len(tableData)):
            tableData[i] = str(tableData[i])
        Query ='''INSERT INTO ''' + tableName + " VALUES ("
        temp = ""
        for data in tableData:
            if (data == "" or data == None):
                temp += "null ,"
            elif type(data) == str:
                temp += "\'" + data + "\',"
            else:
                temp += str(data) + ","
        if mode == "HD" :
            temp = "DEFAULT," + temp
        temp = temp[:len(temp) - 1]
        Query += temp + " )"
        # print(Query)
        return self.make_query(Query)

    def check_existance(self,tableName,columnName,value):
        Query = 'SELECT ' + columnName + ' FROM ' + tableName + ' WHERE ' + columnName + ' = \'' + value + '\';'
        # print(Query)
        return self.make_query(Query)
    def search(self,tableName,indexColumn,indexValue,targetColumn):
        Query = 'SELECT ' + targetColumn + " FROM " + tableName + " WHERE " + indexColumn + " = " + indexValue + ";"
        # print(Query)
        return self.make_query(Query)
# db_connector = GeneralDataBase(
#             dataBase_name="share_holder_db",
#             host_name="127.0.0.1",
#             username="postgres",
#             password="Amin4416"
#         )
# print(db_connector.search("stocks_name","stock_name","\'خفولا\'","stock_id")[0][0])
# db_connector.connection.close()
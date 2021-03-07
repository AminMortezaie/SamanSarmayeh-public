import psycopg2

class GeneralDataBase:
    def __init__(self,host_name,dataBase_name,username,password):
        try:
            self.connector = psycopg2.connect(host = host_name , dbname = dataBase_name , user = username , password = password)
            self.cursor = self.connector.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def make_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def create_table(self, table_query):
        """ take name and table query."""
        self.cursor.execute(table_query)
        self.connection.commit()
        print("Table created successfully in PostgreSQL ")






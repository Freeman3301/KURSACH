import psycopg2

class BaseData:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="kursach",
            user="postgres", 
            host="localhost", 
            password="SAO123_"
        )
        self.cursor = self.conn.cursor()
        print(self.getListTable())
    
    def getData(self, name_table):
        self.cursor.execute("SELECT * FROM %s" % name_table)
        return self.cursor.fetchall()
    
    def getListTable(self):
        self.cursor.execute("""
            SELECT table_name FROM information_schema. tables
            WHERE table_schema='public'
            """)
        return [self.getData(name) for name in self.cursor.fetchall()]

base = BaseData()
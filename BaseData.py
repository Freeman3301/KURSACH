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

    def deleteData(self, data):
        delete_query = "DELETE FROM admin WHERE adminid = %s"
        self.cursor.execute(delete_query, (data))
        self.conn.commit()
    
    def getListColumns(self, name_table):
        self.cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = %s """, name_table
        )
        return [row[0] for row in self.cursor.fetchall()]
    
    def dowonloadData(self, column_names, values):
        insert_query = "INSERT INTO admin (" + ", ".join(column_names) + ") VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_query, values)
        self.conn.commit()

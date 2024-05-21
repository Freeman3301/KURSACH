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
    
    def getData(self, name_table):
        self.cursor.execute("SELECT * FROM %s" % name_table)
        return self.cursor.fetchall()
    
    def getListNamesTables(self):
        self.cursor.execute("""
            SELECT table_name FROM information_schema. tables
            WHERE table_schema='public'
            """)
        return self.cursor.fetchall()
    
    def getListTable(self):
        self.cursor.execute("""
            SELECT table_name FROM information_schema. tables
            WHERE table_schema='public'
            """)
        return [self.getData(name) for name in self.getListNamesTables()]

    def deleteData(self, data):
        delete_query = "DELETE FROM admin WHERE adminid = %s"
        self.cursor.execute(delete_query, (data))
        self.conn.commit()
    
    def getListColumns(self, name_table):
        self.cursor.execute(
            """
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = %s 
            """, name_table
        )
        return [row[0] for row in self.cursor.fetchall()]
    
    def dowonloadData(self, name_table, column_names, values):
        name_table = ', '.join(map(str, name_table))
        columns = ", ".join(column_names)
        placeholders = ", ".join(["%s"] * len(column_names))
        insert_query = "INSERT INTO " + name_table + " (" + columns + ") VALUES (" + placeholders + ")"
        self.cursor.execute(insert_query, values)
        self.conn.commit()
    
    def CloseConnectionWithBase(self):
        self.cursor.close()
        self.conn.close()

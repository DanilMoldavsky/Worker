import sqlite3

class SQLite:
    def __init__(self, db_file, table:str="example"):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.ids_out = []
        
    def __del__(self):
        self.connection.close()

    def execute(self, query, args=None): #, args
        if args == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, args) #, args
        self.connection.commit()
        
    def create_table_takeaccs(self, table:str="example"):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ( ids TEXT )")

    def insert(self, table:str="example", ids:str="hello"):
        
        # ids = f'{ids}' if type(ids) == str else print("Промпт должен быть строкой")
        
        self.cursor.execute(f"INSERT INTO {table} VALUES (?)", (ids,))
        self.connection.commit()
        
    def take_all(self, table:str="example"):
        self.execute(f"SELECT * FROM {table}")
        
        self.ids_out = [ids[0] for ids in self.cursor.fetchall()]
        
import sqlite3

class SQLite:
    def __init__(self, db_file, table:str="example"):
        # for create connection with db
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        # for send data to db
        self.cursor = self.connection.cursor()
        self.ids_out = []
        
        self.rows_text = []
        self.tables = []
        self.name_tables = []
        self.table = table
        self.show_post = None
        self.messages = []
        
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

    def take_alltables(self):
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        self.tables = self.cursor.fetchall()
        for el in self.tables:
            self.name_tables.append(el[1])
        print(f'Такие таблицы, находятся в бд: {self.name_tables}')
    
    def insert(self, table:str="example", ids:str="hello"):
        
        # ids = f'{ids}' if type(ids) == str else print("Промпт должен быть строкой")
        
        self.cursor.execute(f"INSERT INTO {table} VALUES (?)", (ids,))
        self.connection.commit()
        
    def replace_id(self, table:str="example", id:int=1, post:str="empty"):
        post = f'{post}' if type(post) == str else post
        id = f'{id}' if type(id) == str else id
        # self.cursor.execute(f"REPLACE INTO {table} (name, age) VALUES ('Tom', 22)")
        
        self.cursor.execute(f"REPLACE INTO {table} (id, post) VALUES (?, ?)", (id, post))
        self.connection.commit()

    def take_all(self, table:str="example"):
        self.execute(f"SELECT * FROM {table}")
        
        self.ids_out = [ids[0] for ids in self.cursor.fetchall()]
    
    def show_all(self):
        for row in self.rows:
            print(row)
        
    def delete(self, table:str="example", category="id", id:int=1):
        id = f'{id}' if type(id) == str else id
        self.execute(f"DELETE FROM {table} WHERE {category} = ?", (id,))
        self.connection.commit()
        
    def delete_all(self, table:str="example"):
        self.execute(f"DELETE FROM {table}")
        self.connection.commit()
        
        self.take_all(table)
        print(f'Бд очищена, стол {table} включает {len(self.ids_out)} постов') 
        
    def update(self, table:str="example", post:str="hello", category="id", id:int=1):
        post = f'{post}' if type(post) == str else print("Пост должна быть строкой")
        id = f'{id}' if type(id) == str else id
        
        print(f"UPDATE {table} SET post = {post} WHERE {category} = {id}")
        self.execute(f"UPDATE {table} SET post = ? WHERE {category} = ?", (post, id))
        self.connection.commit()
        
    def set_table(self, table:str="example"):
        self.table = table
        print(f'Текущая таблица: {self.table}')
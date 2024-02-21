import sqlite3

class SQLite:
    def __init__(self, db_file, table:str="example"):
        # for create connection with db
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        # for send data to db
        self.cursor = self.connection.cursor()
        self.rows = []
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
        
    def create_table_if_not(self, table:str="example", memory:bool=False):
        if memory == True:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ( post TEXT, role TEXT )")
        # else:
        #     self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (prompt TEXT)")

        
    # def create_table(self, table:str="example"):
        # self.cursor.execute(f"CREATE TABLE {table} (id INTEGER, post TEXT)")
        
    def take_alltables(self):
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        self.tables = self.cursor.fetchall()
        for el in self.tables:
            self.name_tables.append(el[1])
        print(f'Такие таблицы, находятся в бд: {self.name_tables}')
    
    def insert(self, table:str="example", prompt:str="hello", role:str='test'):
        
        prompt = f'{prompt}' if type(prompt) == str else print("Промпт должен быть строкой")
        
        self.cursor.execute(f"INSERT INTO {table} VALUES (?, ?)", (prompt, role,))
        self.connection.commit()
        
    def replace_id(self, table:str="example", id:int=1, post:str="empty"):
        post = f'{post}' if type(post) == str else post
        id = f'{id}' if type(id) == str else id
        # self.cursor.execute(f"REPLACE INTO {table} (name, age) VALUES ('Tom', 22)")
        
        self.cursor.execute(f"REPLACE INTO {table} (id, post) VALUES (?, ?)", (id, post))
        self.connection.commit()
    
    # select all rows into .rows
    def take_valid(self, table:str="example"):
        self.execute(f"SELECT * FROM {table}")
        
        self.rows = self.cursor.fetchall()
        
    def take_all(self, table:str="example"):
        self.execute(f"SELECT * FROM {table}")
        
        self.rows = self.cursor.fetchall()
    
    def show_all(self):
        for row in self.rows:
            print(row)
        
    def delete(self, table:str="example", category="id", id:int=1):
        id = f'{id}' if type(id) == str else id
        self.execute(f"DELETE FROM {table} WHERE {category} = ?", (id,))
        self.connection.commit()
        
    def delete_all(self, table:str="example"):
        self.execute(f"DELETE FROM {table}")
        # id = f'{id}' if type(id) == str else id
        # self.take_all(table)
        # for id, post in self.rows:
        #     self.execute(f"DELETE FROM {table} WHERE {category} = ?", (id,))  # WHERE company='Apple' AND price < 60000;
        self.connection.commit()
        
        self.take_all(table)
        print(f'Бд очищена, стол {table} включает {len(self.rows)} постов') 
        
    def update(self, table:str="example", post:str="hello", category="id", id:int=1):
        post = f'{post}' if type(post) == str else print("Пост должна быть строкой")
        id = f'{id}' if type(id) == str else id
        
        print(f"UPDATE {table} SET post = {post} WHERE {category} = {id}")
        self.execute(f"UPDATE {table} SET post = ? WHERE {category} = ?", (post, id))
        self.connection.commit()
        
    def set_table(self, table:str="example"):
        self.table = table
        print(f'Текущая таблица: {self.table}')
        
    def take_context(self):
        for el in self.rows[:3]:
            mess = {"role" :el[1], "content": el[0]}
            
            print(mess)
            self.messages.append(mess)

        return self.messages
# db = SQLite("db\\test.db")

# db.update("posts", "planeta", "id", 8)

# db.take_all("posts")
# db.show_all()
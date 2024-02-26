import sqlite3

class SQLite:
    def __init__(self, db_file):
        """
        Initialize the class with a database file.

        Parameters:
            db_file (str): The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.ids_out = []
        
    def __del__(self):
        """
        Method to close the connection associated with the object.
        """
        self.connection.close()

    def execute(self, query, args=None):
        """
        Executes a SQL query with optional parameters and commits the transaction.

        :param query: The SQL query to be executed
        :param args: Optional parameters for the query
        """
        if args == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, args)
        self.connection.commit()
        
    def create_table_takeaccs(self, table:str="example"):
        """
        Create a table with the given name if it does not already exist in the database.

        Parameters:
            table (str): The name of the table to be created. Defaults to "example".
        """
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ( ids TEXT )")

    def insert(self, table:str="example", ids:str="hello"):
        """
        Insert data into the specified table using the given ids.

        Args:
            table (str): The name of the table to insert data into. Defaults to "example".
            ids (str): The ids to be inserted into the table. Defaults to "hello".
        """
        self.cursor.execute(f"INSERT INTO {table} VALUES (?)", (ids,))
        self.connection.commit()
        
    def take_all(self, table:str="example"):
        """
        A method to execute a SELECT * FROM query on a specified table and store the result in self.ids_out.
        
        Args:
            table (str): The name of the table to query from. Defaults to "example".
        """
        self.execute(f"SELECT * FROM {table}")
        
        self.ids_out = [ids[0] for ids in self.cursor.fetchall()]
        
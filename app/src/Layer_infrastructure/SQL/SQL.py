# Abstract base class for creating database connections
class DatabaseConnector:
    def create_connection(self):
        pass

# Concrete implementation of DatabaseConnector for MySQL
class MySQLConnector(DatabaseConnector):
    def __init__(self, host_name, user_name, user_password, db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

    def create_connection(self):
        return mysql.connector.connect(
            host=self.host_name,
            user=self.user_name,
            passwd=self.user_password,
            database=self.db_name
        )

# Interface for executing queries
class QueryExecutor:
    def execute_query(self, connection, query):
        pass

# Concrete implementation of QueryExecutor for MySQL
class MySQLQueryExecutor(QueryExecutor):
    def execute_query(self, connection, query):
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()
            print("Query successful")

        except Error as err:
            print(f"Error: '{err}'")

# Configuration class that uses dependency injection to create database connections and execute queries
class Configuration:
    def __init__(self, connector: DatabaseConnector, executor: QueryExecutor) -> None:
        self.connector = connector
        self.executor = executor

    def create_database(self, query):
        connection = self.connector.create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            print("Database created successfully")
            
        except Error as err:
            print(f"Error: '{err}'")

    def execute_query(self, query):
        connection = self.connector.create_connection()
        self.executor.execute_query(connection, query)
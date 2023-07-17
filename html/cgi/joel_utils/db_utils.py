import mysql.connector
import my_secrets

HOST = 'localhost'
USERNAME = 'ubuntu'
DATABASE = 'website'

class MySQLDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self): # allows "with MySQLDatabase() as db:"
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        password = my_secrets.get_secret(my_secrets.DATABASE_PASSWORD)
        self.connection = mysql.connector.connect(
            host = HOST,
            user = USERNAME,
            password = password,
            database = DATABASE
        )
        self.cursor = self.connection.cursor(buffered=True)

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, is_select):
        # TODO: Do I need to sanitize here or elsewhere??
        try:
            self.cursor.execute(query)
            self.connection.commit()
            assert(self.cursor is not None)
            if is_select: # This feels jenk
                return self.cursor.fetchall()
            return None
        except mysql.connector.Error as ex:
            print(f"Error executing query: {ex}")
            raise ex

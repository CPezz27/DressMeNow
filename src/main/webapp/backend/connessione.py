import mysql.connector


class MySQLDatabase:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "password"
        self.database = "provadb"
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_data(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(data.values()))
        self.connection.commit()

        query_get_last_id = "SELECT LAST_INSERT_ID()"
        self.cursor.execute(query_get_last_id)
        last_id = self.cursor.fetchone()[0]

        return last_id

    def delete_data(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
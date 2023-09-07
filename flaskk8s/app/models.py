import config
import psycopg2
import pandas as pd
import socket


import psycopg2

class DatabaseSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            # Initialize the PostgreSQL connection here
            cls._instance.connection = psycopg2.connect(
                **config.DB_PARAMS
            )
        return cls._instance

    def get_connection(self):
        return self.connection

# Usage:
# Create an instance of the DatabaseSingleton class
db_singleton = DatabaseSingleton()

# Get the database connection
db_connection = db_singleton.get_connection()


class DB:
    def get_db_connection(self):
        conn = DatabaseSingleton().get_connection()
        return conn
    
    def create_table_if_not_exists(self,):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS TEST(ID SERIAL PRIMARY KEY,VALUE CHARACTER VARYING(100),CONTAINER_HOST CHARACTER VARYING(100), CONTAINER_IP CHARACTER VARYING(100))')
        conn.commit()
        cursor.close()
        # conn.close()
    
    def get_backend_hostname_ip(self):
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            return host_name, host_ip
        except Exception as err:
            return "NOT FOUND","NOT FOUND"
        
    def get_db_hostname_ip(self,conn):
        try:
            dbhostname = pd.read_sql_query(f"SELECT PG_READ_FILE('/etc/hostname') AS HOSTNAME;", conn).iloc[0][0]
            dbip = pd.read_sql_query(f"SELECT INET_SERVER_ADDR() AS SERVER_IP;", conn).iloc[0][0]
            return dbhostname,dbip
        except Exception as err:
            return "NOT FOUND", "NOT FOUND"

    
    def get_host_info(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        dbhostname,dbip = self.get_db_hostname_ip(conn)
        back_host,back_ip = self.get_backend_hostname_ip()
        conn.commit()
        cursor.close()
        # conn.close()
        host_info = {"flask_host":back_host, "flask_ip":back_ip, "db_host":dbhostname, "db_ip":dbip}
        # conn.close()
        return host_info
    
    def read_db_records(self):
        conn = self.get_db_connection()
        table = pd.read_sql_query('select * from test;', conn)
        return table.to_dict('records')
    
    def add_record(self, value):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        hostname = pd.read_sql_query(f"SELECT PG_READ_FILE('/etc/hostname') AS HOSTNAME;", conn).iloc[0][0]
        ip = pd.read_sql_query(f"SELECT INET_SERVER_ADDR() AS SERVER_IP;", conn).iloc[0][0]
        cursor.execute(f"INSERT INTO TEST(VALUE,CONTAINER_HOST,CONTAINER_IP) VALUES('{value}','{hostname}','{ip}')")
        conn.commit()
        cursor.close()
        # conn.close()

    def delete_record(self, id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM TEST WHERE ID = {int(id)}")
        conn.commit()
        cursor.close()
        # conn.close()

db_obj = DB()
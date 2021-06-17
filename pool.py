import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

conncetPool = mysql.connector.pooling.MySQLConnectionPool(pool_name='mypool',
                        pool_size=5,
                        pool_reset_session=True,
                        host=os.getenv("SQL_HOST"),
                        database=os.getenv("SQL_DATABASE"),
                        user=os.getenv("SQL_USER"),
                        password=os.getenv("SQL_PASSWORD")
)


def closePool(mydb, mycursor):
    if mydb.is_connected():
            mycursor.close()
            mydb.close()

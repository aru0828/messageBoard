
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os 
load_dotenv()

conncetPool = mysql.connector.pooling.MySQLConnectionPool(pool_name='mypool',
                        pool_size=5,
                        pool_reset_session=True,
                        host=os.getenv("SQL_HOST"),
                        database=os.getenv("SQL_DATABASE"),
                        user=os.getenv("SQL_USER"),
                        password=os.getenv("SQL_PASSWORD")
)

mydb = conncetPool.get_connection()
mycursor = mydb.cursor(dictionary=True)

try:
    if mydb.is_connected():
        mycursor.execute(f'''CREATE TABLE message(
                            message_id INT PRIMARY KEY AUTO_INCREMENT,
                            message_text varchar(255),
                            message_img_url VARCHAR(255))'''           
)
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
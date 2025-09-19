import mysql.connector
from mysql.connector import Error

try:
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Blaze@123",
        database="library_db"
    )

    if conn.is_connected():
        print("Connected to mysql sccessfully!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables=[t[0] for t in cursor.fetchall()]
        print("Tables in library database:", tables)

        cursor.execute("SELECT COUNT(*) from Books;")
        count=cursor.fetchone()[0]
        print("Books in tables:", count)

except Error as e:
    print("Connection error:",e)

finally:
    if conn.is_connected():
        conn.close()
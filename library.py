import mysql.connector
from datetime import datetime

# Connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Blaze@123",
        database="library_db"
    )

# Registers the students
def register_student(conn,name,dept):
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Students (Stu_Name, Department) VALUES(%s,%s)", (name, dept))
    conn.commit()
    return cursor.lastrowid

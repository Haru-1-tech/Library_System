import mysql.connector
from datetime import datetime, timedelta

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

# Register the teachers
def register_teacher(conn,name,dept):
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Teachers (Teach_Name, Department) VALUES(%s,%s)",(name,dept))
    conn.commit()
    return cursor.lastrowid

# Shows the book list
def show_books(conn):
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM Books")
    rows= cursor.fetchall()
    print("-- Books in the library --")
    for row in rows:
        print(f"{row[0]}, Title:{row[1]}, Author:{row[2]}, ISBN: {row[3]}, Available: {row[4]}")

# Borrow a book
def borrow_book(conn, book_id, student_id=None, teacher_id=None):
    cursor=conn.cursor()

    # Check if book available
    cursor.execute("SELECT Available FROM Books WHERE BookID = %s",(book_id,))
    available= cursor.fetchone()
    if not available or available[0]==0:
        print("The Book is currently unavailable!")
        return  
    
    borrow_date=datetime.now().date()
    due_date= borrow_date + timedelta(days=15)

    cursor.execute("""INSERT INTO Borrowings (BookID, StudentID, TeacherID, BorrowDate, DueDate, ReturnDate) VALUES (%s, %s, %s, %s, %s)""", (book_id, student_id, teacher_id, borrow_date, due_date))

    cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = %s", (book_id,))
    conn.commit()
    print(f"Book borrowed successfully! Due date:{due_date}")

# Returning the Borrowed Book
def return_book(conn, borrow_id):
    cursor=conn.cursor()
    return_date = datetime.now().date()

    # Get book id
    cursor.execute("SELECT BookId FROM Borrowings WHERE BorrowID =%s", (borrow_id,))
    result=cursor.fetchone()
    if not result:
        print("Invalid Borrow ID")
        return
    book_id =result[0]

    # Update return date and set book as available
    cursor.execute("UPDATE Borrowings SET ReturnDate =%s where BorrowID = %s",(return_date, borrow_id))
    cursor.execute("UPDATE Books SET Available = TRUE where BookID = %s", (book_id,))
    conn.commit()
    print("Book returned successfully!")
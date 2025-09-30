import mysql.connector
from datetime import datetime, timedelta

# Connect to the database
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Blaze@123",
            database="library_db"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Registers the students
def register_student(conn,name,dept):
    try:
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Students (Stu_Name, Department) VALUES(%s,%s)", (name, dept))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error registering student: {e}")
        return None

# Register the teachers
def register_teacher(conn,name,dept):
    try:
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Teachers (Teach_Name, Department) VALUES(%s,%s)",(name,dept))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error registering teacher: {e}")
        return None

# Shows the book list
def show_books(conn, only_available=False):
    try:
        cursor= conn.cursor()
        if only_available:
            cursor.execute("SELECT * FROM Books WHERE Available = TRUE")
        else:
            cursor.execute("SELECT * FROM Books")
        rows= cursor.fetchall()
        print("-- Books in the library --")
        print("Book Id | Title of the books | Author | ISBN | Availablity")
        for row in rows:
            print(f"{row[0]}, Title:{row[1]}, Author:{row[2]}, ISBN: {row[3]}, Available: {row[4]}")
    except mysql.connector.Error as e:
        print(f"Error fetching books: {e}")

# Show all borrowings
def show_borrowings(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT BorrowID, BookID, StudentID, TeacherID, BorrowDate, DueDate, ReturnDate
            FROM Borrowings
        """)
        rows = cursor.fetchall()
        print("\n-- Borrowed Books --")
        for row in rows:
            print(f"BorrowID: {row[0]}, BookID: {row[1]}, StudentID: {row[2]}, "
                  f"TeacherID: {row[3]}, BorrowDate: {row[4]}, DueDate: {row[5]}, ReturnDate: {row[6]}")
    except mysql.connector.Error as e:
        print(f"Error fetching borrowings: {e}")

# Borrow a book
def borrow_book(conn, book_id, student_id=None, teacher_id=None):
    try:
        if student_id and teacher_id:
            print("Error: Borrowing must be either by a student or a teacher, not both.")
            return
        cursor=conn.cursor()

        # Check if book exists or is available
        cursor.execute("SELECT Available FROM Books WHERE BookID = %s",(book_id,))
        available= cursor.fetchone()
        if not available:
            print("Book id is Invalid!")
            return
        if available[0]==0:
            print("The Book is currently unavailable!")
            return  
        
        #Check if student_id exists
        if student_id:
            cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (student_id,))
            if not cursor.fetchone():
                print("Student id doesn't exist!")
                return
        
        # Check if teacher id exists
        if teacher_id:
            cursor.execute("SELECT * FROM Teachers WHERE TeacherID = %s", (teacher_id,))
            if not cursor.fetchone():
                print("Teacher id doesn't exist!")
                return
    
        borrow_date=datetime.now().date()
        due_date= borrow_date + timedelta(days=15)

        cursor.execute("""INSERT INTO Borrowings (BookID, StudentID, TeacherID, BorrowDate, DueDate) VALUES (%s, %s, %s, %s, %s)
                       """, (book_id, student_id, teacher_id, borrow_date, due_date))

        borrow_id= cursor.lastrowid
        print(f"Book borrowed successfully! Your Borrow ID is:{borrow_id} , Due date:{due_date}")
        cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = %s", (book_id,))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error borrowing book: {e}")
        return False


# Returning the Borrowed Book
def return_book(conn, borrow_id,student_id=None, teacher_id=None):
    try:
        cursor=conn.cursor()
        return_date = datetime.now().date()

        # Get the borrow id and the student/teacher id for double checking
        if student_id:
            cursor.execute("SELECT * FROM Borrowings WHERE BorrowID=%s AND StudentID=%s AND ReturnDate IS NULL", (borrow_id,student_id))
        elif teacher_id:
            cursor.execute("SELECT * FROM Borrowings WHERE BorrowID=%s AND TeacherID=%s AND ReturnDate IS NULL", (borrow_id,teacher_id))
        else:
            print("Error: Must provide StudentID or TeacherID to return a book.")
            return
        
        borrow_record=cursor.fetchone()
        if not borrow_record:
            print("Invalid Borrow ID or you are not the borrower of this book.")
            return

        # Update return date and set book as available
        cursor.execute("UPDATE Borrowings SET ReturnDate =%s where BorrowID = %s",(return_date, borrow_id))
        cursor.execute("UPDATE Books SET Available = TRUE where BookID = %s", (borrow_record[1],))
        conn.commit()
        print("Book returned successfully!")
    except mysql.connector.Error as e:
        print(f"Error returning the book: {e}")
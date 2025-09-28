from library import *

# Connecting to the database through the main function
def main():
    conn= connect_db()
    if not conn:
        return
    
    while True:
        print("\n--- Library Menu ---")
        print("1. Register a Student\n2. Register a Teacher\n3. Show Books\n4. Show Available Books\n5. Borrow Book\n6. Return Book\n7. Show Borrowings\n0. Exit")

        try:
            choice=int(input("Enter Your Choice: "))

            #To register a student
            if choice == 1:
                name=input("Enter the name of the Student: ")
                dept=input("Enter the department of the Student: ")
                register_stu=register_student(conn,name,dept)
                print(f"Student registered successfuly! Your Student ID is: {register_stu}")

            # To register a teacher
            elif choice == 2:
                name=input("Enter the name of the Teacher: ")
                dept=input("Enter the department of the Teacher: ")
                register_teach=register_teacher(conn,name,dept)
                print(f"Teacher registered successfully! Your Teacher ID is: {register_teach}")

            # To show all the books present in the library
            elif choice == 3:
                show_books(conn)

            # To show the available books
            elif choice == 4:
                show_books(conn,only_available=True)

            # To borrow a Book
            elif choice == 5:
                try:
                    book_id=int(input("Enter the Book id you want to borrow: "))
                except ValueError:
                    print("Invalid Input! Book Id must in numbers.")
                    continue

                #Asking if the borrower is a teacher or a student
                borrower_type=input(" Are you a student or a teacher? (S/T): ").strip().upper()
                if borrower_type =='S':
                    try:
                        student_id=int(input("Enter your Student ID: "))
                        teacher_id=None
                    except ValueError:
                        print("Invalid Input! The student id must be in numbers.")
                        continue
                elif borrower_type =='T':
                    try:
                        teacher_id=int(input("Enter your Teacher ID: "))
                        student_id=None
                    except ValueError:
                        print("Invalid Input! The teacher id must be in numbers.")
                        continue
                else:
                    print("Invalid Choice! Please enter S for Student or T for Teacher.")
                    continue
                borrow_book(conn,book_id,student_id,teacher_id)

            # To Return a Book
            elif choice == 6:
                try:
                    borrow_id=int(input("Enter the Borrow ID to return the book:"))
                    return_book(conn,borrow_id)
                except ValueError:
                    print("Invalid Input! Borrow ID must in numbers.")

            # Show all the borrowing records
            elif choice == 7:
                show_borrowings(conn)

            # To Exit the Library System    
            elif choice == 0:
                exit(0)
            else:
                print("Invalid Choice! Try again.")
        except ValueError:
            print("Invalid input! Please enter a number.")
            choice = -1

if __name__=="__main__":
    main()            
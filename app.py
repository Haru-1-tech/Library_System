from flask import Flask, render_template, request, redirect, url_for, flash
from library_functions import connect_db, fetch_books, fetch_borrowings, borrow_book, return_book

app= Flask(__name__)
app.secret_key = "Blaze@shadow"

# ROUTES

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/books')
def books():
    conn = connect_db()
    rows=fetch_books(conn)
    conn.close()
    return render_template('books.html', books=rows)

@app.route('/available')
def available_books():
    conn = connect_db()
    rows = fetch_books(conn, only_available=True)
    conn.close()
    return render_template('books.html', books=rows, only_available=True)

@app.route('/borrow', methods=['GET','POST'])
def borrow():
    if request.method == 'POST':
        book_id = request.form['book_id']
        student_id=request.form.get['student_id'] or None
        teacher_id=request.form.get['teacher_id'] or None

        conn=connect_db()
        borrow_book(conn, book_id, student_id, teacher_id)
        conn.close()

        flash("Book borrowed Successfully!","success")
        return redirect(url_for('books'))
    
    conn=connect_db()
    available= fetch_books(conn, only_available=True)
    conn.close()
    return render_template('borrow.html', books=available)

@app.route('/return', methods=['GET','POST'])
def return_page():
    if request.method == "POST":
        borrow_id=request.form['borrow_id']
        student_id=request.form.get('student_id') or None
        teacher_id=request.form.get('teacher_id') or None

        conn=connect_db()
        return_book(conn, borrow_id, student_id, teacher_id)
        conn.close()

        flash("Book returned Successfully!", "success")
        return redirect(url_for('books'))
    
    return render_template('return.html')

@app.route('/borrowings')
def borrowings():
    conn=connect_db()
    rows=fetch_borrowings(conn)
    conn.close()
    return render_template('borrowings.html', borrowings=rows)

if __name__=='__main__':
    app.run(debug=True)
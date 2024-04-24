import sqlite3
import requests
from hashlib import sha256

def get_conn():
    return sqlite3.connect('database.db')

def create_usertable():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Users_Table (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      password TEXT)''')
        conn.commit()

def create_books_table():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Books_Table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                publish_date TEXT,
                isbn TEXT,
                synopsis TEXT
            )
        ''')
        conn.commit()

def create_reviews_table():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Reviews_Table (
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      book_id INTEGER, 
                      user_id INTEGER, 
                      review TEXT, 
                      rating INTEGER, 
                      FOREIGN KEY (book_id) REFERENCES Books_Table (id), 
                      FOREIGN KEY (user_id) REFERENCES Users_Table (id))''')
        conn.commit()

def username_exists(username):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM Users_Table WHERE username = ?', (username,))
        return c.fetchone() is not None

def add_userdata(username, password):
    with get_conn() as conn:
        c = conn.cursor()
        if not username_exists(username):
            try:
                c.execute('INSERT INTO Users_Table(username, password) VALUES (?,?)', (username, password))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
        return False

def make_hashes(password):
    return sha256(str.encode(password)).hexdigest()

def login_user(username, hashed_password):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT id, username FROM Users_Table WHERE username =? AND password = ?', (username, hashed_password))
        data = c.fetchone()
        return data

def get_all_books_from_api():
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "subject:fiction",
        "maxResults": 40
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        books = response.json().get("items", [])
        book_data = []
        for book in books:
            volume_info = book.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = volume_info.get("authors", ["Unknown Author"])
            publish_date = volume_info.get("publishedDate", "")
            isbn_list = volume_info.get("industryIdentifiers", [])
            isbn = next((identifier['identifier'] for identifier in isbn_list if identifier['type'] == 'ISBN_13'), "")
            synopsis = volume_info.get("description", "No description available.")
            book_data.append((title, ", ".join(authors), publish_date, isbn, synopsis))
        return book_data
    else:
        return []

def sync_books_db():
    books_from_api = get_all_books_from_api()
    with get_conn() as conn:
        c = conn.cursor()
        for book in books_from_api:
            # Inserting new books into the Books_Table
            c.execute('INSERT INTO Books_Table (title, author, publish_date, isbn, synopsis) VALUES (?, ?, ?, ?, ?)', book)
        conn.commit()

def get_all_books():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT id, title, author FROM Books_Table')
        return c.fetchall()

def get_book_data(book_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Books_Table WHERE id = ?', (book_id,))
        return c.fetchone()

def get_book_reviews(book_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Reviews_Table WHERE book_id = ?', (book_id,))
        return c.fetchall()

def add_review(book_id, user_id, review, rating):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO Reviews_Table (book_id, user_id, review, rating) VALUES (?, ?, ?, ?)', (book_id, user_id, review, rating))
        conn.commit()

def initialize_books_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM Books_Table')
        if c.fetchone()[0] == 0:
            sync_books_db()  

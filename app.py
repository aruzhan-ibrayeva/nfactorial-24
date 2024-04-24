import streamlit as st
from authentication import sidebar_login
from books import show_books_list, show_book_details
from layout import create_header, create_navbar
from utils import create_usertable, create_books_table, create_reviews_table, initialize_books_db

def main():
    create_usertable()
    create_books_table()
    create_reviews_table()
    initialize_books_db()

    create_header()
    choice = create_navbar()

    if choice == "Home" and 'user_id' in st.session_state:
        st.subheader("Home - Browse Books")
        book_id = show_books_list()
        if book_id is not None: # Add this check
            show_book_details(book_id)


if __name__ == '__main__':
    sidebar_login()
    main()

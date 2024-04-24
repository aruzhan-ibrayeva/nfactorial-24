import streamlit as st
import requests
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

    if choice == "Home":
        if 'user_id' in st.session_state and st.session_state['user_id']:
            st.subheader("Browse Books")
            book_id = show_books_list()
            if book_id is not None: 
                show_book_details(book_id)
        else:
            st.warning("Please log in to view the books list.")

if __name__ == '__main__':
    sidebar_login()
    main()

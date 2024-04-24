import streamlit as st
from utils import get_all_books, get_book_data, get_book_reviews, add_review

def show_books_list():
    books = get_all_books()
    if not books:
        st.warning("No books available to display.")
        return None
    book_id = st.selectbox("Choose a book to view details", books, format_func=lambda x: f"{x[1]} by {x[2]}")
    if book_id:
        return book_id[0]
    return None

def show_book_details(book_id):
    book = get_book_data(book_id)
    if book:
        st.write('Title:', book[1])  
        st.write('Author:', book[2]) 
        st.write('Publish Date:', book[3]) 
        st.write('ISBN:', book[4])  
        st.write('Synopsis:', book[5])  

        reviews = get_book_reviews(book_id)
        if reviews:
            for index, review in enumerate(reviews):
                review_key = f"review_{review[0]}_{index}"  
                st.write('Rating:', '⭐' * review[4]) 
                st.text_area("Review:", review[3], disabled=True, key=review_key)  
        else:
            st.write("No reviews available for this book.")

        with st.form("Review Form"):
            new_review_text = st.text_area("Write your review:")
            new_rating = st.slider("Rating", 1, 5)
            submitted = st.form_submit_button("Submit Review")
            if submitted:
                success = add_review(book_id, st.session_state['user_id'],
                                      new_review_text, new_rating)
                if success:
                    st.success("Review added!")

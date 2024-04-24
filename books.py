import streamlit as st
from utils import get_all_books, get_book_data, get_book_reviews, add_review

def show_books_list():
    books = get_all_books()
    if not books:
        st.warning("No books available to display.")
        return None
    book_options = [(book[0], f"{book[1]} by {book[2]}") for book in books]
    book_tuple = st.selectbox("Choose a book to view details", options=book_options, format_func=lambda x: x[1])
    return book_tuple[0] if book_tuple else None


def show_book_details(book_id):
    book = get_book_data(book_id)
    if book:
        st.markdown(f"## {book[1]}")  
        st.markdown(f"#### by {book[2]}") 
        st.markdown(f"**Publish Date:** {book[3]}")  
        st.markdown(f"**ISBN:** {book[4]}")
        st.markdown(f"**Synopsis:** {book[5]}")

        reviews = get_book_reviews(book_id)
        if reviews:
            with st.expander("See reviews"):
                for index, review in enumerate(reviews):
                    rating_display = '⭐' * int(review[4]) if isinstance(review[4], int) and 0 <= review[4] <= 5 else "No rating"
                    st.write('Rating:', rating_display)
                    st.text_area("Review:", review[3], disabled=True, key=f"review_{index}")
        else:
            st.write("No reviews available for this book.")

        with st.form("Review Form"):
            new_review_text = st.text_area("Write your review:", key="new_review_text")
            new_rating = st.slider("Rating", 1, 5, key="new_rating")
            submitted = st.form_submit_button("Submit Review")
            if submitted and new_review_text:
                add_review(book_id, st.session_state['user_id'], new_review_text, new_rating)
                st.success("Review added!")

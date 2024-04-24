import streamlit as st
from utils import add_userdata, login_user, make_hashes

def sidebar_login():
    with st.sidebar:
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Register"):
            hashed_password = make_hashes(password)
            if add_userdata(username, hashed_password):
                st.success("You have successfully created an account!")
            else:
                st.error("Failed to create an account or username already exists.")

        if st.button("Login"):
            hashed_password = make_hashes(password)
            result = login_user(username, hashed_password)
            if result:
                st.session_state.user_id = result[0]  # Store user ID in session state
                st.session_state.username = result[1]  # Store username in session state
                st.success(f"Logged in as {username}")
            else:
                st.error("Incorrect username or password")
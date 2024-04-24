import streamlit as st

def create_header():
    st.title("Book Review Platform")

def create_navbar():
    menu = ["Home"]
    choice = st.sidebar.selectbox("Menu", menu)
    return choice

import streamlit as st

def create_header():
    st.markdown("""
        <style>
            .header {
                font-size: 32px;
                font-weight: bold;
                color: #4a4a4a;
                text-align: center;
                margin-bottom: 25px;
            }
            
            .stTextInput > label, .stButton > button {
                border-radius: 20px;
                border: 1px solid #ddd;
            }
            .stTextInput > div > div > input {
                padding: 10px;
            }
            .stButton > button {
                margin: 5px 0;
                padding: 5px 15px;
                width: 100%;
            }
            
            .css-1e5imcs {
                background-color: #f0f2f6;
                padding: 10px 20px;
            }
            .sidebar .sidebar-content {
                padding: 25px;
            }
        </style>
        <div class='header'>
            Book Review Platform
        </div>
    """, unsafe_allow_html=True)

def create_navbar():
    menu = ["Home", "About", "Contact"]
    st.sidebar.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #f0f2f6;
                border-radius: 20px;
            }
            .css-2trqyj {
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)
    choice = st.sidebar.selectbox("Menu", menu)
    return choice
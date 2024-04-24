import streamlit as st

def create_header():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap');
            .header {
                font-size: 36px;  /* Increased font size */
                font-weight: bold;
                color: #4a4a4a;
                text-align: center;
                margin-bottom: 25px;
                font-family: 'Open Sans', sans-serif;
            }
            
            .stTextInput > label, .stButton > button, .stSelectbox > label {
                border-radius: 20px;
                border: 1px solid #ddd;
            }
            .stTextInput > div > div > input, .stSelectbox > div > div {
                padding: 10px;
                font-family: 'Open Sans', sans-serif;
            }
            .stButton > button {
                margin: 5px 0;
                padding: 5px 15px;
                width: 100%;
                font-family: 'Open Sans', sans-serif;
            }
            
            .css-1e5imcs {
                background-color: #f0f2f6;
                padding: 10px 20px;
            }
            .sidebar .sidebar-content {
                padding: 25px;
                background-color: #f0f2f6;
                border-radius: 20px;
            }
        </style>
        <div class='header'>
            Book Review Platform
        </div>
    """, unsafe_allow_html=True)

def create_navbar():
    menu = ["Home"]
    choice = st.sidebar.selectbox("Menu", menu, index=0, 
                                  format_func=lambda x: x.upper())
    return choice

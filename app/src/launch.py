import streamlit as st
from app.src.components.multipage import MultiPage
from app.src.components.pages import start, overview, exploration

# Create an instance of the app
app = MultiPage()

# Hide Streamlit footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Title of the main page
try:
    col1, col2 = st.columns(2)
except Exception:
    col1, col2 = st.beta_columns(2)

#col2.title("PBG App")

# Add all your applications (pages) here (remember to import first)
app.add_page("Home", start.app)
app.add_page("Overview", overview.app)
app.add_page("Exploration", exploration.app)

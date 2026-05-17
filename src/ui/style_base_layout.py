import streamlit as st

def style_base_home():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #5865F2 !important;
            font-family: 'Arial', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_base_dahsboard():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E0E3FF !important;
            font-family: 'Arial', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
        /* Hiding the default Streamlit header and footer */
        MainMenu,footer,header{
          visibility: hidden;
        }
        .block-container {
            padding-top: 1.5rem !important;
        }
        h2,h1{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            color: #E0E3FF !important;
            font-height: 1.1 !important;
            margin-bottom: 0.5rem !important;
        }
        h3,h4,p{
            font-family: 'outfit', sans-serif !important;
            color: #E0E3FF !important;
        }
        button {
            background-color: #5865F2 !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 1rem !important;
            border-radius: 1.5rem !important;
            transition: transform 0.3s ease-in-out !important;
        }
        button[kind="secondary"] {
            background-color: #EB459E !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 1rem !important;
            border-radius: 1.5rem !important;
            transition: transform 0.3s ease-in-out !important;
        }
        button[kind="tertiary"] {
            background-color: black !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 1rem !important;
            border-radius: 1.5rem !important;
            transition: transform 0.3s ease-in-out !important;
        }
        button:hover {
            transform: scale(1.05) !important;
        }
        .stApp {
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )
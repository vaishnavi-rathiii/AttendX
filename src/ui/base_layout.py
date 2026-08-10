import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f5f5f5 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f5f5f5 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_base_layout():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');

            /* Hide Tool Bar */
            #MainMenu, footer, header {
               visibility: hidden;
            }

            .block-container {
                padding-top: 1.5rem !important;
            }

            h1 {
                font-family: 'Playfair Display', serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: #333333 !important;
            }

            h2 {
                font-family: 'Playfair Display', serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: #333333 !important;
            }

            h3, h4, p, span {
                font-family: 'Roboto', sans-serif !important;
                color: #333333 !important;
            }

            button[kind="primary"] {
                border-radius: 1.5rem !important;
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button:hover {
                transform: scale(1.05);
            }

        </style>
        """,
        unsafe_allow_html=True
    )
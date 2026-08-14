import streamlit as st


# ============================================================
# HOME BACKGROUND STYLING
# ============================================================

def style_background_home():

    st.markdown(
        """
        <style>

            .stApp {
                background-color: #B8DEC8 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background-color: #FFFFFF !important;
                border-radius: 5rem !important;
                padding: 1.5rem !important;
                box-shadow: 0 4px 6px rgba(27, 94, 75, 0.12) !important;
                text-align: center !important;
                border: 1px solid #D6E5DE !important;
            }

            .stApp div[data-testid="stColumn"] div[data-testid="stVerticalBlock"] {
                align-items: center !important;
            }

            .stApp div[data-testid="stColumn"] div[data-testid="stMarkdownContainer"] {
                text-align: center !important;
                width: 100% !important;
            }

            .stApp div[data-testid="stColumn"] div[data-testid="stButton"] {
                display: flex !important;
                justify-content: center !important;
                width: 100% !important;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD BACKGROUND STYLING
# ============================================================

def style_background_dashboard():

    st.markdown(
        """
        <style>

            .stApp {
                background-color: #F4F8F5 !important;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BASE LAYOUT STYLING
# ============================================================

def style_base_layout():

    st.markdown(
        """
        <style>

            /* ========================================================
               HIDE STREAMLIT DEFAULT UI
               Applies to ALL screens
               ======================================================== */

            #MainMenu,
            footer,
            header {
                visibility: hidden !important;
                display: none !important;
            }


            /* ========================================================
               CUSTOM FONTS
               ======================================================== */

            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Roboto:wght@400;500;600;700&display=swap');


            /* ========================================================
               HEADINGS
               ======================================================== */

            h1 {
                font-family: 'Playfair Display', serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: #1B5E4B !important;
            }

            h2 {
                font-family: 'Playfair Display', serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
                color: #1B5E4B !important;
            }

            h3, h4, p, span {
                font-family: 'Roboto', sans-serif !important;
                color: #1F2933 !important;
            }


            /* ========================================================
               BUTTONS
               ======================================================== */

            button[kind="primary"],
            button[kind="secondary"],
            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: #72B590 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="primary"] p,
            button[kind="secondary"] p,
            button[kind="tertiary"] p {
                color: white !important;
                font-family: 'Roboto', sans-serif !important;
            }

            button[kind="primary"]:hover,
            button[kind="secondary"]:hover,
            button[kind="tertiary"]:hover {
                background-color: #246F58 !important;
                transform: scale(1.05);
            }

        </style>
        """,
        unsafe_allow_html=True
    )
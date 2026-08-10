import streamlit as st


def header_home():
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS026W3Mv_RgTFvKhLfpYUt_51Tb6Lu-DWWgrltv5UNtMMF8HffQAF5KyQ&s=10"

    st.markdown(
        f"""
        <div>
            <img src="{logo_url}" style="height:100px;">
        </div>
        """,
        unsafe_allow_html=True
    )
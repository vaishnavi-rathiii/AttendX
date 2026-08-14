import streamlit as st


# ----------------------------------------
# Home Header
# ----------------------------------------

def header_home():

    # Set the AttendX logo URL
    logo_url = "https://img.icons8.com/pulsar-color/1200/attendance-mark.jpg"

    # Display the logo and AttendX title
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
            .attendx-title {{ font-family: 'Playfair Display', serif !important; font-size: 56px !important; font-weight: 700 !important; color: #1B5E4B !important; text-align: center !important; margin: 10px 0 0 0 !important; }}
        </style>
        <div style="text-align: center; margin-bottom: 30px; margin-top: -20px;">
            <img src="{logo_url}" width="100" style="border: 3px solid #1B5E4B; border-radius: 1rem; padding: 0; display: block; margin: 0 auto;" />
            <div class="attendx-title">AttendX</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tagline
    st.markdown(
        """
        <div style="
            text-align: center;
            font-family: 'Roboto', sans-serif;
            font-size: 20px;
            font-weight: 500;
            font-style: italic;
            color: #8C9692;
            margin-top: -25px;
            margin-bottom: 30px;
        ">
            Intelligent Attendance. Effortless Tracking.
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------
# Dashboard Header
# ----------------------------------------

def header_dashboard():

    # Set the AttendX logo URL
    logo_url = "https://img.icons8.com/pulsar-color/1200/attendance-mark.jpg"

    # Display the logo and AttendX title in the dashboard
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
            .attendx-dashboard-title {{ font-family: 'Playfair Display', serif !important; font-size: 24px !important; font-weight: 700 !important; color: #1B5E4B !important; }}
        </style>
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-top:-10px; margin-bottom:20px;">
            <img src="{logo_url}" width="60" style="border:3px solid #1B5E4B; border-radius:1rem;" />
            <div class="attendx-dashboard-title">AttendX</div>
        </div>
        """,
        unsafe_allow_html=True
    )
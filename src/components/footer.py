import streamlit as st


# ----------------------------------------
# Home Page Footer
# ----------------------------------------

def footer_home():

    # Display footer information on the home page
    st.markdown(
        """
        <div style="text-align:center; margin-top:25px; padding:0;">
            <p style="margin:0; color:#60756D; font-size:20px; line-height:1.5;">
                <b>Created with ❤️ by
                <a href="mailto:rathivaishnavi949@gmail.com"
                   style="color:#2E6F50; text-decoration:none;">
                   <br>Vaishnavi Rathi
                </a>
                </b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------
# Dashboard Footer
# ----------------------------------------

def footer_dashboard():

    # Display footer information on dashboard pages
    st.markdown(
        """
        <div style="text-align:center; margin-top:25px; padding:0;">
            <p style="margin:0; color:#60756D; font-size:22px; line-height:1.5;">
                <b>Created with ❤️ by
                <a href="mailto:rathivaishnavi949@gmail.com"
                   style="color:#2E6F50; text-decoration:none;">
                   <br>Vaishnavi Rathi
                </a>
                </b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
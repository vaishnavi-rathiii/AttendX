import streamlit as st

import segno
import io


# ----------------------------------------
# Share Subject Dialog
# ----------------------------------------

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):

    # ----------------------------------------
    # Generate Class Join URL
    # ----------------------------------------

    app_domain = "https://attendx-ai.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    # ----------------------------------------
    # Generate QR Code
    # ----------------------------------------

    try:
        qr = segno.make(join_url)

        out = io.BytesIO()

        qr.save(
            out,
            kind='png',
            scale=10,
            border=1
        )

    except Exception as e:
        st.error(f"Unable to generate QR code: {str(e)}")
        return

    # ----------------------------------------
    # Display Link and QR Code
    # ----------------------------------------

    col1, col2 = st.columns(2)

    # ----------------------------------------
    # Copy Link Section
    # ----------------------------------------

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    # ----------------------------------------
    # QR Code Section
    # ----------------------------------------

    with col2:
        st.markdown('### Scan to Join')
        st.image(
            out.getvalue(),
            caption='QRCODE for class joining'
        )

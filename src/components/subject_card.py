import streamlit as st


# ----------------------------------------
# Subject Card
# ----------------------------------------

def subject_card(name, code, section, stats=None, footer_callback=None):

    # ----------------------------------------
    # Create Subject Card HTML
    # ----------------------------------------

    html = f"""
        <div style="background:white; border-left: 8px solid #EB459E; padding:25px; border-radius: 20px; border: 1px solid black; margin-bottom:20px;">
        <h3 style="margin:0; color: #1e293b; font-size: 1.5rem ">{name}</h3>
        <p style="color:#64748b; margin:10px 0;">Code : <span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px;">{code} </span> | Section : {section}</p>
        
        """

    # ----------------------------------------
    # Display Subject Statistics
    # ----------------------------------------

    if stats:

        html += """
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
        """

        for icon, label, value in stats:

            # Add each statistic to the subject card
            html += f'<div style="background: #EB459E10; padding:5px 12px; border-radius:12px; font-size:0.9rem">{icon} <b>{value}</b> {label} </div>'

        html += "</div>"

    # ----------------------------------------
    # Display Subject Card
    # ----------------------------------------

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    # ----------------------------------------
    # Execute Footer Callback
    # ----------------------------------------

    if footer_callback:
        footer_callback()
import streamlit as st
from supabase import create_client, Client


# ----------------------------------------
# Create Supabase Client
# ----------------------------------------

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
)
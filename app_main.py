
import streamlit as st
import pandas as pd
import openpyxl
import io
import base64

st.set_page_config(page_title="Κατανομή Μαθητών", layout="wide")

def password_gate():
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False

    if not st.session_state.access_granted:
        code = st.text_input("🔐 Εισάγετε τον κωδικό πρόσβασης", type="password")
        if code == "katanomi2025":
            st.session_state.access_granted = True
        else:
            st.stop()

password_gate()

st.title("Καλωσήρθατε στην εφαρμογή Κατανομής Μαθητών")

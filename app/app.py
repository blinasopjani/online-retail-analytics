"""
Faza 3 — Aplikacioni Streamlit (Dev C).

Skelet fillestar: vetëm struktura e faqeve, ende pa upload/dashboard të plotë.
"""

import streamlit as st

st.set_page_config(page_title="Online Retail Analytics", layout="wide")

st.title("Online Retail Analytics Platform")

st.markdown(
    """
    Mirë se vini. Ky është skeleti fillestar i aplikacionit.

    **Hapat e ardhshëm (Hapi 3.1):**
    - Shtimi i komponentit të upload-it të CSV.
    - Thirrja e `clean_data()` nga `src/data_cleaning.py`.
    - Validimi i formatit të CSV-së.
    """
)

uploaded_file = st.file_uploader("Ngarko CSV mujor", type=["csv"])

if uploaded_file is not None:
    st.info("Upload u pranua — validimi dhe përpunimi do të shtohen në Hapin 3.1.")
